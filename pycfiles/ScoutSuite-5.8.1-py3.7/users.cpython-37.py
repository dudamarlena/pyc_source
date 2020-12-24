# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ScoutSuite/providers/oci/resources/identity/users.py
# Compiled at: 2020-04-02 05:37:10
# Size of source mod 2**32: 958 bytes
from ScoutSuite.providers.oci.resources.base import OracleCompositeResources
from ScoutSuite.providers.utils import get_non_provider_id
from .api_keys import ApiKeys

class Users(OracleCompositeResources):
    _children = [
     (
      ApiKeys, 'api_keys')]

    async def fetch_all(self):
        for raw_user in await self.facade.identity.get_users():
            id, user = await self._parse_user(raw_user)
            self[id] = user

        await self._fetch_children_of_all_resources(resources=self,
          scopes={user_id:{'user': user} for user_id, user in self.items()})

    async def _parse_user(self, raw_user):
        user = {}
        user['identifier'] = raw_user.id
        user['id'] = get_non_provider_id(raw_user.id)
        user['name'] = raw_user.name
        user['identifier'] = raw_user.id
        user['mfa_activated'] = raw_user.is_mfa_activated
        return (user['id'], user)