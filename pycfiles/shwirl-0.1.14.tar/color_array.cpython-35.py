# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/danyvohl/code/shwirl/extern/vispy/color/color_array.py
# Compiled at: 2017-04-05 22:12:59
# Size of source mod 2**32: 14225 bytes
from __future__ import division
import numpy as np
from copy import deepcopy
from ..ext.six import string_types
from ..util import logger
from ._color_dict import _color_dict
from .color_space import _hex_to_rgba, _rgb_to_hex, _rgb_to_hsv, _hsv_to_rgb, _rgb_to_lab, _lab_to_rgb

def _string_to_rgb(color):
    """Convert user string or hex color to color array (length 3 or 4)"""
    if not color.startswith('#'):
        if color.lower() not in _color_dict:
            raise ValueError('Color "%s" unknown' % color)
        color = _color_dict[color]
        assert color[0] == '#'
        color = color[1:]
        lc = len(color)
        if lc in (3, 4):
            color = ''.join(c + c for c in color)
            lc = len(color)
        if lc not in (6, 8):
            raise ValueError('Hex color must have exactly six or eight elements following the # sign')
        color = np.array([int(color[i:i + 2], 16) / 255.0 for i in range(0, lc, 2)])
        return color


def _user_to_rgba(color, expand=True, clip=False):
    """Convert color(s) from any set of fmts (str/hex/arr) to RGB(A) array"""
    if color is None:
        color = np.zeros(4, np.float32)
    if isinstance(color, string_types):
        color = _string_to_rgb(color)
    else:
        if isinstance(color, ColorArray):
            color = color.rgba
        else:
            if isinstance(color, (list, tuple)) and any(isinstance(c, string_types) for c in color):
                color = [_user_to_rgba(c, expand=expand, clip=clip) for c in color]
                if any(len(c) > 1 for c in color):
                    raise RuntimeError('could not parse colors, are they nested?')
                color = [c[0] for c in color]
            color = np.atleast_2d(color).astype(np.float32)
            if color.shape[1] not in (3, 4):
                raise ValueError('color must have three or four elements')
            if expand and color.shape[1] == 3:
                color = np.concatenate((color, np.ones((color.shape[0], 1))), axis=1)
            if color.min() < 0 or color.max() > 1:
                if clip:
                    color = np.clip(color, 0, 1)
                else:
                    raise ValueError('Color values must be between 0 and 1 (or use clip=True to automatically clip the values).')
    return color


def _array_clip_val(val):
    """Helper to turn val into array and clip between 0 and 1"""
    val = np.array(val)
    if val.max() > 1 or val.min() < 0:
        logger.warning('value will be clipped between 0 and 1')
    val[...] = np.clip(val, 0, 1)
    return val


class ColorArray(object):
    __doc__ = 'An array of colors\n\n    Parameters\n    ----------\n    color : str | tuple | list of colors\n        If str, can be any of the names in ``vispy.color.get_color_names``.\n        Can also be a hex value if it starts with ``\'#\'`` as ``\'#ff0000\'``.\n        If array-like, it must be an Nx3 or Nx4 array-like object.\n        Can also be a list of colors, such as\n        ``[\'red\', \'#00ff00\', ColorArray(\'blue\')]``.\n    alpha : float | None\n        If no alpha is not supplied in ``color`` entry and ``alpha`` is None,\n        then this will default to 1.0 (opaque). If float, it will override\n        any alpha values in ``color``, if provided.\n    clip : bool\n        Clip the color value.\n    color_space : \'rgb\' | \'hsv\'\n       \'rgb\' (default) : color tuples are interpreted as (r, g, b) components.\n       \'hsv\' : color tuples are interpreted as (h, s, v) components.\n\n    Examples\n    --------\n    There are many ways to define colors. Here are some basic cases:\n\n        >>> from vispy.color import ColorArray\n        >>> r = ColorArray(\'red\')  # using string name\n        >>> r\n        <ColorArray: 1 color ((1.0, 0.0, 0.0, 1.0))>\n        >>> g = ColorArray((0, 1, 0, 1))  # RGBA tuple\n        >>> b = ColorArray(\'#0000ff\')  # hex color\n        >>> w = ColorArray()  # defaults to black\n        >>> w.rgb = r.rgb + g.rgb + b.rgb\n        >>>hsv_color = ColorArray(color_space="hsv", color=(0, 0, 0.5))\n        >>>hsv_color\n        <ColorArray: 1 color ((0.5, 0.5, 0.5, 1.0))>\n        >>> w == ColorArray(\'white\')\n        True\n        >>> w.alpha = 0\n        >>> w\n        <ColorArray: 1 color ((1.0, 1.0, 1.0, 0.0))>\n        >>> rgb = ColorArray([\'r\', (0, 1, 0), \'#0000FFFF\'])\n        >>> rgb\n        <ColorArray: 3 colors ((1.0, 0.0, 0.0, 1.0) ... (1.0, 0.0, 0.0, 1.0))>\n        >>> rgb == ColorArray([\'red\', \'#00ff00\', ColorArray(\'blue\')])\n        True\n\n    Notes\n    -----\n    Under the hood, this class stores data in RGBA format suitable for use\n    on the GPU.\n    '

    def __init__(self, color=(0.0, 0.0, 0.0), alpha=None, clip=False, color_space='rgb'):
        color = (0, 0, 0, 0) if color is None else color
        if color_space == 'hsv':
            color = _hsv_to_rgb(color)
        elif color_space != 'rgb':
            raise ValueError('color_space should be either "rgb" or"hsv", it is ' + color_space)
        rgba = _user_to_rgba(color, clip=clip)
        if alpha is not None:
            rgba[:, 3] = alpha
        self._rgba = None
        self.rgba = rgba

    def copy(self):
        """Return a copy"""
        return deepcopy(self)

    @classmethod
    def _name(cls):
        """Helper to get the class name once it's been created"""
        return cls.__name__

    def __len__(self):
        return self._rgba.shape[0]

    def __repr__(self):
        nice_str = str(tuple(self._rgba[0]))
        plural = ''
        if len(self) > 1:
            plural = 's'
            nice_str += ' ... ' + str(tuple(self.rgba[(-1)]))
        return '<%s: %i color%s (%s)>' % (self._name(), len(self),
         plural, nice_str)

    def __eq__(self, other):
        return np.array_equal(self._rgba, other._rgba)

    def __getitem__(self, item):
        if isinstance(item, tuple):
            raise ValueError('ColorArray indexing is only allowed along the first dimension.')
        subrgba = self._rgba[item]
        if subrgba.ndim == 1:
            if not len(subrgba) == 4:
                raise AssertionError
        elif subrgba.ndim == 2:
            pass
        assert subrgba.shape[1] in (3, 4)
        return ColorArray(subrgba)

    def __setitem__(self, item, value):
        if isinstance(item, tuple):
            raise ValueError('ColorArray indexing is only allowed along the first dimension.')
        if isinstance(value, ColorArray):
            value = value.rgba
        self._rgba[item] = value

    def extend(self, colors):
        """Extend a ColorArray with new colors

        Parameters
        ----------
        colors : instance of ColorArray
            The new colors.
        """
        colors = ColorArray(colors)
        self._rgba = np.vstack((self._rgba, colors._rgba))
        return self

    @property
    def rgba(self):
        """Nx4 array of RGBA floats"""
        return self._rgba.copy()

    @rgba.setter
    def rgba(self, val):
        """Set the color using an Nx4 array of RGBA floats"""
        rgba = _user_to_rgba(val, expand=False)
        if self._rgba is None:
            self._rgba = rgba
        else:
            self._rgba[:, :rgba.shape[1]] = rgba

    @property
    def rgb(self):
        """Nx3 array of RGB floats"""
        return self._rgba[:, :3].copy()

    @rgb.setter
    def rgb(self, val):
        """Set the color using an Nx3 array of RGB floats"""
        self.rgba = val

    @property
    def RGBA(self):
        """Nx4 array of RGBA uint8s"""
        return (self._rgba * 255).astype(np.uint8)

    @RGBA.setter
    def RGBA(self, val):
        """Set the color using an Nx4 array of RGBA uint8 values"""
        val = np.atleast_1d(val).astype(np.float32) / 255
        self.rgba = val

    @property
    def RGB(self):
        """Nx3 array of RGBA uint8s"""
        return np.round(self._rgba[:, :3] * 255).astype(int)

    @RGB.setter
    def RGB(self, val):
        """Set the color using an Nx3 array of RGB uint8 values"""
        val = np.atleast_1d(val).astype(np.float32) / 255.0
        self.rgba = val

    @property
    def alpha(self):
        """Length-N array of alpha floats"""
        return self._rgba[:, 3]

    @alpha.setter
    def alpha(self, val):
        """Set the color using alpha"""
        self._rgba[:, 3] = _array_clip_val(val)

    @property
    def hex(self):
        """Numpy array with N elements, each one a hex triplet string"""
        return _rgb_to_hex(self._rgba)

    @hex.setter
    def hex(self, val):
        """Set the color values using a list of hex strings"""
        self.rgba = _hex_to_rgba(val)

    @property
    def hsv(self):
        """Nx3 array of HSV floats"""
        return self._hsv

    @hsv.setter
    def hsv(self, val):
        """Set the color values using an Nx3 array of HSV floats"""
        self.rgba = _hsv_to_rgb(val)

    @property
    def _hsv(self):
        """Nx3 array of HSV floats"""
        return _rgb_to_hsv(self._rgba[:, :3])

    @property
    def value(self):
        """Length-N array of color HSV values"""
        return self._hsv[:, 2]

    @value.setter
    def value(self, val):
        """Set the color using length-N array of (from HSV)"""
        hsv = self._hsv
        hsv[:, 2] = _array_clip_val(val)
        self.rgba = _hsv_to_rgb(hsv)

    def lighter(self, dv=0.1, copy=True):
        """Produce a lighter color (if possible)

        Parameters
        ----------
        dv : float
            Amount to increase the color value by.
        copy : bool
            If False, operation will be carried out in-place.

        Returns
        -------
        color : instance of ColorArray
            The lightened Color.
        """
        color = self.copy() if copy else self
        color.value += dv
        return color

    def darker(self, dv=0.1, copy=True):
        """Produce a darker color (if possible)

        Parameters
        ----------
        dv : float
            Amount to decrease the color value by.
        copy : bool
            If False, operation will be carried out in-place.

        Returns
        -------
        color : instance of ColorArray
            The darkened Color.
        """
        color = self.copy() if copy else self
        color.value -= dv
        return color

    @property
    def lab(self):
        return _rgb_to_lab(self._rgba[:, :3])

    @lab.setter
    def lab(self, val):
        self.rgba = _lab_to_rgb(val)


class Color(ColorArray):
    __doc__ = "A single color\n\n    Parameters\n    ----------\n    color : str | tuple\n        If str, can be any of the names in ``vispy.color.get_color_names``.\n        Can also be a hex value if it starts with ``'#'`` as ``'#ff0000'``.\n        If array-like, it must be an 1-dimensional array with 3 or 4 elements.\n    alpha : float | None\n        If no alpha is not supplied in ``color`` entry and ``alpha`` is None,\n        then this will default to 1.0 (opaque). If float, it will override\n        the alpha value in ``color``, if provided.\n    clip : bool\n        If True, clip the color values.\n    "

    def __init__(self, color='black', alpha=None, clip=False):
        """Parse input type, and set attribute"""
        if isinstance(color, (list, tuple)):
            color = np.array(color, np.float32)
        rgba = _user_to_rgba(color, clip=clip)
        if rgba.shape[0] != 1:
            raise ValueError('color must be of correct shape')
        if alpha is not None:
            rgba[:, 3] = alpha
        self._rgba = None
        self.rgba = rgba.ravel()

    @ColorArray.rgba.getter
    def rgba(self):
        return super(Color, self).rgba[0]

    @ColorArray.rgb.getter
    def rgb(self):
        return super(Color, self).rgb[0]

    @ColorArray.RGBA.getter
    def RGBA(self):
        return super(Color, self).RGBA[0]

    @ColorArray.RGB.getter
    def RGB(self):
        return super(Color, self).RGB[0]

    @ColorArray.alpha.getter
    def alpha(self):
        return super(Color, self).alpha[0]

    @ColorArray.hex.getter
    def hex(self):
        return super(Color, self).hex[0]

    @ColorArray.hsv.getter
    def hsv(self):
        return super(Color, self).hsv[0]

    @ColorArray.value.getter
    def value(self):
        return super(Color, self).value[0]

    @ColorArray.lab.getter
    def lab(self):
        return super(Color, self).lab[0]

    @property
    def is_blank(self):
        """Boolean indicating whether the color is invisible.
        """
        return self.rgba[3] == 0

    def __repr__(self):
        nice_str = str(tuple(self._rgba[0]))
        return '<%s: %s>' % (self._name(), nice_str)