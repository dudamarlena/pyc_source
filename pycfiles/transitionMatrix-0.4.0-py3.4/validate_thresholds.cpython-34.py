# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/examples/python/validate_thresholds.py
# Compiled at: 2018-10-21 10:29:17
# Size of source mod 2**32: 1650 bytes
""" Validate a set of calculated thresholds

"""
import transitionMatrix as tm
from datasets import Generic
from transitionMatrix.thresholds.model import ThresholdSet
from transitionMatrix.thresholds.settings import AR_Model
M = tm.TransitionMatrix(values=Generic)
M.print()
M.validate()
Ratings = M.dimension
Default = Ratings - 1
Periods = 5
T = tm.TransitionMatrixSet(values=M, periods=Periods, method='Power', temporal_type='Cumulative')
As = ThresholdSet(TMSet=T)
for ri in range(0, Ratings):
    print('RI: ', ri)
    As.fit(AR_Model, ri)

Q = As.validate(AR_Model)