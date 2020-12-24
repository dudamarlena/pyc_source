# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: pyPRISM/trajectory/__init__.py
# Compiled at: 2018-01-24 15:32:41
"""
PRISM is often used in conjunction with molecular simulation techniques, such
as when using Self-Consistent PRISM. This module is intended to provide classes for
working with and analyzing molecular simulation trajectories.

See :ref:`scprism` for more information on the method.
"""
import warnings
from sys import platform as _platform
try:
    from pyPRISM.trajectory.Debyer import Debyer
except ImportError:
    warnings.warn('Cannot import Debyer: compiled Cython module not found.')

if not (_platform == 'linux' or _platform == 'linux2'):
    warnings.warn('Parallelized Debyer is only supported on Linux. Using slower, serial execution.')