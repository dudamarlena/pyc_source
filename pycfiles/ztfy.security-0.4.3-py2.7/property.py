# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/security/property.py
# Compiled at: 2012-06-20 12:00:41
__docformat__ = 'restructuredtext'
from zope.schema.interfaces import IField
from zope.security.interfaces import IPrincipal
from ztfy.security.interfaces import ISecurityManager
from ztfy.security import _

class RolePrincipalsProperty(object):
    """Principals list property matching local role owners"""

    def __init__(self, field, role, name=None, output=str, **args):
        if not IField.providedBy(field):
            raise ValueError, _('Provided field must implement IField interface...')
        if output not in (str, list):
            raise ValueError, _("Field output must be 'list' or 'str' types")
        if name is None:
            name = field.__name__
        self.__field = field
        self.__name = name
        self.__role = role
        self.__output = output
        self.__args = args
        return

    def __get__(self, instance, klass):
        if instance is None:
            return self
        else:
            sm = ISecurityManager(instance, None)
            if sm is None:
                result = []
            else:
                result = sm.getLocalAllowedPrincipals(self.__role)
            if self.__output is str:
                return (',').join(result)
            return result
            return

    def __set__(self, instance, value):
        if value is None:
            value = []
        else:
            if isinstance(value, (str, unicode)):
                value = value.split(',')
            for i, v in enumerate(value):
                if IPrincipal.providedBy(v):
                    value[i] = v.id

            field = self.__field.bind(instance)
            field.validate(value)
            if field.readonly:
                raise ValueError(self.__name, _('Field is readonly'))
            sm = ISecurityManager(instance, None)
            principals = sm.getLocalAllowedPrincipals(self.__role)
            removed = set(principals) - set(value)
            added = set(value) - set(principals)
            for principal in removed:
                sm.unsetRole(self.__role, principal)

            for principal in added:
                sm.grantRole(self.__role, principal)

        return