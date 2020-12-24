# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tests\test_wsgiakismet.py
# Compiled at: 2006-11-21 16:05:41
import unittest, wsgiakismet
from StringIO import StringIO
from urllib import urlencode
key = ''
blog = 'http://www.example.com/'

class TestWsgiAkisimet(unittest.TestCase):
    __module__ = __name__

    def dummy_sr(self, status, headers, exc_info=None):
        pass

    def test_negative(self):
        env = {'HTTP_METHOD': 'POST', 'wsgi.input': StringIO(''), 'QUERY_STRING': urlencode({'comment_author': 'Bob Saunders', 'comment_author_email': 'bob@saunders.net', 'comment_author_url': '', 'comment': 'The post was informative.'}), 'REMOTE_ADDR': '207.89.134.5', 'HTTP_USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; YPC 3.0.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)'}

        @wsgiakismet.akismet(key, blog)
        def test(environ, start_response):
            start_response('200 OK', [('Content-type', 'text/plain')])
            return ['Good']

        response = test(env, self.dummy_sr)
        self.assertEqual(response[0], 'Good')

    def test_positive(self):
        env = {'HTTP_METHOD': 'POST', 'wsgi.input': StringIO(''), 'QUERY_STRING': urlencode({'comment_author': 'viagra-test-123', 'comment_author_email': 'viagra@viagraoffer.net', 'comment_author_url': '', 'comment': 'VIAGRA! LOTS OF VIAGRA!'}), 'REMOTE_ADDR': '10.9.4.59', 'HTTP_USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; YPC 3.0.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)'}

        @wsgiakismet.akismet(key, blog)
        def test(environ, start_response):
            start_response('200 OK', [('Content-type', 'text/plain')])
            return ['Good']

        response = test(env, self.dummy_sr)
        self.assertEqual(response[0], 'Comment was spam.')


if __name__ == '__main__':
    unittest.main()