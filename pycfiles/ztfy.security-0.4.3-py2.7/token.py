# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/security/auth/token.py
# Compiled at: 2014-04-22 10:27:46
import hmac
from datetime import date
from hashlib import sha1
from persistent import Persistent
from zope.authentication.interfaces import IAuthentication
from zope.container.contained import Contained
from zope.interface import implements, Interface
from zope.pluggableauth.factories import PrincipalInfo
from zope.pluggableauth.interfaces import ICredentialsPlugin, IAuthenticatorPlugin
from zope.pluggableauth.plugins.principalfolder import IInternalPrincipalContainer
from zope.publisher.interfaces.http import IHTTPRequest
from zope.schema import TextLine
from zope.schema.fieldproperty import FieldProperty
from ztfy.utils.traversing import getParent
from ztfy.security import _

class TokenCredentialsUtility(Persistent, Contained):
    """Token credentials extraction utility"""
    implements(ICredentialsPlugin)
    loginfield = 'login'
    tokenfield = 'token'

    def extractCredentials(self, request):
        if not IHTTPRequest.providedBy(request):
            return None
        else:
            if not (request.get(self.loginfield) and request.get(self.tokenfield)):
                return None
            return {'login': request.get(self.loginfield), 'token': request.get(self.tokenfield)}

    def challenge(self, request):
        return False

    def logout(self, request):
        return False


class ITokenAuthenticationUtility(Interface):
    """Token authentication utility interface"""
    encryption_key = TextLine(title=_('Encryption key'), description=_('This key is used to encrypt login:password string with HMAC+SHA1 protocol'), required=True)


class TokenAuthenticationUtility(Persistent, Contained):
    """Token authentication checker utility

    Be warned that authentication mechanism can only be checked against an
    InternalPrincipal using plain text password manager...
    """
    implements(ITokenAuthenticationUtility, IAuthenticatorPlugin)
    encryption_key = FieldProperty(ITokenAuthenticationUtility['encryption_key'])

    def authenticateCredentials(self, credentials):
        if not isinstance(credentials, dict):
            return
        else:
            if not ('login' in credentials and 'token' in credentials):
                return
            login = credentials['login']
            token = credentials['token']
            if not (login and token):
                return
            utility = getParent(self, IAuthentication)
            if utility is None:
                return
            for name, plugin in utility.getAuthenticatorPlugins():
                if not IInternalPrincipalContainer.providedBy(plugin):
                    continue
                try:
                    id = plugin.getIdByLogin(login)
                    principal = plugin[login]
                except KeyError:
                    continue
                else:
                    source = '%s:%s:%s' % (principal.login,
                     principal.password,
                     date.today().strftime('%Y%m%d'))
                    encoded = hmac.new(self.encryption_key.encode('utf-8'), source, sha1)
                    if encoded.hexdigest() == token:
                        return PrincipalInfo(id, principal.login, principal.title, principal.description)

            return

    def principalInfo(self, id):
        return