# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/tom/.local/miniconda/lib/python3.6/site-packages/alphacsc/other/sdtw/soft_dtw.py
# Compiled at: 2019-06-04 04:10:26
# Size of source mod 2**32: 2639 bytes
import numpy as np
from .soft_dtw_fast import _soft_dtw
from .soft_dtw_fast import _soft_dtw_grad

class SoftDTW(object):

    def __init__(self, D, gamma=1.0, sakoe_chiba_band=-1):
        """
        Parameters
        ----------
        D: array, shape = [m, n] or distance object
            Distance matrix between elements of two time series.

        gamma: float
            Regularization parameter.
            Lower is less smoothed (closer to true DTW).

        sakoe_chiba_band: int
            If non-negative, the DTW is restricted to a Sakoe-Chiba band around
            the diagonal. The band has a width of 2 * sakoe_chiba_band + 1.

        Attributes
        ----------
        self.R_: array, shape = [m + 2, n + 2]
            Accumulated cost matrix (stored after calling `compute`).
        """
        if hasattr(D, 'compute'):
            self.D = D.compute()
        else:
            self.D = D
        self.D = self.D.astype(np.float64)
        self.gamma = gamma
        self.sakoe_chiba_band = sakoe_chiba_band
        if sakoe_chiba_band >= 0:
            if not self.D.shape[0] == self.D.shape[1]:
                raise AssertionError

    def compute(self):
        """
        Compute soft-DTW by dynamic programming.

        Returns
        -------
        sdtw: float
            soft-DTW discrepancy.
        """
        m, n = self.D.shape
        self.R_ = np.zeros((m + 2, n + 2), dtype=(np.float64))
        _soft_dtw((self.D), (self.R_), gamma=(self.gamma), sakoe_chiba_band=(self.sakoe_chiba_band))
        return self.R_[(m, n)]

    def grad(self):
        """
        Compute gradient of soft-DTW w.r.t. D by dynamic programming.

        Returns
        -------
        grad: array, shape = [m, n]
            Gradient w.r.t. D.
        """
        if not hasattr(self, 'R_'):
            raise ValueError('Needs to call compute() first.')
        m, n = self.D.shape
        D = np.vstack((self.D, np.zeros(n)))
        D = np.hstack((D, np.zeros((m + 1, 1))))
        E = np.zeros((m + 2, n + 2))
        _soft_dtw_grad(D, (self.R_), E, gamma=(self.gamma), sakoe_chiba_band=(self.sakoe_chiba_band))
        return E[1:-1, 1:-1]