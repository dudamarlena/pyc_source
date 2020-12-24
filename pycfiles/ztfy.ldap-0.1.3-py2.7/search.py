# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/ldap/auth/search.py
# Compiled at: 2012-03-09 07:39:54
from ldappas.interfaces import ILDAPAuthentication
from ztfy.security.interfaces import IAuthenticatorSearchAdapter
from zope.component import adapts
from zope.interface import implements
from ztfy.ldap.auth.interfaces import ILDAPGroupsFolder

class LDAPAuthenticationSearchAdapter(object):
    """LDAP authentication search adapter"""
    adapts(ILDAPAuthentication)
    implements(IAuthenticatorSearchAdapter)

    def __init__(self, context):
        self.context = context

    def search(self, query):
        ldap_query = {self.context.titleAttribute: query}
        return self.context.search(ldap_query)


class LDAPGroupsFolderSearchAdapter(object):
    """LDAP groups folder search adapter"""
    adapts(ILDAPGroupsFolder)
    implements(IAuthenticatorSearchAdapter)

    def __init__(self, context):
        self.context = context

    def search(self, query):
        ldap_query = {self.context.titleAttribute: '*%s*' % query}
        return self.context.search(ldap_query)