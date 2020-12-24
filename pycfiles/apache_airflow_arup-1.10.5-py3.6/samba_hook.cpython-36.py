# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/hooks/samba_hook.py
# Compiled at: 2019-09-11 02:44:38
# Size of source mod 2**32: 1807 bytes
from smbclient import SambaClient
import os
from airflow.hooks.base_hook import BaseHook

class SambaHook(BaseHook):
    __doc__ = '\n    Allows for interaction with an samba server.\n    '

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