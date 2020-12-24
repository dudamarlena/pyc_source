# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/falkolab/cacheburster/testing.py
# Compiled at: 2010-12-07 02:45:55
import os, falkolab.cacheburster
from zope.publisher.interfaces.browser import IBrowserSkinType, IDefaultBrowserLayer
from zope.interface.declarations import alsoProvides, implements
from zope.app.testing.functional import ZCMLLayer
from zope.publisher.browser import BrowserView
from zope.browserresource.resource import Resource
from zope.publisher.interfaces.browser import IBrowserPublisher
from zope.publisher.interfaces import NotFound
from falkolab.cacheburster.interfaces import IVersionedResourceLayer
testsPath = os.path.join(os.path.dirname(falkolab.cacheburster.__file__), 'tests')

class NoFileResource(BrowserView, Resource):
    implements(IBrowserPublisher)

    def publishTraverse(self, request, name):
        raise NotFound(None, name)
        return

    def browserDefault(self, request):
        return (self._getBody, ())

    def _getBody(self):
        return 'no file resource body'


def NoFileResourceFactory(request):
    return NoFileResource(None, request)


class ITestSkin(IVersionedResourceLayer, IDefaultBrowserLayer):
    pass


alsoProvides(ITestSkin, IBrowserSkinType)
CacheBursterLayer = ZCMLLayer(os.path.join(os.path.dirname(__file__), 'ftesting.zcml'), __name__, 'CacheBursterLayer', allow_teardown=True)