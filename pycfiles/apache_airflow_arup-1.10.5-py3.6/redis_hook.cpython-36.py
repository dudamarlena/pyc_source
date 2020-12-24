# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/hooks/redis_hook.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 2229 bytes
"""
RedisHook module
"""
from redis import Redis
from airflow.hooks.base_hook import BaseHook

class RedisHook(BaseHook):
    __doc__ = '\n    Wrapper for connection to interact with Redis in-memory data structure store\n    '

    def __init__(self, redis_conn_id='redis_default'):
        """
        Prepares hook to connect to a Redis database.

        :param conn_id:     the name of the connection that has the parameters
                            we need to connect to Redis.
        """
        self.redis_conn_id = redis_conn_id
        self.redis = None
        self.host = None
        self.port = None
        self.password = None
        self.db = None

    def get_conn(self):
        """
        Returns a Redis connection.
        """
        conn = self.get_connection(self.redis_conn_id)
        self.host = conn.host
        self.port = conn.port
        self.password = None if str(conn.password).lower() in ('none', 'false', '') else conn.password
        self.db = conn.extra_dejson.get('db', None)
        if not self.redis:
            self.log.debug('Initializing redis object for conn_id "%s" on %s:%s:%s', self.redis_conn_id, self.host, self.port, self.db)
            self.redis = Redis(host=(self.host),
              port=(self.port),
              password=(self.password),
              db=(self.db))
        return self.redis