# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/bezel/misc.py
# Compiled at: 2009-02-25 04:20:27
"""
This module provides various utilities for internal use in the bezel
engine.
"""

class InheritProperty(object):
    """Based on the emulation of PyProperty_Type() in Objects/descrobject.c"""

    def __init__(self, fget=None, fset=None, fdel=None, doc=None):
        self.fget = fget
        self.fset = fset
        self.fdel = fdel
        self.__doc__ = doc

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        if self.fget is None:
            raise AttributeError, 'unreadable attribute'
        if self.fget.__name__ == '<lambda>' or not self.fget.__name__:
            return self.fget(obj)
        else:
            return getattr(obj, self.fget.__name__)()
        return

    def __set__(self, obj, value):
        if self.fset is None:
            raise AttributeError, "can't set attribute"
        if self.fset.__name__ == '<lambda>' or not self.fset.__name__:
            self.fset(obj, value)
        else:
            getattr(obj, self.fset.__name__)(value)
        return

    def __delete__(self, obj):
        if self.fdel is None:
            raise AttributeError, "can't delete attribute"
        if self.fdel.__name__ == '<lambda>' or not self.fdel.__name__:
            self.fdel(obj)
        else:
            getattr(obj, self.fdel.__name__)()
        return