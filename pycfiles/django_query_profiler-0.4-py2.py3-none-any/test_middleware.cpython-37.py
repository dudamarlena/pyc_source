# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/yash/Desktop/django-query-profiler/tests/integration/test_middleware.py
# Compiled at: 2020-01-07 01:36:58
# Size of source mod 2**32: 7672 bytes
import json, re
from typing import Dict
from unittest.mock import patch
from django.http import HttpResponse
from django.test import TestCase, override_settings
from tests.testapp.food.models import Topping
from django_query_profiler.chrome_plugin_helpers import ChromePluginData, redis_utils
from django_query_profiler.chrome_plugin_helpers.views import get_query_profiled_data
from django_query_profiler.client.middleware import DETAILED_VIEW_EXCEPTION_LINK_TEXT, DETAILED_VIEW_EXCEPTION_URL
from django_query_profiler.query_profiler_storage import QueryProfilerLevel, SqlStatement

class QueryProfilerMiddlewareTest(TestCase):

    def setUp(self):
        Topping.objects.create(name='jalapenos', is_spicy=True)

    @patch('django_query_profiler.client.middleware.redis_utils')
    def test_headers_with_redis_call_successful(self, mock_redis_utils: redis_utils):
        mock_redis_utils.store_data.return_value = 'mock'
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get(ChromePluginData.QUERY_PROFILER_DETAILED_VIEW_LINK_TEXT), QueryProfilerLevel.QUERY_SIGNATURE.name.lower())
        url_pattern = 'http://.*/django_query_profiler/mock/' + QueryProfilerLevel.QUERY_SIGNATURE.name
        detailed_url = response.get(ChromePluginData.QUERY_PROFILED_DETAILED_URL)
        self.assertEqual(re.match(url_pattern, detailed_url).start(), 0)
        self.assertTrue(response.has_header(ChromePluginData.TIME_SPENT_PROFILING_IN_MICROS))
        self.assertTrue(response.has_header(ChromePluginData.TOTAL_SERVER_TIME_IN_MILLIS))
        summary_data = json.loads(response.get(ChromePluginData.QUERY_PROFILED_SUMMARY_DATA))
        self.assertEqual(summary_data['exact_query_duplicates'], 4)
        self.assertEqual(summary_data[SqlStatement.SELECT.name], 5)
        self.assertEqual(summary_data[SqlStatement.INSERT.name], 0)
        self.assertEqual(summary_data[SqlStatement.UPDATE.name], 0)
        self.assertEqual(summary_data[SqlStatement.DELETE.name], 0)

    @patch('django_query_profiler.client.middleware.redis_utils')
    @override_settings(DJANGO_QUERY_PROFILER_IGNORE_DETAILED_VIEW_EXCEPTION=False)
    def test_headers_with_redis_throws_exception_ignore_detailed_view_exception_false(self, mock_redis_utils: redis_utils):
        mock_redis_utils.store_data.side_effect = Exception('redis not setup')
        with self.assertRaises(Exception) as (context):
            self.client.get('/')
        self.assertTrue('redis not setup' in str(context.exception))

    @patch('django_query_profiler.client.middleware.redis_utils')
    def test_headers_with_redis_throws_exception_ignore_detailed_view_exception_true(self, mock_redis_utils: redis_utils):
        mock_redis_utils.store_data.side_effect = Exception('redis not setup')
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get(ChromePluginData.QUERY_PROFILER_DETAILED_VIEW_LINK_TEXT), DETAILED_VIEW_EXCEPTION_LINK_TEXT)
        url_pattern = DETAILED_VIEW_EXCEPTION_URL
        detailed_url = response.get(ChromePluginData.QUERY_PROFILED_DETAILED_URL)
        self.assertEqual(re.match(url_pattern, detailed_url).start(), 0)
        self.assertTrue(response.has_header(ChromePluginData.TIME_SPENT_PROFILING_IN_MICROS))
        self.assertTrue(response.has_header(ChromePluginData.TOTAL_SERVER_TIME_IN_MILLIS))
        summary_data = json.loads(response.get(ChromePluginData.QUERY_PROFILED_SUMMARY_DATA))
        self.assertEqual(summary_data['exact_query_duplicates'], 4)
        self.assertEqual(summary_data[SqlStatement.SELECT.name], 5)
        self.assertEqual(summary_data[SqlStatement.INSERT.name], 0)
        self.assertEqual(summary_data[SqlStatement.UPDATE.name], 0)
        self.assertEqual(summary_data[SqlStatement.DELETE.name], 0)

    @patch('django_query_profiler.chrome_plugin_helpers.views.redis_utils')
    @patch('django_query_profiler.client.middleware.redis_utils')
    def test_detailed_view_url_from_header_call_successful_query_signature_level(self, mock_redis_utils_store_data: redis_utils, mock_redis_utils_retrieve_data: redis_utils):
        mock_redis_utils_store_data.store_data.return_value = 'mock'
        response_index_view = self.client.get('/')
        query_profiler_detailed_view_url = response_index_view.get(ChromePluginData.QUERY_PROFILED_DETAILED_URL)
        self.assertTrue(QueryProfilerLevel.QUERY_SIGNATURE.name in query_profiler_detailed_view_url)
        args_to_redis_store_data = mock_redis_utils_store_data.store_data.call_args[0][0]
        mock_redis_utils_retrieve_data.retrieve_data.return_value = args_to_redis_store_data
        response_detailed_url = self.client.get(query_profiler_detailed_view_url)
        self.assertEqual(response_detailed_url.resolver_match.url_name, get_query_profiled_data.__name__)
        self.assertContains(response_detailed_url, '<th>5</th>')
        self.assertContains(response_detailed_url, '<th>4</th>')
        self.assertContains(response_detailed_url, 'flamegraphStack')

    @patch('django_query_profiler.chrome_plugin_helpers.views.redis_utils')
    @patch('django_query_profiler.client.middleware.redis_utils')
    @override_settings(DJANGO_QUERY_PROFILER_LEVEL_FUNC=(lambda _: QueryProfilerLevel.QUERY))
    def test_detailed_view_url_from_header_call_successful_query_level(self, mock_redis_utils_store_data: redis_utils, mock_redis_utils_retrieve_data: redis_utils):
        mock_redis_utils_store_data.store_data.return_value = 'mock'
        response_index_view = self.client.get('/')
        query_profiler_detailed_view_url = response_index_view.get(ChromePluginData.QUERY_PROFILED_DETAILED_URL)
        self.assertTrue(QueryProfilerLevel.QUERY.name in query_profiler_detailed_view_url)
        args_to_redis_store_data = mock_redis_utils_store_data.store_data.call_args[0][0]
        mock_redis_utils_retrieve_data.retrieve_data.return_value = args_to_redis_store_data
        response_detailed_url = self.client.get(query_profiler_detailed_view_url)
        self.assertEqual(response_detailed_url.resolver_match.url_name, get_query_profiled_data.__name__)
        self.assertContains(response_detailed_url, '<th>5</th>')
        self.assertContains(response_detailed_url, '<th>4</th>')
        self.assertNotContains(response_detailed_url, 'flamegraphStack')

    @override_settings(DJANGO_QUERY_PROFILER_LEVEL_FUNC=(lambda _: None))
    @patch('django_query_profiler.client.middleware.redis_utils')
    def test_index_view_with_none_profiler_level(self, mock_redis_utils: redis_utils):
        response_index_view = self.client.get('/')
        self.assertIsNone(response_index_view.get(ChromePluginData.QUERY_PROFILED_DETAILED_URL))
        self.assertFalse(mock_redis_utils.called)