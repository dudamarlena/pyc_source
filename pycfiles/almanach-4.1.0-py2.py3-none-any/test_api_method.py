# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/alman/test/test_api_method.py
# Compiled at: 2015-08-31 22:18:14
import alman, mock, requests, unittest

class TestApiMethod(unittest.TestCase):
    method = 'get'
    path = '/testing'
    params = {'param_a': '1'}
    headers = {'header_a': 'a'}

    def setUp(self):
        self.object = alman.apibits.ApiResource()
        self.api_method = alman.apibits.ApiMethod(self.method, self.path, self.params, self.headers, self.object)
        self.client_id = 'test_id'
        self.client_secret = 'test_secret'
        self.api_base = 'http://test.apibits.com'
        alman.CLIENT_ID = self.client_id
        alman.CLIENT_SECRET = self.client_secret
        alman.API_BASE = self.api_base


class TestApiMethodInit(TestApiMethod):

    def test_set_client_id(self):
        self.assertEqual(alman.CLIENT_ID, self.client_id)

    def test_set_client_secret(self):
        self.assertEqual(alman.CLIENT_SECRET, self.client_secret)

    def test_set_api_base(self):
        self.assertEqual(alman.API_BASE, self.api_base)

    @mock.patch('alman.apibits.path_builder.PathBuilder.build', return_value=TestApiMethod.path)
    def test_pathbuilder_with_path_object_and_params(self, request_mock):
        apimethod = alman.apibits.ApiMethod(self.method, self.path, self.params, self.headers, self.object)
        request_mock.assert_called_once_with(self.object, self.params, self.path)

    @mock.patch('alman.apibits.params_builder.ParamsBuilder.build', return_value=TestApiMethod.params)
    def test_paramsbuilder_with_params(self, request_mock):
        apimethod = alman.apibits.ApiMethod(self.method, self.path, self.params, self.headers, self.object)
        request_mock.assert_called_once_with(self.params)

    @mock.patch('alman.apibits.headers_builder.HeadersBuilder.build', return_value=TestApiMethod.headers)
    def test_headersbuilder_with_params(self, request_mock):
        apimethod = alman.apibits.ApiMethod(self.method, self.path, self.params, self.headers, self.object)
        request_mock.assert_called_once_with(self.headers)


class TestApiMethodExecute(TestApiMethod):
    mock_response = mock.Mock()
    mock_response.status_code = 200
    mock_response.text = "{'status': 'success'}"
    mock_response.json = lambda : {'status': 'success'}
    mock_auth_error = mock.Mock()
    mock_auth_error.status_code = 401
    mock_invalid_json = 'not-valid-json'

    @mock.patch('alman.apibits.requester.Requester.request', side_effect=requests.Timeout())
    def test_api_error_on_failed_request(self, request_mock):
        with self.assertRaises(alman.apibits.ApiError):
            self.api_method.execute()

    @mock.patch('alman.apibits.requester.Requester.request', return_value=mock_response)
    def test_response_parsed_as_json(self, request_mock):
        self.assertEqual({'status': 'success'}, self.api_method.execute())

    @mock.patch('alman.apibits.requester.Requester.request', return_value=mock_auth_error)
    def test_401_status_authentication_error(self, request_mock):
        with self.assertRaises(alman.apibits.AuthenticationError):
            self.api_method.execute()

    @mock.patch('requests.Response.content', mock_invalid_json)
    def test_invalid_json_api_error(self):
        with self.assertRaises(alman.apibits.ApiError):
            ret = self.api_method.execute()