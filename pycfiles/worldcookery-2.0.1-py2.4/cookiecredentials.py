# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.8.2-i386/egg/worldcookery/cookiecredentials.py
# Compiled at: 2006-09-21 05:27:36
import base64, urllib
from zope.interface import Interface, implements
from zope.schema import ASCIILine
from zope.publisher.interfaces.http import IHTTPRequest
from zope.i18nmessageid import MessageFactory
_ = MessageFactory('worldcookery')
from zope.app.authentication.session import SessionCredentialsPlugin

class ICookieCredentials(Interface):
    __module__ = __name__
    cookie_name = ASCIILine(title=_('Cookie name'), description=_('Name of the cookie for storing credentials.'), required=True)


class CookieCredentialsPlugin(SessionCredentialsPlugin):
    __module__ = __name__
    implements(ICookieCredentials)
    cookie_name = 'worldcookery.auth'

    def extractCredentials(self, request):
        if not IHTTPRequest.providedBy(request):
            return
        login = request.get(self.loginfield, None)
        password = request.get(self.passwordfield, None)
        cookie = request.get(self.cookie_name, None)
        if login and password:
            val = base64.encodestring('%s:%s' % (login, password))
            request.response.setCookie(self.cookie_name, urllib.quote(val), path='/')
        elif cookie:
            val = base64.decodestring(urllib.unquote(cookie))
            (login, password) = val.split(':')
        else:
            return
        return {'login': login, 'password': password}

    def logout(self, request):
        if not IHTTPRequest.providedBy(request):
            return
        request.response.expireCookie(self.cookie_name, path='/')