# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/alelog01/git/resource_locker/src/resource_locker/factories/redis.py
# Compiled at: 2018-02-01 06:38:36
# Size of source mod 2**32: 920 bytes
import logging, redis_lock
from redis import StrictRedis
from .meta import LockFactoryMeta

class RedisLockFactory(LockFactoryMeta):

    def __init__(self, client=None):
        self.client = client or StrictRedis()
        self.logger = logging.getLogger(__name__)

    def new_lock(self, key, **params):
        """Creates a new lock with a lock manager"""
        opts = {k:v for k, v in params.items() if k in frozenset({'expire', 'auto_renewal'}) if k in frozenset({'expire', 'auto_renewal'})}
        return (redis_lock.Lock)(self.client, name=key, **opts)

    def get_lock_list(self):
        """Gets a list of live locks to optimise acquisition attempts"""
        prefix = 'lock:'
        return [k.decode('utf8').split(':', 1)[1] for k in self.client.keys(f"{prefix}*")]

    def clear_all(self):
        """Clears all locks"""
        self.logger.critical('caution: clearing all locks; collision safety is voided')
        redis_lock.reset_all(self.client)