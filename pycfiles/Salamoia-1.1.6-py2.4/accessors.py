# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/salamoia/h2o/decorators/accessors.py
# Compiled at: 2007-12-02 16:26:56


class accessor(object):
    __module__ = __name__

    def __init__(self, func):
        self.func = func

    def patch(self, obj):
        self.name = self.func.func_name
        self.aname = '_' + self.name
        aname = self.aname
        self.setterName = 'set' + self.name.capitalize()
        self.getterName = 'get' + self.name.capitalize()

        def getter(self):
            return getattr(obj, aname)

        def setter(self, value):
            return setattr(self, aname, value)

        cls = obj.__class__
        setattr(cls, self.getterName, getter)
        setattr(cls, self.setterName, setter)
        setattr(cls, self.name, property(getter, setter))

    def __get__(self, obj, _=None):
        self.patch(obj)
        return getattr(obj, self.aname)

    def __set__(self, obj, value, _=None):
        self.patch(obj)
        return setattr(obj, self.aname, value)


from salamoia.tests import *
runDocTests()