# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/foundation/factories/informix_connection.py
# Compiled at: 2012-10-12 07:02:39
import informixdb
from sql_connection import SQLConnection

class InformixConnection(SQLConnection):

    def __init__(self, params):
        self._db = informixdb.connect(params.get('url'), params.get('username'), params.get('password'))

    def connect(self):
        return self._db

    def cursor(self):
        return self._db.cursor()

    def get_type_from_code(string, code):
        if code == 'serial':
            return 'integer'
        else:
            if code == 'string':
                return 'string'
            if code == 'integer':
                return 'integer'
            if code == 'float':
                return 'float'
            if code == 'decimal':
                return 'decimal'
            if code == 'smallint':
                return 'integer'
            if code == 'char':
                return 'string'
            if code == 'varchar':
                return 'string'
            if code == 'date':
                return 'date'
            if code == 'datetime':
                return 'datetime'
            return 'unknown'