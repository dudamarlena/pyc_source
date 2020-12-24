# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/urltest/__init__.py
# Compiled at: 2009-07-01 11:15:47
"""
A wrapper around WebTest which provides a nice domain specific language for
testing URLs in WSGI applications. The following example demonstrates usage:

#!/usr/bin/env python

from example_app import application
from urltest import verify_urls

if __name__ == "__main__":
    urls = (
        {'url':"/", 'code':200},
        {'url':"/bob", 'code':200},
        {'url':"/jim", 'code':404},
        {'url':"/jim", 'method': "POST", 'code':405},
    )
    verify_urls(urls, application)
"""
import sys, unittest
from webtest import TestApp
CODES = {100: 'Continue', 
   101: 'Switching Protocols', 
   200: 'OK', 
   201: 'Created', 
   202: 'Accepted', 
   203: 'Non-Authoritative Information', 
   204: 'No Content', 
   205: 'Reset Content', 
   206: 'Partial Content', 
   300: 'Multiple Choices', 
   301: 'Moved Permanently', 
   302: 'Found', 
   303: 'See Other', 
   304: 'Not Modified', 
   305: 'Use Proxy', 
   307: 'Temporary Redirect', 
   400: 'Bad Request', 
   401: 'Unauthorized', 
   402: 'Payment Required', 
   403: 'Forbidden', 
   404: 'Not Found', 
   405: 'Method Not Allowed', 
   406: 'Not Acceptable', 
   407: 'Proxy Authentication Required', 
   408: 'Request Time-out', 
   409: 'Conflict', 
   410: 'Gone', 
   411: 'Length Required', 
   412: 'Precondition Failed', 
   413: 'Request Entity Too Large', 
   414: 'Request-URI Too Large', 
   415: 'Unsupported Media Type', 
   416: 'Requested range not satisfiable', 
   417: 'Expectation Failed', 
   500: 'Internal Server Error', 
   501: 'Not Implemented', 
   502: 'Bad Gateway', 
   503: 'Service Unavailable', 
   504: 'Gateway Time-out', 
   505: 'HTTP Version not supported'}

def _get_method(item):
    """Get the HTTP method from the passed data, defaulting to GET"""
    try:
        method = item['method'].lower()
    except KeyError:
        method = 'get'

    if method not in ('get', 'post', 'delete', 'put'):
        method = 'get'
    return method


def _get_test_name(item):
    """Create a user friendly name for the test"""
    return 'test_%s_request_of_%s_returns_%d' % (
     _get_method(item), item['url'], item['code'])


def test_generator(data):
    """
    This function returns a dynamically created test method
    which can be added to a unitest test class
    """

    def test(self):
        """A test dynamically generated test method"""
        method = _get_method(data)
        if method == 'get':
            response = self.app.get(data['url'], expect_errors=True)
        elif method == 'delete':
            response = self.app.delete(data['url'], expect_errors=True)
        elif method == 'post':
            response = self.app.post(data['url'], expect_errors=True)
        elif method == 'put':
            response = self.app.put(data['url'], expect_errors=True)
        self.assertEquals('%s %s' % (data['code'], CODES[data['code']]), response.status)

    return test


def verify_urls(data, application):
    """
    This is the test runner for the DSL. It creates an empty TestCase, parses
    the DSL and dynamically appends the test methods. It then runs the
    test suite and prints the results.
    """

    class TestSuite(unittest.TestCase):
        """A blank TestCase waiting for test methods"""

        def setUp(self):
            """Store the WSGI app for easy access by methods"""
            self.app = TestApp(application)

    for item in data:
        method = _get_method(item)
        test_name = _get_test_name(item)
        test = test_generator(item)
        setattr(TestSuite, test_name, test)

    suite = unittest.TestLoader().loadTestsFromTestCase(TestSuite)
    unittest.TextTestRunner(sys.stdout).run(suite)