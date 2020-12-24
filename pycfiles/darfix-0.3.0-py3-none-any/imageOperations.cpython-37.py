# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/garrigaf/Documents/git/darfix/build/lib/darfix/core/imageOperations.py
# Compiled at: 2020-03-03 09:45:08
# Size of source mod 2**32: 6083 bytes
__authors__ = [
 'J. Garriga']
__license__ = 'MIT'
__date__ = '29/11/2019'
import numpy, silx.math
from enum import Enum

class Method(Enum):
    __doc__ = '\n    Methods available to compute the background.\n    '
    mean = 'mean'
    median = 'median'

    @staticmethod
    def values():
        return list(map(lambda c: c.value, Method))


def background_subtraction(data, bg_frames, method='median'):
    """Function that computes the median between a series of dark images from a dataset
    and substracts it to each frame of the raw data to remove the noise.

    :param ndarray data: The raw data
    :param array_like dark_frames: List of dark frames
    :param method: Method used to determine the background image.
    :type method: Union['mean', 'median', None]
    :returns: ndarray
    :raises: ValueError
    """
    if not bg_frames is not None:
        raise AssertionError('Background frames must be given')
    else:
        background = numpy.zeros(data[0].shape, data.dtype)
        if len(bg_frames):
            if method == 'mean':
                numpy.mean(bg_frames, out=background, axis=0)
            else:
                if method == 'median':
                    numpy.median(bg_frames, out=background, axis=0)
                else:
                    raise ValueError('Invalid method specified. Please use `mean`, or `median`.')
    new_data = numpy.subtract(data, background, dtype=(numpy.int64))
    new_data[new_data < 0] = 0
    return new_data.astype(data.dtype)


def _create_circular_mask(shape, center=None, radius=None):
    """
    Function that given a height and a width returns a circular mask image.

    :param int h: Height
    :param int w: Width
    :param center: Center of the circle
    :type center: Union[[int, int], None]
    :param radius: Radius of the circle
    :type radius: Union[int, None]
    :returns: ndarray
    """
    h, w = shape
    if center is None:
        center = [
         int(h / 2), int(w / 2)]
    if radius is None:
        radius = min(center[0], center[1], h - center[0], w - center[1])
    X, Y = numpy.ogrid[:h, :w]
    dist_from_center = numpy.sqrt((X - center[0]) ** 2 + (Y - center[1]) ** 2)
    mask = dist_from_center <= radius
    return mask


def _create_n_sphere_mask(shape, center=None, radius=None):
    """
    Function that given a list of dimensions returns a n-dimensional sphere mask.

    :param shape: Dimensions of the mask
    :type shape: array_like
    :param center: Center of the sphere
    :type center: Union[array_like, None]
    :param radius: Radius of the sphere
    :type radius: Union[int, None]
    :returns: ndarray
    """
    if not shape:
        assert radius, 'If dimensions are not entered radius must be given'
    dimensions = numpy.array(shape)
    if center is None:
        center = (dimensions / 2).astype(int)
    if radius is None:
        radius = min(numpy.concatenate([center, dimensions - center]))
    C = numpy.ogrid[[slice(0, dim) for dim in dimensions]]
    dist_from_center = numpy.sqrt(numpy.sum((C - center) ** 2))
    mask = dist_from_center <= radius
    return mask


def hot_pixel_removal(data, ksize=3):
    """
    Function to remove hot pixels of the data using median filter.

    :param array_like data: Input data.
    :param str mask: Radius of the cylinder.
    :param int ksize: Size of the mask to apply.
    :returns: ndarray
    """
    corrected_data = numpy.empty((data.shape), dtype=(data.dtype))
    for i, frame in enumerate(data):
        if frame.dtype == numpy.int or frame.dtype == numpy.uint:
            frame = frame.astype(numpy.int16)
        else:
            if frame.dtype == numpy.float:
                frame = frame.astype(numpy.float32)
        corrected_frame = numpy.array(frame)
        median = silx.math.medfilt(frame, ksize)
        hot_pixels = numpy.subtract(frame, median, dtype=(numpy.int64))
        threshold = numpy.std(hot_pixels)
        corrected_frame[hot_pixels > threshold] = median[(hot_pixels > threshold)]
        corrected_data[i] = corrected_frame

    return corrected_data


def threshold_removal(data, bottom=None, top=None):
    """
    Set bottom and top threshold to the images in the dataset.

    :param Dataset dataset: Dataset with the data
    :param int bottom: Bottom threshold
    :param int top: Top threshold
    :returns: ndarray
    """
    frames = []
    for frame in data:
        median = numpy.median(frame)
        if bottom is not None:
            frame[frame < bottom] = median
        if top is not None:
            frame[frame > top] = median
        frames.append(frame)

    return numpy.asarray(frames)