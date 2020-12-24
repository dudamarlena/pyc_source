# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_security/interfaces/base.py
# Compiled at: 2020-02-21 07:52:38
# Size of source mod 2**32: 3339 bytes
__doc__ = 'PyAMS_security.interfaces.base module\n\nThis module defines base security permissions and interfaces.\n'
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
    """IPermission"""
    id = TextLine(title='Unique ID', required=True)
    title = TextLine(title='Title', required=True)
    description = Text(title='Description', required=False)


class IRole(Interface):
    """IRole"""
    id = TextLine(title='Unique ID', required=True)
    title = TextLine(title='Title', required=True)
    description = Text(title='Description', required=False)
    permissions = Set(title='Permissions', description="ID of role's permissions", value_type=TextLine(), required=False)
    managers = Set(title='Managers', description="List of principal IDs allowed to manage this role. If it's a role, use 'role:role_id' syntax...", value_type=TextLine(), required=False)


class IPrincipalInfo(Interface):
    """IPrincipalInfo"""
    id = TextLine(title='Globally unique ID', required=True)
    title = TextLine(title='Principal name', required=True)
    attributes = Dict(title='Principal groups', description='IDs of principals to which this principal directly belongs', value_type=TextLine())