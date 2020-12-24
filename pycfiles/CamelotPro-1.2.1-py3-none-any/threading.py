# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/camelot/core/threading.py
# Compiled at: 2013-04-11 17:47:52
__doc__ = '\nSome helper functions and classes related\nto threading issues\n'
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