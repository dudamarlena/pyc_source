# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ScoutSuite/providers/azure/resources/securitycenter/alerts.py
# Compiled at: 2020-04-02 05:37:10
# Size of source mod 2**32: 788 bytes
from ScoutSuite.providers.azure.facade.base import AzureFacade
from ScoutSuite.providers.azure.resources.base import AzureResources

class Alerts(AzureResources):

    def __init__(self, facade, subscription_id):
        super(Alerts, self).__init__(facade)
        self.subscription_id = subscription_id

    async def fetch_all(self):
        a = await self.facade.securitycenter.get_alerts(self.subscription_id)
        for raw_alert in await self.facade.securitycenter.get_alerts(self.subscription_id):
            id, alert = self._parse_alert(raw_alert)
            self[id] = alert

    def _parse_alert(self, alert):
        alert_dict = {}
        alert_dict['id'] = alert.id
        alert_dict['name'] = alert.name
        return (alert_dict['id'], alert_dict)