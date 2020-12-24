# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/champ/genlouvain.py
# Compiled at: 2017-09-26 14:45:58
# Size of source mod 2**32: 270 bytes
import numpy as np

def genlouvain(B, limit=10000, verbose=False, randord=True, randmove=True):
    n = B.shape[0]
    if len(np.nonzero(B - B.transpose())[0]) > 0:
        raise AssertionError('B must be a symmetric matrix')
    S0 = np.range(n)
    M = B