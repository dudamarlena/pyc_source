# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/ggplot/scales/scale_color_gradient.py
# Compiled at: 2016-07-31 11:30:58
from __future__ import absolute_import, division, print_function, unicode_literals
from .scale import scale
from copy import deepcopy
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, rgb2hex, ColorConverter

def colors_at_breaks(cmap, breaks=[
 0, 0.25, 0.5, 0.75, 1.0]):
    return [ rgb2hex(cmap(bb)[:3]) for bb in breaks ]


class scale_color_gradient(scale):
    r"""
    Specify a two- or three-point gradient.

    Parameters
    ----------
    name:
        Name of an existing gradient scheme
    limis :
        list of the upper and lower bounds of the gradient
    low 
        colour at the lower bound of the gradient
    mid 
        colour at the middle of the gradient
    high:
        Colour at the upper bound of the gradient

    Examples
    --------
    >>> from ggplot import *
    >>> diamons_premium = diamonds[diamonds.cut=='Premium']
    >>> gg = ggplot(diamons_premium, aes(x='depth', y='carat', colour='price')) + \
    ...     geom_point()
    >>> print(gg + scale_colour_gradient(low='red', mid='white', high='blue', limits=[4000,6000]) + \
    ...     ggtitle('With red-blue gradient'))
    >>> print(gg + ggtitle('With standard gradient'))
    """
    VALID_SCALES = [
     b'name', b'limits', b'low', b'mid', b'high']

    def __radd__(self, gg):
        if self.limits is not None:
            gg.color_limits = self.limits
        color_spectrum = []
        if self.low:
            color_spectrum.append(self.low)
        if self.mid:
            color_spectrum.append(self.mid)
        if self.high:
            color_spectrum.append(self.high)
        if self.low and self.high:
            gradient2n = LinearSegmentedColormap.from_list(b'gradient2n', color_spectrum)
            plt.cm.register_cmap(cmap=gradient2n)
            gg.color_scale = colors_at_breaks(gradient2n)
            gg.colormap = gradient2n
        return gg