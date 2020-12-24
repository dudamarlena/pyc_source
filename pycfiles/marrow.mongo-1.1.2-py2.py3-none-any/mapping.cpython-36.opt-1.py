# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /marrow/mongo/core/field/mapping.py
# Compiled at: 2017-09-13 15:15:35
# Size of source mod 2**32: 638 bytes
from __future__ import unicode_literals
from collections import OrderedDict, Mapping as _Mapping
from ....schema import Attribute
from .array import Array

class Mapping(Array):
    key = Attribute(default='name')

    def to_native(self, obj, name, value):
        kind = self._kind(obj.__class__)
        result = super(Mapping, self).to_native(obj, name, value)
        result = ((doc[(~getattr(kind, self.key))], doc) for doc in result)
        return OrderedDict(result)

    def to_foreign(self, obj, name, value):
        if isinstance(value, _Mapping):
            value = value.values()
        return super(Mapping, self).to_foreign(obj, name, value)