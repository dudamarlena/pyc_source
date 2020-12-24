# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/aeolus/plot/mpl.py
# Compiled at: 2020-03-31 18:41:52
# Size of source mod 2**32: 1584 bytes
__doc__ = 'Matplotlib-related utilities.'
import matplotlib.colors as mcolors
from matplotlib.lines import Line2D
import numpy as np
__all__ = ('MidpointNormalize', 'add_custom_legend')

class MidpointNormalize(mcolors.Normalize):
    """MidpointNormalize"""

    def __init__(self, vmin=None, vmax=None, midpoint=None, clip=False):
        self.midpoint = midpoint
        mcolors.Normalize.__init__(self, vmin, vmax, clip)

    def __call__(self, value, clip=None):
        x, y = [
         self.vmin, self.midpoint, self.vmax], [0, 0.5, 1]
        return np.ma.masked_array(np.interp(value, x, y))


def add_custom_legend(ax, styles_and_labels, **leg_kw):
    """
    Add a custom legend to matplotlib axes.

    Parameters
    ----------
    ax: matplotlib.axes._subplots.AxesSubplot
        Axes where to put the legend.
    styles_and_labels: dict
        Dictionary with labels as keys and a dictionary of plot
        keywords as values.
    leg_kw: dict, optional
        Keyword arguments passed to `legend()` function.

    Example
    -------
    >>> import matplotlib.pyplot as plt
    >>> ax = plt.axes()
    >>> my_dict = dict(foo=dict(color='C0', marker="X"),
                       bar=dict(color='C1', marker="o"))
    >>> add_custom_legend(ax, my_dict, loc=2, title="blah")

    """
    lines = [Line2D([0], [0], **style) for style in styles_and_labels.values()]
    leg = (ax.legend)(lines, (styles_and_labels.keys()), **leg_kw)
    if ax.legend_ is not None:
        ax.add_artist(leg)