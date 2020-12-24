# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/svpino/dev/tensorflow-object-detection-sagemaker/todl/tensorflow-object-detection/research/object_detection/utils/np_box_list.py
# Compiled at: 2020-04-05 19:50:58
# Size of source mod 2**32: 4656 bytes
"""Numpy BoxList classes and functions."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import numpy as np
from six.moves import range

class BoxList(object):
    __doc__ = 'Box collection.\n\n  BoxList represents a list of bounding boxes as numpy array, where each\n  bounding box is represented as a row of 4 numbers,\n  [y_min, x_min, y_max, x_max].  It is assumed that all bounding boxes within a\n  given list correspond to a single image.\n\n  Optionally, users can add additional related fields (such as\n  objectness/classification scores).\n  '

    def __init__(self, data):
        """Constructs box collection.

    Args:
      data: a numpy array of shape [N, 4] representing box coordinates

    Raises:
      ValueError: if bbox data is not a numpy array
      ValueError: if invalid dimensions for bbox data
    """
        if not isinstance(data, np.ndarray):
            raise ValueError('data must be a numpy array.')
        else:
            if len(data.shape) != 2 or data.shape[1] != 4:
                raise ValueError('Invalid dimensions for box data.')
            if data.dtype != np.float32:
                if data.dtype != np.float64:
                    raise ValueError('Invalid data type for box data: float is required.')
            assert self._is_valid_boxes(data), 'Invalid box data. data must be a numpy array of N*[y_min, x_min, y_max, x_max]'
        self.data = {'boxes': data}

    def num_boxes(self):
        """Return number of boxes held in collections."""
        return self.data['boxes'].shape[0]

    def get_extra_fields(self):
        """Return all non-box fields."""
        return [k for k in self.data.keys() if k != 'boxes']

    def has_field(self, field):
        return field in self.data

    def add_field(self, field, field_data):
        """Add data to a specified field.

    Args:
      field: a string parameter used to speficy a related field to be accessed.
      field_data: a numpy array of [N, ...] representing the data associated
          with the field.
    Raises:
      ValueError: if the field is already exist or the dimension of the field
          data does not matches the number of boxes.
    """
        if self.has_field(field):
            raise ValueError('Field ' + field + 'already exists')
        if len(field_data.shape) < 1 or field_data.shape[0] != self.num_boxes():
            raise ValueError('Invalid dimensions for field data')
        self.data[field] = field_data

    def get(self):
        """Convenience function for accesssing box coordinates.

    Returns:
      a numpy array of shape [N, 4] representing box corners
    """
        return self.get_field('boxes')

    def get_field(self, field):
        """Accesses data associated with the specified field in the box collection.

    Args:
      field: a string parameter used to speficy a related field to be accessed.

    Returns:
      a numpy 1-d array representing data of an associated field

    Raises:
      ValueError: if invalid field
    """
        if not self.has_field(field):
            raise ValueError('field {} does not exist'.format(field))
        return self.data[field]

    def get_coordinates(self):
        """Get corner coordinates of boxes.

    Returns:
     a list of 4 1-d numpy arrays [y_min, x_min, y_max, x_max]
    """
        box_coordinates = self.get()
        y_min = box_coordinates[:, 0]
        x_min = box_coordinates[:, 1]
        y_max = box_coordinates[:, 2]
        x_max = box_coordinates[:, 3]
        return [y_min, x_min, y_max, x_max]

    def _is_valid_boxes(self, data):
        """Check whether data fullfills the format of N*[ymin, xmin, ymax, xmin].

    Args:
      data: a numpy array of shape [N, 4] representing box coordinates

    Returns:
      a boolean indicating whether all ymax of boxes are equal or greater than
          ymin, and all xmax of boxes are equal or greater than xmin.
    """
        if data.shape[0] > 0:
            for i in range(data.shape[0]):
                if data[(i, 0)] > data[(i, 2)] or data[(i, 1)] > data[(i, 3)]:
                    return False

        return True