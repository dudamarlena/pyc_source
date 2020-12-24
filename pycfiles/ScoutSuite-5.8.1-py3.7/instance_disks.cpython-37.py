# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ScoutSuite/providers/gcp/resources/gce/instance_disks.py
# Compiled at: 2020-04-02 05:37:10
# Size of source mod 2**32: 560 bytes
from ScoutSuite.providers.gcp.resources.gce.disks import Disks

class InstanceDisks(Disks):

    def __init__(self, facade, instance):
        super(InstanceDisks, self).__init__(facade)
        self.instance = instance

    def fetch_all(self):
        raw_disks = self.instance.get('disks', {})
        for raw_disk in raw_disks:
            disk_id, disk = self._parse_disk(raw_disk)
            self[disk_id] = disk

        del self.instance