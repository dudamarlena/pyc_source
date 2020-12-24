# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ScoutSuite/providers/azure/resources/sqldatabase/server_azure_ad_administrators.py
# Compiled at: 2020-04-02 05:37:10
# Size of source mod 2**32: 707 bytes
from ScoutSuite.providers.azure.facade.base import AzureFacade
from ScoutSuite.providers.azure.resources.base import AzureResources

class ServerAzureAdAdministrators(AzureResources):

    def __init__(self, facade, resource_group_name, server_name, subscription_id):
        super(ServerAzureAdAdministrators, self).__init__(facade)
        self.resource_group_name = resource_group_name
        self.server_name = server_name
        self.subscription_id = subscription_id

    async def fetch_all(self):
        self['ad_admin'] = await self.facade.sqldatabase.get_server_azure_ad_administrators(self.resource_group_name, self.server_name, self.subscription_id)