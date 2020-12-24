# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ScoutSuite/providers/azure/resources/securitycenter/information_protection_policies.py
# Compiled at: 2020-04-02 05:37:10
# Size of source mod 2**32: 972 bytes
from ScoutSuite.providers.azure.facade.base import AzureFacade
from ScoutSuite.providers.azure.resources.base import AzureResources

class InformationProtectionPolicies(AzureResources):

    def __init__(self, facade, subscription_id):
        super(InformationProtectionPolicies, self).__init__(facade)
        self.subscription_id = subscription_id

    async def fetch_all(self):
        for raw_information_policies in await self.facade.securitycenter.get_information_protection_policies(self.subscription_id):
            id, information_protection_policies = self._parse_information_protection_policies(raw_information_policies)
            self[id] = information_protection_policies

    def _parse_information_protection_policies(self, auto_provisioning_settings):
        information_protection_policies_dict = {}
        return (information_protection_policies_dict['id'], information_protection_policies_dict)