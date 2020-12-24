# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/namlook/Documents/projects/restdyn/tests/test_client.py
# Compiled at: 2011-09-02 10:47:07
import unittest
from restdyn import Client, RequestFailed
import json
from time import sleep
TEST_SERVER = 'http://localhost:8080'

class ClientTestCase(unittest.TestCase):

    def tearDown(self):
        sleep(2)

    def test_twitter(self):
        TwitterAPi = Client('https://api.twitter.com/1', end_resources='.json')
        res = TwitterAPi.search(q='test')
        self.assertTrue(isinstance(res, dict))
        self.assertEqual(res['page'], 1)

    def test_google_search_set_persistent_params_kwargs(self):
        GoogleAPI = Client('http://ajax.googleapis.com/ajax/services')
        GoogleAPI.set_persistent_params(v='1.0')
        res = GoogleAPI.search.web(q='Earth Day')
        self.assertTrue(isinstance(res, dict))
        self.assertEqual(res['responseStatus'], 200)

    def test_google_search_set_persistent_params_args(self):
        GoogleAPI = Client('http://ajax.googleapis.com/ajax/services')
        GoogleAPI.set_persistent_params({'v': '1.0'})
        res = GoogleAPI.search.web(q='Earth Day')
        self.assertTrue(isinstance(res, dict))
        self.assertEqual(res['responseStatus'], 200)

    def test_google_search_set_persistent_params_bad(self):
        GoogleAPI = Client('http://ajax.googleapis.com/ajax/services')
        self.assertRaises(AssertionError, GoogleAPI.set_persistent_params, 'v=1.0')
        self.assertRaises(AssertionError, GoogleAPI.set_persistent_params, [('v', '1.0')])

    def test_end_resources(self):
        for end_resources in ['.json', '.xml', 'blah']:
            TwitterAPi = Client('https://api.twitter.com/1', end_resources=end_resources)
            url = TwitterAPi.search._get_url()
            self.assertTrue(url.endswith(end_resources))

    def test__getitem__(self):
        GoogleAPI = Client('http://ajax.googleapis.com')
        GoogleAPI.set_persistent_params(v='1.0')
        res = GoogleAPI['ajax'].services['search'].web(q='Earth Day')
        self.assertTrue(isinstance(res, dict))
        self.assertEqual(res['responseStatus'], 200)
        res = GoogleAPI.ajax['services']['search']['web'](q='Earth Day')
        self.assertTrue(isinstance(res, dict))
        self.assertEqual(res['responseStatus'], 200)

    def test_get_last_call(self):
        GoogleAPI = Client('http://ajax.googleapis.com/ajax/services')
        GoogleAPI.set_persistent_params({'v': '1.0'})
        res = GoogleAPI.search.web(q='Earth Day')
        self.assertEqual(res, json.loads(GoogleAPI._last_result))
        self.assertEqual(GoogleAPI._last_response.status_int, 200)

    def test_raise_error(self):
        TwitterAPi = Client('https://api.twitter.com/1', end_resources='.json')
        self.assertRaises(RequestFailed, TwitterAPi.search)

    def test_post_process_result(self):

        class CustomGoogleAPI(Client):

            def post_process_result(self, result):
                if result['responseStatus'] == 400:
                    raise RequestFailed(result['responseDetails'])
                return result

        GoogleAPI = CustomGoogleAPI('http://ajax.googleapis.com/ajax/services')
        try:
            GoogleAPI.search.web(q='toto')
            assert 0
        except RequestFailed, e:
            self.assertEqual(str(e), 'invalid version')

    def test_send_json_query(self):
        import json
        q = dict(foo='bar', eggs='spam')
        jsonapi = Client(TEST_SERVER)
        self.assertEqual(q, jsonapi.tests.jsonquery(q=json.dumps(q)))
        jsonapi = Client(TEST_SERVER, send_json_query='q')
        self.assertEqual(q, jsonapi.tests.jsonquery(**q))
        self.assertEqual(jsonapi._last_response.final_url, TEST_SERVER + '/tests/jsonquery?q=%7B%22eggs%22%3A+%22spam%22%2C+%22foo%22%3A+%22bar%22%7D')
        jsonapi.set_persistent_params(v='1.0')
        self.assertEqual(q, jsonapi.tests.jsonquery(**q))
        self.assertEqual(jsonapi._last_response.final_url, TEST_SERVER + '/tests/jsonquery?q=%7B%22eggs%22%3A+%22spam%22%2C+%22foo%22%3A+%22bar%22%7D&v=1.0')