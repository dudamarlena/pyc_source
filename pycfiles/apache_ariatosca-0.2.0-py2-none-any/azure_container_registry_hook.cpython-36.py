# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/hooks/azure_container_registry_hook.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 1490 bytes
from airflow.hooks.base_hook import BaseHook
from azure.mgmt.containerinstance.models import ImageRegistryCredential

class AzureContainerRegistryHook(BaseHook):
    """AzureContainerRegistryHook"""

    def __init__(self, conn_id='azure_registry'):
        self.conn_id = conn_id
        self.connection = self.get_conn()

    def get_conn(self):
        conn = self.get_connection(self.conn_id)
        return ImageRegistryCredential(server=(conn.host), username=(conn.login), password=(conn.password))