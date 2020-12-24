# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/Cellar/python/2.7.10_2/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/geventwebsocket/logging.py
# Compiled at: 2015-11-13 17:02:49
from __future__ import absolute_import
from logging import getLogger, StreamHandler, getLoggerClass, Formatter, DEBUG

def create_logger(name, debug=False, format=None):
    Logger = getLoggerClass()

    class DebugLogger(Logger):

        def getEffectiveLevel(x):
            if x.level == 0 and debug:
                return DEBUG
            else:
                return Logger.getEffectiveLevel(x)

    class DebugHandler(StreamHandler):

        def emit(x, record):
            StreamHandler.emit(x, record) if debug else None
            return

    handler = DebugHandler()
    handler.setLevel(DEBUG)
    if format:
        handler.setFormatter(Formatter(format))
    logger = getLogger(name)
    del logger.handlers[:]
    logger.__class__ = DebugLogger
    logger.addHandler(handler)
    return logger