# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\pyDots\objects.py
# Compiled at: 2017-01-16 16:07:47
from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals
from collections import Mapping
from datetime import date, datetime
from decimal import Decimal
from types import NoneType, GeneratorType
from pyDots import wrap, unwrap, Data, FlatList, NullType, get_attr, set_attr
_get = object.__getattribute__
_set = object.__setattr__
WRAPPED_CLASSES = set()

class DataObject(Mapping):
    """
    TREAT AN OBJECT LIKE DATA
    """

    def __init__(self, obj):
        _set(self, b'_obj', obj)

    def __getattr__(self, item):
        obj = _get(self, b'_obj')
        output = get_attr(obj, item)
        return datawrap(output)

    def __setattr__(self, key, value):
        obj = _get(self, b'_obj')
        set_attr(obj, key, value)

    def __getitem__(self, item):
        obj = _get(self, b'_obj')
        output = get_attr(obj, item)
        return datawrap(output)

    def keys(self):
        obj = _get(self, b'_obj')
        try:
            return obj.__dict__.keys()
        except Exception as e:
            raise e

    def items(self):
        obj = _get(self, b'_obj')
        try:
            return obj.__dict__.items()
        except Exception as e:
            raise e

    def iteritems(self):
        obj = _get(self, b'_obj')
        try:
            return obj.__dict__.iteritems()
        except Exception as e:

            def output():
                for k in dir(obj):
                    if k.startswith(b'__'):
                        continue
                    yield (
                     k, getattr(obj, k, None))

                return

            return output()

    def __data__(self):
        return self

    def __iter__(self):
        return (k for k in self.keys())

    def __str__(self):
        obj = _get(self, b'_obj')
        return str(obj)

    def __len__(self):
        obj = _get(self, b'_obj')
        return len(obj)

    def __call__(self, *args, **kwargs):
        obj = _get(self, b'_obj')
        return obj(*args, **kwargs)


def datawrap(v):
    type_ = _get(v, b'__class__')
    if type_ is dict:
        m = Data()
        _set(m, b'_dict', v)
        return m
    else:
        if type_ is Data:
            return v
        else:
            if type_ is DataObject:
                return v
            if type_ is NoneType:
                return
            if type_ is list:
                return FlatList(v)
            if type_ is GeneratorType:
                return (wrap(vv) for vv in v)
            if isinstance(v, (Mapping, basestring, int, float, Decimal, datetime, date, Data, FlatList, NullType, NoneType)):
                return v
            if hasattr(v, b'__data__'):
                return v.__data__()
            return DataObject(v)

        return


class DictClass(object):
    """
    ALLOW INSTANCES OF class_ TO ACK LIKE dicts
    ALLOW CONSTRUCTOR TO ACCEPT @use_settings
    """

    def __init__(self, class_):
        WRAPPED_CLASSES.add(class_)
        self.class_ = class_
        self.constructor = class_.__init__

    def __call__(self, *args, **kwargs):
        settings = wrap(kwargs).settings
        params = self.constructor.func_code.co_varnames[1:self.constructor.func_code.co_argcount]
        if not self.constructor.func_defaults:
            defaults = {}
        else:
            defaults = {k:v for k, v in zip(reversed(params), reversed(self.constructor.func_defaults))}
        ordered_params = dict(zip(params, args))
        output = self.class_(**params_pack(params, ordered_params, kwargs, settings, defaults))
        return DataObject(output)


def params_pack(params, *args):
    settings = {}
    for a in args:
        for k, v in a.items():
            k = unicode(k)
            if k in settings:
                continue
            settings[k] = v

    output = {str(k):unwrap(settings[k]) for k in params if k in settings}
    return output