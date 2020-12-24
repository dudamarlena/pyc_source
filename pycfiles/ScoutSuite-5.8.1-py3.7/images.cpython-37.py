# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ScoutSuite/providers/azure/resources/virtualmachines/images.py
# Compiled at: 2020-04-02 05:37:10
# Size of source mod 2**32: 658 bytes
from ScoutSuite.providers.azure.facade.base import AzureFacade
from ScoutSuite.providers.azure.resources.base import AzureResources
from ScoutSuite.providers.utils import get_non_provider_id

class Images(AzureResources):

    def __init__(self, facade, subscription_id):
        super(Images, self).__init__(facade)
        self.subscription_id = subscription_id

    async def fetch_all(self):
        for raw_image in await self.facade.virtualmachines.get_images(self.subscription_id):
            id, image = self._parse_image(raw_image)
            self[id] = image

    def _parse_image(self, raw_image):
        pass