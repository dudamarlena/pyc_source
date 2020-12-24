# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_security/interfaces/base.py
# Compiled at: 2020-02-21 07:52:38
# Size of source mod 2**32: 3339 bytes
"""PyAMS_security.interfaces.base module

This module defines base security permissions and interfaces.
"""
from zope.interface import Interface
from zope.schema import Dict, Set, Text, TextLine
__docformat__ = 'restructuredtext'
FORBIDDEN_PERMISSION = 'system.forbidden'
PUBLIC_PERMISSION = 'public'
VIEW_PERMISSION = 'view'
MANAGE_PERMISSION = 'manage'
VIEW_SYSTEM_PERMISSION = 'pyams.ViewSystem'
MANAGE_SYSTEM_PERMISSION = 'pyams.ManageSystem'
MANAGE_SECURITY_PERMISSION = 'pyams.ManageSecurity'
MANAGE_ROLES_PERMISSION = 'pyams.ManageRoles'

class IPermission(Interface):
    __doc__ = 'Permission interface'
    id = TextLine(title='Unique ID', required=True)
    title = TextLine(title='Title', required=True)
    description = Text(title='Description', required=False)


class IRole(Interface):
    __doc__ = 'Role interface\n\n    A role is a set of permissions; by assigning the role to a principal,\n    these permissions are also granted to the principal.\n    '
    id = TextLine(title='Unique ID', required=True)
    title = TextLine(title='Title', required=True)
    description = Text(title='Description', required=False)
    permissions = Set(title='Permissions', description="ID of role's permissions", value_type=TextLine(), required=False)
    managers = Set(title='Managers', description="List of principal IDs allowed to manage this role. If it's a role, use 'role:role_id' syntax...", value_type=TextLine(), required=False)


class IPrincipalInfo(Interface):
    __doc__ = "Principal info class\n\n    This is the generic interface of objects defined in request 'principal' attribute.\n    "
    id = TextLine(title='Globally unique ID', required=True)
    title = TextLine(title='Principal name', required=True)
    attributes = Dict(title='Principal groups', description='IDs of principals to which this principal directly belongs', value_type=TextLine())