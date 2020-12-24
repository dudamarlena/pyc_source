# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/examples/python/calculate_thresholds.py
# Compiled at: 2018-10-20 09:57:44
# Size of source mod 2**32: 2088 bytes
""" Example of calculating thresholds

"""
import numpy as np
from scipy.stats import norm
import transitionMatrix as tm
from datasets import Minimal, Generic
from transitionMatrix.thresholds.model import ThresholdSet
from transitionMatrix.thresholds.settings import AR_Model
M = tm.TransitionMatrix(values=Generic)
print('> Load and validate a minimal transition matrix')
M.print()
M.validate()
print('> Valid Input Matrix? ', M.validated)
Ratings = M.dimension
Default = Ratings - 1
Periods = 10
T = tm.TransitionMatrixSet(values=M, periods=Periods, method='Power', temporal_type='Cumulative')
print('> Extend the matrix into 10 periods')
As = ThresholdSet(TMSet=T)
print('> Calculate thresholds per initial rating state')
for ri in range(0, Ratings):
    print('Initial Rating: ', ri)
    As.fit(AR_Model, ri)

print('> Display the calculated thresholds')
As.print()