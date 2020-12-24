# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/prihodad/Documents/projects/visitor/golm/golm/core/persistence.py
# Compiled at: 2018-04-15 14:00:29
# Size of source mod 2**32: 767 bytes
import redis
from django.conf import settings
_connection_pool = None
_redis = None

def get_redis():
    global _connection_pool
    global _redis
    if not _connection_pool:
        config = settings.GOLEM_CONFIG.get('REDIS')
        _connection_pool = redis.ConnectionPool(host=(config['HOST']),
          port=(config['PORT']),
          password=(config['PASSWORD']),
          db=0,
          max_connections=2)
    if not _redis:
        _redis = redis.StrictRedis(connection_pool=_connection_pool)
    return _redis


def get_elastic():
    from elasticsearch import Elasticsearch
    config = settings.GOLEM_CONFIG.get('ELASTIC')
    if not config:
        return
    else:
        return Elasticsearch((config['HOST']), port=(config['PORT']))