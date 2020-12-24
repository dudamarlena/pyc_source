# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/svpino/dev/tensorflow-object-detection-sagemaker/todl/tensorflow-object-detection/research/object_detection/core/region_similarity_calculator.py
# Compiled at: 2020-04-05 19:50:57
# Size of source mod 2**32: 5366 bytes
"""Region Similarity Calculators for BoxLists.

Region Similarity Calculators compare a pairwise measure of similarity
between the boxes in two BoxLists.
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from abc import ABCMeta
from abc import abstractmethod
import six, tensorflow as tf
from object_detection.core import box_list_ops
import object_detection.core as fields

class RegionSimilarityCalculator(six.with_metaclass(ABCMeta, object)):
    __doc__ = 'Abstract base class for region similarity calculator.'

    def compare(self, boxlist1, boxlist2, scope=None):
        """Computes matrix of pairwise similarity between BoxLists.

    This op (to be overridden) computes a measure of pairwise similarity between
    the boxes in the given BoxLists. Higher values indicate more similarity.

    Note that this method simply measures similarity and does not explicitly
    perform a matching.

    Args:
      boxlist1: BoxList holding N boxes.
      boxlist2: BoxList holding M boxes.
      scope: Op scope name. Defaults to 'Compare' if None.

    Returns:
      a (float32) tensor of shape [N, M] with pairwise similarity score.
    """
        with tf.name_scope(scope, 'Compare', [boxlist1, boxlist2]) as (scope):
            return self._compare(boxlist1, boxlist2)

    @abstractmethod
    def _compare(self, boxlist1, boxlist2):
        pass


class IouSimilarity(RegionSimilarityCalculator):
    __doc__ = 'Class to compute similarity based on Intersection over Union (IOU) metric.\n\n  This class computes pairwise similarity between two BoxLists based on IOU.\n  '

    def _compare(self, boxlist1, boxlist2):
        """Compute pairwise IOU similarity between the two BoxLists.

    Args:
      boxlist1: BoxList holding N boxes.
      boxlist2: BoxList holding M boxes.

    Returns:
      A tensor with shape [N, M] representing pairwise iou scores.
    """
        return box_list_ops.iou(boxlist1, boxlist2)


class NegSqDistSimilarity(RegionSimilarityCalculator):
    __doc__ = 'Class to compute similarity based on the squared distance metric.\n\n  This class computes pairwise similarity between two BoxLists based on the\n  negative squared distance metric.\n  '

    def _compare(self, boxlist1, boxlist2):
        """Compute matrix of (negated) sq distances.

    Args:
      boxlist1: BoxList holding N boxes.
      boxlist2: BoxList holding M boxes.

    Returns:
      A tensor with shape [N, M] representing negated pairwise squared distance.
    """
        return -1 * box_list_ops.sq_dist(boxlist1, boxlist2)


class IoaSimilarity(RegionSimilarityCalculator):
    __doc__ = 'Class to compute similarity based on Intersection over Area (IOA) metric.\n\n  This class computes pairwise similarity between two BoxLists based on their\n  pairwise intersections divided by the areas of second BoxLists.\n  '

    def _compare(self, boxlist1, boxlist2):
        """Compute pairwise IOA similarity between the two BoxLists.

    Args:
      boxlist1: BoxList holding N boxes.
      boxlist2: BoxList holding M boxes.

    Returns:
      A tensor with shape [N, M] representing pairwise IOA scores.
    """
        return box_list_ops.ioa(boxlist1, boxlist2)


class ThresholdedIouSimilarity(RegionSimilarityCalculator):
    __doc__ = "Class to compute similarity based on thresholded IOU and score.\n\n  This class computes pairwise similarity between two BoxLists based on IOU and\n  a 'score' present in boxlist1. If IOU > threshold, then the entry in the\n  output pairwise tensor will contain `score`, otherwise 0.\n  "

    def __init__(self, iou_threshold=0):
        """Initialize the ThresholdedIouSimilarity.

    Args:
      iou_threshold: For a given pair of boxes, if the IOU is > iou_threshold,
        then the comparison result will be the foreground probability of
        the first box, otherwise it will be zero.
    """
        super(ThresholdedIouSimilarity, self).__init__()
        self._iou_threshold = iou_threshold

    def _compare(self, boxlist1, boxlist2):
        """Compute pairwise IOU similarity between the two BoxLists and score.

    Args:
      boxlist1: BoxList holding N boxes. Must have a score field.
      boxlist2: BoxList holding M boxes.

    Returns:
      A tensor with shape [N, M] representing scores threholded by pairwise
      iou scores.
    """
        ious = box_list_ops.iou(boxlist1, boxlist2)
        scores = boxlist1.get_field(fields.BoxListFields.scores)
        scores = tf.expand_dims(scores, axis=1)
        row_replicated_scores = tf.tile(scores, [1, tf.shape(ious)[(-1)]])
        thresholded_ious = tf.where(ious > self._iou_threshold, row_replicated_scores, tf.zeros_like(ious))
        return thresholded_ious