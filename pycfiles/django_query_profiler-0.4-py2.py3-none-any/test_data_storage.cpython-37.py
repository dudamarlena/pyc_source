# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/yash/Desktop/django-query-profiler/tests/unit/test_data_storage.py
# Compiled at: 2020-01-09 02:51:45
# Size of source mod 2**32: 14559 bytes
from collections import Counter
from typing import Any
from unittest import TestCase
from django_query_profiler.query_profiler_storage import QueryProfiledSummaryData, QueryProfilerLevel, SqlStatement
from django_query_profiler.query_profiler_storage.data_collector import data_collector_thread_local_storage

class DataStorageTest(TestCase):
    __doc__ = '\n    Tests for checking if nesting in context manager works as expected.  Every nested block should return ONLY\n    the data that happened since the start of the block.  These tests are for verifying this.\n    In a way, this test is to make sure that the stack implementation of "data_collector_thread_local_storage" works\n    as it should\n    '
    query_without_params = 'SELECT 1 FROM table where id=%s'
    target_db = 'master'
    query_execution_time_in_micros = 1
    db_row_count = 12

    def setUp(self):
        data_collector_thread_local_storage.reset()

    def test_no_profiler_mode_on(self):
        self._add_query_to_storage(1)
        self._assert_empty_storage()

    def test_enter_and_exit_with_no_queries(self):
        data_collector_thread_local_storage.enter_profiler_mode(QueryProfilerLevel.QUERY_SIGNATURE)
        query_profiled_data = data_collector_thread_local_storage.exit_profiler_mode()
        self._assert_empty_storage()
        self.assertDictEqual(query_profiled_data.query_signature_to_query_signature_statistics, {})
        self.assertCountEqual(query_profiled_data._query_params_db_hash_counter, Counter())

    def test_one_query(self):
        """ When we have just one query executed"""
        data_collector_thread_local_storage.enter_profiler_mode(QueryProfilerLevel.QUERY_SIGNATURE)
        self._add_query_to_storage([1, 2, 3])
        query_profiled_data = data_collector_thread_local_storage.exit_profiler_mode()
        self._assert_empty_storage()
        expected_query_profiled_summary_data = QueryProfiledSummaryData(sql_statement_type_counter=(Counter({SqlStatement.SELECT: 1})),
          exact_query_duplicates=0,
          total_query_execution_time_in_micros=(self.query_execution_time_in_micros),
          total_db_row_count=(self.db_row_count),
          potential_n_plus1_query_count=0)
        self.assertEqual(query_profiled_data.summary, expected_query_profiled_summary_data)
        summary_data_expected_dict = {'exact_query_duplicates':0, 
         'total_query_execution_time_in_micros':1,  'total_db_row_count':12,  'potential_n_plus1_query_count':0, 
         'SELECT':1,  'INSERT':0,  'UPDATE':0,  'DELETE':0,  'TRANSACTIONALS':0, 
         'OTHER':0}
        self.assertDictEqual(query_profiled_data.summary.as_dict(), summary_data_expected_dict)

    def test_two_query_signatures(self):
        """ We have two queries each with different query signatures """
        data_collector_thread_local_storage.enter_profiler_mode(QueryProfilerLevel.QUERY_SIGNATURE)
        self._add_query_to_storage((1, ))
        self._add_query_to_storage((1, ))
        query_profiled_data = data_collector_thread_local_storage.exit_profiler_mode()
        self._assert_empty_storage()
        expected_query_profiled_summary_data = QueryProfiledSummaryData(sql_statement_type_counter=(Counter({SqlStatement.SELECT: 2})),
          exact_query_duplicates=2,
          total_query_execution_time_in_micros=(self.query_execution_time_in_micros * 2),
          total_db_row_count=(self.db_row_count * 2),
          potential_n_plus1_query_count=2)
        self.assertEqual(query_profiled_data.summary, expected_query_profiled_summary_data)
        self.assertEqual(len(query_profiled_data.query_signature_to_query_signature_statistics), 1)

    def test_two_queries_same_query_signature(self):
        """ We  have two queries, and both of them have the same query signature.  We do this by using a loop"""
        data_collector_thread_local_storage.enter_profiler_mode(QueryProfilerLevel.QUERY_SIGNATURE)
        for _ in range(2):
            self._add_query_to_storage((1, ))

        query_profiled_data = data_collector_thread_local_storage.exit_profiler_mode()
        self._assert_empty_storage()
        expected_query_profiled_summary_data = QueryProfiledSummaryData(sql_statement_type_counter=(Counter({SqlStatement.SELECT: 2})),
          exact_query_duplicates=2,
          total_query_execution_time_in_micros=(self.query_execution_time_in_micros * 2),
          total_db_row_count=(self.db_row_count * 2),
          potential_n_plus1_query_count=2)
        self.assertEqual(query_profiled_data.summary, expected_query_profiled_summary_data)
        self.assertEqual(len(query_profiled_data.query_signature_to_query_signature_statistics), 1)

    def test_simple_nested_entry_exit_calls(self):
        """  This is a simulation when it is called from a context manager.  The exit function should return ONLY the
            query profiled data for calls that happened from innermost start

            This is the order of entry-exit in the context manager:
            enter
                1 query
                enter
                    2 queries
                exit -- This should return 2 queries data
            exit -- This should return all queries data

        """
        data_collector_thread_local_storage.enter_profiler_mode(QueryProfilerLevel.QUERY_SIGNATURE)
        self._add_query_to_storage((1, ))
        data_collector_thread_local_storage.enter_profiler_mode(QueryProfilerLevel.QUERY_SIGNATURE)
        self._add_query_to_storage((1, ))
        self._add_query_to_storage((1, ))
        first_exit_query_profiled_data = data_collector_thread_local_storage.exit_profiler_mode()
        self.assertTrue(data_collector_thread_local_storage._query_profiler_enabled)
        self.assertEqual(len(data_collector_thread_local_storage._query_profiled_data_list), 2)
        self.assertListEqual(data_collector_thread_local_storage._entry_index_stack, [0])
        expected_query_profiled_summary_data = QueryProfiledSummaryData(sql_statement_type_counter=(Counter({SqlStatement.SELECT: 2})),
          exact_query_duplicates=2,
          total_query_execution_time_in_micros=(self.query_execution_time_in_micros * 2),
          total_db_row_count=(self.db_row_count * 2),
          potential_n_plus1_query_count=2)
        self.assertEqual(first_exit_query_profiled_data.summary, expected_query_profiled_summary_data)
        second_exit_query_profiled_data = data_collector_thread_local_storage.exit_profiler_mode()
        self._assert_empty_storage()
        expected_query_profiled_summary_data = QueryProfiledSummaryData(sql_statement_type_counter=(Counter({SqlStatement.SELECT: 3})),
          exact_query_duplicates=3,
          total_query_execution_time_in_micros=(self.query_execution_time_in_micros * 3),
          total_db_row_count=(self.db_row_count * 3),
          potential_n_plus1_query_count=3)
        self.assertEqual(second_exit_query_profiled_data.summary, expected_query_profiled_summary_data)

    def test_complex_nested_entry_exit_calls(self):
        """
        This is the order of entry-exit in the context manager:
        entry
            1 sql
            entry
                1 sql
                entry
                    0 sql
                exit --> should return 0 queries data

                entry
                    1 sql
                exit --> should return 1 queries data
            exit --> should return 2 queries data
        exit --> should return all queries data

        """
        data_collector_thread_local_storage.enter_profiler_mode(QueryProfilerLevel.QUERY_SIGNATURE)
        self._add_query_to_storage((1, ))
        data_collector_thread_local_storage.enter_profiler_mode(QueryProfilerLevel.QUERY_SIGNATURE)
        self._add_query_to_storage((1, ))
        data_collector_thread_local_storage.enter_profiler_mode(QueryProfilerLevel.QUERY_SIGNATURE)
        self.assertEqual(len(data_collector_thread_local_storage._query_profiled_data_list), 3)
        self.assertListEqual(data_collector_thread_local_storage._entry_index_stack, [0, 1, 2])
        first_exit_query_profiled_data = data_collector_thread_local_storage.exit_profiler_mode()
        self.assertTrue(data_collector_thread_local_storage._query_profiler_enabled)
        self.assertEqual(len(data_collector_thread_local_storage._query_profiled_data_list), 3)
        self.assertListEqual(data_collector_thread_local_storage._entry_index_stack, [0, 1])
        expected_query_profiled_summary_data = QueryProfiledSummaryData(sql_statement_type_counter=(Counter()),
          exact_query_duplicates=0,
          total_query_execution_time_in_micros=0,
          total_db_row_count=0,
          potential_n_plus1_query_count=0)
        self.assertEqual(first_exit_query_profiled_data.summary, expected_query_profiled_summary_data)
        data_collector_thread_local_storage.enter_profiler_mode(QueryProfilerLevel.QUERY_SIGNATURE)
        self._add_query_to_storage((1, ))
        self.assertListEqual(data_collector_thread_local_storage._entry_index_stack, [0, 1, 3])
        second_exit_query_profiled_data = data_collector_thread_local_storage.exit_profiler_mode()
        self.assertTrue(data_collector_thread_local_storage._query_profiler_enabled)
        self.assertEqual(len(data_collector_thread_local_storage._query_profiled_data_list), 4)
        self.assertListEqual(data_collector_thread_local_storage._entry_index_stack, [0, 1])
        expected_query_profiled_summary_data = QueryProfiledSummaryData(sql_statement_type_counter=(Counter({SqlStatement.SELECT: 1})),
          exact_query_duplicates=0,
          total_query_execution_time_in_micros=(self.query_execution_time_in_micros),
          total_db_row_count=(self.db_row_count),
          potential_n_plus1_query_count=0)
        self.assertEqual(second_exit_query_profiled_data.summary, expected_query_profiled_summary_data)
        self.assertEqual(len(data_collector_thread_local_storage._query_profiled_data_list), 4)
        self.assertListEqual(data_collector_thread_local_storage._entry_index_stack, [0, 1])
        third_exit_query_profiled_data = data_collector_thread_local_storage.exit_profiler_mode()
        self.assertTrue(data_collector_thread_local_storage._query_profiler_enabled)
        self.assertEqual(len(data_collector_thread_local_storage._query_profiled_data_list), 4)
        self.assertListEqual(data_collector_thread_local_storage._entry_index_stack, [0])
        expected_query_profiled_summary_data = QueryProfiledSummaryData(sql_statement_type_counter=(Counter({SqlStatement.SELECT: 2})),
          exact_query_duplicates=2,
          total_query_execution_time_in_micros=(self.query_execution_time_in_micros * 2),
          total_db_row_count=(self.db_row_count * 2),
          potential_n_plus1_query_count=2)
        self.assertEqual(third_exit_query_profiled_data.summary, expected_query_profiled_summary_data)
        self.assertEqual(len(data_collector_thread_local_storage._query_profiled_data_list), 4)
        self.assertListEqual(data_collector_thread_local_storage._entry_index_stack, [0])
        fourth_exit_query_profiled_data = data_collector_thread_local_storage.exit_profiler_mode()
        self.assertFalse(data_collector_thread_local_storage._query_profiler_enabled)
        self.assertEqual(len(data_collector_thread_local_storage._query_profiled_data_list), 0)
        self.assertListEqual(data_collector_thread_local_storage._entry_index_stack, [])
        expected_query_profiled_summary_data = QueryProfiledSummaryData(sql_statement_type_counter=(Counter({SqlStatement.SELECT: 3})),
          exact_query_duplicates=3,
          total_query_execution_time_in_micros=(self.query_execution_time_in_micros * 3),
          total_db_row_count=(self.db_row_count * 3),
          potential_n_plus1_query_count=3)
        self.assertEqual(fourth_exit_query_profiled_data.summary, expected_query_profiled_summary_data)

    def _assert_empty_storage(self) -> None:
        """ This is a helper function for checking if thread local storage is all empty or not"""
        self.assertFalse(data_collector_thread_local_storage._query_profiler_enabled)
        self.assertListEqual(data_collector_thread_local_storage._query_profiled_data_list, [])
        self.assertListEqual(data_collector_thread_local_storage._entry_index_stack, [])

    def _add_query_to_storage(self, params: Any) -> None:
        """
        This function adds one query to the thread local storage.  Note that the stack trace is calculated
        by the function data_collector_thread_local_storage#add_query_profiler_data, and hence if we are
        calling this function from different line numbers - they would have a different stack trace
        """
        data_collector_thread_local_storage.add_query_profiler_data(query_without_params=(self.query_without_params),
          params=params,
          target_db=(self.target_db),
          query_execution_time_in_micros=(self.query_execution_time_in_micros),
          db_row_count=(self.db_row_count))