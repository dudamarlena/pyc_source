# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/zif/jsonserver/tests/test_jsonrpcpublication.py
# Compiled at: 2007-05-25 16:54:16
"""JSON-RPC Publication Tests

modified from zope.app.publication.tests.test_xmlrpcpublication.py jwashin 2005-06-06

removed references to JSONRPCPresentation 20060619 jmw
altered imports to reflect zif namespace 20061216 jmw

"""
import unittest
from zope.app.publication.tests.test_zopepublication import BasePublicationTests
from zope.app.publication.traversers import TestTraverser
from zif.jsonserver.jsonrpc import JSONRPCPublication
from zope.interface import Interface, implements
from zope.proxy import removeAllProxies
from zope.publisher.interfaces import NotFound
from zif.jsonserver.interfaces import IJSONRPCRequest
from zif.jsonserver.interfaces import IJSONRPCPublisher
from zif.jsonserver.jsonrpc import TestRequest
from zope.app.testing import ztapi

class SimpleObject(object):
    __module__ = __name__

    def __init__(self, v):
        self.v = v


class JSONRPCPublicationTests(BasePublicationTests):
    __module__ = __name__
    klass = JSONRPCPublication

    def _createRequest(self, path, publication, **kw):
        request = TestRequest(PATH_INFO=path, **kw)
        request.setPublication(publication)
        return request

    def testTraverseName(self):
        pub = self.klass(self.db)

        class C(object):
            __module__ = __name__
            x = SimpleObject(1)

        ob = C()
        r = self._createRequest('/x', pub)
        ztapi.provideView(None, IJSONRPCRequest, IJSONRPCPublisher, '', TestTraverser)
        ob2 = pub.traverseName(r, ob, 'x')
        self.assertEqual(removeAllProxies(ob2).v, 1)
        return

    def testDenyDirectMethodAccess(self):
        pub = self.klass(self.db)

        class I(Interface):
            __module__ = __name__

        class C(object):
            __module__ = __name__
            implements(I)

            def foo(self):
                return 'bar'

        class V(object):
            __module__ = __name__

            def __init__(self, context, request):
                pass

            implements(IJSONRPCPublisher)

        ob = C()
        r = self._createRequest('/foo', pub)
        ztapi.provideView(I, IJSONRPCPublisher, Interface, 'view', V)
        ztapi.setDefaultViewName(I, 'view', type=IJSONRPCPublisher)
        self.assertRaises(NotFound, pub.traverseName, r, ob, 'foo')

    def testTraverseNameView(self):
        pub = self.klass(self.db)
        from zif.jsonserver.jsonrpc import IJSONRPCPublisher

        class I(Interface):
            __module__ = __name__

        class C(object):
            __module__ = __name__
            implements(I)

        ob = C()

        class V(object):
            __module__ = __name__

            def __init__(self, context, request):
                pass

            implements(IJSONRPCPublisher)

        from zif.jsonserver.jsonrpc import IJSONRPCPublisher
        from zif.jsonserver.interfaces import IJSONRPCRequest
        from zope.app.publication.traversers import SimpleComponentTraverser
        ztapi.provideView(Interface, IJSONRPCRequest, IJSONRPCPublisher, '', SimpleComponentTraverser)
        r = self._createRequest('/@@spam', pub)
        ztapi.provideView(I, IJSONRPCRequest, Interface, 'spam', V)
        ob2 = pub.traverseName(r, ob, '@@spam')
        self.assertEqual(removeAllProxies(ob2).__class__, V)
        ob2 = pub.traverseName(r, ob, 'spam')
        self.assertEqual(removeAllProxies(ob2).__class__, V)

    def testTraverseNameSiteManager(self):
        pub = self.klass(self.db)

        class C(object):
            __module__ = __name__

            def getSiteManager(self):
                return SimpleObject(1)

        ob = C()
        r = self._createRequest('/++etc++site', pub)
        ob2 = pub.traverseName(r, ob, '++etc++site')
        self.assertEqual(removeAllProxies(ob2).v, 1)


def test_suite():
    return unittest.TestSuite((unittest.makeSuite(JSONRPCPublicationTests),))


if __name__ == '__main__':
    unittest.main()