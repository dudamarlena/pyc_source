# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/pynfold/foldIterative.py
# Compiled at: 2018-05-17 07:30:16
from .discretefunctions import f1x
import numpy as np

class iterative:

    def __init__(self, thisfold, measured, iterations=4):
        self.fold = thisfold
        try:
            self.measured = f1x(measured)
        except Exception as e:
            print e
            print 'could not convert that measured histogram'

        self.iterations = iterations
        self.unfolded = False

    def __call__(self):
        self.meas = self.measured.x
        self.R = np.asarray(self.fold.response)
        self.truth = self.fold.truth.x
        self.epsilons = np.asarray(self.fold.response_hist).sum(axis=0) / self.truth
        mu = np.asarray([ self.meas.sum() / len(self.truth) for i in range(len(self.truth))
                        ])
        for i in range(self.iterations):
            mu = self.evaluate_mus(mu)

        self.reco = mu
        self.unfolded = True

    def reco_hist(self):
        if self.unfolded:
            return self.reco
        else:
            self.__call__()
            return self.reco

    def evaluate_mus(self, mu):
        p = mu / mu.sum()
        return divide_zeros((divide_zeros(self.R * p, (self.R * p).sum(axis=1)[:, None]) * self.meas[:, None]).sum(axis=0), self.epsilons)


def divide_zeros(A, B):
    return np.divide(A, B, out=np.zeros_like(A), where=B != 0)