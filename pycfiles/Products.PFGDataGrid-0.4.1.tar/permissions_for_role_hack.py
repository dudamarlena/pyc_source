# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/Products/PermissionComprehensible/_darcs/pristine/permissions_for_role_hack.py
# Compiled at: 2012-01-17 08:01:28
from AccessControl.Permission import Permission
from Products.CMFCore.utils import getToolByName
from AccessControl.PermissionRole import rolesForPermissionOn

def pc_get_permissions_for_role(self, role):
    result = []
    membership = getToolByName(self, 'portal_membership')
    user = membership.getAuthenticatedMember()
    assert user.hasRole('Manager')
    permissions = self.ac_inherited_permissions(1)
    for p in permissions:
        (name, value) = p[:2]
        p = Permission(name, value, self)
        all_permitted_roles = rolesForPermissionOn(name, self)
        all_acquired_roles = p.getRoles()
        if role in all_permitted_roles:
            d = {'name': name, 'acquire': isinstance(all_acquired_roles, list)}
            result.append(d)

    return result