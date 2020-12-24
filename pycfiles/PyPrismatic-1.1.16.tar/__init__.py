# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: pyPRISM/trajectory/__init__.py
# Compiled at: 2018-01-24 15:32:41
__doc__ = '\nPRISM is often used in conjunction with molecular simulation techniques, such\nas when using Self-Consistent PRISM. This module is intended to provide classes for\nworking with and analyzing molecular simulation trajectories.\n\n\nSee :ref:`scprism` for more information on the method.\n'
import warnings
from sys import platform as _platform
try:
    from pyPRISM.trajectory.Debyer import Debyer
except ImportError:
    warnings.warn('Cannot import Debyer: compiled Cython module not found.')

if not (_platform == 'linux' or _platform == 'linux2'):
    warnings.warn('Parallelized Debyer is only supported on Linux. Using slower, serial execution.')