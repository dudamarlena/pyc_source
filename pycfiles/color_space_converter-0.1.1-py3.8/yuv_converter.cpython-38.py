# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/color_space_converter/yuv_converter.py
# Compiled at: 2020-04-19 07:12:08
# Size of source mod 2**32: 7093 bytes
__author__ = 'Christopher Hahne'
__email__ = 'inbox@christopherhahne.de'
__license__ = '\n    Copyright (c) 2020 Christopher Hahne <inbox@christopherhahne.de>\n    This program is free software: you can redistribute it and/or modify\n    it under the terms of the GNU General Public License as published by\n    the Free Software Foundation, either version 3 of the License, or\n    (at your option) any later version.\n    This program is distributed in the hope that it will be useful,\n    but WITHOUT ANY WARRANTY; without even the implied warranty of\n    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\n    GNU General Public License for more details.\n    You should have received a copy of the GNU General Public License\n    along with this program.  If not, see <http://www.gnu.org/licenses/>.\n'
import numpy as np
from color_space_converter.converter_baseclass import ConverterBaseclass
YUV_MAT_BT709 = np.array([[0.2126, 0.7152, 0.0722], [-0.09991, -0.33609, 0.436], [0.615, -0.55861, -0.05639]])
YUV_MAT_BT709_INV = np.array([[1.0, 0.0, 1.28033], [1.0, -0.21482, -0.38059], [1.0, 2.12798, 0.0]])
YUV_MAT_BT601 = np.array([[0.299, 0.587, 0.114], [-0.14713, -0.28886, 0.436], [0.615, -0.51499, -0.10001]])
YUV_MAT_BT601_INV = np.array([[1.0, 0.0, 1.13983], [1.0, -0.39465, -0.5806], [1.0, 2.03211, 0.0]])

class YuvConverter(ConverterBaseclass):

    def __init__(self, *args, **kwargs):
        (super(YuvConverter, self).__init__)(*args, **kwargs)

    def rgb2yuv(self, rgb: np.ndarray=None, standard: str='HDTV') -> np.ndarray:
        """ Convert RGB color space to YUV color space

        :param rgb: input array in red, green and blue (RGB) space
        :type rgb: :class:`~numpy:numpy.ndarray`
        :param standard: option that determines whether head- and footroom are excluded ('HDTV') or considered otherwise
        :type standard: :class:`string`
        :return: array in YUV space
        :rtype: ~numpy:np.ndarray

        """
        self._arr = rgb if rgb is not None else self._arr
        self.orig_shape = self._arr.shape
        yuv_mat = YUV_MAT_BT709 if standard == 'HDTV' else YUV_MAT_BT601
        self._arr = self._arr.reshape(-1, 3).T
        yuv = np.dot(yuv_mat, self._arr)
        yuv = yuv.T.reshape(self.orig_shape)
        return yuv

    def yuv2rgb(self, yuv: np.ndarray=None, standard: str='HDTV') -> np.ndarray:
        """ Convert YUV color space to RGB color space

        :param yuv: input array in red, green and blue (RGB) space
        :type yuv: :class:`~numpy:numpy.ndarray`
        :param standard: option that determines whether head- and footroom are excluded ('HDTV') or considered otherwise
        :type standard: :class:`string`
        :return: array in red, green and blue (RGB) space
        :rtype: ~numpy:np.ndarray

        """
        self._arr = yuv if yuv is not None else self._arr
        self.orig_shape = self._arr.shape
        yuv_mat = YUV_MAT_BT709_INV if standard == 'HDTV' else YUV_MAT_BT601_INV
        self._arr = self._arr.reshape(-1, 3).T
        yuv = np.dot(yuv_mat, self._arr)
        yuv = yuv.T.reshape(self.orig_shape)
        return yuv

    def yuv_conv(self, img: np.ndarray=None, inverse: bool=False, standard: str='HDTV') -> np.ndarray:
        """ Convert YUV color space to RGB color space or vice versa given the inverse option.

        :param img: input array in either RGB or YUV color space
        :type img: :class:`~numpy:numpy.ndarray`
        :param inverse: option that determines whether conversion is from rgb2yuv (False) or yuv2rgb (True)
        :type inverse: :class:`boolean`
        :param standard: option that determines whether head- and footroom are excluded ('HDTV') or considered otherwise
        :type standard: :class:`string`
        :return: color space converted array
        :rtype: ~numpy:np.ndarray

        """
        self._arr = img if img is not None else self._arr
        self._inv = inverse if inverse else self._inv
        if not self._inv:
            arr = self.rgb2yuv(rgb=(self._arr), standard=standard)
        else:
            arr = self.yuv2rgb(yuv=(self._arr), standard=standard)
        return arr


def yuv2rgb(yuv: np.ndarray=None, standard: str='HDTV') -> np.ndarray:
    """ Convert YUV color space to RGB color space

    :param yuv: input array in red, green and blue (RGB) space
    :type yuv: :class:`~numpy:numpy.ndarray`
    :param standard: option that determines whether head- and footroom are excluded ('HDTV') or considered otherwise
    :type standard: :class:`string`
    :return: array in red, green and blue (RGB) space
    :rtype: ~numpy:np.ndarray

    """
    shape = yuv.shape
    yuv_mat = YUV_MAT_BT709_INV if standard == 'HDTV' else YUV_MAT_BT601_INV
    yuv = yuv.reshape(-1, 3).T
    yuv = np.dot(yuv_mat, yuv)
    yuv = yuv.T.reshape(shape)
    return yuv


def rgb2yuv(rgb: np.ndarray=None, standard: str='HDTV') -> np.ndarray:
    """ Convert RGB color space to YUV color space

    :param rgb: input array in red, green and blue (RGB) space
    :type rgb: :class:`~numpy:numpy.ndarray`
    :param standard: option that determines whether head- and footroom are excluded ('HDTV') or considered otherwise
    :type standard: :class:`string`
    :return: array in YUV space
    :rtype: ~numpy:np.ndarray

    """
    shape = rgb.shape
    yuv_mat = YUV_MAT_BT709 if standard == 'HDTV' else YUV_MAT_BT601
    rgb = rgb.reshape(-1, 3).T
    yuv = np.dot(yuv_mat, rgb)
    yuv = yuv.T.reshape(shape)
    return yuv


def yuv_conv(img: np.ndarray=None, inverse: bool=False, standard: str='HDTV') -> np.ndarray:
    """ Convert YUV color space to RGB color space or vice versa given the inverse option.

    :param img: input array in either RGB or YUV color space
    :type img: :class:`~numpy:numpy.ndarray`
    :param inverse: option that determines whether conversion is from rgb2yuv (False) or yuv2rgb (True)
    :type inverse: :class:`boolean`
    :param standard: option that determines whether head- and footroom are excluded ('HDTV') or considered otherwise
    :type standard: :class:`string`
    :return: color space converted array
    :rtype: ~numpy:np.ndarray

    """
    if not inverse:
        arr = rgb2yuv(rgb=img, standard=standard)
    else:
        arr = yuv2rgb(yuv=img, standard=standard)
    return arr