# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/nn_wtf/images_labels_data_set.py
# Compiled at: 2016-12-17 04:58:38
from nn_wtf.data_set_base import DataSetBase
import numpy
__author__ = 'Lene Preuss <lene.preuss@gmail.com>'

class ImagesLabelsDataSet(DataSetBase):

    def __init__(self, images, labels):
        """Construct a DataSet.

        Args:
          images: 4D numpy.ndarray of shape (num images, image height, image width, image depth)
          labels: 1D numpy.ndarray of shape (num images)
        """
        _check_constructor_arguments_valid(images, labels)
        super().__init__(images, labels)
        images = images.reshape(images.shape[0], images.shape[1] * images.shape[2])
        images = normalize(images)
        self._input = images


def normalize(ndarray):
    """Transform a ndarray that contains uint8 values to floats between 0. and 1.

    :param ndarray:
    :return:
    """
    assert isinstance(ndarray, numpy.ndarray)
    assert ndarray.dtype == numpy.uint8
    return numpy.multiply(ndarray.astype(numpy.float32), 1.0 / 255.0)


def invert(ndarray):
    assert isinstance(ndarray, numpy.ndarray)
    assert ndarray.dtype == numpy.float32
    return numpy.subtract(1.0, ndarray)


def _check_constructor_arguments_valid(images, labels):
    assert len(images.shape) == 4, 'images must have 4 dimensions: number of images, image height, image width, color depth'
    assert images.shape[3] == 1, 'image depth must be 1'