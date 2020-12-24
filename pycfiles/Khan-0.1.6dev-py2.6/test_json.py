# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/khan/tests/test_json.py
# Compiled at: 2010-07-26 05:15:38
from khan.utils.testing import *
from khan.utils import unique_id
from khan.json import *

class TestJSONRPCError(TestCase):

    def test(self):
        for (ecode, cls) in jsonrpc_error_map.items():

            def wsgi_app(environ, start_response):
                resp = cls()
                return resp(environ, start_response)

            test_app = TestApp(wsgi_app)
            resp = test_app.get('/', status='*')
            self.failUnlessEqual(resp.status_int, 200)
            json_data = jsonrpc_loads(resp.body)
            self.failUnlessEqual(json_data['error']['message'], cls.message)
            self.failUnlessEqual(json_data['error']['code'], cls.code)


class TestJSONPProxy(TestCase):

    def setUp(self):
        self.app = JSONPProxy()
        self.test_app = TestApp(self.app)

    def test(self):
        param = {'_callback': 'abc'}
        extra_environ = {'HTTP_HOST': 'w3c.org'}
        resp = self.test_app.get('/400', status='*', extra_environ=extra_environ)
        assert resp.status_int == 400, 'error status: %d' % resp.status_int
        resp = self.test_app.get('/404', param, status='*', extra_environ=extra_environ)
        self.assertEqual(502, resp.status_int)
        resp = self.test_app.get('/%s' % unique_id(), param, status='*', extra_environ=extra_environ)
        self.assertEqual(502, resp.status_int)
        resp = self.test_app.get('/', param, status='*', extra_environ=extra_environ)
        self.assertEqual(200, resp.status_int)
        self.assertEqual('text/javascript', resp.content_type)


class TestJSONRPCService(TestCase):

    def setUp(self):
        self.app = JSONRPCService()
        self.app['test.echo'] = self.echo
        self.test_app = TestApp(self.app)

    def echo(self, s):
        return s

    def get_exc_from_resp(self, resp):
        json_resp = jsonrpc_loads(resp.body)
        exc = jsonrpc_error_map[json_resp['error']['code']]
        return exc

    def test_basic(self):
        json_req = JSONRPCBuilder.request('test.echo', 'a', id=10)
        resp = self.test_app.post('/', json_req, status='*')
        assert resp.status_int == 200
        json_resp = jsonrpc_loads(resp.body)
        self.assertEqual(json_resp['id'], 10)
        assert json_resp['result'] == 'a', 'req: %s,  resp: %s' % (json_req, json_resp)
        json_req = JSONRPCBuilder.request('test.echo', {'s': 'a'}, id=0)
        resp = self.test_app.post('/', json_req, status='*')
        json_resp = jsonrpc_loads(resp.body)
        assert json_resp['result'] == 'a', 'req: %s,  resp: %s' % (json_req, json_resp)
        resp = self.test_app.post('/not_implemented', json_req, status='*')
        assert resp.status_int == 200
        for version in [None, '1.0', '2.0']:
            json_req = JSONRPCBuilder.request('test.echo', [1], version=version, id=2)
            resp = self.test_app.post('/', json_req, status='*')
            json = jsonrpc_loads(resp.body)
            self.assertEqual(json['result'], 1)
            self.assertEqual(json['id'], 2)
            self.assertFalse(json.has_key('error'))
            if version == '1.0':
                self.assertTrue(json.has_key('version'))
                self.assertEqual(json['version'], '1.0')
            elif version == '2.0':
                self.assertTrue(json.has_key('jsonrpc'))
                self.assertEqual(json['jsonrpc'], '2.0')
            else:
                self.assertTrue(json.has_key('version'))
                self.assertEqual(json['version'], '1.0')

        return

    def test_with_invalid_request(self):
        resp = self.test_app.get('/', status='*')
        assert resp.status_int == 200
        exc = self.get_exc_from_resp(resp)
        assert JSONRPCInvalidRequestError == exc
        resp = self.test_app.post('/', 'invalid jsonrpc data', status='*')
        exc = self.get_exc_from_resp(resp)
        assert JSONRPCParseError == exc
        json_req = JSONRPCBuilder.request('', 'a')
        resp = self.test_app.post('/', json_req, status='*')
        exc = self.get_exc_from_resp(resp)
        assert JSONRPCParseError == exc

    def test_method_not_found(self):
        json_req = JSONRPCBuilder.request('no method', 'a', id=0)
        resp = self.test_app.post('/', json_req, status='*')
        exc = self.get_exc_from_resp(resp)
        assert JSONRPCMethodNotFoundError == exc

    def test_invalid_params(self):
        json_req = JSONRPCBuilder.request('test.echo', id=0)
        resp = self.test_app.post('/', json_req, status='*')
        exc = self.get_exc_from_resp(resp)
        assert JSONRPCInvalidParamsError == exc

    def test_internal_error(self):

        def raise_error():
            raise ValueError('raised')

        self.app['test.raise_error'] = raise_error
        json_req = JSONRPCBuilder.request('test.raise_error', id=0)
        resp = self.test_app.post('/', json_req, status='*')
        exc = self.get_exc_from_resp(resp)
        assert JSONRPCInternalError == exc

    def test_notification_req(self):
        json_req = JSONRPCBuilder.request('test.echo', [1])
        resp = self.test_app.post('/', json_req, status='*')
        self.assertFalse(resp.body)
        json_req = JSONRPCBuilder.request('test.echo')
        resp = self.test_app.post('/', json_req, status='*')
        self.assertFalse(resp.body)
        json_req = JSONRPCBuilder.request('test.nomethod', [1])
        resp = self.test_app.post('/', json_req, status='*')
        self.assertFalse(resp.body)


if __name__ == '__main__':
    unittest.main()