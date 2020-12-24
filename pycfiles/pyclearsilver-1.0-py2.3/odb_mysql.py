# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pyclearsilver/odb_mysql.py
# Compiled at: 2004-11-19 12:15:33
"""
usage: %(progname)s [args]
"""
import os, sys, string, time, getopt
from log import *
import odb, MySQLdb

class Cursor(odb.Cursor):
    __module__ = __name__

    def insert_id(self, tablename, colname):
        return self.cursor.insert_id()


class Connection(odb.Connection):
    __module__ = __name__

    def __init__(self, host, user, passwd, db):
        odb.Connection.__init__(self)
        self._conn = MySQLdb.connect(host=host, user=user, passwd=passwd, db=db)
        self.SQLError = MySQLdb.Error

    def getConnType(self):
        return 'mysql'

    def cursor(self):
        return Cursor(self._conn.cursor())

    def escape(self, str):
        if str is None:
            return None
        return MySQLdb.escape_string(str)
        return

    def listTables(self, cursor):
        cursor.execute('show tables')
        rows = cursor.fetchall()
        tables = []
        for row in rows:
            tables.append(row[0])

        return tables

    def listIndices(self, tableName, cursor):
        cursor.execute('show index from %s' % tableName)
        rows = cursor.fetchall()
        tables = map(lambda row: row[2], rows)
        return tables

    def listFieldsDict(self, table_name, cursor):
        sql = 'show columns from %s' % table_name
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

    def createTable(self, sql, cursor):
        sql = sql + ' TYPE=INNODB'
        return sql

    def supportsTriggers(self):
        return False