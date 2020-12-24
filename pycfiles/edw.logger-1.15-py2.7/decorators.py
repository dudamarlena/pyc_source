# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/edw/logger/decorators.py
# Compiled at: 2018-03-22 08:59:14
import traceback, json
from edw.logger.config import logger

class LogErrors(object):

    def __init__(self, func, message, context=None):
        self.func = func
        self.message = message
        self.context = context

    def __call__(self, *args, **kwargs):
        try:
            if self.context:
                return self.func(self.context, *args, **kwargs)
            else:
                return self.func(*args, **kwargs)

        except:
            tb = traceback.format_exc()
            self.log_error(tb)

    def log_error(self, tb):
        logger.error(json.dumps(self.build_error(tb)))

    def build_error(self, tb):
        return {'Type': 'LogError', 
           'Message': self.message, 
           'Traceback': tb, 
           'LoggerName': logger.name}


def log_errors(message, factory=LogErrors):

    def decorator(func):
        return factory(func, message)

    return decorator