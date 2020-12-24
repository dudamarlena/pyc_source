# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/examples/python/matrix_set_operations.py
# Compiled at: 2018-10-16 05:05:49
# Size of source mod 2**32: 2092 bytes
""" Examples using transitionMatrix to perform operations with transition matrix sequences

"""
import transitionMatrix as tm
from datasets import Generic as T1
print('-- Lets seed the set with a 3x3 matrix')
A = tm.TransitionMatrix(values=[[0.6, 0.2, 0.2], [0.2, 0.6, 0.2], [0.2, 0.2, 0.6]])
print(A)
print('-- Identical future period transitions in incremental mode')
A_Set = tm.TransitionMatrixSet(values=A, periods=3, method='Copy', temporal_type='Incremental')
print(A_Set.entries)
print('-- Identical future period transitions in cumulative mode using the power method')
B_Set = tm.TransitionMatrixSet(values=A, periods=3, method='Power', temporal_type='Cumulative')
print(B_Set.entries)
print('-- Lets instantiate the set directly using a list of matrices')
C_Vals = [[[0.75, 0.25], [0.0, 1.0]], [[0.75, 0.25], [0.0, 1.0]]]
C_Set = tm.TransitionMatrixSet(values=C_Vals, temporal_type='Incremental')
print(C_Set.entries)
print('-- Validate the constructed sets')
A_Set.validate()
B_Set.validate()
C_Set.validate()
print('-- Convert to Cumulative')
A_Set.cumulate()
print(A_Set.entries)
A_Set.validate()
print('-- Convert back to Incremental')
A_Set.incremental()
print(A_Set.entries)
A_Set.validate()
print('-- Create a multiperiod matrix set and save to json file')
T_Set = tm.TransitionMatrixSet(values=T1, periods=10, method='Power', temporal_type='Cumulative')
T_Set.to_json('Tn.json')