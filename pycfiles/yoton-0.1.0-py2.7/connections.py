# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/yoton/connections.py
# Compiled at: 2016-03-26 02:53:04
from redis import Redis

class ConnectionFactory(object):

    def __init__(self, redis_config):
        self.redis_config = redis_config

    def get_connection(self, cache_key, database=None):
        raise NotImplementedError()


class SimpleConnectionFactory(ConnectionFactory):

    def __init__(self, redis_config):
        super(SimpleConnectionFactory, self).__init__(redis_config)
        self.default_redis_config = redis_config.get('default')
        self.connections = {}

    def get_connection(self, cache_key, database):
        if database not in self.redis_config and not self.default_redis_config:
            raise Exception(('no redis database found for {}, and no default databaseis available').format(database))
        if database in self.connections:
            return self.connections[database]
        connection_config = self.redis_config.get(database)
        if connection_config:
            connection = self._build_redis_connection(**connection_config)
            self.connections[database] = connection
            return connection
        if 'default' in self.connections:
            return self.connections['default']
        default_connection = self._build_redis_connection(**self.default_redis_config)
        self.connections['default'] = default_connection
        return default_connection

    def _build_redis_connection(self, **kwargs):
        return Redis(**kwargs)