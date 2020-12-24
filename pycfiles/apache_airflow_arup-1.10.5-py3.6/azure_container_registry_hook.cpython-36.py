# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/hooks/azure_container_registry_hook.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 1490 bytes
from airflow.hooks.base_hook import BaseHook
from azure.mgmt.containerinstance.models import ImageRegistryCredential

class AzureContainerRegistryHook(BaseHook):
    __doc__ = '\n    A hook to communicate with a Azure Container Registry.\n\n    :param conn_id: connection id of a service principal which will be used\n        to start the container instance\n    :type conn_id: str\n    '

    def __init__(self, conn_id='azure_registry'):
        self.conn_id = conn_id
        self.connection = self.get_conn()

    def get_conn(self):
        conn = self.get_connection(self.conn_id)
        return ImageRegistryCredential(server=(conn.host), username=(conn.login), password=(conn.password))