# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ScoutSuite/providers/azure/resources/sqldatabase/replication_links.py
# Compiled at: 2020-04-02 05:37:10
# Size of source mod 2**32: 965 bytes
from ScoutSuite.providers.azure.facade.base import AzureFacade
from ScoutSuite.providers.azure.resources.base import AzureResources

class ReplicationLinks(AzureResources):

    def __init__(self, facade, resource_group_name, server_name, database_name, subscription_id):
        super(ReplicationLinks, self).__init__(facade)
        self.resource_group_name = resource_group_name
        self.server_name = server_name
        self.database_name = database_name
        self.subscription_id = subscription_id

    async def fetch_all(self):
        links = await self.facade.sqldatabase.get_database_replication_links(self.resource_group_name, self.server_name, self.database_name, self.subscription_id)
        self._parse_links(links)

    def _parse_links(self, links):
        links_count = len(list(links))
        self.update({'replication_configured': links_count > 0})