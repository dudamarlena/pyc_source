# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ScoutSuite/providers/aws/resources/elbv2/load_balancers.py
# Compiled at: 2020-04-02 05:37:10
# Size of source mod 2**32: 1789 bytes
from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.base import AWSCompositeResources
from ScoutSuite.providers.utils import get_non_provider_id
from .listeners import Listeners

class LoadBalancers(AWSCompositeResources):
    _children = [
     (
      Listeners, 'listeners')]

    def __init__(self, facade, region, vpc):
        super(LoadBalancers, self).__init__(facade)
        self.region = region
        self.vpc = vpc

    async def fetch_all(self):
        raw_load_balancers = await self.facade.elbv2.get_load_balancers(self.region, self.vpc)
        for raw_load_balancer in raw_load_balancers:
            id, load_balancer = self._parse_load_balancer(raw_load_balancer)
            self[id] = load_balancer

        await self._fetch_children_of_all_resources(resources=self,
          scopes={load_balancer_id:{'region':self.region,  'load_balancer_arn':load_balancer['arn']} for load_balancer_id, load_balancer in self.items()})

    def _parse_load_balancer(self, load_balancer):
        load_balancer['arn'] = load_balancer.pop('LoadBalancerArn')
        load_balancer['name'] = load_balancer.pop('LoadBalancerName')
        load_balancer['security_groups'] = []
        if 'SecurityGroups' in load_balancer:
            for sg in load_balancer['SecurityGroups']:
                load_balancer['security_groups'].append({'GroupId': sg})

            load_balancer.pop('SecurityGroups')
        if 'Tags' in load_balancer:
            if load_balancer['Tags']:
                load_balancer['tags'] = {x['Key']:x['Value'] for x in load_balancer['Tags']}
                load_balancer.pop('Tags')
        return (
         get_non_provider_id(load_balancer['name']), load_balancer)