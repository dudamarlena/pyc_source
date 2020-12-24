# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ScoutSuite/providers/azure/resources/keyvault/vaults.py
# Compiled at: 2020-04-02 05:37:10
# Size of source mod 2**32: 1225 bytes
from ScoutSuite.providers.azure.facade.base import AzureFacade
from ScoutSuite.providers.azure.resources.base import AzureResources
from ScoutSuite.providers.utils import get_non_provider_id

class Vaults(AzureResources):

    def __init__(self, facade, subscription_id):
        super(Vaults, self).__init__(facade)
        self.subscription_id = subscription_id

    async def fetch_all(self):
        for raw_vault in await self.facade.keyvault.get_key_vaults(self.subscription_id):
            id, vault = self._parse_key_vault(raw_vault)
            self[id] = vault

    def _parse_key_vault(self, raw_vault):
        vault = {}
        vault['id'] = get_non_provider_id(raw_vault.id)
        vault['name'] = raw_vault.name
        vault['type'] = raw_vault.type
        vault['location'] = raw_vault.location
        vault['additional_properties'] = raw_vault.additional_properties
        vault['tags'] = raw_vault.tags
        vault['properties'] = raw_vault.properties
        vault['public_access_allowed'] = self._is_public_access_allowed(raw_vault)
        return (vault['id'], vault)

    def _is_public_access_allowed(self, raw_vault):
        return raw_vault.properties.network_acls is None