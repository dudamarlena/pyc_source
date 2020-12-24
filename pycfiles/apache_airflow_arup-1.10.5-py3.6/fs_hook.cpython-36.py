# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/hooks/fs_hook.py
# Compiled at: 2019-09-11 02:44:38
# Size of source mod 2**32: 1421 bytes
from airflow.hooks.base_hook import BaseHook

class FSHook(BaseHook):
    __doc__ = '\n    Allows for interaction with an file server.\n\n    Connection should have a name and a path specified under extra:\n\n    example:\n    Conn Id: fs_test\n    Conn Type: File (path)\n    Host, Schema, Login, Password, Port: empty\n    Extra: {"path": "/tmp"}\n    '

    def __init__(self, conn_id='fs_default'):
        conn = self.get_connection(conn_id)
        self.basepath = conn.extra_dejson.get('path', '')
        self.conn = conn

    def get_conn(self):
        pass

    def get_path(self):
        return self.basepath