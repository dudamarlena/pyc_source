# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /marrow/mongo/core/field/array.py
# Compiled at: 2017-09-13 15:15:35
# Size of source mod 2**32: 1195 bytes
from __future__ import unicode_literals
from collections import Iterable, Mapping
from ... import Field
from .base import _HasKind, _CastingKind

class Array(_HasKind, _CastingKind, Field):
    __foreign__ = 'array'
    __allowed_operators__ = {'#array', '$elemMatch', '#rel', '$eq'}

    class List(list):
        __doc__ = 'Placeholder list shadow class to identify already-cast arrays.'

        @classmethod
        def new(cls):
            return cls()

    def __init__(self, *args, **kw):
        if kw.get('assign', False):
            kw.setdefault('default', self.List.new)
        (super(Array, self).__init__)(*args, **kw)

    def to_native(self, obj, name, value):
        if isinstance(value, self.List):
            return value
        else:
            result = self.List(super(Array, self).to_native(obj, name, i) for i in value)
            obj.__data__[self.__name__] = result
            return result

    def to_foreign(self, obj, name, value):
        if isinstance(value, Iterable):
            if not isinstance(value, Mapping):
                return self.List(super(Array, self).to_foreign(obj, name, i) for i in value)
        return super(Array, self).to_foreign(obj, name, value)