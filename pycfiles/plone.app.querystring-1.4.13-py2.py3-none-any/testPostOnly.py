# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/plone/app/protect/tests/testPostOnly.py
# Compiled at: 2008-03-07 17:28:21
from unittest import TestCase
from unittest import TestSuite
from unittest import makeSuite
from plone.app.protect.postonly import check
from ZPublisher.HTTPRequest import HTTPRequest
from zExceptions import Forbidden

class PostOnlyTests(TestCase):
    __module__ = __name__

    def makeRequest(self, method):
        return HTTPRequest(None, dict(REQUEST_METHOD=method, SERVER_PORT='80', SERVER_NAME='localhost'), None)

    def testNonHTTPRequestAllowed(self):
        check('not a request')

    def testGETRequestForbidden(self):
        self.assertRaises(Forbidden, check, self.makeRequest('GET'))

    def testPOSTRequestAllowed(self):
        check(self.makeRequest('POST'))


def test_suite():
    suite = TestSuite()
    suite.addTest(makeSuite(PostOnlyTests))
    return suite