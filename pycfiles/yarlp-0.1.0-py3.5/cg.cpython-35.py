# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/yarlp/external/baselines/baselines/common/cg.py
# Compiled at: 2018-04-01 14:21:44
# Size of source mod 2**32: 896 bytes
import numpy as np

def cg(f_Ax, b, cg_iters=10, callback=None, verbose=False, residual_tol=1e-10):
    """
    Demmel p 312
    """
    p = b.copy()
    r = b.copy()
    x = np.zeros_like(b)
    rdotr = r.dot(r)
    fmtstr = '%10i %10.3g %10.3g'
    titlestr = '%10s %10s %10s'
    if verbose:
        print(titlestr % ('iter', 'residual norm', 'soln norm'))
    for i in range(cg_iters):
        if callback is not None:
            callback(x)
        if verbose:
            print(fmtstr % (i, rdotr, np.linalg.norm(x)))
        z = f_Ax(p)
        v = rdotr / p.dot(z)
        x += v * p
        r -= v * z
        newrdotr = r.dot(r)
        mu = newrdotr / rdotr
        p = r + mu * p
        rdotr = newrdotr
        if rdotr < residual_tol:
            break

    if callback is not None:
        callback(x)
    if verbose:
        print(fmtstr % (i + 1, rdotr, np.linalg.norm(x)))
    return x