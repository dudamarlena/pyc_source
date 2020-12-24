# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/ggplot/qplot.py
# Compiled at: 2016-07-11 10:52:39
from __future__ import absolute_import, division, print_function, unicode_literals
from .ggplot import ggplot
from .aes import aes
from .chart_components import ggtitle, xlim, ylim, xlab, ylab, labs
from .geoms import geom_point, geom_bar, geom_histogram, geom_line
from .scales.scale_log import scale_x_log, scale_y_log
import pandas as pd, numpy as np, six

def qplot(x, y=None, color=None, size=None, fill=None, data=None, geom=b'auto', stat=[], position=[], xlim=None, ylim=None, log=b'', main=None, xlab=None, ylab=b'', asp=None):
    """
    Parameters
    ----------
    x: string, pandas series, list, or numpy array
        x values
    y: string, pandas series, list, or numpy array
        y values
    color: string
        color values
    size: string
        size values
    fill: string
        fill values
    data: data frame
        data frame to use for the plot
    geom: string (auto, point, bar, hist, line)
        string that specifies which type of plot to make
    stat: list
        specifies which statistics to use
    position: list
        gives position adjustment to use
    xlim: tuple
        limits on x axis; i.e. (0, 10)
    ylim: tuple, None
        limits on y axis; i.e. (0, 10)
    log: string
        which variables to log transform ("x", "y", or "xy")
    main: string
        title for the plot
    xlab: string
        title for the x axis
    ylab: string
        title for the y axis
    asp: string
        the y/x aspect ratio

    Returns
    -------
    p: ggplot
        returns a plot

    Examples
    --------
    >>> print qplot('mpg', 'drat', data=mtcars, main="plain")
    >>> print qplot('mpg', 'drat', color='cyl', data=mtcars, main="cont. color")
    >>> print qplot('mpg', 'drat', color='name', data=mtcars, main="disc. color")
    >>> print qplot('mpg', 'drat', size='cyl', data=mtcars, main="size")
    >>> print qplot('mpg', 'drat', data=mtcars, log='x', main="log x")
    >>> print qplot('mpg', 'drat', data=mtcars, log='y', main="log y")
    >>> print qplot('mpg', 'drat', data=mtcars, log='xy', main="log xy")
    >>> print qplot('mpg', 'drat', data=mtcars, geom="point", main="point")
    >>> print qplot('mpg', 'drat', data=mtcars, geom="line", main="line")
    >>> print qplot('mpg', data=mtcars, geom="hist", main="hist")
    >>> print qplot('mpg', data=mtcars, geom="histogram", main="histogram")
    >>> print qplot('cyl', 'mpg', data=mtcars, geom="bar", main="bar")
    >>> print qplot('mpg', 'drat', data=mtcars, xlab= "x lab", main="xlab")
    >>> print qplot('mpg', 'drat', data=mtcars, ylab = "y lab", main="ylab")
    """
    if x is not None and not isinstance(x, six.string_types):
        data = pd.DataFrame({b'x': x})
        x = b'x'
    if y is not None and not isinstance(y, six.string_types):
        data[b'y'] = y
        y = b'y'
    aes_elements = {b'x': x}
    if y:
        aes_elements[b'y'] = y
    if color:
        aes_elements[b'color'] = color
    if size:
        aes_elements[b'size'] = size
    if fill:
        aes_elements[b'fill'] = fill
    _aes = aes(**aes_elements)
    geom_map = {b'bar': geom_bar, 
       b'hist': geom_histogram, 
       b'histogram': geom_histogram, 
       b'line': geom_line, 
       b'point': geom_point}
    if geom == b'auto':
        if y is None:
            geom = geom_histogram
        else:
            geom = geom_point
    else:
        geom = geom_map.get(geom, geom_point)
    p = ggplot(_aes, data=data) + geom()
    if b'x' in log:
        p += scale_x_log()
    if b'y' in log:
        p += scale_y_log()
    if xlab:
        p += xlabel(xlab)
    if ylab:
        p += ylabel(ylab)
    if main:
        p += ggtitle(main)
    return p