# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ScoutSuite/providers/aws/resources/redshift/cluster_security_groups.py
# Compiled at: 2020-04-02 05:37:10
# Size of source mod 2**32: 823 bytes
from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.base import AWSResources

class ClusterSecurityGroups(AWSResources):

    def __init__(self, facade, region):
        super(ClusterSecurityGroups, self).__init__(facade)
        self.region = region

    async def fetch_all(self):
        raw_security_groups = await self.facade.redshift.get_cluster_security_groups(self.region)
        for raw_security_group in raw_security_groups:
            id, security_group = self._parse_security_group(raw_security_group)
            self[id] = security_group

    def _parse_security_group(self, raw_security_group):
        name = raw_security_group.pop('ClusterSecurityGroupName')
        raw_security_group['name'] = name
        return (name, raw_security_group)