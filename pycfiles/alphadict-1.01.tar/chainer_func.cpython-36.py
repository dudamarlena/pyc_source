# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/tom/.local/miniconda/lib/python3.6/site-packages/alphacsc/other/sdtw/chainer_func.py
# Compiled at: 2019-06-04 04:10:26
# Size of source mod 2**32: 972 bytes
import numpy as np
from chainer import Function
from .soft_dtw import SoftDTW
from .distance import SquaredEuclidean

class SoftDTWLoss(Function):

    def __init__(self, gamma):
        self.gamma = gamma

    def forward_cpu(self, inputs):
        Z, X = inputs
        assert Z.shape[1] == X.shape[1]
        D = SquaredEuclidean(Z, X)
        self.sdtw_ = SoftDTW(D, gamma=(self.gamma))
        loss = self.sdtw_.compute()
        return (
         np.array(loss),)

    def backward_cpu(self, inputs, grad_outputs):
        Z, X = inputs
        g, = grad_outputs
        D = SquaredEuclidean(Z, X)
        E = self.sdtw_.grad()
        gZ = D.jacobian_product(E).astype(Z.dtype)
        return (
         gZ, np.zeros_like(X))