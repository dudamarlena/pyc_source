# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/examples/python/matrix_operations.py
# Compiled at: 2018-10-22 16:01:11
# Size of source mod 2**32: 3462 bytes
"""
Examples using transitionMatrix to perform various transition matrix operations.

"""
import numpy as np
from scipy.linalg import expm
import transitionMatrix as tm
from datasets import JLT
from transitionMatrix import dataset_path
print('> Initialize a 3x3 matrix with values')
A = tm.TransitionMatrix(values=[[0.6, 0.2, 0.2], [0.2, 0.6, 0.2], [0.2, 0.2, 0.6]])
print(A)
print('> Initialize a generic matrix of dimension n')
B = tm.TransitionMatrix(dimension=4)
print(B)
print('> Any list can be used for initialization (but not all shapes are valid transition matrices!)')
C = tm.TransitionMatrix(values=[1.0, 3.0])
print(C)
print('> Any numpy array can be used for initialization (but not all are valid transition matrices!)')
D = tm.TransitionMatrix(values=np.identity(5))
print(D)
print('> Values can be loaded from json or csv files')
F = tm.TransitionMatrix(json_file=dataset_path + 'JLT.json')
print(F)
print('> Validate that a matrix satisfies probability matrix properties')
print(A.validate())
print(B.validate())
print(C.validate())
print(D.validate())
print(F.validate())
print('> All numpy.matrix / ndarray functionality is available')
E = tm.TransitionMatrix(values=[[0.75, 0.25], [0.0, 1.0]])
print(E.validate())
print(E.ndim)
print(E.shape)
print(E.T)
print(E.I)
print(E.sum(0))
print(E.sum(1))
print('> Lets fix the invalid matrix C')
C = tm.TransitionMatrix(values=np.resize(C, (2, 2)))
C[(0, 1)] = 0.0
C[(1, 0)] = 0.0
C[(1, 1)] = 1.0
print(C.validate())
print('> Computing the generator of a transition matrix')
G = A.generator()
print(A, expm(G))
print('> Transition Matrix algebra is very intuitive')
print(A * A)
print(A ** 2)
print(A ** 10)
print('> Transition matrices properties can be analyzed')
print(A.characterize())
print('> Lets look at a realistic example from the JLT paper')
E = tm.TransitionMatrix(values=JLT)
E_2 = tm.TransitionMatrix(json_file=dataset_path + 'JLT.json')
E_3 = tm.TransitionMatrix(csv_file=dataset_path + 'JLT.csv')
Error = E - E_3
print(np.linalg.norm(Error))
print('> Lets look at validation and generators')
print(E.validate(accuracy=0.001))
print(E.characterize())
print(E.generator())
Error = E - expm(E.generator())
print(np.linalg.norm(Error))
print(np.linalg.norm(Error, 1))
print('> Use pandas style API for saving to files')
E.to_csv('JLT.csv')
E.to_json('JLT.json')