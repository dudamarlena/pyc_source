# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ScoutSuite/providers/gcp/resources/regions.py
# Compiled at: 2020-04-02 05:37:10
# Size of source mod 2**32: 682 bytes
from ScoutSuite.providers.gcp.facade.base import GCPFacade
from ScoutSuite.providers.gcp.resources.base import GCPCompositeResources

class Regions(GCPCompositeResources):

    def __init__(self, facade, project_id):
        super(Regions, self).__init__(facade)
        self.project_id = project_id

    async def fetch_all(self):
        raw_regions = await self.facade.gce.get_regions(self.project_id)
        for raw_region in raw_regions:
            self[raw_region['name']] = {}

        await self._fetch_children_of_all_resources(resources=self,
          scopes={region:{'project_id':self.project_id,  'region':region} for region in self})