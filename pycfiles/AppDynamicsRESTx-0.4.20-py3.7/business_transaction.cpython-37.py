# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/appd/model/business_transaction.py
# Compiled at: 2020-03-11 17:47:43
# Size of source mod 2**32: 2021 bytes
"""
Model classes for AppDynamics REST API

.. moduleauthor:: Todd Radel <tradel@appdynamics.com>
"""
from . import JsonObject, JsonList

class BusinessTransaction(JsonObject):
    __doc__ = '\n    Represents a business transaction definition.\n\n    .. data:: id\n\n        Numeric ID of the BT definition.\n\n    .. data:: name\n\n    '
    FIELDS = {'id':'',  'name':'',  'type':'entryPointType',  'internal_name':'internalName',  'is_background':'background', 
     'tier_id':'tierId',  'tier_name':'tierName'}

    def __init__(self, bt_id=0, name='', internal_name='', tier_id=0, tier_name='', bt_type='POJO', is_background=False):
        self.id, self.name, self.internal_name, self.tier_id, self.tier_name, self.type, self.is_background = (
         bt_id, name, internal_name, tier_id, tier_name, bt_type, is_background)


class BusinessTransactions(JsonList):

    def __init__(self, initial_list=None):
        super(BusinessTransactions, self).__init__(BusinessTransaction, initial_list)

    def __getitem__(self, i):
        """
        :rtype: BusinessTransaction
        """
        return self.data[i]

    def by_name(self, bt_name):
        """
        Searches for business transactions that match a particular name. Note that there may be more than one
        exact match, as different tiers can have transactions with the exact same name.

        :returns: a BusinessTransactions object containing the matching business transactions.
        :rtype: BusinessTransactions
        """
        return BusinessTransactions([x for x in self.data if x.name == bt_name])

    def by_tier_and_name(self, bt_name, tier_name):
        """
        Searches for business transactions that match a particular BT name and tier name.

        :returns: a BusinessTransactions object containing the matching business transactions.
        :rtype: BusinessTransactions
        """
        return BusinessTransactions([x for x in self.data if x.name == bt_name if x.tier_name == tier_name])