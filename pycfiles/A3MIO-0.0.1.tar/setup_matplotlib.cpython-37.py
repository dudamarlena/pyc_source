# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/a3cosmos_gas_evolution/Common_Python_Code/setup_matplotlib.py
# Compiled at: 2019-07-07 18:47:11
# Size of source mod 2**32: 2785 bytes
import os, sys
from matplotlib import pyplot as plt
from matplotlib import ticker
from matplotlib.ticker import MultipleLocator, AutoMinorLocator
from matplotlib import font_manager
import matplotlib as mpl, numpy as np

def setup_matplotlib():
    if os.path.isdir(os.path.expanduser('~') + os.sep + 'Library' + os.sep + 'Fonts'):
        font_dirs = [
         os.path.expanduser('~') + os.sep + 'Library' + os.sep + 'Fonts']
        font_files = font_manager.findSystemFonts(fontpaths=font_dirs)
        font_list = font_manager.createFontList(font_files)
        font_manager.fontManager.ttflist.extend(font_list)
        font_manager.findfont('NGC', rebuild_if_missing=True)
    else:
        mpl.rcParams['font.family'] = 'NGC'
        mpl_version = np.array(mpl.__version__.split('.')).astype(int)
        if not mpl_version[0] > 3:
            if not mpl_version[0] >= 3 or mpl_version[1] >= 1:
                mpl.rcParams['text.latex.preamble'] = '\\usepackage{amsmath}'
                mpl.rcParams['text.latex.preamble'] += '\n'
                mpl.rcParams['text.latex.preamble'] += '\\makeatletter \\newcommand*{\\rom}[1]{\\expandafter\\@slowromancap\\romannumeral #1@} \\makeatother'
        else:
            mpl.rcParams['text.latex.preamble'] = [
             '\\usepackage{amsmath}']
            mpl.rcParams['text.latex.preamble'].append('\\makeatletter \\newcommand*{\\rom}[1]{\\expandafter\\@slowromancap\\romannumeral #1@} \\makeatother')
    mpl.rcParams['axes.labelsize'] = '16'
    mpl.rcParams['axes.grid'] = True
    mpl.rcParams['axes.axisbelow'] = True
    mpl.rcParams['xtick.direction'] = 'in'
    mpl.rcParams['ytick.direction'] = 'in'
    mpl.rcParams['xtick.minor.visible'] = True
    mpl.rcParams['ytick.minor.visible'] = True
    mpl.rcParams['xtick.labelsize'] = '13'
    mpl.rcParams['ytick.labelsize'] = '13'
    mpl.rcParams['xtick.top'] = True
    mpl.rcParams['ytick.right'] = True
    mpl.rcParams['grid.linestyle'] = '--'
    mpl.rcParams['grid.linewidth'] = 0.25
    mpl.rcParams['grid.alpha'] = 0.8
    mpl.rcParams['legend.fontsize'] = '12'
    mpl.rcParams['legend.borderaxespad'] = 0.2