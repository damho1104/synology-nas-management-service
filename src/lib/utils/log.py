#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import datetime
import logging
import logging.handlers
import os
import sys
import traceback
from inspect import currentframe, getframeinfo

from lib import FileUtil

DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

TASK = logging.INFO + 1
LOG_LEVEL_NAME_PROGRESS = 'TASKING'

CHECK_POINT = TASK + 1
LOG_LEVEL_NAME_CHECK_POINT = 'CKPT'

CR = '\r'
CURSOR_UP_ONE = '\x1b[1A'
ERASE_LINE = '\x1b[K'  # instructs the terminal to erase from the cursor to the end of the line.

LOG_FOLDER = FileUtil.get_path('logs')
os.makedirs(LOG_FOLDER, exist_ok=True)

# LOG_FILE_PATH = os.path.join(LOG_FOLDER, f'server.{datetime.datetime.now().strftime("%Y%m%d%H%M%S.%f")}.log')
LOG_FILE_PATH = os.path.join(LOG_FOLDER, f'server.{datetime.datetime.now().strftime("%Y%m%d")}.log')


class FileLogFormatter(logging.Formatter):
    def __init__(self):
        logging.Formatter.__init__(self,
                                   fmt='[%(asctime)s] [%(levelname)-8s] [%(process)d] [%(thread)-5d] [%(threadName)s] %(message)s')


class NoWriteLogFilter(logging.Filter):
    def filter(self, record) -> bool:
        return False


def get_log_file_path() -> str:
    return LOG_FILE_PATH


def set_log_file_path(log_file_path):
    global LOG_FILE_PATH
    LOG_FILE_PATH = log_file_path


def multiprocess_init(log_file_path):
    set_log_file_path(log_file_path)
    init()


def init():
    logging.basicConfig(datefmt=DATE_FORMAT,
                        level=logging.NOTSET)
    logging.addLevelName(TASK, LOG_LEVEL_NAME_PROGRESS)
    logging.addLevelName(CHECK_POINT, LOG_LEVEL_NAME_CHECK_POINT)

    logging.getLogger().handlers = list()

    file_handler = logging.handlers.RotatingFileHandler(
        filename=LOG_FILE_PATH,
        encoding='utf-8',
        maxBytes=4 * 1024 * 1024,
        backupCount=2)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(FileLogFormatter())
    logging.getLogger().addHandler(file_handler)
    logging.getLogger("urllib3.connectionpool").addFilter(NoWriteLogFilter())


def log(level, msg):
    logging.log(level, msg)


def console(msg):
    log(logging.INFO, f'[Console] {msg}')


def debug(msg):
    msg = f'[{getframeinfo(currentframe().f_back.f_back).filename}:{getframeinfo(currentframe().f_back.f_back).lineno}] {msg}'
    log(logging.DEBUG, msg)


def info(msg):
    log(logging.INFO, msg)


def warn(msg):
    debug(''.join(traceback.format_exception(*sys.exc_info())))
    log(logging.WARN, msg)


warning = warn


def error(msg: str = None,
          exc: BaseException = None):
    if not exc:
        exc = sys.exc_info()[0]

    debug(''.join(traceback.format_exception(*sys.exc_info())))
    logging.error(str(exc))

    if msg:
        logging.error(msg)
