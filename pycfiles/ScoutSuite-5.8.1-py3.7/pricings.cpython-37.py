# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ScoutSuite/providers/azure/resources/securitycenter/pricings.py
# Compiled at: 2020-04-02 05:37:10
# Size of source mod 2**32: 805 bytes
from ScoutSuite.providers.azure.facade.base import AzureFacade
from ScoutSuite.providers.azure.resources.base import AzureResources

class Pricings(AzureResources):

    def __init__(self, facade, subscription_id):
        super(Pricings, self).__init__(facade)
        self.subscription_id = subscription_id

    async def fetch_all(self):
        for raw_pricing in await self.facade.securitycenter.get_pricings(self.subscription_id):
            id, pricing = self._parse_pricing(raw_pricing)
            self[id] = pricing

    def _parse_pricing(self, pricing):
        pricing_dict = {}
        pricing_dict['id'] = pricing.id
        pricing_dict['name'] = pricing.name
        pricing_dict['pricing_tier'] = pricing.pricing_tier
        return (
         pricing_dict['id'], pricing_dict)