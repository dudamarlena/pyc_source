# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/go_http/tests/test_metrics.py
# Compiled at: 2017-02-17 10:13:07
"""
Tests for go_http.metrics.
"""
import urlparse, json
from unittest import TestCase
from requests_testadapter import TestAdapter, TestSession
from go_http.metrics import MetricsApiClient

class RecordingAdapter(TestAdapter):
    """ Record the request that was handled by the adapter.
    """
    request = None

    def send(self, request, *args, **kw):
        self.request = request
        return super(RecordingAdapter, self).send(request, *args, **kw)


class TestMetricApiClient(TestCase):

    def setUp(self):
        self.session = TestSession()
        self.client = MetricsApiClient(auth_token='auth-token', api_url='http://example.com/api/v1/go', session=self.session)

    def test_default_session(self):
        import requests
        client = MetricsApiClient(auth_token='auth-token')
        self.assertTrue(isinstance(client.session, requests.Session))

    def test_default_api_url(self):
        client = MetricsApiClient(auth_token='auth-token')
        self.assertEqual(client.api_url, 'https://go.vumi.org/api/v1/go')

    def check_request(self, request, method, params=None, data=None, headers=None):
        self.assertEqual(request.method, method)
        if params is not None:
            url = urlparse.urlparse(request.url)
            qs = urlparse.parse_qsl(url.query)
            self.assertEqual(dict(qs), params)
        if headers is not None:
            for key, value in headers.items():
                self.assertEqual(request.headers[key], value)

        if data is None:
            self.assertEqual(request.body, None)
        else:
            self.assertEqual(json.loads(request.body), data)
        return

    def test_get_metric(self):
        response = {'stores.store_name.metric_name.agg': [
                                               {'x': 1413936000000, 'y': 88916.0},
                                               {'x': 1414022400000, 'y': 91339.0},
                                               {'x': 1414108800000, 'y': 92490.0},
                                               {'x': 1414195200000, 'y': 92655.0},
                                               {'x': 1414281600000, 'y': 92786.0}]}
        adapter = RecordingAdapter(json.dumps(response))
        self.session.mount('http://example.com/api/v1/go/metrics/', adapter)
        result = self.client.get_metric('stores.store_name.metric_name.agg', '-30d', '1d', 'omit')
        self.assertEqual(result, response)
        self.check_request(adapter.request, 'GET', params={'m': 'stores.store_name.metric_name.agg', 
           'interval': '1d', 
           'from': '-30d', 
           'nulls': 'omit'}, headers={'Authorization': 'Bearer auth-token'})

    def test_fire(self):
        response = [
         {'name': 'foo.last', 
            'value': 3.1415, 
            'aggregator': 'last'}]
        adapter = RecordingAdapter(json.dumps(response))
        self.session.mount('http://example.com/api/v1/go/metrics/', adapter)
        result = self.client.fire({'foo.last': 3.1415})
        self.assertEqual(result, response)
        self.check_request(adapter.request, 'POST', data={'foo.last': 3.1415}, headers={'Authorization': 'Bearer auth-token'})