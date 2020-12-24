# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/hooks/samba_hook.py
# Compiled at: 2019-09-11 02:44:38
# Size of source mod 2**32: 1807 bytes
from smbclient import SambaClient
import os
from airflow.hooks.base_hook import BaseHook

class SambaHook(BaseHook):
    """SambaHook"""

    def __init__(self, samba_conn_id):
        self.conn = self.get_connection(samba_conn_id)

    def get_conn(self):
        samba = SambaClient(server=(self.conn.host),
          share=(self.conn.schema),
          username=(self.conn.login),
          ip=(self.conn.host),
          password=(self.conn.password))
        return samba

    def push_from_local(self, destination_filepath, local_filepath):
        samba = self.get_conn()
        if samba.exists(destination_filepath):
            if samba.isfile(destination_filepath):
                samba.remove(destination_filepath)
        else:
            folder = os.path.dirname(destination_filepath)
        if not samba.exists(folder):
            samba.mkdir(folder)
        samba.upload(local_filepath, destination_filepath)