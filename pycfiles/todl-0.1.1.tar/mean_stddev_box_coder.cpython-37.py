# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/svpino/dev/tensorflow-object-detection-sagemaker/todl/tensorflow-object-detection/research/object_detection/box_coders/mean_stddev_box_coder.py
# Compiled at: 2020-04-05 19:50:57
# Size of source mod 2**32: 2592 bytes
"""Mean stddev box coder.

This box coder use the following coding schema to encode boxes:
rel_code = (box_corner - anchor_corner_mean) / anchor_corner_stddev.
"""
from object_detection.core import box_coder
from object_detection.core import box_list

class MeanStddevBoxCoder(box_coder.BoxCoder):
    __doc__ = 'Mean stddev box coder.'

    def __init__(self, stddev=0.01):
        """Constructor for MeanStddevBoxCoder.

    Args:
      stddev: The standard deviation used to encode and decode boxes.
    """
        self._stddev = stddev

    @property
    def code_size(self):
        return 4

    def _encode(self, boxes, anchors):
        """Encode a box collection with respect to anchor collection.

    Args:
      boxes: BoxList holding N boxes to be encoded.
      anchors: BoxList of N anchors.

    Returns:
      a tensor representing N anchor-encoded boxes

    Raises:
      ValueError: if the anchors still have deprecated stddev field.
    """
        box_corners = boxes.get()
        if anchors.has_field('stddev'):
            raise ValueError("'stddev' is a parameter of MeanStddevBoxCoder and should not be specified in the box list.")
        means = anchors.get()
        return (box_corners - means) / self._stddev

    def _decode(self, rel_codes, anchors):
        """Decode.

    Args:
      rel_codes: a tensor representing N anchor-encoded boxes.
      anchors: BoxList of anchors.

    Returns:
      boxes: BoxList holding N bounding boxes

    Raises:
      ValueError: if the anchors still have deprecated stddev field and expects
        the decode method to use stddev value from that field.
    """
        means = anchors.get()
        if anchors.has_field('stddev'):
            raise ValueError("'stddev' is a parameter of MeanStddevBoxCoder and should not be specified in the box list.")
        box_corners = rel_codes * self._stddev + means
        return box_list.BoxList(box_corners)