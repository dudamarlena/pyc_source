# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/webdb/adapter/sqlite.py
# Compiled at: 2018-02-14 05:43:10
# Size of source mod 2**32: 1483 bytes
import sqlite3, os
from .exceptions import DatabaseError
from .abstractsql import AbstractSQLDB
from .abc import AbstractDBMS

class SqliteDB(AbstractSQLDB):
    __doc__ = '\n\tSQLite3 adapter.\n\n\tThe constuctor requires the filename of the\n\tdatabase file.\n\t'

    def __init__(self, filename):
        AbstractSQLDB.__init__(self)
        self.filename = filename

    def open(self):
        self._con = sqlite3.connect(self.filename)

    def close(self):
        self._con.close()

    def get_column_names(self, table):
        if table not in self.get_table_names():
            raise DatabaseError('unknown table: {}'.format(table))
        cursor = self._con.cursor()
        cursor.execute('PRAGMA table_info({})'.format(table))
        return [row[1] for row in cursor.fetchall()]

    def get_table_names(self):
        cursor = self._con.cursor()
        cursor.execute('SELECT name FROM sqlite_master WHERE type = "table"')
        return [row[0] for row in cursor.fetchall()]


class SqliteDBMS(AbstractDBMS):
    __doc__ = '\n\tDBMS for SQLite files. All databases are files under ``path``.\n\t'

    def __init__(self, path, filenames, inject=None, inject_as=None):
        AbstractDBMS.__init__(self)
        self._path = path
        self._filenames = filenames
        self.inject = inject
        self.inject_as = inject_as

    def dispatch_DB(self, db_name):
        if db_name not in self._filenames:
            raise DatabaseError('unknown database')
        full_path = os.path.join(self._path, db_name)
        if not os.path.exists(full_path):
            raise DatabaseError('database does not exist')
        return SqliteDB(full_path)