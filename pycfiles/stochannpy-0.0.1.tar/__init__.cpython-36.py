# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\keurf\Documents\GitHub\StochANNPy\stochannpy\__init__.py
# Compiled at: 2018-04-04 15:44:41
# Size of source mod 2**32: 489 bytes
"""
StochANNPy (STOCHAstic Artificial Neural Network for PYthon) provides
user-friendly routines compatible with Scikit-Learn for stochastic learning.

Author: Keurfon Luu <keurfon.luu@mines-paristech.fr>
License: MIT
"""
from .bayesian_neural_network import BNNClassifier
from .evolutionary_neural_network import ENNClassifier
from .mccv import MCCVClassifier
__all__ = [
 'BNNClassifier', 'ENNClassifier', 'MCCVClassifier']
__version__ = '0.0.1'