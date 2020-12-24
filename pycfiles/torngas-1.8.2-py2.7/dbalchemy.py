# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/torngas/middleware/dbalchemy.py
# Compiled at: 2016-02-16 00:41:00
"""
dbalchemy中间件，加入此中间件可以自动帮助dbalchemy模块处理连接的关闭
"""
from ..db.dbalchemy import Connector
from tornado.ioloop import PeriodicCallback
from tornado.gen import coroutine
from sqlalchemy import exc
from sqlalchemy import event
from sqlalchemy.pool import Pool
from ..logger import SysLogger
from ..settings_manager import settings
connection = Connector.conn_pool

def connection_event():

    @event.listens_for(Pool, 'checkout')
    def ping_connection(dbapi_connection, connection_record, connection_proxy):
        cursor = dbapi_connection.cursor()
        try:
            cursor.execute('SELECT 1')
        except:
            SysLogger.error('database pool has gone away')
            connection_proxy._pool.dispose()

        cursor.close()


def ping_db(conn_, ping_inteval):

    @coroutine
    def ping_func():
        yield [ conn_.ping_db() for _ in range(settings.PING_CONN_COUNT if 'PING_CONN_COUNT' in settings else 5) ]

    PeriodicCallback(ping_func, ping_inteval * 1000).start()


class DBAlchemyMiddleware(object):

    def process_init(self, application):
        if settings.PING_DB:
            connection_event()
            interval = settings.PING_DB
            if interval > 0:
                for k, conn in connection.items():
                    ping_db(conn, interval)

    def process_endcall(self, handler, clear):
        for k, conn in connection.items():
            if hasattr(conn, 'remove'):
                callable(conn.remove) and conn.remove()