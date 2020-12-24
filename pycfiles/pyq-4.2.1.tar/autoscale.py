# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyp_beagle/dependencies/autoscale.py
# Compiled at: 2019-07-16 04:25:49
import numpy as np
default_bot = np.inf
default_top = -np.inf

def get_autoscale_y(ax, margin=0.1, ylog=False, top_margin=None, bottom_margin=None):
    """
    This function rescales the y-axis based on the data that is visible given the current xlim of the axis.
    ax -- a matplotlib axes object
    margin -- the fraction of the total height of the y-data to pad the upper and lower ylims
    top_margin -- the fraction of the total height of the y-data to pad the upper ylims
    bottom_margin -- the fraction of the total height of the y-data to pad the upper ylims
    """
    if top_margin is None:
        top_margin = margin
    if bottom_margin is None:
        bottom_margin = margin

    def get_bottom_top(line):
        xd = line.get_xdata()
        yd = line.get_ydata()
        lo, hi = ax.get_xlim()
        y_displayed = yd[((xd > lo) & (xd < hi))]
        if ylog:
            y_displayed = y_displayed[(y_displayed > 0.0)]
        if len(y_displayed) > 0:
            ymax = np.amax(y_displayed)
            if ylog:
                ymax = np.log10(ymax)
            ymin = np.amin(y_displayed)
            if ylog:
                ymin = np.log10(ymin)
            h = ymax - ymin
            if ylog:
                bot = ymin - bottom_margin
                top = ymax + top_margin
            else:
                bot = ymin - bottom_margin * h
                top = ymax + top_margin * h
            if ylog:
                bot = 10.0 ** bot
                top = 10.0 ** top
        else:
            bot, top = default_bot, default_top
        return (bot, top)

    lines = ax.get_lines()
    bot, top = default_bot, default_top
    for line in lines:
        new_bot, new_top = get_bottom_top(line)
        if new_bot < bot:
            bot = new_bot
        if new_top > top:
            top = new_top

    return [
     bot, top]


def autoscale_y(ax, margin=0.1, ylog=False, top_margin=None, bottom_margin=None):
    """
    This function rescales the y-axis based on the data that is visible given the current xlim of the axis.
    ax -- a matplotlib axes object
    margin -- the fraction of the total height of the y-data to pad the upper and lower ylims
    top_margin -- the fraction of the total height of the y-data to pad the upper ylims
    bottom_margin -- the fraction of the total height of the y-data to pad the upper ylims
    """
    bot, top = get_autoscale_y(ax, margin, ylog, top_margin, bottom_margin)
    ax.set_ylim(bot, top)