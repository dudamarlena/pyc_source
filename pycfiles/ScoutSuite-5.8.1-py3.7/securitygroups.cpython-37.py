# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ScoutSuite/providers/aws/resources/rds/securitygroups.py
# Compiled at: 2020-04-02 05:37:10
# Size of source mod 2**32: 866 bytes
from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.base import AWSResources

class SecurityGroups(AWSResources):

    def __init__(self, facade, region):
        super(SecurityGroups, self).__init__(facade)
        self.region = region

    async def fetch_all(self):
        raw_security_groups = await self.facade.rds.get_security_groups(self.region)
        for raw_security_group in raw_security_groups:
            name, resource = self._parse_security_group(raw_security_group)
            self[name] = resource

    def _parse_security_group(self, raw_security_group):
        raw_security_group['arn'] = raw_security_group.pop('DBSecurityGroupArn')
        raw_security_group['name'] = raw_security_group.pop('DBSecurityGroupName')
        return (raw_security_group['name'], raw_security_group)