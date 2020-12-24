# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ScoutSuite/providers/azure/resources/securitycenter/settings.py
# Compiled at: 2020-04-02 05:37:10
# Size of source mod 2**32: 687 bytes
from ScoutSuite.providers.azure.facade.base import AzureFacade
from ScoutSuite.providers.azure.resources.base import AzureResources

class Settings(AzureResources):

    def __init__(self, facade, subscription_id):
        super(Settings, self).__init__(facade)
        self.subscription_id = subscription_id

    async def fetch_all(self):
        for raw_settings in await self.facade.securitycenter.get_settings(self.subscription_id):
            id, settings = self._parse_settings(raw_settings)
            self[id] = settings

    def _parse_settings(self, settings):
        settings_dict = {}
        return (settings_dict['id'], settings_dict)