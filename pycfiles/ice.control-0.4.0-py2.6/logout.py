# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ice/control/skin/authentication/logout.py
# Compiled at: 2010-08-27 06:32:04
from zc.resourcelibrary import need
from zope import interface, component
from zope.authentication.interfaces import IUnauthenticatedPrincipal
from zope.authentication.interfaces import IAuthentication, ILogout
from zope.app.pagetemplate import ViewPageTemplateFile

class Pagelet(object):
    interface.implements(ILogout)
    confirmation = ViewPageTemplateFile('logout.pt')
    redirect = ViewPageTemplateFile('redirect.pt')

    def render(self):
        nextURL = self.request.get('nextURL')
        if not IUnauthenticatedPrincipal(self.request.principal, False):
            auth = component.getUtility(IAuthentication)
            ILogout(auth).logout(self.request)
            if nextURL:
                return self.redirect()
        if nextURL is None:
            return self.confirmation()
        else:
            return self.request.response.redirect(nextURL)