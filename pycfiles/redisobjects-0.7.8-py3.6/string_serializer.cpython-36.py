# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/redisobjects/serializers/string_serializer.py
# Compiled at: 2019-09-28 15:18:33
# Size of source mod 2**32: 198 bytes


class StringSerializer:

    def serialize(self, s):
        if s is not None:
            return s.encode()

    def deserialize(self, value):
        if value is None:
            return value
        else:
            return value.decode()