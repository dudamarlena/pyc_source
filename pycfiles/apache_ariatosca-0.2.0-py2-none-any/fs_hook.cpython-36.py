# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/hooks/fs_hook.py
# Compiled at: 2019-09-11 02:44:38
# Size of source mod 2**32: 1421 bytes
from airflow.hooks.base_hook import BaseHook

class FSHook(BaseHook):
    """FSHook"""

    def __init__(self, conn_id='fs_default'):
        conn = self.get_connection(conn_id)
        self.basepath = conn.extra_dejson.get('path', '')
        self.conn = conn

    def get_conn(self):
        pass

    def get_path(self):
        return self.basepath