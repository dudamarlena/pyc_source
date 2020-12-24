# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ScoutSuite/providers/aws/resources/ec2/volumes.py
# Compiled at: 2020-04-02 05:37:10
# Size of source mod 2**32: 780 bytes
from ScoutSuite.providers.aws.resources.base import AWSResources
from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.utils import get_name

class Volumes(AWSResources):

    def __init__(self, facade, region):
        super(Volumes, self).__init__(facade)
        self.region = region

    async def fetch_all(self):
        raw_volumes = await self.facade.ec2.get_volumes(self.region)
        for raw_volume in raw_volumes:
            name, resource = self._parse_volume(raw_volume)
            self[name] = resource

    def _parse_volume(self, raw_volume):
        raw_volume['id'] = raw_volume.pop('VolumeId')
        raw_volume['name'] = get_name(raw_volume, raw_volume, 'id')
        return (raw_volume['id'], raw_volume)