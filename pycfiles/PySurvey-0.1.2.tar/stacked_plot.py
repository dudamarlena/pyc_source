# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jonathanfriedman/Dropbox/python_dev_library/PySurvey/pysurvey/plotting/stacked_plot.py
# Compiled at: 2013-04-02 18:46:29
"""
Created on Jul 13, 2011

@author: jonathanfriedman

Create stacked/area plots.
Adopted from: http://stackoverflow.com/questions/2225995/how-can-i-create-stacked-line-graph-with-matplotlib
"""
import pylab, numpy as np
from colors import array2colors

def stacked_plot(x, y, **kwargs):
    """
    Make a stacked line (area) plot, e.g. for plotting multiple time series. 
    x is a single sequence.
    y is at least 2 sequences, each of len(x). lines will be plotted with y[0] at the bottom, with filling between consecutive entries in y.
    Supports only positive values!
    """
    x = np.asarray(x)
    y = np.array(y)
    if y.min() < 0:
        raise ValueError, 'Only positive y values are supported, y contains value %f' % y.min()
    y_stacked = np.cumsum(y, axis=0)
    (n, m) = np.shape(y)
    fill_alpha = kwargs.pop('fill_alpha', 0.7)
    line_color = kwargs.pop('line_color', 'k')
    labels = kwargs.pop('labels', None)
    if 'linewidth' not in kwargs:
        kwargs['linewidth'] = 0.3
    if labels:
        label_flag = True
    else:
        label_flag = False
        labels = [''] * n
    cmap = kwargs.pop('cmap', 'Spectral')
    colors = kwargs.pop('colors', array2colors(np.arange(n), cmap=cmap))
    fig = pylab.figure()
    ax = fig.add_subplot(111)
    lines = []
    for i in xrange(0, n):
        lines.append(ax.plot(x, y_stacked[i, :], color=line_color, **kwargs))
        if i == 0:
            bottom = 0
        else:
            bottom = y_stacked[i - 1, :]
        ax.fill_between(x, bottom, y_stacked[i, :], facecolor=colors[i], alpha=fill_alpha, lw=0)
        ax.bar(0, 0, label=labels[i], facecolor=colors[i], alpha=fill_alpha, lw=0)

    if label_flag:
        pylab.legend(loc='best')
    return lines


if __name__ == '__main__':
    from Beautification import *
    n = 50
    x = np.arange(n)
    y = np.random.rand(4, n)
    labels = ['A', 'B', 'C', 'D']
    stacked_plot(x, y, cmap='Spectral', linewidth=0, alpha=0.7, fill_alpha=0.7, labels=labels)
    ax = pylab.gca()
    half_frame(ax)
    polish_legend(ax)
    pylab.show()