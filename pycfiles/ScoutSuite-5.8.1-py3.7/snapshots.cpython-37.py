# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ScoutSuite/providers/gcp/resources/gce/snapshots.py
# Compiled at: 2020-04-02 05:37:10
# Size of source mod 2**32: 1293 bytes
from ScoutSuite.providers.base.resources.base import Resources
from ScoutSuite.providers.gcp.facade.base import GCPFacade

class Snapshots(Resources):

    def __init__(self, facade, project_id):
        super(Snapshots, self).__init__(facade)
        self.project_id = project_id

    async def fetch_all(self):
        raw_snapshots = await self.facade.gce.get_snapshots(self.project_id)
        for raw_snapshot in raw_snapshots:
            snapshot_id, snapshot = self._parse_snapshot(raw_snapshot)
            self[snapshot_id] = snapshot

    def _parse_snapshot(self, raw_snapshot):
        snapshot_dict = {}
        snapshot_dict['id'] = raw_snapshot['id']
        snapshot_dict['name'] = raw_snapshot['name']
        snapshot_dict['description'] = self._get_description(raw_snapshot)
        snapshot_dict['creation_timestamp'] = raw_snapshot['creationTimestamp']
        snapshot_dict['status'] = raw_snapshot['status']
        snapshot_dict['source_disk_id'] = raw_snapshot['sourceDiskId']
        snapshot_dict['source_disk_url'] = raw_snapshot['sourceDisk']
        return (snapshot_dict['id'], snapshot_dict)

    def _get_description(self, raw_snapshot):
        description = raw_snapshot.get('description')
        if description:
            return description
        return 'N/A'