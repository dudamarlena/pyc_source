# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/ore/wsgiapp/publication.py
# Compiled at: 2008-05-01 10:27:18
"""
$Id: $
"""
from zope.app.publication.browser import BrowserPublication
from zope.app.publication.interfaces import IRequestPublicationFactory, IBrowserRequestFactory
from zope.publisher.browser import BrowserRequest
from zope import component, interface
import interfaces

class Publication(BrowserPublication):

    def getApplication(self, request):
        app = component.getUtility(interfaces.IApplication)
        return app


class BrowserFactory(object):
    interface.implements(IRequestPublicationFactory)

    def canHandle(self, environment):
        return True

    def __call__(self):
        request_class = component.queryUtility(IBrowserRequestFactory, default=BrowserRequest)
        return (request_class, Publication)