# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/khan/tests/test_cache.py
# Compiled at: 2010-05-12 10:25:54
import time, unittest
from khan.utils.testing import *
from khan.cache import *

class TestEtagCached(TestCase):

    def app(self, environ, start_response):
        start_response('200 OK', [('content-type', 'text/plain')])
        return [environ['PATH_INFO']]

    def test_with_expires(self):
        app = etag_cached(2)(self.app)
        test_app = TestApp(app)
        resp = test_app.get('/a', status='*')
        headers = [('If-None-Match', resp.headers['ETag']),
         (
          'If-Modified-Since', resp.headers['Last-Modified'])]
        resp1 = test_app.get('/b', status='*', headers=headers)
        self.failUnlessEqual(resp1.status_int, 304)
        app = etag_cached(1)(self.app)
        test_app = TestApp(app)
        resp = test_app.get('/a', status='*')
        headers = [('If-None-Match', resp.headers['ETag']),
         (
          'If-Modified-Since', resp.headers['Last-Modified'])]
        time.sleep(1)
        resp1 = test_app.get('/b', status='*', headers=headers)
        self.failUnlessEqual(resp1.status_int, 200)
        self.assertTrue('Etag' in resp1.headers)
        self.assertTrue('Last-Modified' in resp1.headers)
        self.assertTrue(resp.headers['ETag'] == resp1.headers['Etag'])
        self.failUnlessEqual(resp1.body, '/b')

    def test_no_expires(self):
        app = etag_cached()(self.app)
        test_app = TestApp(app)
        resp = test_app.get('/a', status='*')
        headers = [('If-None-Match', resp.headers['ETag']),
         (
          'If-Modified-Since', resp.headers['Last-Modified'])]
        resp1 = test_app.get('/b', status='*', headers=headers)
        self.failUnlessEqual(resp1.status_int, 304)


class TestCached(TestCase):

    def app(self, environ, start_response):
        start_response('200 OK', [('content-type', 'plain/text')])
        body = str(time.time())
        return [body]

    def test_no_cache(self):

        def app(environ, start_response):
            start_response('404 Not Found', [('content-type', 'plain/text')])
            body = str(time.time())
            return [body]

        app = cached(catch_status=[200])(app)
        test_app = TestApp(app)
        resp1 = test_app.get('/', status='*')
        time.sleep(1)
        resp2 = test_app.get('/', status='*')
        assert resp1.status_int == 404 and resp2.status_int == 404
        assert resp1.body != resp2.body, 'resp1 body is : %s' % resp1.body

    def test_no_expires(self):
        app = cached()(self.app)
        test_app = TestApp(app)
        resp1 = test_app.get('/')
        time.sleep(1)
        resp2 = test_app.get('/')
        assert resp1.body == resp2.body

    def test_with_expires(self):
        cur_body = []

        def app(environ, start_response):
            start_response('200 OK', [('content-type', 'plain/text')])
            body = str(time.time())
            cur_body = []
            cur_body.append(body)
            return [body]

        expires = 2
        app = cached(expires=expires)(app)
        test_app = TestApp(app)
        resp1 = test_app.get('/')
        time.sleep(1)
        resp2 = test_app.get('/')
        assert resp1.body == resp2.body
        time.sleep(expires)
        resp3 = test_app.get('/')
        assert resp3.body != resp1.body


if __name__ == '__main__':
    unittest.main()