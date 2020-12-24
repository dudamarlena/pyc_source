# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_security/property.py
# Compiled at: 2020-02-21 07:52:38
# Size of source mod 2**32: 3303 bytes
"""PyAMS_security.property module

This module defines a custom field property used to store roles.
"""
from zope.schema.interfaces import IField, ISet
from pyams_security.interfaces import IProtectedObject, IRoleProtectedObject
from pyams_security.interfaces.base import IRole, IPrincipalInfo
from pyams_security.schema import IPrincipalBaseField
__docformat__ = 'restructuredtext'

class RolePrincipalsFieldProperty:
    __doc__ = 'Custom field property used to handle role principals'

    def __init__(self, field, role_id=None, name=None, **args):
        if not IField.providedBy(field):
            raise ValueError('Provided field must implement IField interface')
        if role_id is None:
            if not IPrincipalBaseField.providedBy(field):
                raise ValueError('Provided field must implement IRoleField interface or you must provide a role ID')
            role_id = field.role_id
        elif IRole.providedBy(role_id):
            role_id = role_id.id
        if role_id is None:
            raise ValueError("Can't get role ID")
        if name is None:
            name = field.__name__
        self._RolePrincipalsFieldProperty__field = field
        self._RolePrincipalsFieldProperty__name = name
        self._RolePrincipalsFieldProperty__role_id = role_id

    def __get__(self, instance, klass):
        if instance is None:
            return self
        protection = IProtectedObject(instance, None)
        if protection is None:
            return set()
        return protection.get_principals(self._RolePrincipalsFieldProperty__role_id)

    def __set__(self, instance, value):
        field = self._RolePrincipalsFieldProperty__field.bind(instance)
        if ISet.providedBy(field):
            if value is None:
                value = set()
            elif isinstance(value, str):
                value = set(value.split(','))
            value = set(map(lambda x: x.id if IPrincipalInfo.providedBy(x) else x, value))
        else:
            value = value.id if IPrincipalInfo.providedBy(value) else value
        field.validate(value)
        if field.readonly:
            raise ValueError('Field {0} is readonly!'.format(self._RolePrincipalsFieldProperty__name))
        protection = IProtectedObject(instance, None)
        if not IRoleProtectedObject.providedBy(protection):
            raise ValueError("Can't use role properties on object not providing IRoleProtectedObject interface!")
        old_principals = protection.get_principals(self._RolePrincipalsFieldProperty__role_id)
        if not isinstance(value, set):
            value = {
             value}
        added = value - old_principals
        removed = old_principals - value
        for principal_id in added:
            protection.grant_role(self._RolePrincipalsFieldProperty__role_id, principal_id)

        for principal_id in removed:
            protection.revoke_role(self._RolePrincipalsFieldProperty__role_id, principal_id)