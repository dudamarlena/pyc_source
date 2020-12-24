# uncompyle6 version 3.6.7
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pyclearsilver/odb_sqlite.py
# Compiled at: 2004-11-19 12:15:44
__doc__ = '\nusage: %(progname)s [args]\n'
import os, sys, string, time, getopt
from log import *
import odb, sqlite

class Cursor(odb.Cursor):
    __module__ = __name__

    def insert_id(self, tablename, colname):
        return self.cursor.lastrowid

    def execute(self, sql):
        return self.cursor.execute(sql)


class Connection(odb.Connection):
    __module__ = __name__

    def __init__(self, *args, **kwargs):
        odb.Connection.__init__(self)
        self._conn = apply(sqlite.connect, args, kwargs)
        self.SQLError = sqlite.Error

    def getConnType(self):
        return 'sqlite'

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
        cursor.execute("select name from sqlite_master where type='table'")
        rows = cursor.fetchall()
        tables = []
        for row in rows:
            tables.append(row[0])

        return tables

    def supportsTriggers(self):
        return True

    def listTriggers(self, cursor):
        cursor.execute("select name from sqlite_master where type='trigger'")
        rows = cursor.fetchall()
        tables = []
        for row in rows:
            tables.append(row[0])

        return tables

    def listIndices(self, tableName, cursor):
        cursor.execute("select name from sqlite_master where type='index'")
        rows = cursor.fetchall()
        tables = []
        for row in rows:
            tables.append(row[0])

        return tables

    def listFieldsDict(self, table_name, cursor):
        sql = 'pragma table_info(%s)' % table_name
        cursor.execute(sql)
        rows = cursor.fetchall()
        columns = {}
        for row in rows:
            colname = row[1]
            columns[colname] = row

        return columns

    def _tableCreateStatement(self, table_name, cursor):
        sql = "select sql from sqlite_master where type='table' and name='%s'" % table_name
        print sql
        cursor.execute(sql)
        row = cursor.fetchone()
        sqlstatement = row[0]
        return sqlstatement

    def alterTableToMatch(self, table, cursor):
        tableName = table.getTableName()
        tmpTableName = tableName + '_' + str(os.getpid())
        (invalidAppCols, invalidDBCols) = table.checkTable(warnflag=0)
        if not invalidAppCols and not invalidDBCols:
            return
        oldcols = self.listFieldsDict(tableName, cursor)
        tmpcols = []
        newcols = table.getAppColumnList()
        for (colname, coltype, options) in newcols:
            if oldcols.has_key(colname):
                tmpcols.append(colname)

        tmpcolnames = string.join(tmpcols, ',')
        statements = []
        sql = 'create temporary table %s (%s)' % (tmpTableName, tmpcolnames)
        statements.append(sql)
        sql = 'insert into %s select %s from %s' % (tmpTableName, tmpcolnames, tableName)
        statements.append(sql)
        sql = 'drop table %s' % tableName
        statements.append(sql)
        sql = table._createTableSQL()
        statements.append(sql)
        sql = 'insert into %s(%s) select %s from %s' % (tableName, tmpcolnames, tmpcolnames, tmpTableName)
        statements.append(sql)
        sql = 'drop table %s' % tmpTableName
        statements.append(sql)
        for statement in statements:
            print statement
            cursor.execute(statement)


def test():
    pass


def usage(progname):
    print __doc__ % vars()


def main(argv, stdout, environ):
    progname = argv[0]
    (optlist, args) = getopt.getopt(argv[1:], '', ['help', 'test', 'debug'])
    testflag = 0
    if len(args) == 0:
        usage(progname)
        return
    for (field, val) in optlist:
        if field == '--help':
            usage(progname)
            return
        elif field == '--debug':
            debugfull()
        elif field == '--test':
            testflag = 1

    if testflag:
        test()
        return


if __name__ == '__main__':
    main(sys.argv, sys.stdout, os.environ)