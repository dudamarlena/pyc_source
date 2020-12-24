# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/winkidney/.virtualenvs/huobi/lib/python2.7/site-packages/pyalgotrade/logger.py
# Compiled at: 2016-11-29 01:45:48
__doc__ = '\n.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>\n'
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
        fileHandler = logging.FileHandler(file_log)
        init_handler(fileHandler)
        logger.addHandler(fileHandler)
    if console_log:
        consoleHandler = logging.StreamHandler()
        init_handler(consoleHandler)
        logger.addHandler(consoleHandler)
    return


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
        if newDateTime is None:
            ret = super(Formatter, self).formatTime(record, datefmt)
        else:
            ret = str(newDateTime)
        return ret