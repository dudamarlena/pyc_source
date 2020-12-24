# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/svpino/dev/tensorflow-object-detection-sagemaker/todl/tensorflow-object-detection/research/object_detection/utils/np_box_mask_list.py
# Compiled at: 2020-04-05 19:50:58
# Size of source mod 2**32: 2541 bytes
"""Numpy BoxMaskList classes and functions."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import numpy as np
from object_detection.utils import np_box_list

class BoxMaskList(np_box_list.BoxList):
    __doc__ = 'Convenience wrapper for BoxList with masks.\n\n  BoxMaskList extends the np_box_list.BoxList to contain masks as well.\n  In particular, its constructor receives both boxes and masks. Note that the\n  masks correspond to the full image.\n  '

    def __init__(self, box_data, mask_data):
        super(BoxMaskList, self).__init__(box_data)
        if not isinstance(mask_data, np.ndarray):
            raise ValueError('Mask data must be a numpy array.')
        if len(mask_data.shape) != 3:
            raise ValueError('Invalid dimensions for mask data.')
        if mask_data.dtype != np.uint8:
            raise ValueError('Invalid data type for mask data: uint8 is required.')
        if mask_data.shape[0] != box_data.shape[0]:
            raise ValueError('There should be the same number of boxes and masks.')
        self.data['masks'] = mask_data

    def get_masks(self):
        """Convenience function for accessing masks.

    Returns:
      a numpy array of shape [N, height, width] representing masks
    """
        return self.get_field('masks')