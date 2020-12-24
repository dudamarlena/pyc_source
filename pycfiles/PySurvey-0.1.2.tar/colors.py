# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jonathanfriedman/Dropbox/python_dev_library/PySurvey/pysurvey/plotting/colors.py
# Compiled at: 2013-04-04 09:41:18
"""
Created on Jul 8, 2011

@author: jonathanfriedman
"""
import pylab as pl, matplotlib.cm as cm, numpy as np
from matplotlib.colors import rgb2hex

def array2colors(x, cmap=cm.jet, **kwargs):
    """
    Return rgba colors corresponding to values of x from desired colormap.
    Inputs:
        x         = 1D iterable of strs/floats/ints to be mapped to colors.
        cmap      = either color map instance or name of colormap as string. 
        vmin/vmax = (optional) float/int min/max values for the mapping.
                    If not provided, set to the min/max of x.
    Outputs:
        colors = array of rgba color values. each row corresponds to a value in x.
    """
    if type(cmap) is str:
        if cmap not in cm.datad:
            raise ValueError('Unkown colormap %s' % cmap)
        cmap = cm.get_cmap(cmap)
    x = np.asarray(x)
    isstr = np.issubdtype(x.dtype, str)
    if isstr:
        temp = np.copy(x)
        x_set = set(x)
        temp_d = dict((val, i) for (i, val) in enumerate(x_set))
        x = [ temp_d[id] for id in temp ]
    vmin = kwargs.get('vmin', np.min(x))
    vmax = kwargs.get('vmax', np.max(x))
    t = cm.ScalarMappable(cmap=cmap)
    t.set_clim(vmin, vmax)
    colors = t.to_rgba(x)
    if hex:
        colors = [ rgb2hex(c) for c in colors ]
    return colors


if __name__ == '__main__':
    test_array2colors()
    test_array2colors2()