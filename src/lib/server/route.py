#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import HTTPException, BackgroundTasks, Request
from fastapi.responses import JSONResponse, Response

import lib
from lib.core import app
from lib import log
from .service.synology import *


def supports_nas_name(nas_name: str) -> bool:
    if nas_name == "all" or nas_name in lib.configuration.get_servers().keys():
        return True
    return False


def check_and_raise(nas_name: str):
    if not supports_nas_name(nas_name):
        msg = f'"{nas_name}" does not contain servers.'
        log.error(msg)
        raise HTTPException(detail=msg, status_code=404)
    return


@app.get('/info')
def get_info():
    return JSONResponse(content={
        "ip": lib.configuration.get_ip(),
        "port": lib.configuration.get_port(),
        "status": "active"}, status_code=200)


@app.get('/nas/status', response_class=JSONResponse)
def get_nas_status_all():
    return asyncio.run(lib.syno_manager.get_nas_status_all_async())


@app.get('/nas/status/{nas_name}', response_class=JSONResponse)
def get_nas_status(nas_name: str):
    check_and_raise(nas_name)
    return lib.syno_manager.get_nas_status(nas_name)


@app.get('/nas/all/shutdown', response_class=Response)
def shutdown_nas_all(request: Request, background_tasks: BackgroundTasks):
    if request.query_params.get('background_mode', False):
        background_tasks.add_task(lib.syno_manager.power_off_all)
    else:
        asyncio.run(lib.syno_manager.power_off_all_async())
    return "OK"


@app.get('/nas/shutdown/{nas_name}', response_class=Response)
def shutdown_nas(nas_name: str):
    check_and_raise(nas_name)
    return lib.syno_manager.power_off(nas_name)


@app.get('/nas/all/power/on', response_class=Response)
def power_on_nas_all(request: Request, background_tasks: BackgroundTasks):
    if request.query_params.get('background_mode', False):
        background_tasks.add_task(lib.syno_manager.power_on_all)
    else:
        asyncio.run(lib.syno_manager.power_on_all_async())
    return "OK"


@app.get('/nas/power/on/{nas_name}', response_class=Response)
def power_on_nas(nas_name: str):
    check_and_raise(nas_name)
    if not lib.syno_manager.power_on(nas_name):
        return "Fail"
    return "OK"
