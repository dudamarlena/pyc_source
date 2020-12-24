# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/peewee/playhouse/hybrid.py
# Compiled at: 2018-07-11 18:15:31


class hybrid_method(object):

    def __init__(self, func, expr=None):
        self.func = func
        self.expr = expr or func

    def __get__(self, instance, instance_type):
        if instance is None:
            return self.expr.__get__(instance_type, instance_type.__class__)
        else:
            return self.func.__get__(instance, instance_type)

    def expression(self, expr):
        self.expr = expr
        return self


class hybrid_property(object):

    def __init__(self, fget, fset=None, fdel=None, expr=None):
        self.fget = fget
        self.fset = fset
        self.fdel = fdel
        self.expr = expr or fget

    def __get__(self, instance, instance_type):
        if instance is None:
            return self.expr(instance_type)
        else:
            return self.fget(instance)

    def __set__(self, instance, value):
        if self.fset is None:
            raise AttributeError('Cannot set attribute.')
        self.fset(instance, value)
        return

    def __delete__(self, instance):
        if self.fdel is None:
            raise AttributeError('Cannot delete attribute.')
        self.fdel(instance)
        return

    def setter(self, fset):
        self.fset = fset
        return self

    def deleter(self, fdel):
        self.fdel = fdel
        return self

    def expression(self, expr):
        self.expr = expr
        return self