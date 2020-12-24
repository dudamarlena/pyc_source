# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ScoutSuite/providers/aws/resources/rds/parametergroups.py
# Compiled at: 2020-04-02 05:37:10
# Size of source mod 2**32: 1094 bytes
from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.base import AWSResources
from ScoutSuite.providers.utils import get_non_provider_id

class ParameterGroups(AWSResources):

    def __init__(self, facade, region):
        super(ParameterGroups, self).__init__(facade)
        self.region = region

    async def fetch_all(self):
        raw_parameter_groups = await self.facade.rds.get_parameter_groups(self.region)
        for raw_parameter_group in raw_parameter_groups:
            name, resource = self._parse_parameter_group(raw_parameter_group)
            self[name] = resource

    def _parse_parameter_group(self, raw_parameter_group):
        raw_parameter_group['arn'] = raw_parameter_group.pop('DBParameterGroupArn')
        raw_parameter_group['name'] = raw_parameter_group.pop('DBParameterGroupName')
        raw_parameter_group['parameters'] = raw_parameter_group.pop('Parameters')
        parameter_group_id = get_non_provider_id(raw_parameter_group['name'])
        return (parameter_group_id, raw_parameter_group)