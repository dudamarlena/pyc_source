# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/yash/Desktop/django-query-profiler/tests/integration/test_django_stack_trace_analyze.py
# Compiled at: 2020-01-09 23:35:03
# Size of source mod 2**32: 12614 bytes
from django.db.models import Prefetch
from django.test import TestCase
from tests.integration.fixtures import bulk_create_toppings_pizzas_restaurants
from tests.testapp.food.models import Pizza, Restaurant
from django_query_profiler.client.context_manager import QueryProfiler
from django_query_profiler.query_profiler_storage import QueryProfilerLevel, QuerySignatureAnalyzeResult

def run_twice_with_debug_toggled(test_func):
    """
    This decorator runs the same test twice - one with DEBUG=True, and one with DEBUG=False
    We want to do that because Django has two cursorWrapper - CursorWrapper and CursorDebugWrapper, and it
    chooses the one based on the settings DEBUG attribute
    """

    def wrapper(*args, **kwargs):
        self = args[0]
        for debug in (True, False):
            with self.subTest():
                with self.settings(DEBUG=debug):
                    return test_func(*args, **kwargs)

    return wrapper


class QueryProfilerCodeSuggestions(TestCase):

    def setUp(self):
        bulk_create_toppings_pizzas_restaurants()

    @run_twice_with_debug_toggled
    def test_missing_prefetch(self):
        pizzas = Pizza.objects.all()
        with QueryProfiler(QueryProfilerLevel.QUERY_SIGNATURE) as (qp_pizzas_without_prefetch):
            for pizza in pizzas:
                str(pizza)

        query_signature_to_query_signature_statistics = qp_pizzas_without_prefetch.query_profiled_data.query_signature_to_query_signature_statistics
        self.assertEqual(len(query_signature_to_query_signature_statistics), 2)
        checked_for_table_pizza = checked_for_table_toppings = False
        for query_signature, query_signature_statistics in query_signature_to_query_signature_statistics.items():
            if query_signature_statistics.frequency == 1:
                self.assertEqual(query_signature.analysis, QuerySignatureAnalyzeResult.UNKNOWN)
                checked_for_table_pizza = True

        self.assertTrue(checked_for_table_pizza)
        self.assertTrue(checked_for_table_toppings)

    @run_twice_with_debug_toggled
    def test_after_applying_prefetch(self):
        pizzas = Pizza.objects.prefetch_related('toppings').all()
        with QueryProfiler(QueryProfilerLevel.QUERY_SIGNATURE) as (qp_pizzas_with_prefetch):
            for pizza in pizzas:
                str(pizza)

        query_signature_to_query_signature_statistics = qp_pizzas_with_prefetch.query_profiled_data.query_signature_to_query_signature_statistics
        self.assertEqual(len(query_signature_to_query_signature_statistics), 2)
        frequencies = {query_signature_statistics.frequency for query_signature_statistics in query_signature_to_query_signature_statistics.values()}
        query_signature_analysis = {query_signature.analysis for query_signature in query_signature_to_query_signature_statistics.keys()}
        self.assertSetEqual(frequencies, {1})
        self.assertSetEqual(query_signature_analysis, {QuerySignatureAnalyzeResult.UNKNOWN,
         QuerySignatureAnalyzeResult.PREFETCHED_RELATED})

    @run_twice_with_debug_toggled
    def test_spicy_toppings_db_filtering(self):
        """ Test to verify that no amount of prefetching would help if we do db filtering"""
        pizzas = Pizza.objects.all()
        with QueryProfiler(QueryProfilerLevel.QUERY_SIGNATURE) as (qp_pizzas_without_prefetch):
            for pizza in pizzas:
                pizza.spicy_toppings_db_filtering()

        query_signature_to_query_signature_statistics = qp_pizzas_without_prefetch.query_profiled_data.query_signature_to_query_signature_statistics
        self.assertEqual(len(query_signature_to_query_signature_statistics), 2)
        checked_for_table_pizza = checked_for_table_toppings = False
        for query_signature, query_signature_statistics in query_signature_to_query_signature_statistics.items():
            if query_signature_statistics.frequency == 1:
                self.assertEqual(query_signature.analysis, QuerySignatureAnalyzeResult.UNKNOWN)
                checked_for_table_pizza = True

        self.assertTrue(checked_for_table_pizza)
        self.assertTrue(checked_for_table_toppings)
        pizzas = Pizza.objects.prefetch_related('toppings').all()
        with QueryProfiler(QueryProfilerLevel.QUERY_SIGNATURE) as (qp_pizzas_wit_prefetch):
            for pizza in pizzas:
                pizza.spicy_toppings_db_filtering()

        query_signature_to_query_signature_statistics = qp_pizzas_wit_prefetch.query_profiled_data.query_signature_to_query_signature_statistics
        self.assertEqual(len(query_signature_to_query_signature_statistics), 3)
        frequencies = [query_signature_statistics.frequency for query_signature_statistics in query_signature_to_query_signature_statistics.values()]
        query_signature_analysis = {query_signature.analysis for query_signature in query_signature_to_query_signature_statistics.keys()}
        self.assertListEqual(frequencies, [1, 1, 3])
        self.assertSetEqual(query_signature_analysis, {QuerySignatureAnalyzeResult.FILTER,
         QuerySignatureAnalyzeResult.PREFETCHED_RELATED,
         QuerySignatureAnalyzeResult.UNKNOWN})

    @run_twice_with_debug_toggled
    def test_spicy_toppings_python_filtering(self):
        """ Test to verify that if filtering is done in python, we have a chance to optimize """
        pizzas = Pizza.objects.all()
        with QueryProfiler(QueryProfilerLevel.QUERY_SIGNATURE) as (qp_pizzas_without_prefetch):
            for pizza in pizzas:
                pizza.spicy_toppings_python_filtering()

        query_signature_to_query_signature_statistics = qp_pizzas_without_prefetch.query_profiled_data.query_signature_to_query_signature_statistics
        self.assertEqual(len(query_signature_to_query_signature_statistics), 2)
        checked_for_table_pizza = checked_for_table_toppings = False
        for query_signature, query_signature_statistics in query_signature_to_query_signature_statistics.items():
            if query_signature_statistics.frequency == 1:
                self.assertEqual(query_signature.analysis, QuerySignatureAnalyzeResult.UNKNOWN)
                checked_for_table_pizza = True

        self.assertTrue(checked_for_table_pizza)
        self.assertTrue(checked_for_table_toppings)
        pizzas = Pizza.objects.prefetch_related('toppings').all()
        with QueryProfiler(QueryProfilerLevel.QUERY_SIGNATURE) as (qp_pizzas_wit_prefetch):
            for pizza in pizzas:
                pizza.spicy_toppings_python_filtering()

        query_signature_to_query_signature_statistics = qp_pizzas_wit_prefetch.query_profiled_data.query_signature_to_query_signature_statistics
        self.assertEqual(len(query_signature_to_query_signature_statistics), 2)
        frequencies = [query_signature_statistics.frequency for query_signature_statistics in query_signature_to_query_signature_statistics.values()]
        query_signature_analysis = {query_signature.analysis for query_signature in query_signature_to_query_signature_statistics.keys()}
        self.assertListEqual(frequencies, [1, 1])
        self.assertSetEqual(query_signature_analysis, {QuerySignatureAnalyzeResult.UNKNOWN,
         QuerySignatureAnalyzeResult.PREFETCHED_RELATED})

    @run_twice_with_debug_toggled
    def test_missing_select_related(self):
        """
        This function tests various select_related and prefetch_related on the function
        food.models.py#toppings_of_best_pizza_serving_restaurants
        """
        pizza = Pizza.objects.first()
        with QueryProfiler(QueryProfilerLevel.QUERY_SIGNATURE) as (qp_no_prefetch_select_related):
            str(pizza.toppings_of_best_pizza_serving_restaurants())
        query_signature_to_query_signature_statistics = qp_no_prefetch_select_related.query_profiled_data.query_signature_to_query_signature_statistics
        query_signature_analysis = [query_signature.analysis for query_signature in query_signature_to_query_signature_statistics.keys()]
        expected_query_signature_analysis = [
         QuerySignatureAnalyzeResult.MISSING_PREFETCH_RELATED,
         QuerySignatureAnalyzeResult.MISSING_SELECT_RELATED,
         QuerySignatureAnalyzeResult.MISSING_PREFETCH_RELATED]
        self.assertListEqual(query_signature_analysis, expected_query_signature_analysis)
        pizza = Pizza.objects.prefetch_related('restaurants').first()
        with QueryProfiler(QueryProfilerLevel.QUERY_SIGNATURE) as (qp_no_select_related):
            str(pizza.toppings_of_best_pizza_serving_restaurants())
        query_signature_to_query_signature_statistics = qp_no_select_related.query_profiled_data.query_signature_to_query_signature_statistics
        query_signature_analysis = [query_signature.analysis for query_signature in query_signature_to_query_signature_statistics.keys()]
        expected_query_signature_analysis = [
         QuerySignatureAnalyzeResult.MISSING_SELECT_RELATED,
         QuerySignatureAnalyzeResult.MISSING_PREFETCH_RELATED]
        self.assertListEqual(query_signature_analysis, expected_query_signature_analysis)
        pizza = Pizza.objects.prefetch_related(Prefetch('restaurants', queryset=(Restaurant.objects.select_related('best_pizza')))).first()
        with QueryProfiler(QueryProfilerLevel.QUERY_SIGNATURE) as (qp_no_select_related):
            str(pizza.toppings_of_best_pizza_serving_restaurants())
        query_signature_to_query_signature_statistics = qp_no_select_related.query_profiled_data.query_signature_to_query_signature_statistics
        query_signature_analysis = [query_signature.analysis for query_signature in query_signature_to_query_signature_statistics.keys()]
        expected_query_signature_analysis = [
         QuerySignatureAnalyzeResult.MISSING_PREFETCH_RELATED]
        self.assertListEqual(query_signature_analysis, expected_query_signature_analysis)