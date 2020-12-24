# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\ISEN\AppData\Local\Temp\pip-install-whg15vss\serial\serial\hooks.py
# Compiled at: 2019-09-23 04:34:10
# Size of source mod 2**32: 8749 bytes
from __future__ import nested_scopes, generators, division, absolute_import, with_statement, print_function, unicode_literals
from utilities.compatibility import backport
backport()
import serial.abc
from copy import deepcopy
import serial
from .utilities import qualified_name
from abc.model import Model
try:
    import typing
except ImportError as e:
    try:
        typing = None
    finally:
        e = None
        del e

class Hooks(object):

    def __init__(self, before_marshal=None, after_marshal=None, before_unmarshal=None, after_unmarshal=None, before_serialize=None, after_serialize=None, before_deserialize=None, after_deserialize=None, before_validate=None, after_validate=None):
        self.before_marshal = before_marshal
        self.after_marshal = after_marshal
        self.before_unmarshal = before_unmarshal
        self.after_unmarshal = after_unmarshal
        self.before_serialize = before_serialize
        self.after_serialize = after_serialize
        self.before_deserialize = before_deserialize
        self.after_deserialize = after_deserialize
        self.before_validate = before_validate
        self.after_validate = after_validate

    def __copy__(self):
        return (self.__class__)(**vars(self))

    def __deepcopy__(self, memo=None):
        return (self.__class__)(**)

    def __bool__(self):
        return True


class Object(Hooks):

    def __init__(self, before_marshal=None, after_marshal=None, before_unmarshal=None, after_unmarshal=None, before_serialize=None, after_serialize=None, before_deserialize=None, after_deserialize=None, before_validate=None, after_validate=None, before_setattr=None, after_setattr=None, before_setitem=None, after_setitem=None):
        self.before_marshal = before_marshal
        self.after_marshal = after_marshal
        self.before_unmarshal = before_unmarshal
        self.after_unmarshal = after_unmarshal
        self.before_serialize = before_serialize
        self.after_serialize = after_serialize
        self.before_deserialize = before_deserialize
        self.after_deserialize = after_deserialize
        self.before_validate = before_validate
        self.after_validate = after_validate
        self.before_setattr = before_setattr
        self.after_setattr = after_setattr
        self.before_setitem = before_setitem
        self.after_setitem = after_setitem


class Array(Hooks):

    def __init__(self, before_marshal=None, after_marshal=None, before_unmarshal=None, after_unmarshal=None, before_serialize=None, after_serialize=None, before_deserialize=None, after_deserialize=None, before_validate=None, after_validate=None, before_setitem=None, after_setitem=None, before_append=None, after_append=None):
        self.before_marshal = before_marshal
        self.after_marshal = after_marshal
        self.before_unmarshal = before_unmarshal
        self.after_unmarshal = after_unmarshal
        self.before_serialize = before_serialize
        self.after_serialize = after_serialize
        self.before_deserialize = before_deserialize
        self.after_deserialize = after_deserialize
        self.before_validate = before_validate
        self.after_validate = after_validate
        self.before_setitem = before_setitem
        self.after_setitem = after_setitem
        self.before_append = before_append
        self.after_append = after_append


class Dictionary(Hooks):

    def __init__(self, before_marshal=None, after_marshal=None, before_unmarshal=None, after_unmarshal=None, before_serialize=None, after_serialize=None, before_deserialize=None, after_deserialize=None, before_validate=None, after_validate=None, before_setitem=None, after_setitem=None):
        self.before_marshal = before_marshal
        self.after_marshal = after_marshal
        self.before_unmarshal = before_unmarshal
        self.after_unmarshal = after_unmarshal
        self.before_serialize = before_serialize
        self.after_serialize = after_serialize
        self.before_deserialize = before_deserialize
        self.after_deserialize = after_deserialize
        self.before_validate = before_validate
        self.after_validate = after_validate
        self.before_setitem = before_setitem
        self.after_setitem = after_setitem


def read(model_instance):
    """
    Read metadata from a model instance (the returned metadata may be inherited, and therefore should not be written to)
    """
    if isinstance(model_instance, type):
        return model_instance._hooks
    if isinstance(model_instance, Model):
        return model_instance._hooks or read(type(model_instance))


def writable(model_instance):
    """
    Retrieve a metadata instance. If the instance currently inherits its metadata from a class or superclass,
    this funtion will copy that metadata and assign it directly to the model instance.
    """
    if isinstance(model_instance, type):
        if model_instance._hooks is None:
            model_instance._hooks = Object() if issubclass(model_instance, serial.model.Object) else Array() if issubclass(model_instance, serial.model.Array) else Dictionary() if issubclass(model_instance, serial.model.Dictionary) else None
        else:
            for b in model_instance.__bases__:
                if hasattr(b, '_hooks') and model_instance._hooks is b._hooks:
                    model_instance._hooks = deepcopy(model_instance._hooks)
                    break

    elif isinstance(model_instance, Model) and model_instance._hooks is None:
        model_instance._hooks = deepcopy(writable(type(model_instance)))
    return model_instance._hooks


def write(model_instance, meta):
    """
    Write metadata to a class or instance
    """
    if isinstance(model_instance, type):
        t = model_instance
        mt = Object if issubclass(model_instance, serial.model.Object) else Array if issubclass(model_instance, serial.model.Array) else Dictionary if issubclass(model_instance, serial.model.Dictionary) else None
    else:
        if isinstance(model_instance, Model):
            t = type(model_instance)
            mt = Object if isinstance(model_instance, serial.model.Object) else Array if isinstance(model_instance, serial.model.Array) else Dictionary if isinstance(model_instance, serial.model.Dictionary) else None
        else:
            assert isinstance(meta, mt), 'Hooks assigned to `%s` must be of type `%s`' % (
             qualified_name(t),
             qualified_name(mt))
        model_instance._hooks = meta