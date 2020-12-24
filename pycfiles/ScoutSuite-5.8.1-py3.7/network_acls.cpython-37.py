# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ScoutSuite/providers/aws/resources/vpc/network_acls.py
# Compiled at: 2020-04-02 05:37:10
# Size of source mod 2**32: 2250 bytes
from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.base import AWSResources
from ScoutSuite.providers.aws.utils import get_name
from ScoutSuite.core.fs import load_data
protocols_dict = load_data('protocols.json', 'protocols')

class NetworkACLs(AWSResources):

    def __init__(self, facade, region, vpc):
        self.region = region
        self.vpc = vpc
        super(NetworkACLs, self).__init__(facade)

    async def fetch_all(self):
        raw_network_acls = await self.facade.ec2.get_network_acls(self.region, self.vpc)
        for raw_network_acl in raw_network_acls:
            id, network_acl = self._parse_network_acl(raw_network_acl)
            self[id] = network_acl

    def _parse_network_acl(self, raw_network_acl):
        raw_network_acl['id'] = raw_network_acl.pop('NetworkAclId')
        get_name(raw_network_acl, raw_network_acl, 'id')
        raw_network_acl['rules'] = {}
        raw_network_acl['rules']['ingress'] = self._parse_network_acl_entries(raw_network_acl['Entries'], False)
        raw_network_acl['rules']['egress'] = self._parse_network_acl_entries(raw_network_acl['Entries'], True)
        raw_network_acl.pop('Entries')
        return (
         raw_network_acl['id'], raw_network_acl)

    @staticmethod
    def _parse_network_acl_entries(entries, egress):
        acl_dict = {}
        for entry in entries:
            if entry['Egress'] == egress:
                acl = {}
                for key in ('RuleAction', 'RuleNumber'):
                    acl[key] = entry[key]

                acl['CidrBlock'] = entry['CidrBlock'] if 'CidrBlock' in entry else entry['Ipv6CidrBlock']
                acl['protocol'] = protocols_dict[entry['Protocol']]
                if 'PortRange' in entry:
                    from_port = entry['PortRange']['From'] if entry['PortRange']['From'] else 1
                    to_port = entry['PortRange']['To'] if entry['PortRange']['To'] else 65535
                    acl['port_range'] = from_port if from_port == to_port else str(from_port) + '-' + str(to_port)
                else:
                    acl['port_range'] = '1-65535'
                acl_dict[acl.pop('RuleNumber')] = acl

        return acl_dict