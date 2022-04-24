#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import lib
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
        self.synology_core: base_api_core.Core = None

    def __enter__(self):
        self.synology_core = base_api_core.Core(ip_address=self.ip, port=self.port,
                                                username=self.id, password=self.pw,
                                                dsm_version=6)
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

    @classmethod
    def shutdown_all(cls):
        log.info(f'[Shutdown NAS] Run Shutdown NAS for all.')
        server_dict = lib.configuration.get_servers()
        result_dict = {}
        for nas_name in server_dict.keys():
            try:
                with SynologyService(info_dict=server_dict.get(nas_name)) as synology:
                    if not synology.shutdown():
                        result_dict[nas_name] = cls.generate_result_dict(False)
                        continue
                    result_dict[nas_name] = cls.generate_result_dict(True)
            except Exception as e:
                log.error(str(e), e)
                result_dict[nas_name] = cls.generate_result_dict(False, exception=e)
        log.info(f'[Shutdown NAS] Result: {result_dict}')
