# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/redisobjects/serializers/tuple_serializer.py
# Compiled at: 2019-09-28 15:18:33
# Size of source mod 2**32: 1441 bytes
from .identity_serializer import IdentitySerializer

class TupleSerializer:

    def __init__(self, *value_serializers, separator=','):
        self.value_serializers = value_serializers
        self.separator = separator

    def serialize(self, value):
        if type(value) is not tuple:
            raise RuntimeError('Value must be a tuple!')
        if len(value) != len(self.value_serializers):
            raise RuntimeError('Tuple must be of size %s' % (len(self.value_serializers),))
        return self.separator.join(self.value_serializers[i].serialize(value[i]) for i in range(len(value)))

    def deserialize(self, value):
        parts = value.decode().split(self.separator)
        n = len(self.value_serializers)
        if len(parts) != n:
            raise RuntimeError('Tuple must be of size %s' % (n,))
        return tuple(self.value_serializers[i].deserialize(parts[i]) for i in range(n))

    @staticmethod
    def create_homogeneous(n, value_serializer=IdentitySerializer(), *, separator=','):
        value_serializers = [value_serializer] * n
        return TupleSerializer(*value_serializers, **{'separator': separator})