# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nodeconductor_sugarcrm/cost_tracking.py
# Compiled at: 2016-09-28 11:51:43
from nodeconductor.cost_tracking import CostTrackingStrategy, CostTrackingRegister, ConsumableItem
from . import models

class CRMStrategy(CostTrackingStrategy):
    resource_class = models.CRM

    class Types(object):
        SUPPORT = 'support'
        USERS = 'users'

    class Keys(object):
        SUPPORT = 'premium'
        USERS = 'count'

    @classmethod
    def get_consumable_items(cls):
        return [
         ConsumableItem(item_type=cls.Types.USERS, key=cls.Keys.USERS, name='Users count'),
         ConsumableItem(item_type=cls.Types.SUPPORT, key=cls.Keys.SUPPORT, name='Support: premium')]

    @classmethod
    def get_configuration(cls, crm):
        user_count = crm.quotas.get(name=crm.Quotas.user_count).limit
        return {ConsumableItem(item_type=cls.Types.USERS, key=cls.Keys.USERS): user_count, 
           ConsumableItem(item_type=cls.Types.SUPPORT, key=cls.Keys.SUPPORT): 1}


CostTrackingRegister.register_strategy(CRMStrategy)