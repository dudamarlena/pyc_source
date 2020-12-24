# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pydo/drivers/mysqlconn.py
# Compiled at: 2007-02-15 13:23:36
__doc__ = '\nPyDO driver for MySQL, using the MySQLdb driver.\n\n'
from pydo.dbi import DBIBase, ConnectionPool
from pydo.exceptions import PyDOError
from pydo.operators import BindingConverter
from pydo.dbtypes import DATE, TIMESTAMP, BINARY, INTERVAL
from pydo.field import Field, Unique, Sequence
from pydo.log import debug
import MySQLdb

class MysqlConverter(BindingConverter):
    __module__ = __name__
    converters = {DATE: lambda x: x.value, TIMESTAMP: lambda x: x.value, 
       BINARY: lambda x: x.value, 
       INTERVAL: lambda x: x.value}


class MysqlDBI(DBIBase):
    __module__ = __name__
    auto_increment = True
    autocommit = True
    has_sane_rowcount = False

    def __init__(self, connectArgs, pool=None, verbose=False, initFunc=None):
        if pool and not hasattr(pool, 'connect'):
            pool = ConnectionPool()
        super(MysqlDBI, self).__init__(connectArgs, MySQLdb.connect, MySQLdb, pool, verbose, initFunc)

    def getAutoIncrement(self, name):
        try:
            return self.conn.insert_id()
        except AttributeError:
            raise PyDOError, 'could not get insert id!'

    def getConverter(self):
        return MysqlConverter(self.paramstyle)

    def listTables(self, schema=None):
        """ lists tables in the database."""
        sql = 'SHOW TABLES'
        cur = self.conn.cursor()
        if self.verbose:
            debug('SQL: %s', (sql,))
        cur.execute(sql)
        res = cur.fetchall()
        cur.close()
        if not res:
            return []
        return sorted((x[0] for x in res))

    def describeTable(self, table, schema=None):
        cur = self.conn.cursor()
        if self.verbose:

            def execute(sql):
                debug('SQL: %s', (sql,))
                cur.execute(sql)

        else:
            execute = cur.execute
        sql = "SHOW TABLES LIKE '%s'" % table
        execute(sql)
        res = cur.fetchone()
        if not res:
            raise ValueError, 'table %s not found' % table
        sql = 'SHOW COLUMNS FROM %s' % table
        execute(sql)
        res = cur.fetchall()
        fields = {}
        nullableFields = []
        for row in res:
            (name, tipe, nullable, key, default, extra) = row
            if nullable:
                nullableFields.append(name)
            if not nullable and extra == 'auto_increment':
                fields[name] = Sequence(name)
            else:
                fields[name] = Field(name)

        sql = 'SHOW INDEX FROM %s' % table
        execute(sql)
        res = cur.fetchall()
        cur.close()
        indices = {}
        blacklist = set(nullableFields)
        for row in res:
            keyname = row[2]
            colname = row[4]
            notunique = row[1]
            if notunique:
                blacklist.add(keyname)
                continue
            if keyname in blacklist:
                continue
            indices.setdefault(keyname, [])
            indices[keyname].append(colname)

        unique = set((frozenset(x) for x in indices.values()))
        return (
         fields, unique)