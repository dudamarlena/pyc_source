# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/appd/model/license_module.py
# Compiled at: 2020-03-11 17:47:43
# Size of source mod 2**32: 1437 bytes
"""
Model classes for AppDynamics REST API
"""
from . import JsonObject, JsonList

class LicenseModule(JsonObject):
    FIELDS = {'name': ''}

    def __init__(self, name=None):
        self.name = name


class LicenseModuleList(JsonList):
    __doc__ = '\n    Represents a collection of :class:Account objects. Extends :class:UserList, so it supports the\n    standard array index and :keyword:`for` semantics.\n    '

    def __init__(self, initial_list=None):
        super(LicenseModuleList, self).__init__(LicenseModule, initial_list)

    def __getitem__(self, i):
        """
        :rtype: LicenseModule
        """
        return self.data[i]

    def by_name(self, name):
        """
        Finds an account by name.

        :returns: First account with the correct name
        :rtype: LicenseModule
        """
        found = [x for x in self.data if x.name == name]
        try:
            return found[0]
        except IndexError:
            raise KeyError(name)

    def __contains__(self, item):
        found = [x for x in self.data if x.name == item]
        if found:
            return True
        return False


class LicenseModules(JsonObject):
    FIELDS = {}

    def __init__(self):
        self.modules = LicenseModuleList()

    @classmethod
    def from_json(cls, json_dict):
        obj = super(LicenseModules, cls).from_json(json_dict)
        obj.modules = LicenseModuleList.from_json(json_dict['modules'])
        return obj