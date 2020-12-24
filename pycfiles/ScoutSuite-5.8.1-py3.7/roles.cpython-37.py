# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ScoutSuite/providers/azure/resources/arm/roles.py
# Compiled at: 2020-04-02 05:37:10
# Size of source mod 2**32: 1294 bytes
from ScoutSuite.providers.azure.facade.base import AzureFacade
from ScoutSuite.providers.azure.resources.base import AzureResources

class Roles(AzureResources):

    def __init__(self, facade, subscription_id):
        super(Roles, self).__init__(facade)
        self.subscription_id = subscription_id

    async def fetch_all(self):
        for raw_role in await self.facade.arm.get_roles(self.subscription_id):
            id, role = self._parse_role(raw_role)
            self[id] = role

    def _parse_role(self, raw_role):
        role_dict = {}
        role_dict['id'] = raw_role.name
        role_dict['name'] = raw_role.role_name
        role_dict['type'] = raw_role.type
        role_dict['description'] = raw_role.description
        role_dict['role_type'] = raw_role.role_type
        role_dict['permissions'] = raw_role.permissions
        role_dict['assignable_scopes'] = raw_role.assignable_scopes
        role_dict['additional_properties'] = raw_role.additional_properties
        role_dict['assignments_count'] = 0
        role_dict['assignments'] = {'users':[],  'groups':[],  'service_principals':[]}
        return (
         role_dict['id'], role_dict)