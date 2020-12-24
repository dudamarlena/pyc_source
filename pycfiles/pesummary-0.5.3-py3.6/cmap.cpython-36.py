# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/pesummary/gw/plots/cmap.py
# Compiled at: 2020-04-21 06:57:35
# Size of source mod 2**32: 1960 bytes
from matplotlib import cm
from matplotlib import colors
import numpy as np, pesummary

def cylon():
    path = pesummary.__file__[:-12]
    with open(path + '/gw/plots/cylon.csv') as (f):
        data = np.loadtxt(f, delimiter=',')
    cmap = colors.LinearSegmentedColormap.from_list('cylon', data)
    locals().update({'cylon': cmap})
    cm.register_cmap(cmap=cmap)


def colormap_with_fixed_hue(color, N=10):
    """Create a linear colormap with fixed hue

    Parameters
    ----------
    color: tuple
        color that determines the hue
    N: int, optional
        number of colors used in the palette
    """
    import seaborn
    from matplotlib.colors import LinearSegmentedColormap
    from matplotlib.colors import rgb_to_hsv, hsv_to_rgb, hex2color
    color_hsv = rgb_to_hsv(hex2color(color))
    base = seaborn.color_palette('Blues', 10)
    base_hsv = np.array(list(map(rgb_to_hsv, base)))
    h, s, v = base_hsv.T
    h_fixed = np.ones_like(h) * color_hsv[0]
    color_array = np.array(list(map(hsv_to_rgb, np.vstack([h_fixed, s * color_hsv[1], v]).T)))
    return LinearSegmentedColormap.from_list('mycmap', color_array)