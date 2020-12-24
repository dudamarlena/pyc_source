# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ScoutSuite/providers/aws/resources/ses/identity_policies.py
# Compiled at: 2020-04-02 05:37:10
# Size of source mod 2**32: 628 bytes
import json
from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.base import AWSResources

class IdentityPolicies(AWSResources):

    def __init__(self, facade, region, identity_name):
        super(IdentityPolicies, self).__init__(facade)
        self.region = region
        self.identity_name = identity_name

    async def fetch_all(self):
        raw_policies = await self.facade.ses.get_identity_policies(self.region, self.identity_name)
        for policy_name, raw_policy in raw_policies.items():
            self[policy_name] = json.loads(raw_policy)