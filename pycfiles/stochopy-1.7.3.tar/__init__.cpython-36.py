# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ..\stochopy\__init__.py
# Compiled at: 2018-04-26 12:25:53
# Size of source mod 2**32: 535 bytes
"""
StochOPy (STOCHastic OPtimization for PYthon) provides user-friendly routines
to sample or optimize objective functions with the most popular algorithms.

Author: Keurfon Luu <keurfon.luu@mines-paristech.fr>
License: MIT
"""
from .monte_carlo import MonteCarlo
from .evolutionary_algorithm import Evolutionary
from .benchmark_functions import BenchmarkFunction
from .gui import StochOGUI
__all__ = [
 'MonteCarlo', 'Evolutionary', 'BenchmarkFunction', 'StochOGUI']
__version__ = '1.7.3'