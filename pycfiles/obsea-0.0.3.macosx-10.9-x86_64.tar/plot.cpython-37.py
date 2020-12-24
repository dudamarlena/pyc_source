# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Alister/miniconda3/envs/obsea/lib/python3.7/site-packages/obsea/plot.py
# Compiled at: 2019-07-10 06:05:58
# Size of source mod 2**32: 888 bytes
"""
Plot module.

Used to plot complex representations.

"""
import numpy as np
import matplotlib.pyplot as plt
import colorcet as cc

def plot_azigram(xarr, **kwargs):
    """
    Plot an azigram with transparency.

    Parameters
    ----------
    xarr : xarray.DataArray
        Azigram
    **kwargs
        Additional arguments to pass to pcolormesh.

    Returns
    -------
    matplotlib.QuadMesh
        Azigram plot.

    """
    result = np.rad2deg(np.arctan2(xarr.real, xarr.imag)) % 360
    if xarr.attrs['double_angle']:
        result /= 2
        vmax = 180
    else:
        vmax = 360
    alpha = np.abs(xarr).values.ravel()[(..., np.newaxis)]
    img = (result.plot)(cmap=cc.cm.colorwheel, vmin=0, vmax=vmax, **kwargs)
    plt.draw()
    white = np.array([1, 1, 1, 1])
    img.set_facecolor(img.get_facecolor() * alpha + white * (1 - alpha))
    plt.draw()
    return img