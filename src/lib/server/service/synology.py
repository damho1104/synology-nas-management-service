#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import asyncio
import time
import copy
import lib
import socket, struct
from datetime import datetime
from lib import SingleTone, log
from synology_api import base_api_core
from collections import OrderedDict


class SynologyService:
    def __init__(self, info_dict: OrderedDict):
        super().__init__()
        self.ip = info_dict.get('ip')
        self.port = info_dict.get('port')
        self.id = info_dict.get('id')
        self.pw = info_dict.get('pw')
        self.dsm_version = info_dict.get('dsm_major_version', 6)
        self.synology_core: base_api_core.Core = None

    def __enter__(self):
        self.synology_core = base_api_core.Core(ip_address=self.ip, port=self.port,
                                                username=self.id, password=self.pw,
                                                dsm_version=self.dsm_version)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.synology_core.logout()

    def shutdown(self):
        system_dict: OrderedDict = self.synology_core.core_list.get('SYNO.Core.System')
        try:
            response = self.synology_core.session.request_data('SYNO.Core.System', system_dict.get('path'),
                                                               {"method": "shutdown",
                                                                "local": True,
                                                                "force": False,
                                                                "firmware_upgrade": False,
                                                                "version": "1"},
                                                               'post', response_json=False)
            if response.status_code != 200:
                return False, response.json()
            return True, response.json()
        except Exception as e:
            return False, e


class SynologyManager(SingleTone):
    def __init__(self):
        super().__init__()

    @staticmethod
    def generate_result_dict(result: bool, exception: BaseException = None) -> OrderedDict:
        return {
            "Result": result,
            "Exception": "" if exception is None else f"Occurred({str(exception)})",
            "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

    @staticmethod
    def send_wol(mac_address: str, ip: str):
        delimiter = mac_address[2]
        removed_delim_mac_address = mac_address.replace(delimiter, '')

        data = b'FFFFFFFFFFFF' + (removed_delim_mac_address*16).encode()
        send_data = b''

        for i in range(0, len(data), 2):
            send_data += struct.pack('B', int(data[i:i+2], 16))

        broadcast = f"{ip[:ip.rfind('.')]}.255"

        try:
            # UDP
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
                sock.sendto(send_data, (broadcast, 9))
            return True
        except Exception as e:
            log.error(str(e), e)
            return False

    @classmethod
    async def power_off_async(cls, nas_name: str, enable_name: bool = False):
        def get_return_value(msg: str):
            if enable_name:
                return {"name": nas_name, "result": msg}
            else:
                return msg

        if nas_name.lower() == "all":
            await cls.power_off_all_async()
            return "OK"
        server_dict = lib.configuration.get_server(nas_name)
        try:
            with SynologyService(info_dict=server_dict) as synology:
                if not synology.shutdown():
                    return get_return_value("Fail")
                return get_return_value("OK")
        except Exception as e:
            log.error(str(e), e)
            return get_return_value("Fail")

    @classmethod
    def power_off_all(cls):
        log.info(f'[Shutdown NAS] Run Shutdown NAS for all.')
        server_dict = lib.configuration.get_servers()
        result_list = [asyncio.run(cls.power_off_async(nas_name, enable_name=True)) for nas_name in server_dict.keys()]
        log.info(f'[Shutdown NAS] Result: {result_list}')

    @classmethod
    async def power_off_all_async(cls):
        log.info(f'[Shutdown NAS] Run Shutdown NAS for all.')
        server_dict = lib.configuration.get_servers()
        task_list = [asyncio.create_task(cls.power_off_async(nas_name, enable_name=True)) for nas_name in server_dict.keys()]
        result_list = await asyncio.gather(*task_list)
        log.info(f'[Shutdown NAS] Result: {result_list}')

    @classmethod
    async def power_on_async(cls, nas_name: str, enable_sleep=True):
        if nas_name.lower() == 'all':
            return await cls.power_on_all_async()
        try:
            server_dict = lib.configuration.get_server(nas_name)
            if not cls.send_wol(server_dict.get('mac'), server_dict.get('ip')):
                log.error(f'[Startup NAS] Cannot send WOL({nas_name})')
                return False
            log.info(f'[Startup NAS] Send WOL magic packet({nas_name})')
            return True
        finally:
            if enable_sleep:
                await asyncio.sleep(3)

    @classmethod
    def power_on_all(cls):
        log.info(f'[Startup NAS] Run Startup NAS for all.')
        server_info_dict = lib.configuration.get_servers()
        result_list = []
        for nas_name in server_info_dict.keys():
            result_list.append(asyncio.run(cls.power_on_async(nas_name, enable_sleep=False)))
            time.sleep(3)
        if False in result_list:
            return False
        return True

    @classmethod
    async def power_on_all_async(cls):
        log.info(f'[Startup NAS] Run Startup NAS for all.')
        server_info_dict = lib.configuration.get_servers()
        task_list = [asyncio.create_task(cls.power_on_async(nas_name)) for nas_name in server_info_dict.keys()]
        result_list = await asyncio.gather(*task_list)
        if False in result_list:
            return False
        return True

    @classmethod
    async def get_nas_status_async(cls, nas_name: str, enable_name: bool = True):
        def get_return_value(return_dict: OrderedDict):
            if enable_name:
                return_dict['name'] = nas_name
            return return_dict

        if nas_name.lower() == "all":
            return await cls.get_nas_status_all_async()
        server_dict = lib.configuration.get_server(nas_name)
        try:
            with SynologyService(info_dict=server_dict):
                return get_return_value({"ip": server_dict.get("ip"), "port": server_dict.get("port"), "active": True})
        except Exception as e:
            log.error(str(e), e)
            return get_return_value({"active": False})

    @classmethod
    def get_nas_status_all(cls):
        result_dict = OrderedDict()
        for nas_name in lib.configuration.get_servers().keys():
            element = copy.deepcopy(asyncio.run(cls.get_nas_status_async(nas_name, enable_name=False)))
            result_dict[nas_name] = element
        return result_dict

    @classmethod
    async def get_nas_status_all_async(cls):
        server_dict = lib.configuration.get_servers()
        result_dict = OrderedDict()
        task_list = [asyncio.create_task(cls.get_nas_status_async(nas_name, enable_name=True)) for nas_name in server_dict.keys()]
        for element in await asyncio.gather(*task_list):
            result_dict[element.get('name')] = OrderedDict({
                'ip': element.get('ip'),
                'port': element.get('port'),
                'active': element.get('active')
            })
        return result_dict

