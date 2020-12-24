# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/flame/stats/scale.py
# Compiled at: 2018-05-22 12:10:29
# Size of source mod 2**32: 1630 bytes
import numpy as np

def center(X):
    """Centers the numpy matrix (X) provided as argument"""
    mu = np.mean(X, axis=0)
    return (X - mu, mu)


def scale(X, autoscale):
    """Scales the numpy matrix (X) provided as argument by
       dividing the values by the standard deviation

       The standard deviation is computed as SSX/(N-1)

       Return the scaled matrix and the inverse of the sd (weights)
    """
    nobj, nvar = np.shape(X)
    wg = np.ones(nvar, dtype=(np.float64))
    if not autoscale:
        return (X, wg)
    else:
        st = np.std(X, axis=0, ddof=1)
        for i in range(nvar):
            sti = st[i]
            if sti < 1e-07:
                wg[i] = 0.0
            else:
                wg[i] /= sti

        return (
         X * wg, wg)