# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ScoutSuite/providers/aws/resources/vpc/subnets.py
# Compiled at: 2020-04-02 05:37:10
# Size of source mod 2**32: 1049 bytes
from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.base import AWSResources
from ScoutSuite.providers.aws.utils import get_name

class Subnets(AWSResources):

    def __init__(self, facade, region, vpc):
        self.region = region
        self.vpc = vpc
        super(Subnets, self).__init__(facade)

    async def fetch_all(self):
        raw_subnets = await self.facade.ec2.get_subnets(self.region, self.vpc)
        for raw_subnet in raw_subnets:
            id, subnet = self._parse_subnet(raw_subnet)
            self[id] = subnet

    def _parse_subnet(self, raw_subnet):
        raw_subnet['id'] = raw_subnet['SubnetId']
        get_name(raw_subnet, raw_subnet, 'SubnetId')
        raw_subnet.pop('SubnetId')
        if raw_subnet['Ipv6CidrBlockAssociationSet']:
            raw_subnet['CidrBlockv6'] = raw_subnet['Ipv6CidrBlockAssociationSet'][0]['Ipv6CidrBlock']
        else:
            raw_subnet['CidrBlockv6'] = None
        return (raw_subnet['id'], raw_subnet)