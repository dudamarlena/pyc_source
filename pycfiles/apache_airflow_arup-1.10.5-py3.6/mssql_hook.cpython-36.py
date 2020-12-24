# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/hooks/mssql_hook.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 1747 bytes
import pymssql
from airflow.hooks.dbapi_hook import DbApiHook

class MsSqlHook(DbApiHook):
    __doc__ = '\n    Interact with Microsoft SQL Server.\n    '
    conn_name_attr = 'mssql_conn_id'
    default_conn_name = 'mssql_default'
    supports_autocommit = True

    def __init__(self, *args, **kwargs):
        (super(MsSqlHook, self).__init__)(*args, **kwargs)
        self.schema = kwargs.pop('schema', None)

    def get_conn(self):
        """
        Returns a mssql connection object
        """
        conn = self.get_connection(self.mssql_conn_id)
        conn = pymssql.connect(server=(conn.host),
          user=(conn.login),
          password=(conn.password),
          database=(self.schema or conn.schema),
          port=(conn.port))
        return conn

    def set_autocommit(self, conn, autocommit):
        conn.autocommit(autocommit)

    def get_autocommit(self, conn):
        return conn.autocommit_state