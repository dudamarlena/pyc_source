# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/foundation/factories/postgres_connection.py
# Compiled at: 2012-10-12 07:02:39
import psycopg2
from sql_connection import SQLConnection

class PostgresConnection(SQLConnection):

    def __init__(self, params):
        self._db = psycopg2.connect(database=params.get('database', None), host=params.get('hostname', '127.0.0.1'), user=params.get('username', ''), password=params.get('password', ''))
        return

    def connect(self):
        return self._db

    def cursor(self):
        return self._db.cursor()

    def bind_param(self, offset):
        return '%s'

    def get_type_from_code(string, code):
        if code == psycopg2.STRING:
            return 'string'
        else:
            if code == psycopg2.BINARY:
                return 'binary'
            if code == psycopg2.DATETIME:
                return 'datetime'
            if code == psycopg2.extensions.DATE:
                return 'date'
            if code == psycopg2.extensions.FLOAT:
                return 'float'
            if code == psycopg2.extensions.INTEGER:
                return 'integer'
            if code == psycopg2.extensions.UNICODE:
                return 'string'
            return 'unknown'