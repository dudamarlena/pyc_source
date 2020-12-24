# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/z3c/referercredentials/credentials.py
# Compiled at: 2007-08-27 17:51:44
"""HTTP Referer Credentials interfaces

$Id: credentials.py 77105 2007-06-26 17:05:05Z srichter $
"""
__docformat__ = 'reStructuredText'
import persistent, transaction, urllib2, zope.interface
from zope.app.component import hooks
from zope.app.container import contained
from zope.app.session.interfaces import ISession
from zope.publisher.interfaces.http import IHTTPRequest
from zope.traversing.browser import absoluteURL
from z3c.referercredentials import interfaces

class HTTPRefererCredentials(persistent.Persistent, contained.Contained):
    __module__ = __name__
    zope.interface.implements(interfaces.IHTTPRefererCredentials)
    sessionKey = 'z3c.referercredentials'
    allowedHosts = ('localhost', )
    credentials = None
    challengeView = 'unauthorized.html'

    def extractCredentials(self, request):
        """See zope.app.authentication.interfaces.ICredentialsPlugin"""
        if not IHTTPRequest.providedBy(request):
            return
        url = request.getHeader('Referer', '')
        host = urllib2.splithost(urllib2.splittype(url)[(-1)])[0]
        if host in self.allowedHosts:
            ISession(request)[self.sessionKey]['authenticated'] = True
        if ISession(request)[self.sessionKey].get('authenticated'):
            return self.credentials
        return

    def challenge(self, request):
        """See zope.app.authentication.interfaces.ICredentialsPlugin"""
        if not IHTTPRequest.providedBy(request):
            return False
        site = hooks.getSite()
        url = '%s/@@%s' % (absoluteURL(site, request), self.challengeView)
        request.response.redirect(url)
        return True

    def logout(self, request):
        """See zope.app.authentication.interfaces.ICredentialsPlugin"""
        if not IHTTPRequest.providedBy(request):
            return False
        del ISession(request)[self.sessionKey]['authenticated']
        transaction.commit()
        return True