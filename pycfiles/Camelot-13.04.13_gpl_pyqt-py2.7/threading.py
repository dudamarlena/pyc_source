# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/camelot/core/threading.py
# Compiled at: 2013-04-11 17:47:52
"""
Some helper functions and classes related
to threading issues
"""
from PyQt4 import QtCore

def synchronized(original_function):
    """Decorator for synchronized access to an object, the object should
    have an attribute _mutex which is of type QMutex
    """
    from functools import wraps

    @wraps(original_function)
    def wrapper(self, *args, **kwargs):
        locker = QtCore.QMutexLocker(self._mutex)
        result = original_function(self, *args, **kwargs)
        locker.unlock()
        return result

    return wrapper