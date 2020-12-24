# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.8.2-i386/egg/worldcookery/browser/login.py
# Compiled at: 2006-09-21 05:27:35
from zope.publisher.browser import BrowserPage
from zope.app.pagetemplate import ViewPageTemplateFile
from zope.app.security.interfaces import IUnauthenticatedPrincipal

class LoginPage(BrowserPage):
    __module__ = __name__
    template = ViewPageTemplateFile('login.pt')

    def __call__(self):
        request = self.request
        if not IUnauthenticatedPrincipal.providedBy(request.principal) and 'worldcookery.Login' in request:
            camefrom = request.get('camefrom', '.')
            request.response.redirect(camefrom)
        else:
            return self.template()