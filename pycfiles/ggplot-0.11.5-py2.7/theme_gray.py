# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/ggplot/themes/theme_gray.py
# Compiled at: 2016-07-11 10:52:39
from __future__ import absolute_import, division, print_function, unicode_literals
import matplotlib as mpl
from cycler import cycler
from .theme import theme_base

class theme_gray(theme_base):
    """
    Standard theme for ggplot. Gray background w/ white gridlines.

    Copied from the the ggplot2 codebase:
        https://github.com/hadley/ggplot2/blob/master/R/theme-defaults.r
    """

    def __init__(self):
        super(theme_gray, self).__init__()
        self._rcParams[b'timezone'] = b'UTC'
        self._rcParams[b'lines.linewidth'] = b'1.0'
        self._rcParams[b'lines.antialiased'] = b'True'
        self._rcParams[b'patch.linewidth'] = b'0.5'
        self._rcParams[b'patch.facecolor'] = b'348ABD'
        self._rcParams[b'patch.edgecolor'] = b'#E5E5E5'
        self._rcParams[b'patch.antialiased'] = b'True'
        self._rcParams[b'font.family'] = b'sans-serif'
        self._rcParams[b'font.size'] = b'12.0'
        self._rcParams[b'font.serif'] = [b'Times', b'Palatino',
         b'New Century Schoolbook',
         b'Bookman', b'Computer Modern Roman',
         b'Times New Roman']
        self._rcParams[b'font.sans-serif'] = [b'Helvetica', b'Avant Garde',
         b'Computer Modern Sans serif',
         b'Arial']
        self._rcParams[b'axes.facecolor'] = b'#E5E5E5'
        self._rcParams[b'axes.edgecolor'] = b'bcbcbc'
        self._rcParams[b'axes.linewidth'] = b'1'
        self._rcParams[b'axes.grid'] = b'True'
        self._rcParams[b'axes.titlesize'] = b'x-large'
        self._rcParams[b'axes.labelsize'] = b'large'
        self._rcParams[b'axes.labelcolor'] = b'black'
        self._rcParams[b'axes.axisbelow'] = b'True'
        self._rcParams[b'axes.prop_cycle'] = cycler(b'color', [b'#333333', b'#348ABD', b'#7A68A6',
         b'#A60628', b'#467821', b'#CF4457', b'#188487', b'#E24A33'])
        self._rcParams[b'grid.color'] = b'white'
        self._rcParams[b'grid.linewidth'] = b'1.4'
        self._rcParams[b'grid.linestyle'] = b'solid'
        self._rcParams[b'xtick.major.size'] = b'0'
        self._rcParams[b'xtick.minor.size'] = b'0'
        self._rcParams[b'xtick.major.pad'] = b'6'
        self._rcParams[b'xtick.minor.pad'] = b'6'
        self._rcParams[b'xtick.color'] = b'#7F7F7F'
        self._rcParams[b'xtick.direction'] = b'out'
        self._rcParams[b'ytick.major.size'] = b'0'
        self._rcParams[b'ytick.minor.size'] = b'0'
        self._rcParams[b'ytick.major.pad'] = b'6'
        self._rcParams[b'ytick.minor.pad'] = b'6'
        self._rcParams[b'ytick.color'] = b'#7F7F7F'
        self._rcParams[b'ytick.direction'] = b'out'
        self._rcParams[b'legend.fancybox'] = b'True'
        self._rcParams[b'figure.figsize'] = b'11, 8'
        self._rcParams[b'figure.facecolor'] = b'1.0'
        self._rcParams[b'figure.edgecolor'] = b'0.50'
        self._rcParams[b'figure.subplot.hspace'] = b'0.5'

    def apply_final_touches(self, ax):
        """Styles x,y axes to appear like ggplot2
        Must be called after all plot and axis manipulation operations have
        been carried out (needs to know final tick spacing)

        From: https://github.com/wrobstory/climatic/blob/master/climatic/stylers.py
        """
        for child in ax.get_children():
            if isinstance(child, mpl.spines.Spine):
                child.set_alpha(0)

        for line in ax.get_xticklines() + ax.get_yticklines():
            line.set_markersize(5)
            line.set_markeredgewidth(1.4)

        ax.xaxis.set_ticks_position(b'bottom')
        ax.yaxis.set_ticks_position(b'left')
        ax.grid(True, b'minor', color=b'#F2F2F2', linestyle=b'-', linewidth=0.7)
        if not isinstance(ax.xaxis.get_major_locator(), mpl.ticker.LogLocator):
            ax.xaxis.set_minor_locator(mpl.ticker.AutoMinorLocator(2))
        if not isinstance(ax.yaxis.get_major_locator(), mpl.ticker.LogLocator):
            ax.yaxis.set_minor_locator(mpl.ticker.AutoMinorLocator(2))