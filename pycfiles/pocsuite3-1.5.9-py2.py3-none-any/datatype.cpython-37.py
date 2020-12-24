# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/boyhack/programs/pocsuite3/pocsuite3/lib/core/datatype.py
# Compiled at: 2019-03-15 03:35:12
# Size of source mod 2**32: 1165 bytes
from collections import OrderedDict

class AttribDict(OrderedDict):
    __doc__ = "\n    AttrDict extends OrderedDict to provide attribute-style access.\n    Items starting with __ or _OrderedDict__ can't be accessed as attributes.\n    "
    __exclude_keys__ = set()

    def __getattr__(self, name):
        if name.startswith('__') or name.startswith('_OrderedDict__') or name in self.__exclude_keys__:
            return super(AttribDict, self).__getattribute__(name)
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, name, value):
        if name.startswith('__') or name.startswith('_OrderedDict__') or name in self.__exclude_keys__:
            return super(AttribDict, self).__setattr__(name, value)
        self[name] = value

    def __delattr__(self, name):
        if name.startswith('__') or name.startswith('_OrderedDict__') or name in self.__exclude_keys__:
            return super(AttribDict, self).__delattr__(name)
        del self[name]