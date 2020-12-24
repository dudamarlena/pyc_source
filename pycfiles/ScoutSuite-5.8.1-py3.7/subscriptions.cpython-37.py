# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ScoutSuite/providers/azure/resources/subscriptions.py
# Compiled at: 2020-04-02 05:37:10
# Size of source mod 2**32: 1560 bytes
from ScoutSuite.providers.azure.resources.base import AzureCompositeResources

class Subscriptions(AzureCompositeResources):
    __doc__ = 'This class represents a collection of Azure Resources that are grouped by subscription.\n    Classes extending Subscriptions should implement the method _fetch_children() with a subscription ID as paramater.\n    The children resources will be stored with the following structure {<subscriptions>: {<subscription_id>: {<child_name>: {<child_id>: <child_instance>}}}}.\n    '

    async def fetch_all(self):
        """This method fetches all the Azure subscriptions that can be accessed with the given run configuration.
        It then fetches all the children defined in _children and groups them by subscription.
        """
        raw_subscriptions = await self.facade.get_subscriptions()
        if raw_subscriptions:
            self['subscriptions'] = {subscription.subscription_id:{} for subscription in raw_subscriptions}
        else:
            self['subscriptions'] = {}
        await self._fetch_children_of_all_resources(resources=(self['subscriptions']),
          scopes={subscription_id:{'subscription_id': subscription_id} for subscription_id in self['subscriptions']})
        self._set_counts()

    def _set_counts(self):
        for _, child_name in self._children:
            self[child_name + '_count'] = sum([subscription[(child_name + '_count')] for subscription in self['subscriptions'].values()])