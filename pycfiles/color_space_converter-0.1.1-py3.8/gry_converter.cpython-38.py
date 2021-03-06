# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/color_space_converter/gry_converter.py
# Compiled at: 2020-04-19 07:12:08
# Size of source mod 2**32: 5341 bytes
__author__ = 'Christopher Hahne'
__email__ = 'inbox@christopherhahne.de'
__license__ = '\n    Copyright (c) 2020 Christopher Hahne <inbox@christopherhahne.de>\n    This program is free software: you can redistribute it and/or modify\n    it under the terms of the GNU General Public License as published by\n    the Free Software Foundation, either version 3 of the License, or\n    (at your option) any later version.\n    This program is distributed in the hope that it will be useful,\n    but WITHOUT ANY WARRANTY; without even the implied warranty of\n    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\n    GNU General Public License for more details.\n    You should have received a copy of the GNU General Public License\n    along with this program.  If not, see <http://www.gnu.org/licenses/>.\n'
import numpy as np
from color_space_converter.converter_baseclass import ConverterBaseclass
MAT_GRY_HDTV = np.array([0.2126, 0.7152, 0.0722])
MAT_GRY_SDTV = np.array([0.299, 0.587, 0.114])

class GryConverter(ConverterBaseclass):

    def __init__(self, *args, **kwargs):
        (super(GryConverter, self).__init__)(*args, **kwargs)

    def rgb2gry(self, rgb: np.ndarray=None, standard: str='HDTV') -> np.ndarray:
        """ Convert RGB color space to monochromatic color space

        :param rgb: input array in red, green and blue (RGB) space
        :type rgb: :class:`~numpy:numpy.ndarray`
        :param standard: option that determines whether head- and footroom are excluded ('HDTV') or considered otherwise
        :type standard: :class:`string`
        :return: array in monochromatic space
        :rtype: ~numpy:np.ndarray

        """
        self._arr = rgb if rgb is not None else self._arr
        self.orig_shape = self._arr.shape
        self._arr = self._arr.reshape(-1, 3).T
        mat = MAT_GRY_HDTV if standard == 'HDTV' else MAT_GRY_SDTV
        arr = np.dot(mat, self._arr)
        arr = arr.reshape(self.orig_shape[:2] + (1, ))
        return arr

    def gry2ch3(self, gry: np.ndarray=None) -> np.ndarray:
        """ Convert monochromatic color space to 3-channel array

        :param gry: input array in monochromatic space
        :type gry: :class:`~numpy:numpy.ndarray`
        :return: array in red, green and blue (RGB) space
        :rtype: ~numpy:np.ndarray

        """
        self._arr = gry if gry is not None else self._arr
        return np.repeat((self._arr), repeats=3, axis=2)

    def gry_conv(self, img: np.ndarray=None, inverse: bool=False) -> np.ndarray:
        """ Convert RGB color space to monochromatic color space or to 3-channel array given the inverse option.

        :param img: input array in either RGB or monochromatic color space
        :type img: :class:`~numpy:numpy.ndarray`
        :param inverse: option that determines whether conversion is from rgb2gry (False) or gry2ch3 (True)
        :type inverse: :class:`boolean`
        :return: color space converted array
        :rtype: ~numpy:np.ndarray

        """
        self._arr = img if img is not None else self._arr
        self._inv = inverse if inverse else self._inv
        if not self._inv:
            arr = self.rgb2gry(self._arr)
        else:
            arr = self.gry2ch3(self._arr)
        return arr


def rgb2gry(rgb: np.ndarray=None, standard: str='HDTV') -> np.ndarray:
    """ Convert RGB color space to monochromatic color space

    :param rgb: input array in red, green and blue (RGB) space
    :type rgb: :class:`~numpy:numpy.ndarray`
    :param standard: option that determines whether head- and footroom are excluded ('HDTV') or considered otherwise
    :type standard: :class:`string`
    :return: array in monochromatic space
    :rtype: ~numpy:np.ndarray

    """
    shape = rgb.shape
    rgb = rgb.reshape(-1, 3).T
    mat = MAT_GRY_HDTV if standard == 'HDTV' else MAT_GRY_SDTV
    arr = np.dot(mat, rgb)
    arr = arr.reshape(shape[:2] + (1, ))
    return arr


def gry2ch3(gry: np.ndarray=None) -> np.ndarray:
    """ Convert monochromatic color space to 3-channel array

    :param gry: input array in monochromatic space
    :type gry: :class:`~numpy:numpy.ndarray`
    :return: array in red, green and blue (RGB) space
    :rtype: ~numpy:np.ndarray

    """
    return np.repeat(gry, repeats=3, axis=2)


def gry_conv(img: np.ndarray=None, inverse: bool=False) -> np.ndarray:
    """ Convert RGB color space to monochromatic color space or to 3-channel array given the inverse option.

    :param img: input array in either RGB or monochromatic color space
    :type img: :class:`~numpy:numpy.ndarray`
    :param inverse: option that determines whether conversion is from rgb2gry (False) or gry2ch3 (True)
    :type inverse: :class:`boolean`
    :return: color space converted array
    :rtype: ~numpy:np.ndarray

    """
    if not inverse:
        arr = rgb2gry(img)
    else:
        arr = gry2ch3(img)
    return arr