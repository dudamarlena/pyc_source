# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ScoutSuite/providers/aws/resources/elbv2/listeners.py
# Compiled at: 2020-04-02 05:37:10
# Size of source mod 2**32: 845 bytes
from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.base import AWSResources

class Listeners(AWSResources):

    def __init__(self, facade, region, load_balancer_arn):
        super(Listeners, self).__init__(facade)
        self.region = region
        self.load_balancer_arn = load_balancer_arn

    async def fetch_all(self):
        listeners = await self.facade.elbv2.get_listeners(self.region, self.load_balancer_arn)
        for raw_listener in listeners:
            id, listener = self._parse_listener(raw_listener)
            self[id] = listener

    def _parse_listener(self, raw_listener):
        raw_listener.pop('ListenerArn')
        raw_listener.pop('LoadBalancerArn')
        port = raw_listener.pop('Port')
        return (port, raw_listener)