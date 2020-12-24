# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/peewee/playhouse/berkeleydb.py
# Compiled at: 2018-07-11 18:15:31
import datetime, decimal
from playhouse.sqlite_ext import *
from pysqlite2 import dbapi2 as berkeleydb
berkeleydb.register_adapter(decimal.Decimal, str)
berkeleydb.register_adapter(datetime.date, str)
berkeleydb.register_adapter(datetime.time, str)

class BerkeleyDatabase(SqliteExtDatabase):

    def __init__(self, database, pragmas=None, cache_size=None, page_size=None, multiversion=None, *args, **kwargs):
        super(BerkeleyDatabase, self).__init__(database, pragmas=pragmas, *args, **kwargs)
        if multiversion:
            self._pragmas.append(('multiversion', 'on'))
        if page_size:
            self._pragmas.append(('page_size', page_size))
        if cache_size:
            self._pragmas.append(('cache_size', cache_size))

    def _connect(self, database, **kwargs):
        conn = berkeleydb.connect(database, **kwargs)
        conn.isolation_level = None
        self._add_conn_hooks(conn)
        return conn

    def _set_pragmas(self, conn):
        if self._pragmas:
            cursor = conn.cursor()
            for pragma, value in self._pragmas:
                if pragma == 'multiversion':
                    try:
                        cursor.execute('PRAGMA %s = %s;' % (pragma, value))
                    except berkeleydb.OperationalError:
                        pass

                else:
                    cursor.execute('PRAGMA %s = %s;' % (pragma, value))

            cursor.close()