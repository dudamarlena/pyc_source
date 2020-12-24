# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_security/schema.py
# Compiled at: 2020-02-21 07:52:38
# Size of source mod 2**32: 5371 bytes
"""PyAMS_security.schema module

This module contains security-related schema fields.
"""
from zope.interface import Interface, implementer
from zope.schema import Choice, Set, TextLine
from zope.schema.interfaces import IChoice, ISet, ITextLine
from pyams_security.interfaces.base import IPermission, IRole, IPrincipalInfo
from pyams_security.interfaces.names import PERMISSIONS_VOCABULARY_NAME, ROLES_VOCABULARY_NAME
__docformat__ = 'restructuredtext'

class IPermissionField(IChoice):
    __doc__ = 'Permission field interface'


@implementer(IPermissionField)
class PermissionField(Choice):
    __doc__ = 'Permission field'

    def __init__(self, **kwargs):
        if 'vocabulary' in kwargs:
            del kwargs['vocabulary']
        super(PermissionField, self).__init__(vocabulary=PERMISSIONS_VOCABULARY_NAME, **kwargs)

    def validate(self, value):
        if IPermission.providedBy(value):
            value = value.id
        super(PermissionField, self).validate(value)

    def set(self, object, value):
        if IPermission.providedBy(value):
            value = value.id
        super(PermissionField, self).set(object, value)


class IPermissionsSetField(ISet):
    __doc__ = 'Permissions set field interface'


def get_permission_id(value):
    """Get permission ID"""
    if IPermission.providedBy(value):
        return value.id
    return value


@implementer(IPermissionsSetField)
class PermissionsSetField(Set):
    __doc__ = 'Permissions set field'
    value_type = PermissionField()

    def __init__(self, **kwargs):
        if 'value_type' in kwargs:
            del kwargs['value_type']
        super(PermissionsSetField, self).__init__(value_type=PermissionField(), **kwargs)

    def set(self, object, value):
        if value:
            value = set(map(get_permission_id, value))
        super(PermissionsSetField, self).set(object, value)


class IRoleField(IChoice):
    __doc__ = 'Role field interface'


@implementer(IRoleField)
class RoleField(Choice):
    __doc__ = 'Role field'

    def __init__(self, **kwargs):
        if 'vocabulary' in kwargs:
            del kwargs['vocabulary']
        super(RoleField, self).__init__(vocabulary=ROLES_VOCABULARY_NAME, **kwargs)

    def validate(self, value):
        if IRole.providedBy(value):
            value = value.id
        super(RoleField, self).validate(value)

    def set(self, object, value):
        if IRole.providedBy(value):
            value = value.id
        super(RoleField, self).set(object, value)


class IRolesSetField(ISet):
    __doc__ = 'Roles set field interface'


def get_role_id(value):
    """Get role ID"""
    if IRole.providedBy(value):
        return value.id
    return value


@implementer(IRolesSetField)
class RolesSetField(Set):
    __doc__ = 'Roles set field'
    value_type = RoleField()

    def __init__(self, **kwargs):
        if 'value_type' in kwargs:
            del kwargs['value_type']
        super(RolesSetField, self).__init__(value_type=RoleField(), **kwargs)

    def set(self, object, value):
        if value:
            value = set(map(get_role_id, value))
        super(RolesSetField, self).set(object, value)


class IPrincipalBaseField(Interface):
    __doc__ = 'Base role field interface'
    role_id = TextLine(title='Matching role ID', required=False)


class IPrincipalField(ITextLine, IPrincipalBaseField):
    __doc__ = 'Principal field interface'


@implementer(IPrincipalField)
class PrincipalField(TextLine):
    __doc__ = 'Principal field'
    role_id = None

    def __init__(self, **kwargs):
        if 'role_id' in kwargs:
            self.role_id = kwargs.pop('role_id')
        super(PrincipalField, self).__init__(**kwargs)

    def validate(self, value):
        if IPrincipalInfo.providedBy(value):
            value = value.id
        super(PrincipalField, self).validate(value)

    def set(self, object, value):
        if IPrincipalInfo.providedBy(value):
            value = value.id
        super(PrincipalField, self).set(object, value)


class IPrincipalsSetField(ISet, IPrincipalBaseField):
    __doc__ = 'Principals set interface'


def get_principal_id(value):
    """Get principal ID"""
    if IPrincipalInfo.providedBy(value):
        return value.id
    return value


@implementer(IPrincipalsSetField)
class PrincipalsSetField(Set):
    __doc__ = 'Principals set field'
    role_id = None
    value_type = PrincipalField()

    def __init__(self, **kwargs):
        if 'role_id' in kwargs:
            self.role_id = kwargs.pop('role_id')
        super(PrincipalsSetField, self).__init__(**kwargs)

    def set(self, object, value):
        if value:
            value = set(map(get_principal_id, value))
        super(PrincipalsSetField, self).set(object, value)