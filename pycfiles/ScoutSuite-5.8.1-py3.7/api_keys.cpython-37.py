# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ScoutSuite/providers/oci/resources/identity/api_keys.py
# Compiled at: 2020-04-02 05:37:10
# Size of source mod 2**32: 926 bytes
from ScoutSuite.providers.oci.facade.base import OracleFacade
from ScoutSuite.providers.oci.resources.base import OracleResources
from ScoutSuite.providers.utils import get_non_provider_id

class ApiKeys(OracleResources):

    def __init__(self, facade, user):
        super(ApiKeys, self).__init__(facade)
        self.user = user

    async def fetch_all(self):
        for raw_user_api_key in await self.facade.identity.get_user_api_keys(user_id=(self.user['identifier'])):
            id, api_key = await self._parse_api_key(raw_user_api_key)
            self[id] = api_key

    async def _parse_api_key(self, raw_api_key):
        api_key = {}
        api_key['id'] = get_non_provider_id(raw_api_key.key_id)
        api_key['identifier'] = raw_api_key.key_id
        api_key['fingerprint'] = raw_api_key.fingerprint
        api_key['state'] = raw_api_key.lifecycle_state
        return (api_key['id'], api_key)