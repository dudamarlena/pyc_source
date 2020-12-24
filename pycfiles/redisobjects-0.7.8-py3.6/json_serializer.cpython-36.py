# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/redisobjects/serializers/json_serializer.py
# Compiled at: 2019-10-06 11:19:37
# Size of source mod 2**32: 274 bytes
import json

class JsonSerializer:

    def __init__(self, *, sort_keys=False):
        self.sort_keys = sort_keys

    def serialize(self, value):
        return json.dumps(value, sort_keys=(self.sort_keys))

    def deserialize(self, value):
        return json.loads(value)