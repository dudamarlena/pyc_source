# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ScoutSuite/providers/oci/resources/identity/policies.py
# Compiled at: 2020-04-02 05:37:10
# Size of source mod 2**32: 940 bytes
from ScoutSuite.providers.oci.facade.base import OracleFacade
from ScoutSuite.providers.oci.resources.base import OracleResources
from ScoutSuite.providers.utils import get_non_provider_id

class Policies(OracleResources):

    def __init__(self, facade):
        super(Policies, self).__init__(facade)

    async def fetch_all(self):
        for raw_policy in await self.facade.identity.get_policies():
            id, policy = await self._parse_policy(raw_policy)
            self[id] = policy

    async def _parse_policy(self, raw_policy):
        policy = {}
        policy['id'] = get_non_provider_id(raw_policy.id)
        policy['identifier'] = raw_policy.id
        policy['name'] = raw_policy.name
        policy['description'] = raw_policy.description
        policy['statements'] = [s.lower() for s in raw_policy.statements]
        policy['state'] = raw_policy.lifecycle_state
        return (policy['id'], policy)