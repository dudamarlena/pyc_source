# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ice/control/skin/authentication/login.py
# Compiled at: 2010-08-27 06:32:04
from zope import interface, component
from zope.app.publisher.interfaces.http import ILogin
from zope.authentication.interfaces import IUnauthenticatedPrincipal
from zope.authentication.interfaces import IAuthentication
from zope.app.pagetemplate import ViewPageTemplateFile

class Pagelet(object):
    interface.implements(ILogin)
    confirmation = ViewPageTemplateFile('login.pt')
    failed = ViewPageTemplateFile('login_failed.pt')

    def render(self):
        nextURL = self.request.get('nextURL')
        if IUnauthenticatedPrincipal(self.request.principal, False):
            component.getUtility(IAuthentication).unauthorized(self.request.principal.id, self.request)
            return self.failed()
        else:
            if nextURL is None:
                return self.confirmation()
            self.request.response.redirect(nextURL)
            return