# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-x86_64/egg/bird/__init__.py
# Compiled at: 2014-10-25 04:32:37
"""
BIRD
====

Pure Python implementation of the BIRD algorithm. BIRD is a denoising
algorithm using randomized greedy pursuits. It works for single
signal and supports (structured)-sparsity for multivariate signals, e.g.
multichannel array data.

Reference
---------
Algorithm presented here are described in:

Blind Denoising with Random Greedy Pursuits.
Moussallam, M., Gramfort, A., Daudet, L., & Richard, G. (2014).
IEEE Signal Processing Letters, 21(11), 1341-1345
Preprint available at: http://arxiv.org/abs/1312.5444
"""
__version__ = '0.1'
from ._bird import bird, s_bird