# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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