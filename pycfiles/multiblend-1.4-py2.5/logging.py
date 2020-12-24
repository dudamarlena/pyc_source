# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/multiblend/logging.py
# Compiled at: 2009-04-08 10:17:34
"""More-or-less drop-in replacement for the logging module logger."""
import sys, traceback
LEVELS = {'DEBUG': 1, 
   'INFO': 2, 
   'WARN': 3, 
   'ERROR': 4, 
   'CRITICAL': 5, 
   'EXCEPTION': 5}
module = sys.modules[__name__]
module.__dict__.update(LEVELS)

class Logger(object):
    log_level = INFO

    def __init__(self, name):
        self.name = name

    def logger_builder(logname):
        logger_level = LEVELS[logname]

        def logger(self, msg):
            'Logs to level %s' % logname
            if logger_level < Logger.log_level:
                return
            print '%s %s: %s' % (logname, self.name, msg)

        return logger

    debug = logger_builder('DEBUG')
    info = logger_builder('INFO')
    warn = logger_builder('WARN')
    error = logger_builder('ERROR')
    critical = logger_builder('CRITICAL')
    __exception = logger_builder('EXCEPTION')

    def exception(self, msg):
        """Logs the message and shows the exception."""
        self.__exception(msg)
        traceback.print_exc()


def set_level(log_level):
    """Sets the global log level"""
    Logger.log_level = log_level