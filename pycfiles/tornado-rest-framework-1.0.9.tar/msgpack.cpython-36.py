# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/work/lib/pyenv/versions/3.6.1/envs/maestro/lib/python3.6/site-packages/rest_framework/core/serializers/msgpack.py
# Compiled at: 2018-05-15 02:30:30
# Size of source mod 2**32: 203 bytes
import msgpack

class Handler:

    def dumps(self, value):
        return msgpack.dumps(value)

    def loads(self, value):
        return msgpack.loads(value, encoding='utf-8')