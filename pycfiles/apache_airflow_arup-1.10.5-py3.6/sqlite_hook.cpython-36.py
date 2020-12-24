# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/hooks/sqlite_hook.py
# Compiled at: 2019-09-11 02:44:38
# Size of source mod 2**32: 1271 bytes
import sqlite3
from airflow.hooks.dbapi_hook import DbApiHook

class SqliteHook(DbApiHook):
    __doc__ = '\n    Interact with SQLite.\n    '
    conn_name_attr = 'sqlite_conn_id'
    default_conn_name = 'sqlite_default'
    supports_autocommit = False

    def get_conn(self):
        """
        Returns a sqlite connection object
        """
        conn = self.get_connection(self.sqlite_conn_id)
        conn = sqlite3.connect(conn.host)
        return conn