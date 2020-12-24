# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/hooks/azure_container_volume_hook.py
# Compiled at: 2019-09-11 02:44:38
# Size of source mod 2**32: 2204 bytes
from airflow.hooks.base_hook import BaseHook
from azure.mgmt.containerinstance.models import Volume, AzureFileVolume

class AzureContainerVolumeHook(BaseHook):
    """AzureContainerVolumeHook"""

    def __init__(self, wasb_conn_id='wasb_default'):
        self.conn_id = wasb_conn_id

    def get_storagekey(self):
        conn = self.get_connection(self.conn_id)
        service_options = conn.extra_dejson
        if 'connection_string' in service_options:
            for keyvalue in service_options['connection_string'].split(';'):
                key, value = keyvalue.split('=', 1)
                if key == 'AccountKey':
                    return value

        return conn.password

    def get_file_volume(self, mount_name, share_name, storage_account_name, read_only=False):
        return Volume(name=mount_name, azure_file=AzureFileVolume(share_name=share_name, storage_account_name=storage_account_name,
          read_only=read_only,
          storage_account_key=(self.get_storagekey())))