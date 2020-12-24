# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyp_beagle/dependencies/set_shared_labels.py
# Compiled at: 2019-07-16 04:25:49
import matplotlib.pyplot as plt

def set_shared_ylabel(a, ylabel, labelpad=0.01):
    """Set a y label shared by multiple axes
    Parameters
    ----------
    a: list of axes
    ylabel: string
    labelpad: float
        Sets the padding between ticklabels and axis label"""
    f = plt.figure()
    f.canvas.draw()
    top = a[0].get_position().y1
    bottom = a[(-1)].get_position().y0
    x0 = 1
    for at in a:
        at.set_ylabel('')
        bboxes, _ = at.yaxis.get_ticklabel_extents(f.canvas.renderer)
        bboxes = bboxes.inverse_transformed(f.transFigure)
        xt = bboxes.x0
        if xt < x0:
            x0 = xt

    tick_label_left = x0
    a[(-1)].set_ylabel(ylabel)
    a[(-1)].yaxis.set_label_coords(tick_label_left - labelpad, (bottom + top) / 2, transform=f.transFigure)


def set_shared_xlabel(a, xlabel, labelpad=0.01):
    """Set a x label shared by multiple axes
    Parameters
    ----------
    a: list of axes
    ylabel: string
    labelpad: float
        Sets the padding between ticklabels and axis label"""
    f = plt.figure()
    f.canvas.draw()
    left = a[0].get_position().x0
    right = a[(-1)].get_position().x1
    y0 = 1
    for at in a:
        at.set_xlabel('')
        bboxes, _ = at.xaxis.get_ticklabel_extents(f.canvas.renderer)
        bboxes = bboxes.inverse_transformed(f.transFigure)
        yt = bboxes.y0
        if yt < y0:
            y0 = yt

    tick_label_bottom = y0
    a[(-1)].set_xlabel(xlabel)
    a[(-1)].xaxis.set_label_coords((left + right) / 2, tick_label_bottom - labelpad, transform=f.transFigure)