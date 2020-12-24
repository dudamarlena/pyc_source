# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\multiprocessing\patch.py
# Compiled at: 2009-07-30 09:32:54
"""Monkey patch collection
"""
import sys, threading
from __builtin__ import property as bltin_property
__all__ = ('property', 'monkey')
property = None

class property26(bltin_property):
    __module__ = __name__

    def getter(self, fget):
        global property
        return property(fget, self.fset, self.fdel, self.__doc__)

    def setter(self, fset):
        return property(self.fget, fset, self.fdel, self.__doc__)

    def deleter(self, fdel):
        return property(self.fget, self.fset, fdel, self.__doc__)


class ThreadPatch(object):
    """Monkey patch for threading.Thread
    """
    __module__ = __name__
    is_alive = threading.Thread.isAlive.im_func
    name = bltin_property(threading.Thread.getName.im_func, threading.Thread.setName.im_func)
    daemon = bltin_property(threading.Thread.isDaemon.im_func, threading.Thread.setDaemon.im_func)


class ConditionPatch(object):
    """Monkey patch for threading._Condition
    """
    __module__ = __name__
    notify_all = threading._Condition.notifyAll.im_func


def monkey():
    """Monkey patch
    """
    global property
    if property is not None:
        return
    elif sys.version_info >= (2, 6):
        property = bltin_property
        return
    property = property26
    if ThreadPatch not in threading.Thread.__bases__:
        threading.Thread.__bases__ += (ThreadPatch,)
    if ConditionPatch not in threading._Condition.__bases__:
        threading._Condition.__bases__ += (ConditionPatch,)
    threading.current_thread = threading.currentThread
    return