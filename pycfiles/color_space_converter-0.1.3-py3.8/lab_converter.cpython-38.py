# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/color_space_converter/lab_converter.py
# Compiled at: 2020-04-24 19:21:21
# Size of source mod 2**32: 4913 bytes
__author__ = 'Christopher Hahne'
__email__ = 'inbox@christopherhahne.de'
__license__ = '\n    Copyright (c) 2020 Christopher Hahne <inbox@christopherhahne.de>\n    This program is free software: you can redistribute it and/or modify\n    it under the terms of the GNU General Public License as published by\n    the Free Software Foundation, either version 3 of the License, or\n    (at your option) any later version.\n    This program is distributed in the hope that it will be useful,\n    but WITHOUT ANY WARRANTY; without even the implied warranty of\n    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\n    GNU General Public License for more details.\n    You should have received a copy of the GNU General Public License\n    along with this program.  If not, see <http://www.gnu.org/licenses/>.\n'
import numpy as np
from color_space_converter.converter_baseclass import ConverterBaseclass
from color_space_converter.xyz_converter import XyzConverter, rgb2xyz, xyz2rgb
REF_X = 95.047
REF_Y = 100.0
REF_Z = 108.883

class LabConverter(XyzConverter, ConverterBaseclass):

    def __init__(self, *args, **kwargs):
        (super(LabConverter, self).__init__)(*args, **kwargs)

    def lab_conv(self, img: np.ndarray=None, inverse: bool=False) -> np.ndarray:
        """ Convert RGB color space to Lab color space or vice versa given the inverse option.

        :param img: input array in either RGB or Lab color space
        :type img: :class:`~numpy:numpy.ndarray`
        :param inverse: option that determines whether conversion is from rgb2lab (False) or lab2rgb (True)
        :type inverse: :class:`boolean`
        :return: color space converted array
        :rtype: ~numpy:np.ndarray

        """
        self._arr = img if img is not None else self._arr
        self._inv = inverse if inverse else self._inv
        if not self._inv:
            self._arr = rgb2lab(self._arr)
        else:
            self._arr = lab2rgb(self._arr)
        return self._arr


def rgb2lab(rgb: np.ndarray=None) -> np.ndarray:
    """ Convert RGB color space to Lab color space

    :param rgb: input array in red, green and blue (RGB) space
    :type rgb: :class:`~numpy:numpy.ndarray`
    :return: array in Lab space
    :rtype: ~numpy:np.ndarray

    """
    xyz = rgb2xyz(rgb)
    lab = xyz2lab(xyz)
    return lab


def lab2rgb(lab: np.ndarray=None) -> np.ndarray:
    """ Convert Lab color space to RGB color space

    :param lab: input array in Lab space
    :type lab: :class:`~numpy:numpy.ndarray`
    :return: array in red, green and blue (RGB) space
    :rtype: ~numpy:np.ndarray

    """
    xyz = lab2xyz(lab)
    rgb = xyz2rgb(xyz)
    return rgb


def lab_conv(img: np.ndarray=None, inverse: bool=False) -> np.ndarray:
    """ Convert RGB color space to Lab color space or vice versa given the inverse option.

    :param img: input array in either RGB or Lab color space
    :type img: :class:`~numpy:numpy.ndarray`
    :param inverse: option that determines whether conversion is from rgb2lab (False) or lab2rgb (True)
    :type inverse: :class:`boolean`
    :return: color space converted array
    :rtype: ~numpy:np.ndarray

    """
    if not inverse:
        arr = rgb2lab(img)
    else:
        arr = lab2rgb(img)
    return arr


def xyz2lab(xyz: np.ndarray=None) -> np.ndarray:
    """ Convert xyz color space to Lab color space

    :param xyz: input array in xyz space
    :type xyz: :class:`~numpy:numpy.ndarray`
    :return: array in Lab space
    :rtype: ~numpy:np.ndarray

    """
    xyz[(Ellipsis, 0)] /= REF_X
    xyz[(Ellipsis, 1)] /= REF_Y
    xyz[(Ellipsis, 2)] /= REF_Z
    for ch in range(xyz.shape[2]):
        mask = xyz[(..., ch)] > 0.008856
        xyz[(..., ch)][mask] = np.power(xyz[(..., ch)], 0.3333333333333333)[mask]
        xyz[(..., ch)][~mask] = (7.787 * xyz[(..., ch)] + 0.13793103448275862)[(~mask)]
    else:
        lab = np.zeros(xyz.shape)
        lab[(Ellipsis, 0)] = 116 * xyz[(Ellipsis, 1)] - 16
        lab[(Ellipsis, 1)] = 500 * (xyz[(Ellipsis, 0)] - xyz[(Ellipsis, 1)])
        lab[(Ellipsis, 2)] = 200 * (xyz[(Ellipsis, 1)] - xyz[(Ellipsis, 2)])
        return lab


def lab2xyz(lab: np.ndarray=None) -> np.ndarray:
    """ Convert Lab color space to RGB color space

    :param lab: input array in Lab space
    :type lab: :class:`~numpy:numpy.ndarray`
    :return: array in red, green and blue (RGB) space
    :rtype: ~numpy:np.ndarray

    """
    xyz = np.zeros(lab.shape)
    xyz[(Ellipsis, 1)] = (lab[(Ellipsis, 0)] + 16) / 116.0
    xyz[(Ellipsis, 0)] = lab[(Ellipsis, 1)] / 500.0 + xyz[(Ellipsis, 1)]
    xyz[(Ellipsis, 2)] = xyz[(Ellipsis, 1)] - lab[(Ellipsis, 2)] / 200.0
    for ch in range(xyz.shape[2]):
        mask = np.power(xyz[(..., ch)], 3) > 0.008856
        xyz[(..., ch)][mask] = np.power(xyz[(..., ch)], 3)[mask]
        xyz[(..., ch)][~mask] = (xyz[(..., ch)] - 0.13793103448275862)[(~mask)] / 7.787
    else:
        xyz[(Ellipsis, 0)] *= REF_X
        xyz[(Ellipsis, 1)] *= REF_Y
        xyz[(Ellipsis, 2)] *= REF_Z
        return xyz