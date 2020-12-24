# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/color_space_converter/hsv_converter.py
# Compiled at: 2020-04-19 07:12:08
# Size of source mod 2**32: 7438 bytes
__author__ = 'Christopher Hahne'
__email__ = 'inbox@christopherhahne.de'
__license__ = '\n    Copyright (c) 2020 Christopher Hahne <inbox@christopherhahne.de>\n    This program is free software: you can redistribute it and/or modify\n    it under the terms of the GNU General Public License as published by\n    the Free Software Foundation, either version 3 of the License, or\n    (at your option) any later version.\n    This program is distributed in the hope that it will be useful,\n    but WITHOUT ANY WARRANTY; without even the implied warranty of\n    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\n    GNU General Public License for more details.\n    You should have received a copy of the GNU General Public License\n    along with this program.  If not, see <http://www.gnu.org/licenses/>.\n'
import numpy as np
from color_space_converter.converter_baseclass import ConverterBaseclass

class HsvConverter(ConverterBaseclass):

    def __init__(self, *args, **kwargs):
        (super(HsvConverter, self).__init__)(*args, **kwargs)

    def rgb2hsv(self, rgb: np.ndarray=None) -> np.ndarray:
        """ Convert RGB color space to HSV color space

        :param rgb: input array in red, green and blue (RGB) space
        :type rgb: :class:`~numpy:numpy.ndarray`
        :return: array in hue, saturation and value (HSV) space
        :rtype: ~numpy:np.ndarray

        """
        self._arr = rgb if rgb is not None else self._arr
        self._arr = self._arr.astype('float')
        maxv = np.amax((self._arr), axis=2)
        maxc = np.argmax((self._arr), axis=2)
        minv = np.amin((self._arr), axis=2)
        minc = np.argmin((self._arr), axis=2)
        hsv = np.zeros((self._arr.shape), dtype='float')
        hsv[(maxc == minc, 0)] = np.zeros(hsv[(maxc == minc, 0)].shape)
        hsv[(maxc == 0, 0)] = ((self._arr[(Ellipsis, 1)] - self._arr[(Ellipsis, 2)]) * 60.0 / (maxv - minv + np.spacing(1)) % 360.0)[(maxc == 0)]
        hsv[(maxc == 1, 0)] = ((self._arr[(Ellipsis, 2)] - self._arr[(Ellipsis, 0)]) * 60.0 / (maxv - minv + np.spacing(1)) + 120.0)[(maxc == 1)]
        hsv[(maxc == 2, 0)] = ((self._arr[(Ellipsis, 0)] - self._arr[(Ellipsis, 1)]) * 60.0 / (maxv - minv + np.spacing(1)) + 240.0)[(maxc == 2)]
        hsv[(maxv == 0, 1)] = np.zeros(hsv[(maxv == 0, 1)].shape)
        hsv[(maxv != 0, 1)] = (1 - minv / (maxv + np.spacing(1)))[(maxv != 0)]
        hsv[(Ellipsis, 2)] = maxv
        return hsv

    def hsv2rgb(self, hsv: np.ndarray=None) -> np.ndarray:
        """ Convert HSV color space to RGB color space

        :param hsv: input array in hue, saturation and value (HSV) space
        :type hsv: :class:`~numpy:numpy.ndarray`
        :return: array in red, green and blue (RGB) space
        :rtype: ~numpy:np.ndarray

        """
        self._arr = hsv if hsv is not None else self._arr
        hi = np.floor(self._arr[(Ellipsis, 0)] / 60.0) % 6
        hi = hi.astype('uint8')
        v = self._arr[(Ellipsis, 2)].astype('float')
        f = self._arr[(Ellipsis, 0)] / 60.0 - np.floor(self._arr[(Ellipsis, 0)] / 60.0)
        p = v * (1.0 - self._arr[(Ellipsis, 1)])
        q = v * (1.0 - f * self._arr[(Ellipsis, 1)])
        t = v * (1.0 - (1.0 - f) * self._arr[(Ellipsis, 1)])
        rgb = np.zeros(self._arr.shape)
        rgb[hi == 0, :] = np.dstack((v, t, p))[hi == 0, :]
        rgb[hi == 1, :] = np.dstack((q, v, p))[hi == 1, :]
        rgb[hi == 2, :] = np.dstack((p, v, t))[hi == 2, :]
        rgb[hi == 3, :] = np.dstack((p, q, v))[hi == 3, :]
        rgb[hi == 4, :] = np.dstack((t, p, v))[hi == 4, :]
        rgb[hi == 5, :] = np.dstack((v, p, q))[hi == 5, :]
        return rgb

    def hsv_conv(self, img: np.ndarray=None, inverse: bool=False) -> np.ndarray:
        """ Convert RGB color space to HSV color space or vice versa given the inverse option.

        :param img: input array in either RGB or HSV color space
        :type img: :class:`~numpy:numpy.ndarray`
        :param inverse: option that determines whether conversion is from rgb2hsv (False) or hsv2rgb (True)
        :type inverse: :class:`boolean`
        :return: color space converted array
        :rtype: ~numpy:np.ndarray

        """
        self._arr = img if img is not None else self._arr
        self._inv = inverse if inverse else self._inv
        if not self._inv:
            arr = self.rgb2hsv(self._arr)
        else:
            arr = self.hsv2rgb(self._arr)
        return arr


def rgb2hsv(rgb: np.ndarray=None) -> np.ndarray:
    """ Convert RGB color space to HSV color space

    :param rgb: input array in red, green and blue (RGB) space
    :type rgb: :class:`~numpy:numpy.ndarray`
    :return: array in hue, saturation and value (HSV) space
    :rtype: ~numpy:np.ndarray

    """
    rgb = rgb.astype('float')
    maxv = np.amax(rgb, axis=2)
    maxc = np.argmax(rgb, axis=2)
    minv = np.amin(rgb, axis=2)
    minc = np.argmin(rgb, axis=2)
    hsv = np.zeros((rgb.shape), dtype='float')
    hsv[(maxc == minc, 0)] = np.zeros(hsv[(maxc == minc, 0)].shape)
    hsv[(maxc == 0, 0)] = ((rgb[(Ellipsis, 1)] - rgb[(Ellipsis, 2)]) * 60.0 / (maxv - minv + np.spacing(1)) % 360.0)[(maxc == 0)]
    hsv[(maxc == 1, 0)] = ((rgb[(Ellipsis, 2)] - rgb[(Ellipsis, 0)]) * 60.0 / (maxv - minv + np.spacing(1)) + 120.0)[(maxc == 1)]
    hsv[(maxc == 2, 0)] = ((rgb[(Ellipsis, 0)] - rgb[(Ellipsis, 1)]) * 60.0 / (maxv - minv + np.spacing(1)) + 240.0)[(maxc == 2)]
    hsv[(maxv == 0, 1)] = np.zeros(hsv[(maxv == 0, 1)].shape)
    hsv[(maxv != 0, 1)] = (1 - minv / (maxv + np.spacing(1)))[(maxv != 0)]
    hsv[(Ellipsis, 2)] = maxv
    return hsv


def hsv2rgb(hsv: np.ndarray=None) -> np.ndarray:
    """ Convert HSV color space to RGB color space

    :param hsv: input array in hue, saturation and value (HSV) space
    :type hsv: :class:`~numpy:numpy.ndarray`
    :return: array in red, green and blue (RGB) space
    :rtype: ~numpy:np.ndarray

    """
    hi = np.floor(hsv[(Ellipsis, 0)] / 60.0) % 6
    hi = hi.astype('uint8')
    v = hsv[(Ellipsis, 2)].astype('float')
    f = hsv[(Ellipsis, 0)] / 60.0 - np.floor(hsv[(Ellipsis, 0)] / 60.0)
    p = v * (1.0 - hsv[(Ellipsis, 1)])
    q = v * (1.0 - f * hsv[(Ellipsis, 1)])
    t = v * (1.0 - (1.0 - f) * hsv[(Ellipsis, 1)])
    rgb = np.zeros(hsv.shape)
    rgb[hi == 0, :] = np.dstack((v, t, p))[hi == 0, :]
    rgb[hi == 1, :] = np.dstack((q, v, p))[hi == 1, :]
    rgb[hi == 2, :] = np.dstack((p, v, t))[hi == 2, :]
    rgb[hi == 3, :] = np.dstack((p, q, v))[hi == 3, :]
    rgb[hi == 4, :] = np.dstack((t, p, v))[hi == 4, :]
    rgb[hi == 5, :] = np.dstack((v, p, q))[hi == 5, :]
    return rgb


def hsv_conv(img: np.ndarray=None, inverse: bool=False) -> np.ndarray:
    """ Convert RGB color space to HSV color space or vice versa given the inverse option.

    :param img: input array in either RGB or HSV color space
    :type img: :class:`~numpy:numpy.ndarray`
    :param inverse: option that determines whether conversion is from rgb2hsv (False) or hsv2rgb (True)
    :type inverse: :class:`boolean`
    :return: color space converted array
    :rtype: ~numpy:np.ndarray

    """
    if not inverse:
        arr = rgb2hsv(img)
    else:
        arr = hsv2rgb(img)
    return arr