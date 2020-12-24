# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ScoutSuite/providers/aws/resources/ec2/networkinterfaces.py
# Compiled at: 2020-04-02 05:37:10
# Size of source mod 2**32: 869 bytes
from ScoutSuite.providers.aws.resources.base import AWSResources
from ScoutSuite.providers.aws.facade.base import AWSFacade

class NetworkInterfaces(AWSResources):

    def __init__(self, facade, region, vpc):
        super(NetworkInterfaces, self).__init__(facade)
        self.region = region
        self.vpc = vpc

    async def fetch_all(self):
        raw_security_groups = await self.facade.ec2.get_network_interfaces(self.region, self.vpc)
        for raw_security_groups in raw_security_groups:
            name, resource = self._parse_network_interface(raw_security_groups)
            self[name] = resource

    def _parse_network_interface(self, raw_network_interface):
        raw_network_interface['name'] = raw_network_interface['NetworkInterfaceId']
        return (raw_network_interface['NetworkInterfaceId'], raw_network_interface)