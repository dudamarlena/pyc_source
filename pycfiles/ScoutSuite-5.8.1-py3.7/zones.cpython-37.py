# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ScoutSuite/providers/gcp/resources/zones.py
# Compiled at: 2020-04-02 05:37:10
# Size of source mod 2**32: 660 bytes
from ScoutSuite.providers.gcp.facade.base import GCPFacade
from ScoutSuite.providers.gcp.resources.base import GCPCompositeResources

class Zones(GCPCompositeResources):

    def __init__(self, facade, project_id):
        super(Zones, self).__init__(facade)
        self.project_id = project_id

    async def fetch_all(self):
        raw_zones = await self.facade.gce.get_zones(self.project_id)
        for raw_zone in raw_zones:
            self[raw_zone['name']] = {}

        await self._fetch_children_of_all_resources(resources=self,
          scopes={zone:{'project_id':self.project_id,  'zone':zone} for zone in self})