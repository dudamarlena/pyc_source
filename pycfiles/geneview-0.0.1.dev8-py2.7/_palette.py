# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/geneview/util/_palette.py
# Compiled at: 2016-01-31 11:10:59
from __future__ import print_function, division
import colorsys, warnings, os
from distutils.version import LooseVersion
import matplotlib as mpl, matplotlib.colors as mplcol
mpl_ge_150 = LooseVersion(mpl.__version__) >= '1.5.0'

def desaturate(color, prop):
    """Decrease the saturation channel of a color by some percent.

    Parameters
    ----------
    color : matplotlib color
        hex, rgb-tuple, or html color name
    prop : float
        saturation channel of color will be multiplied by this value

    Returns
    -------
    new_color : rgb tuple
        desaturated color code in RGB tuple representation

    """
    if not 0 <= prop <= 1:
        raise ValueError('prop must be between 0 and 1')
    rgb = mplcol.colorConverter.to_rgb(color)
    h, l, s = colorsys.rgb_to_hls(*rgb)
    s *= prop
    new_color = colorsys.hls_to_rgb(h, l, s)
    return new_color


def set_hls_values(color, h=None, l=None, s=None):
    """Independently manipulate the h, l, or s channels of a color.

    Parameters
    ----------
    color : matplotlib color
        hex, rgb-tuple, or html color name
    h, l, s : floats between 0 and 1, or None
        new values for each channel in hls space

    Returns
    -------
    new_color : rgb tuple
        new color code in RGB tuple representation

    """
    rgb = mplcol.colorConverter.to_rgb(color)
    vals = list(colorsys.rgb_to_hls(*rgb))
    for i, val in enumerate([h, l, s]):
        if val is not None:
            vals[i] = val

    rgb = colorsys.hls_to_rgb(*vals)
    return rgb


def get_color_cycle():
    if mpl_ge_150:
        cyl = mpl.rcParams['axes.prop_cycle']
        try:
            return [ x['color'] for x in cyl ]
        except KeyError:
            pass

    return mpl.rcParams['axes.color_cycle']