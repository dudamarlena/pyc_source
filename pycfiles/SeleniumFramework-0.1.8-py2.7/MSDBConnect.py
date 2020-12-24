# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\MSDBConnect.py
# Compiled at: 2018-03-27 19:20:48
import pymssql

class MSDBConnect:
    server = None
    port = None
    user = None
    password = None
    database = None
    conn = None

    def connect(self, connection_info):
        if 'port' in connection_info:
            self.conn = pymssql.connect(server=connection_info['server'], port=connection_info['port'], user=connection_info['user'], password=connection_info['password'], database=connection_info['database'])
        else:
            self.conn = pymssql.connect(server=connection_info['server'], user=connection_info['user'], password=connection_info['password'], database=connection_info['database'])

    def disconnect(self):
        self.conn.close()

    def execute(self, query):
        cursor = self.conn.cursor()
        cursor.execute(query)
        return cursor.fetchall()