# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/object_detection/box_coders/faster_rcnn_box_coder.py
# Compiled at: 2018-06-15 01:39:54
# Size of source mod 2**32: 3837 bytes
"""Faster RCNN box coder.

Faster RCNN box coder follows the coding schema described below:
  ty = (y - ya) / ha
  tx = (x - xa) / wa
  th = log(h / ha)
  tw = log(w / wa)
  where x, y, w, h denote the box's center coordinates, width and height
  respectively. Similarly, xa, ya, wa, ha denote the anchor's center
  coordinates, width and height. tx, ty, tw and th denote the anchor-encoded
  center, width and height respectively.

  See http://arxiv.org/abs/1506.01497 for details.
"""
import tensorflow as tf
from object_detection.core import box_coder
from object_detection.core import box_list
EPSILON = 1e-08

class FasterRcnnBoxCoder(box_coder.BoxCoder):
    __doc__ = 'Faster RCNN box coder.'

    def __init__(self, scale_factors=None):
        """Constructor for FasterRcnnBoxCoder.

    Args:
      scale_factors: List of 4 positive scalars to scale ty, tx, th and tw.
        If set to None, does not perform scaling. For Faster RCNN,
        the open-source implementation recommends using [10.0, 10.0, 5.0, 5.0].
    """
        if scale_factors:
            assert len(scale_factors) == 4
            for scalar in scale_factors:
                if not scalar > 0:
                    raise AssertionError

        self._scale_factors = scale_factors

    @property
    def code_size(self):
        return 4

    def _encode(self, boxes, anchors):
        """Encode a box collection with respect to anchor collection.

    Args:
      boxes: BoxList holding N boxes to be encoded.
      anchors: BoxList of anchors.

    Returns:
      a tensor representing N anchor-encoded boxes of the format
      [ty, tx, th, tw].
    """
        ycenter_a, xcenter_a, ha, wa = anchors.get_center_coordinates_and_sizes()
        ycenter, xcenter, h, w = boxes.get_center_coordinates_and_sizes()
        ha += EPSILON
        wa += EPSILON
        h += EPSILON
        w += EPSILON
        tx = (xcenter - xcenter_a) / wa
        ty = (ycenter - ycenter_a) / ha
        tw = tf.log(w / wa)
        th = tf.log(h / ha)
        if self._scale_factors:
            ty *= self._scale_factors[0]
            tx *= self._scale_factors[1]
            th *= self._scale_factors[2]
            tw *= self._scale_factors[3]
        return tf.transpose(tf.stack([ty, tx, th, tw]))

    def _decode(self, rel_codes, anchors):
        """Decode relative codes to boxes.

    Args:
      rel_codes: a tensor representing N anchor-encoded boxes.
      anchors: BoxList of anchors.

    Returns:
      boxes: BoxList holding N bounding boxes.
    """
        ycenter_a, xcenter_a, ha, wa = anchors.get_center_coordinates_and_sizes()
        ty, tx, th, tw = tf.unstack(tf.transpose(rel_codes))
        if self._scale_factors:
            ty /= self._scale_factors[0]
            tx /= self._scale_factors[1]
            th /= self._scale_factors[2]
            tw /= self._scale_factors[3]
        w = tf.exp(tw) * wa
        h = tf.exp(th) * ha
        ycenter = ty * ha + ycenter_a
        xcenter = tx * wa + xcenter_a
        ymin = ycenter - h / 2.0
        xmin = xcenter - w / 2.0
        ymax = ycenter + h / 2.0
        xmax = xcenter + w / 2.0
        return box_list.BoxList(tf.transpose(tf.stack([ymin, xmin, ymax, xmax])))