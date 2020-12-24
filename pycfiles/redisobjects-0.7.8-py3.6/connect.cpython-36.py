# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/redisobjects/connect.py
# Compiled at: 2019-10-05 22:02:52
# Size of source mod 2**32: 577 bytes
from aioredis import create_connection
import fakeredis
from .redis_manager import RedisManager
from .redis_adapter import RedisAdapter

async def connect(address, **kwargs):
    connection = await create_connection(address, **kwargs)
    redis_manager = RedisManager(connection)
    return redis_manager


def connect_adapter(redis):
    return RedisManager(RedisAdapter(redis))


def connect_fakeredis():
    return RedisManager(RedisAdapter(fakeredis.FakeStrictRedis()))