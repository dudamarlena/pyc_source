# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/test/hydro/connectors/check_connections.py
# Compiled at: 2014-11-23 10:45:29
__author__ = 'yanivshalev'
from hydro.connectors.mysql import MySqlConnector
if __name__ == '__main__':
    params = {'source_type': 'mysql', 'connection_type': 'connection_string', 
       'connection_string': '127.0.0.1', 
       'db_name': 'test', 
       'db_user': 'xxx', 
       'db_password': 'yyy'}
    con = MySqlConnector(params)
    print con.execute('select 1 a')