# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taco/common/logger_based_object.py
# Compiled at: 2019-09-05 09:49:59
import taco.logger.logger

class LoggerBasedObject(object):

    def __init__(self, logger=None):
        logger_name = self.__class__.__name__
        if logger is None:
            self._logger = taco.logger.logger.get_logger(logger_name)
        else:
            self._logger = logger.get_child(logger_name)
        return