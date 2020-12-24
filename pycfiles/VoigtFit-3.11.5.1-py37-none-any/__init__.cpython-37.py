# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/krogager/Projects/VoigtFit/build/lib/VoigtFit/__init__.py
# Compiled at: 2020-03-27 14:32:28
# Size of source mod 2**32: 1219 bytes
"""
VoigtFit is a Python package designed to fit Voigt profiles to absorption
lines in spectral data. The package handles multiple spectra simultaneously,
and fits multiple component structure of several absorption lines using a
Levenberg--Marquardt minimization algorithm to identify the optimal parameters.

Written by Jens-Kristian Krogager.
"""
__author__ = 'Jens-Kristian Krogager'
from os import path
from sys import version_info
import warnings, matplotlib
with warnings.catch_warnings():
    warnings.simplefilter('ignore')
    matplotlib.use('TkAgg')
from . import dataset
from .dataset import DataSet
from . import lines
from .lines import show_transitions
from . import hdf5_save
from .hdf5_save import load_dataset, save_dataset
from . import line_complexes
from . import molecules
from . import output
from . import regions
from . import voigt
code_dir = path.dirname(path.abspath(__file__))
with open(path.join(code_dir, 'VERSION')) as (version_file):
    version = version_file.read().strip()
    if version_info[0] >= 3:
        v_items = version.split('.')
        v_items[0] = '3'
        version = '.'.join(v_items)
    __version__ = version