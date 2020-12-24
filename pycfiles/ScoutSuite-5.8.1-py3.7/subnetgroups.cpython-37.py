# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ScoutSuite/providers/aws/resources/rds/subnetgroups.py
# Compiled at: 2020-04-02 05:37:10
# Size of source mod 2**32: 794 bytes
from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.base import AWSResources

class SubnetGroups(AWSResources):

    def __init__(self, facade, region, vpc):
        super(SubnetGroups, self).__init__(facade)
        self.region = region
        self.vpc = vpc

    async def fetch_all(self):
        raw_subnet_groups = await self.facade.rds.get_subnet_groups(self.region, self.vpc)
        for raw_subnet_group in raw_subnet_groups:
            name, resource = self._parse_subnet_group(raw_subnet_group)
            self[name] = resource

    def _parse_subnet_group(self, raw_subnet_group):
        raw_subnet_group['name'] = raw_subnet_group['DBSubnetGroupName']
        return (raw_subnet_group['name'], raw_subnet_group)