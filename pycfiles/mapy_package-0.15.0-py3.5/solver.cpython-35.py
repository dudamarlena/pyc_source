# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\mapy\solver\solver.py
# Compiled at: 2017-04-12 19:32:03
# Size of source mod 2**32: 704 bytes
import numpy as np, time, scipy, scipy.sparse as ss, scipy.sparse.linalg as linalg

def solve_k_coo_sub(model):
    full_displ = {}
    full_F = {}
    for sub in model.subcases.values():
        F = model.F[sub.id]
        K = model.k_coo_sub[sub.id]
        x = linalg.spsolve(K.tocsc(), F)
        index_to_zero = model.index_to_delete[sub.id]
        full_displ[sub.id] = x
        full_F[sub.id] = np.dot(model.k_coo, x)

    return [full_displ, full_F]