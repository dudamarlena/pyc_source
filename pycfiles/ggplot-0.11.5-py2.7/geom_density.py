# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/ggplot/geoms/geom_density.py
# Compiled at: 2016-07-31 12:14:34
from scipy.stats import gaussian_kde
import numpy as np
from .geom import geom

class geom_density(geom):
    """
    Gaussian kernel density estimation for distribution of x parameter

    Parameters
    ----------
    x:
        value to be smoothed
    color:
        color of line
    alpha:
        transparency of fill
    linetype:
        type of the line ('solid', 'dashed', 'dashdot', 'dotted')
    size:
        thickness of line

    Examples
    --------
    """
    DEFAULT_AES = {'alpha': None, 'color': 'black', 'linetype': 'solid', 
       'size': 1.0}
    REQUIRED_AES = {'x'}
    DEFAULT_PARAMS = {}
    _extra_requires = {
     'y'}
    _aes_renames = {'linetype': 'linestyle', 'size': 'linewidth'}

    def _calculate_density(self, x):
        if len(x) <= 1:
            return (x, x)
        kde = gaussian_kde(x)
        bottom = np.min(x)
        top = np.max(x)
        step = (top - bottom) / 1000.0
        x = np.arange(bottom, top, step)
        y = kde.evaluate(x)
        return (x, y)

    def plot(self, ax, data, _aes):
        data, _aes = self._update_data(data, _aes)
        params = self._get_plot_args(data, _aes)
        variables = _aes.data
        x = data[variables['x']]
        x = x[(x.isnull() == False)]
        x, y = self._calculate_density(x)
        ax.plot(x, y, **params)