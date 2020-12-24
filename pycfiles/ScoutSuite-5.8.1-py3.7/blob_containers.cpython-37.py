# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ScoutSuite/providers/azure/resources/storageaccounts/blob_containers.py
# Compiled at: 2020-04-02 05:37:10
# Size of source mod 2**32: 1324 bytes
from ScoutSuite.providers.azure.facade.base import AzureFacade
from ScoutSuite.providers.azure.resources.base import AzureResources

class BlobContainers(AzureResources):

    def __init__(self, facade, resource_group_name, storage_account_name, subscription_id):
        super(BlobContainers, self).__init__(facade)
        self.resource_group_name = resource_group_name
        self.storage_account_name = storage_account_name
        self.subscription_id = subscription_id

    async def fetch_all(self):
        raw_blob_containers = await self.facade.storageaccounts.get_blob_containers(self.resource_group_name, self.storage_account_name, self.subscription_id)
        for raw_blob_container in raw_blob_containers:
            id, blob_container = self._parse_blob_container(raw_blob_container)
            self[id] = blob_container

    def _parse_blob_container(self, raw_blob_container):
        blob_container = {}
        blob_container['id'] = raw_blob_container.name
        blob_container['public_access_allowed'] = raw_blob_container.public_access != 'None'
        return (
         blob_container['id'], blob_container)