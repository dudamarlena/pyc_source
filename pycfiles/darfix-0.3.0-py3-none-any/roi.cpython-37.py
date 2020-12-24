# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/garrigaf/Documents/git/darfix/build/lib/darfix/core/roi.py
# Compiled at: 2020-03-03 08:28:12
# Size of source mod 2**32: 4373 bytes
__authors__ = [
 'J. Garriga']
__license__ = 'MIT'
__date__ = '06/12/2019'
import numpy

def apply_2D_ROI(img, origin=None, size=None, center=None):
    """Function that computes a ROI at an image.

    :param array_like img: Image
    :param origin: Origin of the roi
    :param 2d-vector size: [Height, Width] of the roi.
    :param center: Center of the roi
    :type origin: Union[2d vector, None]
    :type center: Union[2d vector, None]
    :returns: ndarray
    :raises: AssertionError, ValueError
    """
    if not size is not None:
        raise AssertionError('The size of the roi must be given')
    else:
        img = numpy.asanyarray(img)
        if origin is not None:
            if not (all((i >= 0 for i in origin)) and all((j < img.shape[i] for i, j in enumerate(origin)))):
                raise AssertionError('Origin must be a valid pixel')
            origin = numpy.array(origin)
            size = numpy.array(size)
            points = numpy.array([origin, origin + size])
        else:
            if center is not None:
                if not (all((i >= 0 for i in center)) and all((j < img.shape[i] for i, j in enumerate(center)))):
                    raise AssertionError('Center must be a valid pixel')
                center = numpy.array(center)
                size = numpy.array(size) * 0.5
                points = numpy.ceil([center - size, center + size]).astype(numpy.int)
                points[points < 0] = 0
                points[1] = numpy.minimum(points[1], img.shape)
            else:
                raise ValueError('Origin or center expected')
    return img[points[(0, 0)]:points[(1, 0)], points[(0, 1)]:points[(1, 1)]]


def apply_3D_ROI(data, origin=None, size=None, center=None):
    """Function that computes the ROI of each image in stack of images.

    :param array_like data: The stack of images
    :param origin: Origin of the roi
    :param 2d-vector size: [Height, Width] of the roi.
    :param center: Center of the roi
    :type origin: Union[2d vector, None]
    :type center: Union[2d vector, None]
    :returns: ndarray
    :raises: AssertionError, ValueError
    """
    if not size is not None:
        raise AssertionError('The size of the roi must be given')
    else:
        data = numpy.asanyarray(data)
        if origin is not None:
            if not (all((i >= 0 for i in origin)) and all((j < data[0].shape[i] for i, j in enumerate(origin)))):
                raise AssertionError('Origin must be a valid pixel')
            origin = numpy.array(origin)
            size = numpy.array(size)
            points = numpy.array([origin, origin + size])
        else:
            if center is not None:
                if not (all((i >= 0 for i in center)) and all((j < data[0].shape[i] for i, j in enumerate(center)))):
                    raise AssertionError('Center must be a valid pixel')
                center = numpy.array(center)
                size = numpy.array(size) * 0.5
                points = numpy.ceil([center - size, center + size]).astype(numpy.int)
                points[points < 0] = 0
                points[1] = numpy.minimum(points[1], data[0].shape)
            else:
                raise ValueError('Origin or center expected')
    return data[:, points[(0, 0)]:points[(1, 0)], points[(0, 1)]:points[(1, 1)]]