#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import HTTPException
from fastapi.responses import JSONResponse, Response

import lib
from lib.core import app
from lib import log
from .service.synology import *


@app.get('/info')
def get_info():
    return JSONResponse(content={
        "ip": lib.configuration.get_ip(),
        "port": lib.configuration.get_port(),
        "status": "active"}, status_code=200)


@app.get('/{nas_name}/status', response_class=JSONResponse)
def get_nas_status(nas_name: str):
    if nas_name not in lib.configuration.get_servers().keys():
        log.error(f'"{nas_name}" does not contain servers.')
        raise HTTPException(status_code=404)
    server_dict = lib.configuration.get_server(nas_name)
    try:
        with SynologyService(info_dict=server_dict):
            return {"name": nas_name, "ip": server_dict.get("ip"), "port": server_dict.get("port"), "active": True}
    except Exception as e:
        log.error(str(e), e)
        return {"name": nas_name, "active": False}


@app.get('/nas/shutdown/{nas_name}', response_class=Response)
def shutdown_nas(nas_name: str):
    if nas_name not in lib.configuration.get_servers().keys():
        log.error(f'"{nas_name}" does not contain servers.')
        raise HTTPException(status_code=404)
    server_dict = lib.configuration.get_server(nas_name)
    try:
        with SynologyService(info_dict=server_dict) as synology:
            if not synology.shutdown():
                return "Fail"
            return "OK"
    except Exception as e:
        log.error(str(e), e)
        return "Fail"


@app.get('/nas/shutdown/all', response_class=JSONResponse)
def shutdown_nas_all():
    server_dict = lib.configuration.get_servers()
    result_dict = {}
    for nas_name in server_dict.keys():
        try:
            with SynologyService(info_dict=server_dict.get(nas_name)) as synology:
                if not synology.shutdown():
                    result_dict[nas_name] = False
                    continue
                result_dict[nas_name] = True
        except Exception as e:
            log.error(str(e), e)
            result_dict[nas_name] = False
    return result_dict
