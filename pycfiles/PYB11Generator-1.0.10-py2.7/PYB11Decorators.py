# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/PYB11Generator/PYB11Decorators.py
# Compiled at: 2019-03-09 13:37:40
from functools import wraps as PYB11wraps
import decorator as PYB11decorator, types

def PYB11ignore(thing):
    thing.PYB11ignore = True
    return thing


class PYB11template:

    def __init__(self, *args):
        self.template = []
        for t in args:
            assert len(t.split()) in (1, 2)
            if len(t.split()) == 1:
                self.template.append('typename %s' % t)
            else:
                self.template.append(t)

    def __call__(self, thing):
        if self.template:
            thing.PYB11ignore = True
        else:
            thing.PYB11ignore = False
        thing.PYB11template = self.template
        return thing


class PYB11template_dict:

    def __init__(self, val):
        assert isinstance(val, dict)
        self.val = val

    def __call__(self, thing):
        thing.PYB11template_dict = self.val
        return thing


def PYB11singleton(cls):
    cls.PYB11singleton = True
    return cls


class PYB11holder:

    def __init__(self, x):
        self.val = x

    def __call__(self, thing):
        thing.PYB11holder = self.val
        return thing


def PYB11dynamic_attr(cls):
    cls.PYB11dynamic_attr = True
    return cls


class PYB11namespace:

    def __init__(self, x):
        self.namespace = x
        if self.namespace[:-2] != '::':
            self.namespace += '::'

    def __call__(self, thing):
        thing.PYB11namespace = self.namespace
        return thing


class PYB11pycppname:

    def __init__(self, x):
        self.x = x

    def __call__(self, thing):
        thing.PYB11cppname = self.x
        thing.PYB11pyname = self.x
        return thing


class PYB11cppname:

    def __init__(self, x):
        self.cppname = x

    def __call__(self, thing):
        thing.PYB11cppname = self.cppname
        return thing


class PYB11pyname:

    def __init__(self, x):
        self.pyname = x

    def __call__(self, thing):
        thing.PYB11pyname = self.pyname
        return thing


def PYB11virtual(f):
    f.PYB11virtual = True
    return f


def PYB11pure_virtual(f):
    f.PYB11pure_virtual = True
    return f


def PYB11protected(f):
    f.PYB11protected = True
    return f


def PYB11const(f):
    f.PYB11const = True
    return f


def PYB11static(f):
    f.PYB11static = True
    return f


def PYB11noconvert(f):
    f.PYB11noconvert = True
    return f


class PYB11implementation:

    def __init__(self, x):
        self.val = x

    def __call__(self, thing):
        thing.PYB11implementation = self.val
        return thing


class PYB11returnpolicy:

    def __init__(self, x):
        self.val = x

    def __call__(self, thing):
        thing.PYB11returnpolicy = self.val
        return thing


class PYB11keepalive:

    def __init__(self, *args):
        self.val = tuple(args)
        assert len(self.val) == 2

    def __call__(self, thing):
        thing.PYB11keepalive = self.val
        return thing


class PYB11call_guard:

    def __init__(self, x):
        self.val = x

    def __call__(self, thing):
        thing.PYB11call_guard = self.val
        return thing


class PYB11module:

    def __init__(self, x):
        self.val = x

    def __call__(self, thing):
        if not hasattr(thing, 'PYB11module'):
            thing.PYB11module = {}
        thing.PYB11module[thing] = self.val
        return thing