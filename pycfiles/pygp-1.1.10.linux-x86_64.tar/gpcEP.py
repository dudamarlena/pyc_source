# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/pygp/gp/gpcEP.py
# Compiled at: 2013-04-10 06:45:39
"""
Class for Gaussian process classification using EP
==================================================

"""
import scipy as SP
from pygp.likelihood.EP import sigmoid
from pygp.gp.gprEP import GPEP
from pygp.likelihood.likelihood_base import GaussLikISO, ProbitLik

class GPCEP(GPEP):
    __slots__ = []

    def __init__(self, *argin, **kwargin):
        likelihood = ProbitLik()
        super(GPCEP, self).__init__(likelihood=likelihood, *argin, **kwargin)
        self.Nep = 3

    def predict(self, *argin, **kwargin):
        """Binary classification prediction"""
        MU, S2 = GPEP.predict(self, *argin, **kwargin)
        Pt = sigmoid(MU / SP.sqrt(1 + S2))
        return [Pt, MU, S2]

    def setData(self, x, y, *args, **kwargin):
        """set Data
        x: inputs [N,D]
        t: targets [N]
        - targets are either -1,+1 or False/True
        """
        assert isinstance(y, SP.ndarray), 'setData requires numpy arrays'
        if y.dtype == 'bool':
            y_ = SP.ones([y.shape[0]])
            y_[y] = +1
            y_[~y] = -1
            y = y_
        else:
            assert len(SP.unique(y)) == 2, 'need either binary inputs or inputs of length 2 for classification'
        GPEP.setData(self, x=x, y=y, *args, **kwargin)