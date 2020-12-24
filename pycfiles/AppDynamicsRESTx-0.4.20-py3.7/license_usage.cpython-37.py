# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/appd/model/license_usage.py
# Compiled at: 2020-03-11 17:54:36
# Size of source mod 2**32: 2092 bytes
"""
Model classes for AppDynamics REST API
"""
from . import JsonObject, JsonList
from appd.time import from_ts

class LicenseUsage(JsonObject):
    FIELDS = {'id':'', 
     'account_id':'accountId', 
     'units_used':'unitsUsed', 
     'units_allowed':'unitsAllowed', 
     'units_provisioned':'unitsProvisioned', 
     'license_module':'agentType', 
     'created_on_ms':'createdOn'}

    def __init__(self, id=0, account_id=0, license_module=None, units_used=0, units_allowed=0, units_provisioned=None, created_on_ms=0):
        self.id, self.account_id, self.license_module, self.units_used, self.units_allowed, self.units_provisioned, self.created_on_ms = (
         id, account_id, license_module,
         units_used, units_allowed,
         units_provisioned, created_on_ms)

    @property
    def created_on(self):
        """
        :rtype: datetime.datetime
        """
        return from_ts(self.created_on_ms)


class LicenseUsageList(JsonList):

    def __init__(self, initial_list=None):
        super(LicenseUsageList, self).__init__(LicenseUsage, initial_list)

    def __getitem__(self, i):
        """
        :rtype: LicenseUsage
        """
        return self.data[i]

    def by_account_id(self, account_id):
        """
        :rtype: LicenseUsageList
        """
        return LicenseUsageList([x for x in self.data if x.account_id == account_id])

    def by_license_module(self, license_module):
        """
        :rtype: LicenseUsageList
        """
        return LicenseUsageList([x for x in self.data if x.license_module == license_module])


class LicenseUsages(JsonObject):
    FIELDS = {}

    def __init__(self):
        self.usages = LicenseUsageList()

    @classmethod
    def from_json(cls, json_dict):
        obj = super(LicenseUsages, cls).from_json(json_dict)
        obj.usages = LicenseUsageList.from_json(json_dict['usages'])
        return obj