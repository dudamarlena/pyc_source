# uncompyle6 version 3.6.7
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pyclearsilver/odb_postgres.py
# Compiled at: 2004-11-19 12:15:55
__doc__ = '\nusage: %(progname)s [args]\n'
import os, sys, string, time, getopt
from log import *
import odb
from pyPgSQL import PgSQL

class Cursor(odb.Cursor):
    __module__ = __name__

    def insert_id(self, tablename, colname):
        self.execute('select last_value from %s_%s_seq' % (tablename, colname))
        row = self.fetchone()
        return row[0]


class Connection(odb.Connection):
    __module__ = __name__

    def __init__(self, *args, **kwargs):
        odb.Connection.__init__(self)
        self._conn = apply(PgSQL.connect, args, kwargs)
        self.SQLError = PgSQL.OperationalError

    def getConnType(self):
        return 'postgres'

    def cursor(self):
        return Cursor(self._conn.cursor())

    def escape(self, str):
        if str is None:
            return None
        elif type(str) == type(''):
            return string.replace(str, "'", "''")
        elif type(str) == type(1):
            return str
        else:
            raise 'unknown column data type: %s' % type(str)
        return

    def listTables(self, cursor):
        cursor.execute('select tablename from pg_catalog.pg_tables')
        rows = cursor.fetchall()
        tables = []
        for row in rows:
            tables.append(row[0])

        return tables

    def listIndices(self, tableName, cursor):
        sql = "select indexname from pg_catalog.pg_indexes where tablename='%s'" % tableName
        cursor.execute(sql)
        rows = cursor.fetchall()
        tables = map(lambda row: row[0], rows)
        return tables

    def listFieldsDict(self, table_name, cursor):
        sql = "SELECT c.oid,  n.nspname,  c.relname FROM pg_catalog.pg_class c     LEFT JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace WHERE pg_catalog.pg_table_is_visible(c.oid)      AND c.relname = '%s' ORDER BY 2, 3;" % table_name
        cursor.execute(sql)
        row = cursor.fetchone()
        oid = row[0]
        sql = "SELECT a.attname,  pg_catalog.format_type(a.atttypid, a.atttypmod),  (SELECT substring(d.adsrc for 128) FROM pg_catalog.pg_attrdef d   WHERE d.adrelid = a.attrelid AND d.adnum = a.attnum AND a.atthasdef),  a.attnotnull, a.attnum FROM pg_catalog.pg_attribute a WHERE a.attrelid = '%s' AND a.attnum > 0 AND NOT a.attisdropped ORDER BY a.attnum" % oid
        cursor.execute(sql)
        rows = cursor.fetchall()
        columns = {}
        for row in rows:
            colname = row[0]
            columns[colname] = row

        return columns

    def alterTableToMatch(self, table, cursor):
        (invalidAppCols, invalidDBCols) = table.checkTable()
        if not invalidAppCols:
            return
        defs = []
        for colname in invalidAppCols.keys():
            col = table.getColumnDef(colname)
            colname = col[0]
            coltype = col[1]
            options = col[2]
            defs.append(table._colTypeToSQLType(colname, coltype, options))

        defs = string.join(defs, ', ')
        sql = 'alter table %s add column ' % table.getTableName()
        sql = sql + '(' + defs + ')'
        print sql
        cursor.execute(sql)

    def auto_increment(self, coltype):
        return (
         'SERIAL', None)
        return

    def supportsTriggers(self):
        return False