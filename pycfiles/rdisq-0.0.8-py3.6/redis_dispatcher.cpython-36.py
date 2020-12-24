# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/rdisq/redis_dispatcher.py
# Compiled at: 2020-03-07 02:12:19
# Size of source mod 2**32: 1209 bytes
__author__ = 'smackware'
from redis import Redis
from redis import ConnectionPool

class AbstractRedisDispatcher(object):

    def __init__(self, *args, **kwargs):
        pass

    def get_redis(self, *args, **kwargs):
        """
        Produce an instance of an active redis connection
        """
        raise NotImplementedError('Must implement get_redis(self) method of Rdisq subclass')


class SimpleRedisDispatcher(AbstractRedisDispatcher):
    redis_args = None
    redis_kwargs = None

    def __init__(self, *redis_args, **redis_kwargs):
        self.redis_args = redis_args
        self.redis_kwargs = redis_kwargs
        AbstractRedisDispatcher.__init__(self)

    def get_redis(self):
        return Redis(*self.redis_args, **self.redis_kwargs)


class LocalRedisDispatcher(SimpleRedisDispatcher):

    def __init__(self):
        SimpleRedisDispatcher.__init__(self)


class PoolRedisDispatcher(AbstractRedisDispatcher):
    redis_pool = None

    def __init__(self, *pool_args, **pool_kwargs):
        self.redis_pool = ConnectionPool(*pool_args, **pool_kwargs)
        AbstractRedisDispatcher.__init__(self)

    def get_redis(self):
        return Redis(connection_pool=(self.redis_pool))