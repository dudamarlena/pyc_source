# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/zif/jsonserver/tests/test_directives.py
# Compiled at: 2007-05-25 16:54:16
"""Test 'jsonrpc' ZCML Namespace directives.

mod from zope.app.publisher.xmlrpc.tests.test_directives.py jwashin 2005-06-06
altered imports for zif namespace jwashin 2006-12-16
"""
import unittest
from zope.configuration import xmlconfig
from zope.configuration.exceptions import ConfigurationError
from zope.app.component.tests.views import IC, V1, Request
from zope.app.testing.placelesssetup import PlacelessSetup
from zope.security.proxy import ProxyFactory
from zif.jsonserver.interfaces import IJSONRPCRequest
from zif import jsonserver
from zif.jsonserver import jsonrpc
from zope.interface import implements
from zope.component import queryMultiAdapter, getMultiAdapter
import zif.jsonserver.tests
request = Request(IJSONRPCRequest)

class Ob(object):
    __module__ = __name__
    implements(IC)


ob = Ob()

class DirectivesTest(PlacelessSetup, unittest.TestCase):
    __module__ = __name__

    def testView(self):
        self.assertEqual(queryMultiAdapter((ob, request), name='test'), None)
        xmlconfig.file('jsonrpc.zcml', jsonserver.tests)
        view = queryMultiAdapter((ob, request), name='test')
        self.assert_(V1 in view.__class__.__bases__)
        self.assert_(jsonrpc.MethodPublisher in view.__class__.__bases__)
        return

    def testInterfaceProtectedView(self):
        xmlconfig.file('jsonrpc.zcml', jsonserver.tests)
        v = getMultiAdapter((ob, request), name='test2')
        v = ProxyFactory(v)
        self.assertEqual(v.index(), 'V1 here')
        self.assertRaises(Exception, getattr, v, 'action')

    def testAttributeProtectedView(self):
        xmlconfig.file('jsonrpc.zcml', jsonserver.tests)
        v = getMultiAdapter((ob, request), name='test3')
        v = ProxyFactory(v)
        self.assertEqual(v.action(), 'done')
        self.assertRaises(Exception, getattr, v, 'index')

    def testInterfaceAndAttributeProtectedView(self):
        xmlconfig.file('jsonrpc.zcml', jsonserver.tests)
        v = getMultiAdapter((ob, request), name='test4')
        self.assertEqual(v.index(), 'V1 here')
        self.assertEqual(v.action(), 'done')

    def testDuplicatedInterfaceAndAttributeProtectedView(self):
        xmlconfig.file('jsonrpc.zcml', jsonserver.tests)
        v = getMultiAdapter((ob, request), name='test5')
        self.assertEqual(v.index(), 'V1 here')
        self.assertEqual(v.action(), 'done')

    def testIncompleteProtectedViewNoPermission(self):
        self.assertRaises(ConfigurationError, xmlconfig.file, 'jsonrpc_error.zcml', jsonserver.tests)

    def test_no_name(self):
        xmlconfig.file('jsonrpc.zcml', jsonserver.tests)
        v = getMultiAdapter((ob, request), name='index')
        self.assertEqual(v(), 'V1 here')
        v = getMultiAdapter((ob, request), name='action')
        self.assertEqual(v(), 'done')


def test_suite():
    return unittest.TestSuite((unittest.makeSuite(DirectivesTest),))


if __name__ == '__main__':
    unittest.main()