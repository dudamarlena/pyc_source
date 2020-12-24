# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/hooks/vertica_hook.py
# Compiled at: 2019-09-11 02:44:38
# Size of source mod 2**32: 1616 bytes
from vertica_python import connect
from airflow.hooks.dbapi_hook import DbApiHook

class VerticaHook(DbApiHook):
    __doc__ = '\n    Interact with Vertica.\n    '
    conn_name_attr = 'vertica_conn_id'
    default_conn_name = 'vertica_default'
    supports_autocommit = True

    def get_conn(self):
        """
        Returns verticaql connection object
        """
        conn = self.get_connection(self.vertica_conn_id)
        conn_config = {'user':conn.login, 
         'password':conn.password or '', 
         'database':conn.schema, 
         'host':conn.host or 'localhost'}
        if not conn.port:
            conn_config['port'] = 5433
        else:
            conn_config['port'] = int(conn.port)
        conn = connect(**conn_config)
        return conn