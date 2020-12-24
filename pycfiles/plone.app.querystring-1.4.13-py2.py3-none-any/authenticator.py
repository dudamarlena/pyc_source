# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/plone/app/protect/authenticator.py
# Compiled at: 2008-03-07 17:28:21
import hmac, sha
from zope.component import getUtility
from zope.interface import implements
from AccessControl import getSecurityManager
from zExceptions import Forbidden
from ZPublisher.HTTPRequest import HTTPRequest
from Products.Five import BrowserView
from plone.keyring.interfaces import IKeyManager
from plone.app.protect.interfaces import IAuthenticatorView
from plone.app.protect.utils import protect
from zope.deprecation import deprecated

def _getUserName():
    user = getSecurityManager().getUser()
    if user is None:
        return 'Anonymous User'
    return user.getUserName()


def _verify(request):
    auth = request.get('_authenticator')
    if auth is None:
        return False
    manager = getUtility(IKeyManager)
    ring = manager['_system']
    user = _getUserName()
    for key in ring:
        if key is None:
            continue
        correct = hmac.new(key, user, sha).hexdigest()
        if correct == auth:
            return True

    return False


class AuthenticatorView(BrowserView):
    __module__ = __name__
    implements(IAuthenticatorView)

    def authenticator(self):
        manager = getUtility(IKeyManager)
        secret = manager.secret()
        user = _getUserName()
        auth = hmac.new(secret, user, sha).hexdigest()
        return '<input type="hidden" name="_authenticator" value="%s"/>' % auth

    def verify(self):
        return _verify(self.request)


def check(request):
    if isinstance(request, HTTPRequest):
        if not _verify(request):
            raise Forbidden('Form authenticator is invalid.')


def AuthenticateForm(callable):
    return protect(callable, check)


deprecated('AuthenticateForm', 'Please use postonly(CheckAuthenticator)')
__all__ = [
 'AuthenticatorView', 'AuthenticateForm', 'check']