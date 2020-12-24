# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/object_detection/matchers/bipartite_matcher_test.py
# Compiled at: 2018-06-15 01:39:54
# Size of source mod 2**32: 2929 bytes
"""Tests for object_detection.core.bipartite_matcher."""
import tensorflow as tf
from object_detection.matchers import bipartite_matcher

class GreedyBipartiteMatcherTest(tf.test.TestCase):

    def test_get_expected_matches_when_all_rows_are_valid(self):
        similarity_matrix = tf.constant([[0.5, 0.1, 0.8], [0.15, 0.2, 0.3]])
        num_valid_rows = 2
        expected_match_results = [-1, 1, 0]
        matcher = bipartite_matcher.GreedyBipartiteMatcher()
        match = matcher.match(similarity_matrix, num_valid_rows=num_valid_rows)
        with self.test_session() as (sess):
            match_results_out = sess.run(match._match_results)
            self.assertAllEqual(match_results_out, expected_match_results)

    def test_get_expected_matches_with_valid_rows_set_to_minus_one(self):
        similarity_matrix = tf.constant([[0.5, 0.1, 0.8], [0.15, 0.2, 0.3]])
        num_valid_rows = -1
        expected_match_results = [-1, 1, 0]
        matcher = bipartite_matcher.GreedyBipartiteMatcher()
        match = matcher.match(similarity_matrix, num_valid_rows=num_valid_rows)
        with self.test_session() as (sess):
            match_results_out = sess.run(match._match_results)
            self.assertAllEqual(match_results_out, expected_match_results)

    def test_get_no_matches_with_zero_valid_rows(self):
        similarity_matrix = tf.constant([[0.5, 0.1, 0.8], [0.15, 0.2, 0.3]])
        num_valid_rows = 0
        expected_match_results = [-1, -1, -1]
        matcher = bipartite_matcher.GreedyBipartiteMatcher()
        match = matcher.match(similarity_matrix, num_valid_rows=num_valid_rows)
        with self.test_session() as (sess):
            match_results_out = sess.run(match._match_results)
            self.assertAllEqual(match_results_out, expected_match_results)

    def test_get_expected_matches_with_only_one_valid_row(self):
        similarity_matrix = tf.constant([[0.5, 0.1, 0.8], [0.15, 0.2, 0.3]])
        num_valid_rows = 1
        expected_match_results = [-1, -1, 0]
        matcher = bipartite_matcher.GreedyBipartiteMatcher()
        match = matcher.match(similarity_matrix, num_valid_rows=num_valid_rows)
        with self.test_session() as (sess):
            match_results_out = sess.run(match._match_results)
            self.assertAllEqual(match_results_out, expected_match_results)


if __name__ == '__main__':
    tf.test.main()