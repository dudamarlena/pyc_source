# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nodeconductor_saltstack/sharepoint/cost_tracking.py
# Compiled at: 2016-09-28 02:05:53
from nodeconductor.cost_tracking import CostTrackingRegister, ConsumableItem, CostTrackingStrategy
from . import models

class SharepointTenantStrategy(CostTrackingStrategy):
    resource_class = models.SharepointTenant

    class Types(object):
        SUPPORT = 'support'
        STORAGE = 'storage'

    class Keys(object):
        STORAGE = '1 GB'
        SUPPORT = 'premium'

    @classmethod
    def get_consumable_items(cls):
        return [
         ConsumableItem(item_type=cls.Types.STORAGE, key=cls.Keys.STORAGE, name='1 GB of storage', units='GB'),
         ConsumableItem(item_type=cls.Types.SUPPORT, key=cls.Keys.SUPPORT, name='Support: premium')]

    @classmethod
    def get_configuration(cls, tenant):
        storage = tenant.quotas.get(name=models.SharepointTenant.Quotas.mailbox_size).usage
        return {ConsumableItem(item_type=cls.Types.STORAGE, key=cls.Keys.STORAGE): float(storage) / 1024, 
           ConsumableItem(item_type=cls.Types.SUPPORT, key=cls.Keys.SUPPORT): 1}


CostTrackingRegister.register_strategy(SharepointTenantStrategy)