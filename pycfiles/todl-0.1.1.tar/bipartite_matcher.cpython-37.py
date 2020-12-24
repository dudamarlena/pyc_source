# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/svpino/dev/tensorflow-object-detection-sagemaker/todl/tensorflow-object-detection/research/object_detection/matchers/bipartite_matcher.py
# Compiled at: 2020-04-05 19:50:57
# Size of source mod 2**32: 2824 bytes
"""Bipartite matcher implementation."""
import tensorflow as tf
from tensorflow.contrib.image.python.ops import image_ops
from object_detection.core import matcher

class GreedyBipartiteMatcher(matcher.Matcher):
    __doc__ = 'Wraps a Tensorflow greedy bipartite matcher.'

    def __init__(self, use_matmul_gather=False):
        """Constructs a Matcher.

    Args:
      use_matmul_gather: Force constructed match objects to use matrix
        multiplication based gather instead of standard tf.gather.
        (Default: False).
    """
        super(GreedyBipartiteMatcher, self).__init__(use_matmul_gather=use_matmul_gather)

    def _match(self, similarity_matrix, valid_rows):
        """Bipartite matches a collection rows and columns. A greedy bi-partite.

    TODO(rathodv): Add num_valid_columns options to match only that many columns
    with all the rows.

    Args:
      similarity_matrix: Float tensor of shape [N, M] with pairwise similarity
        where higher values mean more similar.
      valid_rows: A boolean tensor of shape [N] indicating the rows that are
        valid.

    Returns:
      match_results: int32 tensor of shape [M] with match_results[i]=-1
        meaning that column i is not matched and otherwise that it is matched to
        row match_results[i].
    """
        valid_row_sim_matrix = tf.gather(similarity_matrix, tf.squeeze((tf.where(valid_rows)), axis=(-1)))
        invalid_row_sim_matrix = tf.gather(similarity_matrix, tf.squeeze((tf.where(tf.logical_not(valid_rows))), axis=(-1)))
        similarity_matrix = tf.concat([
         valid_row_sim_matrix, invalid_row_sim_matrix],
          axis=0)
        distance_matrix = -1 * similarity_matrix
        num_valid_rows = tf.reduce_sum(tf.cast(valid_rows, dtype=(tf.float32)))
        _, match_results = image_ops.bipartite_match(distance_matrix,
          num_valid_rows=num_valid_rows)
        match_results = tf.reshape(match_results, [-1])
        match_results = tf.cast(match_results, tf.int32)
        return match_results