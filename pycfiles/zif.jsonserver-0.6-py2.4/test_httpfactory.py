# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/zif/jsonserver/tests/test_httpfactory.py
# Compiled at: 2007-05-25 16:54:16
"""Tests for the JSONRPC Publication Request Factory.

modified from zope.app.publication.tests.test_requestpublicationfactories.py jwashin 2005-11-06
Altered imports to reflect zif namespace

"""
from unittest import TestCase, TestSuite, main, makeSuite
from StringIO import StringIO
from zope import component, interface
from zope.publisher.browser import BrowserRequest
from zope.publisher.http import HTTPRequest
from zif.jsonserver.jsonrpc import JSONRPCRequest
from zope.component.testing import PlacelessSetup
from zif.jsonserver.interfaces import IJSONRPCRequestFactory
from zope.app.publication.httpfactory import HTTPPublicationRequestFactory
from zope.app.publication.browser import BrowserPublication
from zope.app.publication.http import HTTPPublication
from zif.jsonserver.requestpublicationfactory import JSONRPCFactory
from zif.jsonserver.jsonrpc import JSONRPCPublication
from zope.app.testing import ztapi

class DummyRequestFactory(object):
    __module__ = __name__

    def __call__(self, input_stream, env):
        self.input_stream = input_stream
        self.env = env
        return self

    def setPublication(self, pub):
        self.pub = pub


class Test(PlacelessSetup, TestCase):
    __module__ = __name__

    def setUp(self):
        super(Test, self).setUp()
        self.__factory = HTTPPublicationRequestFactory(None)
        self.__env = {'SERVER_URL': 'http://127.0.0.1', 'HTTP_HOST': '127.0.0.1', 'CONTENT_LENGTH': '0', 'GATEWAY_INTERFACE': 'TestFooInterface/1.0'}
        return

    def test_jsonrpcfactory(self):
        jsonrpcrequestfactory = DummyRequestFactory()
        interface.directlyProvides(jsonrpcrequestfactory, IJSONRPCRequestFactory)
        component.provideUtility(jsonrpcrequestfactory)
        env = self.__env
        factory = JSONRPCFactory()
        self.assertEqual(factory.canHandle(env), True)
        (request, publication) = factory()
        self.assertEqual(isinstance(request, DummyRequestFactory), True)
        self.assertEqual(publication, JSONRPCPublication)


def test_suite():
    return TestSuite((makeSuite(Test),))


if __name__ == '__main__':
    main(defaultTest='test_suite')