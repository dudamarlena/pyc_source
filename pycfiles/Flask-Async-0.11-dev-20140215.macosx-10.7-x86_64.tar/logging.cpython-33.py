# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mrdon/dev/flask-async/venv/lib/python3.3/site-packages/flask/logging.py
# Compiled at: 2014-01-20 12:41:11
# Size of source mod 2**32: 1398 bytes
"""
    flask.logging
    ~~~~~~~~~~~~~

    Implements the logging support for Flask.

    :copyright: (c) 2014 by Armin Ronacher.
    :license: BSD, see LICENSE for more details.
"""
from __future__ import absolute_import
from logging import getLogger, StreamHandler, Formatter, getLoggerClass, DEBUG

def create_logger(app):
    """Creates a logger for the given application.  This logger works
    similar to a regular Python logger but changes the effective logging
    level based on the application's debug flag.  Furthermore this
    function also removes all attached handlers in case there was a
    logger with the log name before.
    """
    Logger = getLoggerClass()

    class DebugLogger(Logger):

        def getEffectiveLevel(x):
            if x.level == 0 and app.debug:
                return DEBUG
            return Logger.getEffectiveLevel(x)

    class DebugHandler(StreamHandler):

        def emit(x, record):
            StreamHandler.emit(x, record) if app.debug else None
            return

    handler = DebugHandler()
    handler.setLevel(DEBUG)
    handler.setFormatter(Formatter(app.debug_log_format))
    logger = getLogger(app.logger_name)
    del logger.handlers[:]
    logger.__class__ = DebugLogger
    logger.addHandler(handler)
    return logger