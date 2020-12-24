# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ScoutSuite/providers/azure/resources/securitycenter/auto_provisioning_settings.py
# Compiled at: 2020-04-02 05:37:10
# Size of source mod 2**32: 1138 bytes
from ScoutSuite.providers.azure.facade.base import AzureFacade
from ScoutSuite.providers.azure.resources.base import AzureResources

class AutoProvisioningSettings(AzureResources):

    def __init__(self, facade, subscription_id):
        super(AutoProvisioningSettings, self).__init__(facade)
        self.subscription_id = subscription_id

    async def fetch_all(self):
        for raw_settings in await self.facade.securitycenter.get_auto_provisioning_settings(self.subscription_id):
            id, auto_provisioning_settings = self._parse_auto_provisioning_settings(raw_settings)
            self[id] = auto_provisioning_settings

    def _parse_auto_provisioning_settings(self, auto_provisioning_settings):
        auto_provisioning_setting_dict = {}
        auto_provisioning_setting_dict['id'] = auto_provisioning_settings.id
        auto_provisioning_setting_dict['name'] = auto_provisioning_settings.name
        auto_provisioning_setting_dict['auto_provision'] = auto_provisioning_settings.auto_provision
        return (
         auto_provisioning_setting_dict['id'], auto_provisioning_setting_dict)