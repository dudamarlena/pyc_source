# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/InverseProblem/functions.py
# Compiled at: 2015-06-29 15:16:39
# Size of source mod 2**32: 892 bytes
"""
define a function that takes a contaminated matrix, A, uses SVD to decompose it, and then gives the solution to Ax=b
Requires matrix A, vector b, parameters k&l, 

"""

def joke():
    return 'Actions demolish their alternatives. Experiments reveal them.'


import numpy as np, pandas as pd, statsmodels.formula.api as smf

def invert(A, b, k, l):
    U, s, V = np.linalg.svd(A, full_matrices=False)
    c1 = np.matrix(s).shape[1]
    S = np.diag(s)
    Si = S
    for i in range(0, c1):
        Si[(i, i)] = 1 / Si[(i, i)] - 1 / Si[(i, i)] * (l / (l + Si[(i, i)] ** 2)) ** k

    x1 = V * Si * U.transpose() * b
    return x1
    print('This is the solution, X, to AX=b where A is ill-conditioned and b is noisy using a iterative Tikhonov regularization approach.')