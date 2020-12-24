# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pydo/drivers/sqlite3conn.py
# Compiled at: 2007-02-15 13:23:35
"""
PyDO driver for sqlite3, using the pysqlite2 adapter or Python 2.5's
sqlite3 package.
"""
from pydo.dbi import DBIBase, ConnectionPool
from pydo.field import Field, Sequence
from pydo.exceptions import PyDOError
from pydo.dbtypes import DATE, TIMESTAMP, BINARY, INTERVAL, date_formats, timestamp_formats
from pydo.log import debug
from pydo.operators import BindingConverter
import time, datetime
try:
    import sqlite3 as sqlite
except ImportError:
    from pysqlite2 import dbapi2 as sqlite

class Sqlite3DBI(DBIBase):
    __module__ = __name__
    auto_increment = True
    paramstyle = sqlite.paramstyle
    _keeps_tables = True

    def __init__(self, connectArgs, pool=None, verbose=False, initFunc=None):
        if pool and not hasattr(pool, 'connect'):
            pool = ConnectionPool()
        super(Sqlite3DBI, self).__init__(connectArgs, sqlite.connect, sqlite, pool, verbose, initFunc)
        self._lastrowid = None
        return

    def _execute_hook(self, cursor, sql, values, qualified):
        self._lastrowid = cursor.lastrowid

    def getAutoIncrement(self, name):
        return self._lastrowid

    def listTables(self, schema=None):
        """list the tables in the database schema.
      The schema parameter is not supported by this driver.
      """
        if schema is not None:
            raise ValueError, 'db schemas not supported by sqlite driver'
        sql = "SELECT name FROM sqlite_master WHERE type='table' ORDER BY NAME"
        c = self.conn.cursor()
        c.execute(sql)
        res = c.fetchall()
        if res:
            return sorted((x[0] for x in res))
        return ()

    def describeTable(self, table, schema=None):
        if schema is not None:
            raise ValueError, 'db schemas not supported by sqlite driver'
        fields = {}
        unique = set()
        nullable = []
        c = self.conn.cursor()
        if self.verbose:

            def execute(sql):
                debug('SQL: %s', (sql,))
                c.execute(sql)

        else:
            execute = c.execute
        sql = "pragma table_info('%s')" % table
        execute(sql)
        res = c.fetchall()
        if not res:
            raise ValueError, 'no such table: %s' % table
        for row in res:
            (cid, name, type, notnull, dflt_value, pk) = row
            if type == 'INTEGER':
                if int(pk):
                    fields[name] = Sequence(name)
                else:
                    fields[name] = Field(name)
                int(notnull) or nullable.append(name)

        sql = "pragma index_list('%s')" % table
        execute(sql)
        res = c.fetchall()
        for row in res:
            (seq, name, uneek) = row
            if uneek:
                sql = "pragma index_info('%s')" % name
                execute(sql)
                subres = c.fetchall()
                unset = frozenset((x[(-1)] for x in subres))
                if not unset.intersection(nullable):
                    unique.add(unset)

        c.close()
        return (fields, unique)

    def autocommit():

        def fget(self):
            return self.conn.isolation_level == 'IMMEDIATE'

        def fset(self, val):
            val = ['', 'IMMEDIATE'][bool(val)]
            self.conn.isolation_level = val

        return (fget, fset, None, None)

    autocommit = property(*autocommit())