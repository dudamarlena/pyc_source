# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/hooks/sqlite_hook.py
# Compiled at: 2019-09-11 02:44:38
# Size of source mod 2**32: 1271 bytes
import sqlite3
from airflow.hooks.dbapi_hook import DbApiHook

class SqliteHook(DbApiHook):
    """SqliteHook"""
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