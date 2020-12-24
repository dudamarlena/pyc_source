# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/keystoneredis/common/session.py
# Compiled at: 2013-02-13 13:57:35
"""Redis backends for the various services."""
import redis, redismultiwrite as redismw
from keystoneredis.common.redissl import Connection as SslConnection
from keystone.common import logging
from keystone import config
from keystone.openstack.common import cfg
LOG = logging.getLogger(__name__)
CONF = config.CONF
CONF.register_opt(cfg.StrOpt('read_connection', default=None), group='redis')
CONF.register_opt(cfg.StrOpt('connection', default='localhost'), group='redis')
CONF.register_opt(cfg.MultiStrOpt('xdc_connection'), group='redis')
CONF.register_opt(cfg.IntOpt('idle_timeout', default=200), group='redis')
CONF.register_opt(cfg.IntOpt('database', default=0), group='redis')
CONF.register_opt(cfg.IntOpt('retries', default=3), group='redis')
CONF.register_opt(cfg.IntOpt('greenpool_size', default=None), group='redis')
CONF.register_opt(cfg.BoolOpt('ssl', default=False), group='redis')
CONF.register_opt(cfg.StrOpt('keyfile', default=None), group='redis')
CONF.register_opt(cfg.StrOpt('certfile', default=None), group='redis')
CONF.register_opt(cfg.StrOpt('ca_certs', default=None), group='redis')

class RedisSession(object):

    def __init__(self, **kwargs):
        read = kwargs.get('read_connection', CONF.redis.read_connection)
        local = kwargs.get('connection', CONF.redis.connection)
        xdc = kwargs.get('xdc_connections', CONF.redis.xdc_connection) or []
        database = kwargs.get('database', CONF.redis.database)
        idle_timeout = kwargs.get('idle_timeout', CONF.redis.idle_timeout)
        retries = kwargs.get('retries', CONF.redis.retries)
        greenpool_size = kwargs.get('greenpool_size', CONF.redis.greenpool_size)
        self.ttl_seconds = CONF.token.expiration
        self.local_client = self._create_client(local, database, idle_timeout)
        self.xdc_clients = [ self._create_client(conn, database, idle_timeout) for conn in xdc
                           ]
        local = self._create_client(local, database, idle_timeout)
        remote = [ self._create_client(conn, database, idle_timeout) for conn in xdc
                 ]
        self.conn = redismw.RedisMultiWrite(local, remote, retries=retries, log=LOG, pool_size=greenpool_size)
        if read:
            self.readonly = self._create_client(read, database, idle_timeout)
        else:
            self.readonly = self.local_client

    def _create_client(self, connection, database, idle_timeout):
        try:
            host, port = connection.rsplit(':', 1)
        except ValueError:
            host = connection
            port = 6379

        if CONF.redis.ssl:
            pool = redis.ConnectionPool(connection_class=SslConnection, host=host, port=port, db=database, socket_timeout=idle_timeout, keyfile=CONF.redis.keyfile, certfile=CONF.redis.certfile, ca_certs=CONF.redis.ca_certs)
        else:
            pool = redis.ConnectionPool(host=host, port=port, db=database, socket_timeout=idle_timeout)
        return redis.StrictRedis(connection_pool=pool)