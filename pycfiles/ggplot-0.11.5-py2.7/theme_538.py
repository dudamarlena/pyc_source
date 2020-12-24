# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/ggplot/themes/theme_538.py
# Compiled at: 2016-07-11 10:52:39
from __future__ import absolute_import, division, print_function, unicode_literals
from .theme import theme_base

class theme_538(theme_base):
    """
    Theme for 538.

    Copied from CamDavidsonPilon's gist:
        https://gist.github.com/CamDavidsonPilon/5238b6499b14604367ac

   """

    def __init__(self):
        super(theme_538, self).__init__()
        self._rcParams[b'lines.linewidth'] = b'2.0'
        self._rcParams[b'patch.linewidth'] = b'0.5'
        self._rcParams[b'legend.fancybox'] = b'True'
        self._rcParams[b'axes.prop_cycle'] = cycler(b'color', [b'#30a2da', b'#fc4f30', b'#e5ae38',
         b'#6d904f', b'#8b8b8b'])
        self._rcParams[b'axes.facecolor'] = b'#f0f0f0'
        self._rcParams[b'axes.labelsize'] = b'large'
        self._rcParams[b'axes.axisbelow'] = b'True'
        self._rcParams[b'axes.grid'] = b'True'
        self._rcParams[b'patch.edgecolor'] = b'#f0f0f0'
        self._rcParams[b'axes.titlesize'] = b'x-large'
        self._rcParams[b'examples.directory'] = b''
        self._rcParams[b'figure.facecolor'] = b'#f0f0f0'
        self._rcParams[b'grid.linestyle'] = b'-'
        self._rcParams[b'grid.linewidth'] = b'1.0'
        self._rcParams[b'grid.color'] = b'#cbcbcb'
        self._rcParams[b'axes.edgecolor'] = b'#f0f0f0'
        self._rcParams[b'xtick.major.size'] = b'0'
        self._rcParams[b'xtick.minor.size'] = b'0'
        self._rcParams[b'ytick.major.size'] = b'0'
        self._rcParams[b'ytick.minor.size'] = b'0'
        self._rcParams[b'axes.linewidth'] = b'3.0'
        self._rcParams[b'font.size'] = b'14.0'
        self._rcParams[b'lines.linewidth'] = b'4'
        self._rcParams[b'lines.solid_capstyle'] = b'butt'
        self._rcParams[b'savefig.edgecolor'] = b'#f0f0f0'
        self._rcParams[b'savefig.facecolor'] = b'#f0f0f0'
        self._rcParams[b'figure.subplot.left'] = b'0.08'
        self._rcParams[b'figure.subplot.right'] = b'0.95'
        self._rcParams[b'figure.subplot.bottom'] = b'0.07'