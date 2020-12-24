# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/doorpi/action/base.py
# Compiled at: 2016-08-01 11:57:45
import logging
logger = logging.getLogger(__name__)
logger.debug('%s loaded', __name__)
from time import sleep
import importlib

class SingleAction:
    action_name = None
    single_fire_action = False

    @property
    def name(self):
        return '%s with args %s and kwargs %s' % (
         self.action_name,
         self.__args,
         self.__kwargs)

    def __init__(self, callback, *args, **kwargs):
        self.__callback = callback
        self.__args = args
        self.__kwargs = kwargs
        if len(self.__class__.__bases__) is 0:
            self.action_name = str(callback)
        else:
            self.action_name = self.__class__.__name__

    def __str__(self):
        return self.name

    def run(self, silent_mode=False):
        if not silent_mode:
            logger.trace('run %s with args %s and kwargs %s', self.__class__.__name__, self.__args, self.__kwargs)
        try:
            if len(self.__args) is not 0 and len(self.__kwargs) is not 0:
                return self.__callback(*self.__args, **self.__kwargs)
            else:
                if len(self.__args) is 0 and len(self.__kwargs) is not 0:
                    return self.__callback(**self.__kwargs)
                if len(self.__args) is not 0 and len(self.__kwargs) is 0:
                    return self.__callback(*self.__args)
                return self.__callback()

        except TypeError as ex:
            logger.exception(ex)

    @staticmethod
    def from_string(config_string):
        try:
            action_name = config_string.split(':', 1)[0]
            try:
                parameters = config_string.split(':', 1)[1]
            except:
                parameters = ''

            return importlib.import_module('doorpi.action.SingleActions.' + action_name).get(parameters)
        except:
            logger.exception('error while creating SingleAction from config string: %s', config_string)
            return

        return