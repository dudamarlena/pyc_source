# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: lo/wrappers/fht_lo.py
# Compiled at: 2010-07-02 11:29:53
"""Wrap fast hadamard transform (fht) into LinearOperator instances"""
import numpy as np, fht as fht_mod, lo

def fht(shapein, **kargs):
    """
    Fast Hadamard transform LinearOperator
    """

    def matvec(arr):
        return fht_mod.fht(arr, **kargs)

    return lo.ndoperator(shapein, shapein, matvec=matvec, rmatvec=matvec, dtype=np.float64)