# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/minideblib/LoggableObject.py
# Compiled at: 2007-11-06 15:08:00
__revision__ = 'r' + '$Revision: 47 $'[11:-2]
__all__ = ['LoggableObject']
import logging

class LazyInit(object):

    def __init__(self, calculate_function):
        self._calculate = calculate_function

    def __get__(self, obj, _=None):
        if obj is None:
            return self
        value = self._calculate(obj)
        setattr(obj, self._calculate.func_name, value)
        return value


class LoggableObject:

    def _logger(self):
        """ Returns logger and initializes default handlers if needed """
        logger = logging.getLogger(self.__module__)
        c = logger
        found = False
        while c:
            if c.handlers:
                found = True
                break
            c = c.parent

        if not found:
            logging.basicConfig()
        return logger

    _logger = LazyInit(_logger)