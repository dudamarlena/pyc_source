# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/object_detection/matchers/bipartite_matcher.py
# Compiled at: 2018-06-15 01:39:54
# Size of source mod 2**32: 2176 bytes
"""Bipartite matcher implementation."""
import tensorflow as tf
from tensorflow.contrib.image.python.ops import image_ops
from object_detection.core import matcher

class GreedyBipartiteMatcher(matcher.Matcher):
    __doc__ = 'Wraps a Tensorflow greedy bipartite matcher.'

    def _match(self, similarity_matrix, num_valid_rows=-1):
        """Bipartite matches a collection rows and columns. A greedy bi-partite.

    TODO: Add num_valid_columns options to match only that many columns with
        all the rows.

    Args:
      similarity_matrix: Float tensor of shape [N, M] with pairwise similarity
        where higher values mean more similar.
      num_valid_rows: A scalar or a 1-D tensor with one element describing the
        number of valid rows of similarity_matrix to consider for the bipartite
        matching. If set to be negative, then all rows from similarity_matrix
        are used.

    Returns:
      match_results: int32 tensor of shape [M] with match_results[i]=-1
        meaning that column i is not matched and otherwise that it is matched to
        row match_results[i].
    """
        distance_matrix = -1 * similarity_matrix
        _, match_results = image_ops.bipartite_match(distance_matrix, num_valid_rows)
        match_results = tf.reshape(match_results, [-1])
        match_results = tf.cast(match_results, tf.int32)
        return match_results