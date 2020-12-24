# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/mail/adapter.py
# Compiled at: 2013-11-20 11:00:47
from zope.pluggableauth.interfaces import IAuthenticatorPlugin
from zope.security.interfaces import IPrincipal
from ztfy.mail.interfaces import IPrincipalMailInfo
from zope.component import getUtilitiesFor

def getPrincipalAddress(principal):
    """Get email address of given principal"""
    if IPrincipal.providedBy(principal):
        principal = principal.id
    for _name, plugin in getUtilitiesFor(IAuthenticatorPlugin):
        principal_info = plugin.principalInfo(principal)
        if principal_info is not None:
            principal_email = IPrincipalMailInfo(principal_info, None)
            if principal_email is not None:
                return principal_email.getAddresses()

    return