# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ScoutSuite/providers/aws/resources/redshift/cluster_parameters.py
# Compiled at: 2020-04-02 05:37:10
# Size of source mod 2**32: 917 bytes
from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.base import AWSResources

class ClusterParameters(AWSResources):

    def __init__(self, facade, region, parameter_group_name):
        super(ClusterParameters, self).__init__(facade)
        self.region = region
        self.parameter_group_name = parameter_group_name

    async def fetch_all(self):
        raw_parameters = await self.facade.redshift.get_cluster_parameters(self.region, self.parameter_group_name)
        for raw_parameter in raw_parameters:
            id, parameter = self._parse_parameter(raw_parameter)
            self[id] = parameter

    def _parse_parameter(self, raw_parameter):
        parameter = {'value':raw_parameter['ParameterValue'],  'source':raw_parameter['Source']}
        return (raw_parameter['ParameterName'], parameter)