# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ScoutSuite/providers/azure/resources/sqldatabase/databases.py
# Compiled at: 2020-04-02 05:37:10
# Size of source mod 2**32: 1833 bytes
from ScoutSuite.providers.azure.facade.base import AzureFacade
from ScoutSuite.providers.azure.resources.base import AzureCompositeResources
from .database_blob_auditing_policies import DatabaseBlobAuditingPolicies
from .database_threat_detection_policies import DatabaseThreatDetectionPolicies
from .replication_links import ReplicationLinks
from .transparent_data_encryptions import TransparentDataEncryptions

class Databases(AzureCompositeResources):
    _children = [
     (
      DatabaseBlobAuditingPolicies, 'auditing'),
     (
      DatabaseThreatDetectionPolicies, 'threat_detection'),
     (
      ReplicationLinks, None),
     (
      TransparentDataEncryptions, None)]

    def __init__(self, facade, resource_group_name, server_name, subscription_id):
        super(Databases, self).__init__(facade)
        self.resource_group_name = resource_group_name
        self.server_name = server_name
        self.subscription_id = subscription_id

    async def fetch_all(self):
        for db in await self.facade.sqldatabase.get_databases(self.resource_group_name, self.server_name, self.subscription_id):
            if db.name == 'master':
                continue
            self[db.name] = {'id':db.name,  'name':db.name}

        await self._fetch_children_of_all_resources(resources=self,
          scopes={db_id:{'resource_group_name':self.resource_group_name,  'server_name':self.server_name,  'database_name':db['name'],  'subscription_id':self.subscription_id} for db_id, db in self.items()})