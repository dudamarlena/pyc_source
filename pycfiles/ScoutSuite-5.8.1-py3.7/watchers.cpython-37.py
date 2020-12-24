# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ScoutSuite/providers/azure/resources/network/watchers.py
# Compiled at: 2020-04-02 05:37:10
# Size of source mod 2**32: 1227 bytes
from ScoutSuite.providers.azure.facade.base import AzureFacade
from ScoutSuite.providers.azure.resources.base import AzureResources
from ScoutSuite.providers.utils import get_non_provider_id

class Watchers(AzureResources):

    def __init__(self, facade, subscription_id):
        super(Watchers, self).__init__(facade)
        self.subscription_id = subscription_id

    async def fetch_all(self):
        for raw_watcher in await self.facade.network.get_network_watchers(self.subscription_id):
            id, network_watcher = self._parse_network_watcher(raw_watcher)
            self[id] = network_watcher

    def _parse_network_watcher(self, raw_watcher):
        watcher_dict = {}
        watcher_dict['id'] = get_non_provider_id(raw_watcher.id)
        watcher_dict['name'] = raw_watcher.name
        watcher_dict['type'] = raw_watcher.type
        watcher_dict['location'] = raw_watcher.location
        watcher_dict['tags'] = raw_watcher.tags
        watcher_dict['etag'] = raw_watcher.etag
        watcher_dict['additional_properties'] = raw_watcher.additional_properties
        watcher_dict['provisioning_state'] = raw_watcher.provisioning_state
        return (watcher_dict['id'], watcher_dict)