# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_security/plugin/admin.py
# Compiled at: 2020-02-21 07:52:38
# Size of source mod 2**32: 3805 bytes
__doc__ = 'PyAMS_security.plugin.admin module\n\nThis module defines system principals which are used for system management tasks and for\ninternal services.\n'
from persistent import Persistent
from zope.container.contained import Contained
from zope.interface import implementer
from zope.password.interfaces import IPasswordManager
from zope.schema.fieldproperty import FieldProperty
from pyams_security.interfaces import IAdminAuthenticationPlugin, IDirectoryPlugin
from pyams_security.principal import PrincipalInfo
from pyams_utils.registry import get_utility
__docformat__ = 'restructuredtext'

@implementer(IAdminAuthenticationPlugin, IDirectoryPlugin)
class AdminAuthenticationPlugin(Persistent, Contained):
    """AdminAuthenticationPlugin"""
    prefix = FieldProperty(IAdminAuthenticationPlugin['prefix'])
    title = FieldProperty(IAdminAuthenticationPlugin['title'])
    enabled = FieldProperty(IAdminAuthenticationPlugin['enabled'])
    login = FieldProperty(IAdminAuthenticationPlugin['login'])
    _password = FieldProperty(IAdminAuthenticationPlugin['password'])

    @property
    def password(self):
        """Get current password"""
        return self._password

    @password.setter
    def password(self, value):
        """Encode passsword before storing new value"""
        if value:
            manager = get_utility(IPasswordManager, name='SSHA')
            self._password = manager.encodePassword(value)
        else:
            self._password = None

    def authenticate(self, credentials, request):
        """Try to authenticate principal using given credentials"""
        if not (self.enabled and self.password):
            return
        attrs = credentials.attributes
        login = attrs.get('login')
        password = attrs.get('password')
        manager = get_utility(IPasswordManager, name='SSHA')
        if login == self.login and manager.checkPassword(self._password, password):
            return '{0}:{1}'.format(self.prefix, login)

    def get_principal(self, principal_id, info=True):
        """Get principal matching given principal ID"""
        if not self.enabled:
            return
        if not principal_id.startswith(self.prefix + ':'):
            return
        prefix, login = principal_id.split(':', 1)
        if prefix == self.prefix and login == self.login:
            if info:
                return PrincipalInfo(id=principal_id, title=self.title)
            return self

    def get_all_principals(self, principal_id):
        """Get all principals matching given principal ID"""
        if not self.enabled:
            return set()
        if self.get_principal(principal_id) is not None:
            return {principal_id}
        return set()

    def find_principals(self, query):
        """Search principals matching given query"""
        if not query:
            return
        query = query.lower()
        if query == self.login or query in self.title.lower():
            yield PrincipalInfo(id='{0}:{1}'.format(self.prefix, self.login), title=self.title)