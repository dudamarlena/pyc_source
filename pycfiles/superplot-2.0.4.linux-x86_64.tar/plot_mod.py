# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/michael/anaconda2/lib/python2.7/site-packages/superplot/plotlib/plot_mod.py
# Compiled at: 2017-08-19 22:58:02
"""
================
plotlib.plot_mod
================
General functions for plotting data, defined once so that they can be used/edited
in a consistent manner.
"""
import subprocess, os, appdirs
from matplotlib.ticker import AutoMinorLocator
from matplotlib.pylab import *

def plot_data(x, y, scheme, zorder=1):
    """ 
    Plot a point with a particular color scheme.

    :param x: Data to be plotted on x-axis
    :type x: numpy.ndarray, numpy.dtype
    :param y: Data to be plotted on y-axis
    :type y: numpy.ndarray, numpy.dtype
    :param scheme: Object containing plot appearance options
    :type scheme: :py:class:`schemes.Scheme`
    :param zorder: Draw order - lower numbers are plotted first
    :type zorder: integer

    """
    plt.plot(x, y, scheme.symbol, color=scheme.colour, label=scheme.label, ms=scheme.size, zorder=zorder)


def appearance(plot_name):
    """
    Specify the plot's appearance, with e.g. font types etc.
    from an mplstyle file.

    Options in the style sheet associated with the plot name
    override any in default.mplstyle.

    :param plot_name: Name of the plot (class name)
    :type plot_name: string

    .. Warning: If the user wants LaTeX, we first check if the 'latex'         shell command is available (as this is what matplotlib uses to         interface with LaTeX). If it isn't, we issue a warning and fall         back to mathtext.
    """
    style_sheet_name = ('{}.mplstyle').format(plot_name)
    script_dir = os.path.dirname(os.path.realpath(__file__))
    home_dir_locfile = os.path.join(os.path.dirname(script_dir), 'user_home.txt')
    style_sheet_path = None
    default_style_sheet_path = None
    if os.path.exists(home_dir_locfile):
        with open(home_dir_locfile, 'rb') as (f):
            home_dir_path = f.read()
            style_sheet_path = os.path.join(home_dir_path, 'styles', style_sheet_name)
            default_style_sheet_path = os.path.join(home_dir_path, 'styles', 'default.mplstyle')
    if style_sheet_path is None or not os.path.exists(style_sheet_path):
        style_sheet_path = os.path.join(os.path.split(os.path.abspath(__file__))[0], 'styles', style_sheet_name)
    if default_style_sheet_path is None or not os.path.exists(default_style_sheet_path):
        default_style_sheet_path = os.path.join(os.path.split(os.path.abspath(__file__))[0], 'styles', 'default.mplstyle')
    plt.style.use([default_style_sheet_path, style_sheet_path])
    if rcParams['text.usetex']:
        try:
            subprocess.call(['latex', '-version'])
        except OSError as err:
            rc('text', usetex=False)
            if err.errno == os.errno.ENOENT:
                warnings.warn("Cannot find `latex` command. Using matplotlib's mathtext.")

    return


def legend(leg_title=None, leg_position=None):
    """ 
    Turn on the legend.
    
    .. Warning::
        Legend properties specfied in by mplstyle, but could be
        overridden here.
    
    :param leg_title: Title of legend
    :type leg_title: string
    :param leg_position: Position of legend
    :type leg_position: string
    """
    if leg_position != 'no legend':
        plt.legend(prop={'size': 16}, title=leg_title, loc=leg_position)


def plot_limits(ax, limits=None):
    """ 
    If specified plot limits, set them.

    :param ax: Axis object
    :type ax: matplotlib.axes.Axes
    :param limits: Plot limits
    :type limits: list [xmin,xmax,ymin,ymax]
    """
    if limits is not None:
        ax.set_xlim([limits[0], limits[1]])
        ax.set_ylim([limits[2], limits[3]])
    return


def plot_ticks(xticks, yticks, ax):
    """ 
    Set the numbers of ticks on the axis.

    :param ax: Axis object
    :type ax: matplotlib.axes.Axes
    :param xticks: Number of required major x ticks
    :type xticks: integer
    :param yticks: Number of required major y ticks
    :type yticks: integer

    """
    ax.xaxis.set_major_locator(MaxNLocator(xticks))
    ax.yaxis.set_major_locator(MaxNLocator(yticks))
    ax.xaxis.set_minor_locator(AutoMinorLocator())
    ax.yaxis.set_minor_locator(AutoMinorLocator())


def plot_labels(xlabel, ylabel, plot_title=None, title_position='right'):
    """ 
    Plot axis labels.

    :param xlabel: Label for x-axis
    :type xlabel: string
    :param ylabel: Label for y-axis
    :type ylabel: string
    :param plot_title: Title appearing above plot
    :type plot_title: string
    :param title_position: Location of title
    :type title_position: string

    """
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(plot_title, loc=title_position)


def plot_image(data, bin_limits, plot_limits, scheme):
    """ 
    Plot data as an image.
    
    .. Warning::
        Interpolating perhaps misleads. If you don't want it set
        interpolation='nearest'. 
        
    :param data: x-, y- and z-data
    :type data: numpy.ndarray
    :param bin_limits: Bin limits
    :type bin_limits: list [[xmin,xmax],[ymin,ymax]]
    :param plot_limits: Plot limits
    :type plot_limits: list [xmin,xmax,ymin,ymax]
    :param scheme: Object containing appearance options, colours etc
    :type scheme: :py:class:`schemes.Scheme`
    """
    bin_limits = np.array((
     bin_limits[0][0],
     bin_limits[0][1],
     bin_limits[1][0],
     bin_limits[1][1]))
    aspect = (plot_limits[1] - plot_limits[0]) / (plot_limits[3] - plot_limits[2])
    plt.im = plt.imshow(data.T, cmap=scheme.colour_map, extent=bin_limits, interpolation='bilinear', label=scheme.label, origin='lower', aspect=aspect)
    cb = plt.colorbar(plt.im, orientation='vertical', fraction=0.046, pad=0.04)
    cb.locator = MaxNLocator(4)
    cb.update_ticks()
    cb.ax.set_ylabel(scheme.colour_bar_title)


def plot_contour(data, levels, scheme, bin_limits):
    """ 
    Make unfilled contours for a plot.

    :param data: Data to be contoured
    :type data: numpy.ndarray
    :param levels: Levels at which to draw contours
    :type levels: list [float,]
    :param scheme: Object containing appearance options, colours etc
    :type scheme: :py:class:`schemes.Scheme`
    :param bin_limits: Bin limits
    :type bin_limits: list [[xmin,xmax],[ymin,ymax]]
    """
    bin_limits = np.array((
     bin_limits[0][0],
     bin_limits[0][1],
     bin_limits[1][0],
     bin_limits[1][1]))
    cset = plt.contour(data.T, levels, colors=scheme.colour, hold='on', extent=bin_limits, interpolation='bilinear', origin=None, linestyles=[
     '--', '-'])
    fmt = dict(zip(cset.levels, scheme.level_names))
    plt.clabel(cset, inline=True, fmt=fmt, fontsize=12, hold='on')
    x_outside = 10.0 * abs(bin_limits[1])
    y_outside = 10.0 * abs(bin_limits[3])
    for name, style in zip(scheme.level_names, ['--', '-']):
        plt.plot(x_outside, y_outside, style, color=scheme.colour, label=name, alpha=0.7)

    return


def plot_filled_contour(data, levels, scheme, bin_limits):
    """ 
    Make filled contours for a plot.

    :param data: Data to be contoured
    :type data: numpy.ndarray
    :param levels: Levels at which to draw contours
    :type levels: list [float,]
    :param scheme: Object containing appearance options, colours etc
    :type scheme: :py:class:`schemes.Scheme`
    :param bin_limits: Bin limits
    :type bin_limits: list [[xmin,xmax],[ymin,ymax]]
    """
    bin_limits = np.array((
     bin_limits[0][0],
     bin_limits[0][1],
     bin_limits[1][0],
     bin_limits[1][1]))
    levels = sort(levels)
    levels = np.append(levels, data.max())
    plt.contourf(data.T, levels, colors=scheme.colours, hold='on', extent=bin_limits, interpolation='bilinear', origin=None, alpha=0.7)
    x_outside = 10.0 * abs(bin_limits[1])
    y_outside = 10.0 * abs(bin_limits[3])
    for name, color in zip(scheme.level_names, scheme.colours):
        plt.plot(x_outside, y_outside, 's', color=color, label=name, alpha=0.7, ms=15)

    return


def plot_band(x_data, y_data, width, ax, scheme):
    """
    Plot a band around a line.
    
    This is typically for a theoretical error. Vary x by +/- width
    and find the variation in y. Fill between these largest 
    and smallest y for a given x.

    :param x_data: x-data to be plotted
    :type x_data: numpy.ndarray
    :param y_data: y-data to be plotted
    :type y_data: numpy.ndarray
    :param width: Width of band - width on the left and right hand-side
    :type width: integer
    :param ax: An axis object to plot the band on
    :type ax: matplotlib.axes.Axes
    :param scheme: Object containing appearance options, colours etc
    :type scheme: :py:class:`schemes.Scheme`
    """
    upper_y = np.full(len(y_data), -float('inf'))
    lower_y = np.full(len(y_data), float('inf'))
    for index, x in enumerate(x_data):
        for x_prime, y_prime in zip(x_data, y_data):
            if abs(x - x_prime) < width:
                if y_prime < lower_y[index]:
                    lower_y[index] = y_prime
                elif y_prime > upper_y[index]:
                    upper_y[index] = y_prime

    ax.fill_between(x_data, lower_y, upper_y, where=None, facecolor=scheme.colour, alpha=0.7)
    plt.plot(-1, -1, 's', color=scheme.colour, label=scheme.label, alpha=0.7, ms=15)
    return