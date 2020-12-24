# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ..\indicatorModule\pyalgotrade\logger.py
# Compiled at: 2019-07-11 23:29:37
# Size of source mod 2**32: 2269 bytes
"""
.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>
"""
import logging, threading
initLock = threading.Lock()
rootLoggerInitialized = False
log_format = '%(asctime)s %(name)s [%(levelname)s] %(message)s'
level = logging.INFO
file_log = None
console_log = True

def init_handler(handler):
    handler.setFormatter(Formatter(log_format))


def init_logger(logger):
    logger.setLevel(level)
    if file_log is not None:
        fileHandler = logging.FileHandler(file_log, mode='w')
        init_handler(fileHandler)
        logger.addHandler(fileHandler)
    if console_log:
        consoleHandler = logging.StreamHandler()
        init_handler(consoleHandler)
        logger.addHandler(consoleHandler)


def initialize():
    global rootLoggerInitialized
    with initLock:
        if not rootLoggerInitialized:
            init_logger(logging.getLogger())
            rootLoggerInitialized = True


def getLogger(name=None):
    initialize()
    return logging.getLogger(name)


class Formatter(logging.Formatter):
    DATETIME_HOOK = None

    def formatTime(self, record, datefmt=None):
        newDateTime = None
        if Formatter.DATETIME_HOOK is not None:
            newDateTime = Formatter.DATETIME_HOOK()
        else:
            if newDateTime is None:
                ret = super(Formatter, self).formatTime(record, datefmt)
            else:
                ret = str(newDateTime)
        return ret