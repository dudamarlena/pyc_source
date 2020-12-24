# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/rwproperty.py
# Compiled at: 2006-02-23 19:56:50
import sys
__all__ = [
 'getproperty', 'setproperty', 'delproperty']

class rwproperty(object):
    __module__ = __name__

    def __new__(cls, func):
        name = func.__name__
        frame = sys._getframe(1)
        locals = frame.f_locals
        if name not in locals:
            return cls.createProperty(func)
        oldprop = locals[name]
        if isinstance(oldprop, property):
            return cls.enhanceProperty(oldprop, func)
        raise TypeError('read & write properties cannot be mixed with other attributes except regular property objects.')

    @staticmethod
    def createProperty(func):
        raise NotImplementedError

    @staticmethod
    def enhanceProperty(oldprop, func):
        raise NotImplementedError


class getproperty(rwproperty):
    __module__ = __name__

    @staticmethod
    def createProperty(func):
        return property(func)

    @staticmethod
    def enhanceProperty(oldprop, func):
        return property(func, oldprop.fset, oldprop.fdel)


class setproperty(rwproperty):
    __module__ = __name__

    @staticmethod
    def createProperty(func):
        return property(None, func)

    @staticmethod
    def enhanceProperty(oldprop, func):
        return property(oldprop.fget, func, oldprop.fdel)


class delproperty(rwproperty):
    __module__ = __name__

    @staticmethod
    def createProperty(func):
        return property(None, None, func)

    @staticmethod
    def enhanceProperty(oldprop, func):
        return property(oldprop.fget, oldprop.fset, func)


if __name__ == '__main__':
    import doctest
    doctest.testfile('rwproperty.txt')