# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ScoutSuite/providers/azure/resources/sqldatabase/database_threat_detection_policies.py
# Compiled at: 2020-04-02 05:37:10
# Size of source mod 2**32: 1224 bytes
from ScoutSuite.providers.azure.facade.base import AzureFacade
from ScoutSuite.providers.azure.resources.base import AzureResources

class DatabaseThreatDetectionPolicies(AzureResources):

    def __init__(self, facade, resource_group_name, server_name, database_name, subscription_id):
        super(DatabaseThreatDetectionPolicies, self).__init__(facade)
        self.resource_group_name = resource_group_name
        self.server_name = server_name
        self.database_name = database_name
        self.subscription_id = subscription_id

    async def fetch_all(self):
        policies = await self.facade.sqldatabase.get_database_threat_detection_policies(self.resource_group_name, self.server_name, self.database_name, self.subscription_id)
        self._parse_policies(policies)

    def _parse_policies(self, policies):
        self.update({'threat_detection_enabled':policies.state == 'Enabled', 
         'alerts_enabled':policies.disabled_alerts == '', 
         'send_alerts_enabled':policies.email_addresses != '' and policies.email_account_admins == 'Enabled', 
         'retention_days':policies.retention_days})