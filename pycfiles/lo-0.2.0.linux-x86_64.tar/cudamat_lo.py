# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: lo/wrappers/cudamat_lo.py
# Compiled at: 2010-09-30 09:56:04
"""
Use cudamat to perform faster matrix vector multiplications
"""
import cudamat
from cudamat import CUDAMatrix
import numpy as np, lo

def cudamat_aslinearoperator(a):
    if isinstance(a, np.ndarray):
        a_gpu = CUDAMatrix(a)
    elif isinstance(a, CUDAMatrix):
        a_gpu = a
    else:
        raise ValueError('Expected CUDAMatrix or ndarray')

    def matvec(x):
        if isinstance(x, np.ndarray):
            x.resize((x.size, 1))
            x_gpu = CUDAMatrix(x)
            return cudamat.dot(a_gpu, x_gpu).asarray()
        if isinstance(x, CUDAMatrix):
            x_gpu = x
            return cudamat.dot(a_gpu, x_gpu)
        raise ValueError('Expected CUDAMatrix or ndarray')

    def rmatvec(x):
        if isinstance(x, np.ndarray):
            x.resize((x.size, 1))
            x_gpu = CUDAMatrix(x)
            return cudamat.dot(a_gpu.transpose(), x_gpu).asarray()
        if isinstance(x, CUDAMatrix):
            x_gpu = x
            return cudamat.dot(a_gpu.transpose(), x_gpu)
        raise ValueError('Expected CUDAMatrix or ndarray')

    return lo.LinearOperator(a.shape, matvec, rmatvec, dtype=a.dtype)