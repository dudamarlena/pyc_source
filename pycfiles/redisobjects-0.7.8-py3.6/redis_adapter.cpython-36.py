# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/redisobjects/redis_adapter.py
# Compiled at: 2019-10-05 22:02:52
# Size of source mod 2**32: 627 bytes
"""
The RedisAdapter class is used to adapt to synchronoous Redis APIs that do not have a generic
execute method, but do have 1:1 methods for each Redis command.
"""

class RedisAdapter:

    def __init__(self, redis):
        self.redis = redis

    async def execute(self, *args):
        if len(args) == 0:
            pass
        method_name = args[0]
        if method_name == 'del':
            method_name = 'delete'
        method = getattr(self.redis, method_name)
        if method is None:
            raise LookupError('Method was not found for the given Redis API implementation.')
        return method(*args[1:])