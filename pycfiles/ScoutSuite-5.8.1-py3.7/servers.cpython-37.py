# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ScoutSuite/providers/azure/resources/sqldatabase/servers.py
# Compiled at: 2020-04-02 05:37:10
# Size of source mod 2**32: 1791 bytes
from ScoutSuite.providers.azure.facade.base import AzureFacade
from ScoutSuite.providers.azure.resources.base import AzureCompositeResources
from ScoutSuite.providers.azure.utils import get_resource_group_name
from ScoutSuite.providers.utils import get_non_provider_id
from .databases import Databases
from .server_azure_ad_administrators import ServerAzureAdAdministrators
from .server_blob_auditing_policies import ServerBlobAuditingPolicies
from .server_security_alert_policies import ServerSecurityAlertPolicies

class Servers(AzureCompositeResources):
    _children = [
     (
      Databases, 'databases'),
     (
      ServerAzureAdAdministrators, None),
     (
      ServerBlobAuditingPolicies, 'auditing'),
     (
      ServerSecurityAlertPolicies, 'threat_detection')]

    def __init__(self, facade, subscription_id):
        super(Servers, self).__init__(facade)
        self.subscription_id = subscription_id

    async def fetch_all(self):
        for raw_server in await self.facade.sqldatabase.get_servers(self.subscription_id):
            id, server = self._parse_server(raw_server)
            self[id] = server

        await self._fetch_children_of_all_resources(resources=self,
          scopes={server_id:{'resource_group_name':server['resource_group_name'],  'server_name':server['name'],  'subscription_id':self.subscription_id} for server_id, server in self.items()})

    def _parse_server(self, raw_server):
        server = {}
        server['id'] = get_non_provider_id(raw_server.id)
        server['name'] = raw_server.name
        server['resource_group_name'] = get_resource_group_name(raw_server.id)
        return (server['id'], server)