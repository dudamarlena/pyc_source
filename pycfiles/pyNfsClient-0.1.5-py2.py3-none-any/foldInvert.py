# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/pynfold/foldInvert.py
# Compiled at: 2018-05-17 07:33:06
from .discretefunctions import f1x
import numpy as np
from scipy.sparse.linalg import lsqr

class invert:

    def __init__(self, response, measured):
        self.response = np.matrix(response)
        try:
            self.measured = f1x(inputarray=measured)
        except Exception as e:
            print e
            print type(measured)
            print 'could not convert that measured histogram'

        self.unfolded = False

    def __call__(self):
        meas = np.asarray(self.measured.x)
        try:
            inverse = np.linalg.inv(self.response)
            self.reco = (inverse * meas.T).T
        except Exception as e:
            print e
            print 'matrix not invertable'
            print 'using least squares'
            self.reco = lsqr(self.response, meas)[0]

        self.unfolded = True

    def reco_hist(self):
        if self.unfolded:
            return self.reco
        else:
            self.__call__()
            return self.reco