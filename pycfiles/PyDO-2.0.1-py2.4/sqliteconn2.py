# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pydo/drivers/sqliteconn2.py
# Compiled at: 2007-02-15 13:23:35
"""
PyDO driver for sqlite v3, using the sqlite3 module
(built in to Python 2.5+), falling back to the external
pysqlite2 module.

"""
from pydo.dbi import DBIBase, ConnectionPool
from pydo.field import Field, Sequence
from pydo.exceptions import PyDOError
from pydo.log import debug
from pydo.operators import BindingConverter
try:
    from sqlite3 import dbapi2 as sqlite
except ImportError:
    from pysqlite2 import dbapi2 as sqlite

for (t, ulist) in (('date', ('DATE', )), ('timestamp', ('TIMESTAMP', 'DATE'))):
    try:
        c = sqlite.converters[t]
    except KeyError:
        continue
    else:
        for u in ulist:
            if u not in sqlite.converters:
                sqlite.register_converter(u, c)

        del c
        del u

del t
del ulist

class SqliteConverter(BindingConverter):
    __module__ = __name__
    converters = {}


def sqlite_connect(*args, **kwargs):
    return sqlite.connect(detect_types=sqlite.PARSE_DECLTYPES, *args, **kwargs)


class SqliteDBI(DBIBase):
    __module__ = __name__
    auto_increment = True
    paramstyle = 'qmark'

    def __init__(self, connectArgs, pool=None, verbose=False, initFunc=None):
        if pool and not hasattr(pool, 'connect'):
            pool = ConnectionPool()
        super(SqliteDBI, self).__init__(connectArgs, sqlite_connect, sqlite, pool, verbose, initFunc)
        self._isolation_level = ''

    def getConverter(self):
        return SqliteConverter(self.paramstyle)

    def getAutoIncrement(self, name):
        sql = 'SELECT last_insert_rowid ()'
        return self.conn.execute(sql).fetchone()[0]

    def listTables(self, schema=None):
        """list the tables in the database schema.
      The schema parameter is not supported by this driver.
      """
        if schema is not None:
            raise ValueError, 'db schemas not supported by sqlite driver'
        sql = "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
        return self.conn.execute(sql).fetchall()

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
            return self.conn.isolation_level is None

        def fset(self, val):
            current_value = self.conn.isolation_level is None
            if bool(current_value) != bool(val):
                if val:
                    self._isolation_level = self.conn.isolation_level
                    self.conn.isolation_level = None
                else:
                    self.conn.isolation_level = self._isolation_level or ''
            return

        return (
         fget, fset, None, None)

    autocommit = property(*autocommit())