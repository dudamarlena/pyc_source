# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/aaron/projects/chai/tests/samples.py
# Compiled at: 2014-10-14 17:00:38
"""
Contains sample classes and situations that we want to test.
"""
from collections import deque

def mod_func_1(*args, **kwargs):
    pass


def mod_func_2(*args, **kwargs):
    mod_func_1(*args, **kwargs)


def mod_func_3(val):
    return 3 * val


def mod_func_4(val):
    return 3 * mod_func_3(val)


class ModInstance(object):

    @classmethod
    def foo(self):
        pass


mod_instance = ModInstance()
mod_instance_foo = mod_instance.foo

class SampleBase(object):
    a_class_value = 'sample in a jar'

    def __init__(self, *args, **kwargs):
        self._args = args
        self._kwargs = kwargs
        self._prop_value = 5
        self._deque = deque()

    @property
    def prop(self):
        return self._prop_value

    @prop.setter
    def set_property(self, val):
        self._prop_value = val

    @prop.deleter
    def del_property(self):
        self._prop_value = None
        return

    @staticmethod
    def a_staticmethod(arg):
        return str(arg)

    @classmethod
    def a_classmethod(cls):
        return cls.a_class_value

    def add_to_list(self, value):
        self._deque.append(value)

    def bound_method(self, arg1, arg2='two'):
        self._arg1 = arg1
        self._arg2 = arg2

    def callback_source(self):
        self.callback_target()

    def callback_target(self):
        self._cb_target = 'called'


class SampleChild(SampleBase):

    def bound_method(self, arg1, arg2='two', arg3='three'):
        super(SampleBase, self).bound_method(arg1, arg2)
        self._arg3 = arg3

    @classmethod
    def a_classmethod(cls):
        return 'fixed value'

    @property
    def prop(self):
        return 'child property'