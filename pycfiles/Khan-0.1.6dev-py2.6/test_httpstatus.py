# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/khan/tests/test_httpstatus.py
# Compiled at: 2010-05-12 10:25:54
import unittest
from webob.exc import status_map
from webob import Response
from khan.utils.testing import *
from khan.httpstatus import HTTPStatus, HTTPStatusDispatcher

class TestHTTPStatus(TestCase):

    def test(self):
        self.assertTrue(HTTPStatus(404), Response)
        app = TestApp(HTTPStatus(404, detail='text'))
        self.assertTrue('text' in app.get('/', status='*').body)
        for (code, cls) in status_map.items():
            if code in (304, 204):
                continue

            def wsgi_app(environ, start_response):
                resp = HTTPStatus(code)
                return resp(environ, start_response)

            test_app = TestApp(wsgi_app)
            resp = test_app.get('/', status='*')
            self.assertTrue(resp.status_int == code)


class TestHTTPStatusDispatcherMiddleware(TestCase):

    def test_basic(self):
        app = HTTPStatusDispatcher(lambda environ, start_response: HTTPStatus(404)(environ, start_response))
        app[404] = lambda environ, start_response: HTTPStatus(500)(environ, start_response)
        res = TestApp(app).get('/', status='*')
        assert res.status_int == 404
        app = HTTPStatusDispatcher(lambda environ, start_response: HTTPStatus(404)(environ, start_response), False)
        app[404] = lambda environ, start_response: HTTPStatus(500)(environ, start_response)
        res = TestApp(app).get('/', status='*')
        assert res.status_int == 500
        app = HTTPStatusDispatcher(lambda environ, start_response: HTTPStatus(200)(environ, start_response), False)
        app[404] = lambda environ, start_response: HTTPStatus(500)(environ, start_response)
        res = TestApp(app).get('/', status='*')
        assert res.status_int == 200


if __name__ == '__main__':
    unittest.main()