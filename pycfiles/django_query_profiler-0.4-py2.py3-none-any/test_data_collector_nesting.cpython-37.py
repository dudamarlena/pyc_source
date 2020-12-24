# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/yash/Desktop/django-query-profiler/tests/integration/test_data_collector_nesting.py
# Compiled at: 2020-01-09 23:55:49
# Size of source mod 2**32: 9055 bytes
from unittest import TestCase
from tests.testapp.food.models import Pizza
from django_query_profiler.client.context_manager import QueryProfiler
from django_query_profiler.query_profiler_storage import QueryProfilerLevel
from django_query_profiler.query_profiler_storage.data_collector import data_collector_thread_local_storage
from .fixtures import bulk_create_toppings_pizzas_restaurants

class QueryProfilerQueryAndQuerySignatureTest(TestCase):
    __doc__ = '\n    This class contains tests where we would be calling QueryProfiler - with Query and QuerySignature.  We want to\n    test if intermingling of Query and QuerySignature in a nested setting does not lead to problems\n    '

    @classmethod
    def setUpClass(cls):
        bulk_create_toppings_pizzas_restaurants()

    def test_query_signature_followed_by_query(self):
        """ This is the simplest case where one is followed by other, and hence there is no overlapping """
        with QueryProfiler(QueryProfilerLevel.QUERY_SIGNATURE) as (qp_query_signature):
            str(Pizza.objects.all())
            self.assertEqual(data_collector_thread_local_storage._current_query_profiler_level, QueryProfilerLevel.QUERY_SIGNATURE)
        self.assertIsNone(data_collector_thread_local_storage._current_query_profiler_level)
        with QueryProfiler(QueryProfilerLevel.QUERY) as (qp_query):
            str(Pizza.objects.all())
            self.assertEqual(data_collector_thread_local_storage._current_query_profiler_level, QueryProfilerLevel.QUERY)
        self.assertIsNone(data_collector_thread_local_storage._current_query_profiler_level)
        self.assertEqual(qp_query_signature.query_profiled_data.summary.total_query_count, 4)
        self.assertIsNotNone(qp_query_signature.query_profiled_data.summary.potential_n_plus1_query_count)
        self.assertIsNone(qp_query.query_profiled_data.summary.potential_n_plus1_query_count)
        self.assertTrue(qp_query.query_profiled_data.summary.total_query_count, 4)

    def test_query_followed_by_query_signature(self):
        """ This is the simplest case where one is followed by other, and hence there is no overlapping """
        with QueryProfiler(QueryProfilerLevel.QUERY) as (qp_query):
            str(Pizza.objects.all())
            self.assertEqual(data_collector_thread_local_storage._current_query_profiler_level, QueryProfilerLevel.QUERY)
        self.assertIsNone(data_collector_thread_local_storage._current_query_profiler_level)
        with QueryProfiler(QueryProfilerLevel.QUERY_SIGNATURE) as (qp_query_signature):
            str(Pizza.objects.all())
            self.assertEqual(data_collector_thread_local_storage._current_query_profiler_level, QueryProfilerLevel.QUERY_SIGNATURE)
        self.assertIsNone(data_collector_thread_local_storage._current_query_profiler_level)
        self.assertIsNotNone(qp_query_signature.query_profiled_data.summary.potential_n_plus1_query_count)
        self.assertIsNone(qp_query.query_profiled_data.summary.potential_n_plus1_query_count)
        self.assertEqual(qp_query_signature.query_profiled_data.summary.total_query_count, 4)
        self.assertTrue(qp_query.query_profiled_data.summary.total_query_count, 4)

    def test_query_nested_by_another_query(self):
        with QueryProfiler(QueryProfilerLevel.QUERY) as (qp_query):
            str(Pizza.objects.all())
            self.assertEqual(data_collector_thread_local_storage._current_query_profiler_level, QueryProfilerLevel.QUERY)
            with QueryProfiler(QueryProfilerLevel.QUERY) as (qp_query_nested):
                str(Pizza.objects.all())
                self.assertEqual(data_collector_thread_local_storage._current_query_profiler_level, QueryProfilerLevel.QUERY)
            self.assertEqual(data_collector_thread_local_storage._current_query_profiler_level, QueryProfilerLevel.QUERY)
        self.assertIsNone(qp_query_nested.query_profiled_data.summary.potential_n_plus1_query_count)
        self.assertIsNotNone(str(data_collector_thread_local_storage))

    def test_query_nesting_query_signature_one_level(self):
        """ We call query_signature inside the profiler with Query type """
        with QueryProfiler(QueryProfilerLevel.QUERY) as (qp_query):
            str(Pizza.objects.all())
            self.assertEqual(data_collector_thread_local_storage._current_query_profiler_level, QueryProfilerLevel.QUERY)
            with QueryProfiler(QueryProfilerLevel.QUERY_SIGNATURE) as (qp_query_signature):
                str(Pizza.objects.all())
                self.assertEqual(data_collector_thread_local_storage._current_query_profiler_level, QueryProfilerLevel.QUERY_SIGNATURE)
            self.assertEqual(data_collector_thread_local_storage._current_query_profiler_level, QueryProfilerLevel.QUERY)
        self.assertIsNone(data_collector_thread_local_storage._current_query_profiler_level)
        self.assertIsNotNone(qp_query_signature.query_profiled_data.summary.potential_n_plus1_query_count)
        self.assertIsNone(qp_query.query_profiled_data.summary.potential_n_plus1_query_count)
        self.assertEqual(qp_query_signature.query_profiled_data.summary.total_query_count, 4)
        self.assertTrue(qp_query.query_profiled_data.summary.total_query_count, 8)

    def test_query_signature_nesting_query_one_level(self):
        """ We call query inside the profiler with query_signature type """
        with QueryProfiler(QueryProfilerLevel.QUERY_SIGNATURE) as (qp_query_signature):
            str(Pizza.objects.all())
            self.assertEqual(data_collector_thread_local_storage._current_query_profiler_level, QueryProfilerLevel.QUERY_SIGNATURE)
            with QueryProfiler(QueryProfilerLevel.QUERY) as (qp_query):
                str(Pizza.objects.all())
                self.assertEqual(data_collector_thread_local_storage._current_query_profiler_level, QueryProfilerLevel.QUERY_SIGNATURE)
            self.assertEqual(data_collector_thread_local_storage._current_query_profiler_level, QueryProfilerLevel.QUERY_SIGNATURE)
        self.assertIsNone(data_collector_thread_local_storage._current_query_profiler_level)
        self.assertIsNotNone(qp_query_signature.query_profiled_data.summary.potential_n_plus1_query_count)
        self.assertIsNotNone(qp_query.query_profiled_data.summary.potential_n_plus1_query_count)
        self.assertTrue(qp_query.query_profiled_data.summary.total_query_count, 4)
        self.assertEqual(qp_query_signature.query_profiled_data.summary.total_query_count, 8)

    def test_complex_nesting(self):
        with QueryProfiler(QueryProfilerLevel.QUERY_SIGNATURE) as (qp_query_signature_1):
            str(Pizza.objects.all())
            self.assertEqual(data_collector_thread_local_storage._current_query_profiler_level, QueryProfilerLevel.QUERY_SIGNATURE)
            with QueryProfiler(QueryProfilerLevel.QUERY) as (qp_query_1):
                str(Pizza.objects.all())
                self.assertEqual(data_collector_thread_local_storage._current_query_profiler_level, QueryProfilerLevel.QUERY_SIGNATURE)
            self.assertEqual(data_collector_thread_local_storage._current_query_profiler_level, QueryProfilerLevel.QUERY_SIGNATURE)
            with QueryProfiler(QueryProfilerLevel.QUERY) as (qp_query_2):
                str(Pizza.objects.all())
                self.assertEqual(data_collector_thread_local_storage._current_query_profiler_level, QueryProfilerLevel.QUERY_SIGNATURE)
                with QueryProfiler(QueryProfilerLevel.QUERY_SIGNATURE) as (_):
                    str(Pizza.objects.all())
                    self.assertEqual(data_collector_thread_local_storage._current_query_profiler_level, QueryProfilerLevel.QUERY_SIGNATURE)
            self.assertEqual(data_collector_thread_local_storage._current_query_profiler_level, QueryProfilerLevel.QUERY_SIGNATURE)
        self.assertIsNone(data_collector_thread_local_storage._current_query_profiler_level)
        self.assertIsNotNone(qp_query_signature_1.query_profiled_data.summary.potential_n_plus1_query_count)
        self.assertEqual(qp_query_signature_1.query_profiled_data.summary.total_query_count, 16)
        self.assertIsNotNone(qp_query_1.query_profiled_data.summary.potential_n_plus1_query_count)
        self.assertTrue(qp_query_1.query_profiled_data.summary.total_query_count, 4)
        self.assertIsNotNone(qp_query_2.query_profiled_data.summary.potential_n_plus1_query_count)
        self.assertTrue(qp_query_2.query_profiled_data.summary.total_query_count, 4)