# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/pynfold/__init__.py
# Compiled at: 2018-05-17 06:38:11
from __future__ import absolute_import, division, print_function
import numpy as np
from .discretefunctions import f1x, Axy
from .foldFBU import fbu
from .foldIterative import iterative
from .foldInvert import invert
from .foldRegularised import regularised

class fold:

    def __init__(self, npoints=None, xlo=None, xhi=None, iterations=4, data=[], response=[], method='iterative'):
        self.response = response
        self.iterations = iterations
        self.tau = 0.1
        self.data = data
        if npoints and xlo and xhi:
            self.measured = f1x(npoints=npoints, xlo=xlo, xhi=xhi)
            self.truth = f1x(npoints=int(npoints), xlo=xlo, xhi=xhi)
            self.response = Axy(npoints=npoints, xlo=xlo, xhi=xhi)
        self.FilledResponse = False
        self.method = method.lower()

    def run(self):
        if self.FilledResponse and not isinstance(self.response, list):
            self.response_hist = np.matrix(self.response.x, dtype=float)
            truth_hist = np.matrix(self.truth.x)
            response_matrix = np.divide(self.response_hist, truth_hist, out=np.zeros_like(self.response_hist), where=truth_hist != 0)
            self.response = response_matrix.tolist()
        if 'fbu' in self.method:
            upper = []
            lower = []
            for point in self.data:
                if point > 0:
                    upper.append(int(point * 10))
                    lower.append(0)
                else:
                    upper.append(100)
                    lower.append(0)

            upper = (np.ones(len(self.data)) * 3000).tolist()
            lower = np.zeros(len(self.data)).tolist()
            self.fbu = fbu(data=self.data, lower=lower, upper=upper, response=self.response)
            self.fbu()
        if 'iterative' in self.method:
            self.iterative = iterative(self, self.data, self.iterations)
            self.iterative()
        if 'invert' in self.method:
            self.invert = invert(self.response, self.data)
            self.invert()
        if 'regularised' in self.method:
            self.regularised = regularised(self.response, self.data, self.tau)
            self.regularised()

    def fill(self, xr, xt):
        self.FilledResponse = True
        if self.response is None or isinstance(self.response, list):
            print('response matrix parameters not set.')
            print('please call set_response(n_points, x_low, x_high)')
        if isinstance(xr, float) and isinstance(xt, float):
            self.measured.fill(xr)
            self.truth.fill(xt)
            self.response.fill(xr, xt)
        return

    def miss(self, xt):
        self.FilledResponse = True
        if self.response is None or isinstance(self.response, list):
            print('response matrix parameters not set.')
            print('please call set_response(n_points, x_low, x_high)')
        self.truth.fill(xt)
        return

    def set_response(self, npoints, xlo, xhi):
        """
        :rtype: None
        """
        self.xhi = xhi
        self.xlo = xlo
        self.measured = f1x(npoints=npoints, xlo=xlo, xhi=xhi)
        self.truth = f1x(npoints=int(npoints / 2), xlo=xlo, xhi=xhi)
        self.response = Axy(npoints=npoints, xlo=xlo, xhi=xhi)