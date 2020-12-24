# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ScoutSuite/providers/aws/resources/redshift/cluster_parameter_groups.py
# Compiled at: 2020-04-02 05:37:10
# Size of source mod 2**32: 2033 bytes
from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.base import AWSCompositeResources
from ScoutSuite.providers.utils import get_non_provider_id
from .cluster_parameters import ClusterParameters

class ClusterParameterGroups(AWSCompositeResources):
    _children = [
     (
      ClusterParameters, 'parameters')]

    def __init__(self, facade, region):
        super(ClusterParameterGroups, self).__init__(facade)
        self.region = region

    async def fetch_all(self):
        raw_parameter_groups = await self.facade.redshift.get_cluster_parameter_groups(self.region)
        for raw_parameter_group in raw_parameter_groups:
            id, parameter_group = self._parse_parameter_group(raw_parameter_group)
            self[id] = parameter_group

        await self._fetch_children_of_all_resources(resources=self,
          scopes={parameter_group_id:{'region':self.region,  'parameter_group_name':parameter_group['name']} for parameter_group_id, parameter_group in self.items()})

    def _parse_parameter_group(self, raw_parameter_group):
        parameter_group = {}
        parameter_group['name'] = raw_parameter_group.get('ParameterGroupName')
        parameter_group['id'] = get_non_provider_id(parameter_group['name'])
        parameter_group['family'] = raw_parameter_group.get('ParameterGroupFamily')
        parameter_group['description'] = raw_parameter_group.get('Description')
        parameter_group['is_default'] = self._is_default(raw_parameter_group)
        parameter_group['tags'] = raw_parameter_group.get('Tags')
        return (parameter_group['id'], parameter_group)

    def _is_default(self, raw_parameter_group):
        if 'Default parameter group for' in raw_parameter_group.get('Description'):
            if 'default.' in raw_parameter_group.get('ParameterGroupName'):
                return True
        return False