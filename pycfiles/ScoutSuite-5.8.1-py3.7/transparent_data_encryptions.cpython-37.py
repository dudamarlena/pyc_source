# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ScoutSuite/providers/azure/resources/sqldatabase/transparent_data_encryptions.py
# Compiled at: 2020-04-02 05:37:10
# Size of source mod 2**32: 1016 bytes
from ScoutSuite.providers.azure.facade.base import AzureFacade
from ScoutSuite.providers.azure.resources.base import AzureResources

class TransparentDataEncryptions(AzureResources):

    def __init__(self, facade, resource_group_name, server_name, database_name, subscription_id):
        super(TransparentDataEncryptions, self).__init__(facade)
        self.resource_group_name = resource_group_name
        self.server_name = server_name
        self.database_name = database_name
        self.subscription_id = subscription_id

    async def fetch_all(self):
        encryptions = await self.facade.sqldatabase.get_database_transparent_data_encryptions(self.resource_group_name, self.server_name, self.database_name, self.subscription_id)
        self._parse_encryptions(encryptions)

    def _parse_encryptions(self, encryptions):
        self.update({'transparent_data_encryption_enabled': encryptions.status == 'Enabled'})