# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/duranton/Documents/CERFACS/CODES/arnica/src/arnica/utils/plot_ave_with_interval.py
# Compiled at: 2020-04-15 10:56:59
# Size of source mod 2**32: 2167 bytes
"""
*Plot graphs from 1D average array with or without its confidence interval. Rotate the graph from 90 deg.*
"""
import matplotlib.pyplot as plt

def plot_ave_with_interval(x_arr, average, profile='average-interval', upper=None, lower=None, **kw_args):
    """
    *Plot average profile with or without confidence interval*

    :param x_arr: Array of float of x-axis
    :type x_arr: np.array
    :param average: Array of float of average curve
    :type average: np.array
    :param profile: Plot type (average-interval, average, integral)
    :type profile: str
    :param upper: Array of float of upper interval values
    :type upper: np.array
    :param lower: Array of float of lower interval values
    :type upper: np.array

    Optional Keyword Args:

    :param x_label: Label for x-axe
    :type x_label: str
    :param y_label: Label for y-axe
    :type y_label: str
    :param style: Style of the axes - plain or sci
    :type style: str

    :return:

        - **plt** - Matplotlib.pyplot object
    """
    fig = plt.figure(figsize=(5.5, 5))
    fig.subplots_adjust(left=0.15, right=0.97, bottom=0.15, top=0.9,
      wspace=0.27)
    axe = fig.add_subplot(111)
    x_label = kw_args.get('x_label')
    if x_label is None:
        x_label = 'x'
    y_label = kw_args.get('y_label')
    if y_label is None:
        y_label = 'y'
    axe.set_ylabel(y_label)
    axe.set_xlabel(x_label)
    if 'average' in profile:
        axe.plot(average, x_arr, c='k', lw=0.5)
    if 'interval' in profile:
        if upper is not None:
            if lower is not None:
                axe.fill_betweenx(x_arr, upper, lower, facecolor='red', alpha=0.4)
    axe.grid(which='major', color='gray', linestyle='--', dashes=(8, 12),
      linewidth=0.5)
    style = kw_args.get('style')
    if style is None:
        style = 'plain'
    axe.ticklabel_format(axis='both', style=style, scilimits=(0, 0))
    return plt