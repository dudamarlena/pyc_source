# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/Products/BastionBanking/Permissions.py
# Compiled at: 2015-07-18 19:38:10
import AccessControl, AccessControl
from AccessControl.Permissions import view
add_merchant_service = 'BastionBanking: Add'
add_bank_service = 'BastionBanking: Add'
manage_bastionbanking = 'BastionBanking: Manage'
operate_bastionbanking = 'BastionBanking: Operate'
add_payee = 'BastionBanking: Add Payee'

def setDefaultRoles(permission, roles, object, acquire=1):
    registered = AccessControl.Permission._registeredPermissions
    if not registered.has_key(permission):
        registered[permission] = 1
        Products.__ac_permissions__ = Products.__ac_permissions__ + ((permission, (), roles),)
        mangled = AccessControl.Permission.pname(permission)
        setattr(Globals.ApplicationDefaultPermissions, mangled, roles)
    current = object.rolesOfPermission(permission)
    roles = list(roles)
    for dict in current:
        if dict.get('selected'):
            roles.append(dict['name'])

    object.manage_permission(permission, roles, acquire)


def securityPolicy(bastionservice):
    """
    set up a default security policy for a BastionBank or BastionMerchant service

    presently, this just turns off view permission ...
    """
    setDefaultRoles(view, ('Manager', ), bastionservice, 0)