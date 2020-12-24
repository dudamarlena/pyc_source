# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/khan/tests/test_proxy.py
# Compiled at: 2010-05-12 10:25:54
from khan.utils.testing import *
from khan.proxy import *

class TestProxy(TestCase):
    TARGET = 'http://www.google.com'

    def test(self):
        app = Proxy(self.TARGET)
        app = TestApp(app)
        resp = app.get('/', status='*')
        self.assertEqual(resp.status_int, 200)
        self.assertEqual('google' in resp.body, True, resp.body)

    def test_timeout(self):
        app = Proxy(self.TARGET, timeout=0.01)
        app = TestApp(app)
        resp = app.get('/', status='*')
        self.assertEqual(resp.status_int, 502)

    def test_server_not_found(self):
        app = Proxy('http://...')
        app = TestApp(app)
        resp = app.get('/', status='*')
        self.assertEqual(resp.status_int, 404)


class TestTransparentProxy(TestCase):
    HOST = 'www.google.com'

    def test(self):
        app = TransparentProxy(force_host=self.HOST)
        app = TestApp(app)
        resp = app.get('/', status='*')
        self.assertEqual(resp.status_int, 200)
        self.assertEqual('google' in resp.body, True)

    def test_timeout(self):
        app = TransparentProxy(force_host=self.HOST, timeout=0.01)
        app = TestApp(app)
        resp = app.get('/', status='*')
        self.assertEqual(resp.status_int, 502)

    def test_server_not_found(self):
        app = TransparentProxy(force_host='...')
        app = TestApp(app)
        resp = app.get('/', status='*')
        self.assertEqual(resp.status_int, 404)


if __name__ == '__main__':
    unittest.main()