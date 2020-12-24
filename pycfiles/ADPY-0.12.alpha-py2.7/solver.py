# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ADPY/SOLVER/solver.py
# Compiled at: 2013-11-25 05:46:29
""" 
    Copyright 2013 Oliver Schnabel
    
    This file is part of ADPY.
    ADPY is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    any later version.

    ADPY is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with ADPY.  If not, see <http://www.gnu.org/licenses/>.
"""
from __future__ import division
import numpy as np
from numpy.linalg import norm
from ..ADFUN import adfun

class solver:

    def __init__(self, GLS, x0, x=[], tol=0.0001, maxx=10, algo='leven', SYMPY=False):
        self.x0 = np.array(x0, dtype=float)
        self.sol = None
        self.x = x
        self.tol = tol
        self.maxx = maxx
        self.algo = algo
        if SYMPY == True:
            self.foo_ad = adfun(GLS, (x, x0), SYMPY=True)
        else:
            self.foo_ad = adfun(GLS, x0)
        self.foo_ad.init_forward_jac()
        self.F = self.foo_ad.f
        self.J = self.foo_ad.jac_forward
        return

    def solve(self):
        if self.algo == 'newton':
            print '###############################'
            print '### run newton solver with   ###'
            print '###           ADPY           ###'
            print '###############################'
            self.newton()
        if self.algo == 'gauss':
            print '###############################'
            print '### run gauss solver with   ###'
            print '###           ADPY           ###'
            print '###############################'
            self.gauss()
        if self.algo == 'leven':
            print '###################################'
            print '###  Levenberg-Marquet-Solver   ###'
            print '###           ADPY              ###'
            print '###################################'
            self.leven()
        if self.sol == None:
            print 'Wrong solver'
            return self.x0
        else:
            return self.sol
            return

    def newton(self):
        res = 1
        i = 0
        x0 = self.x0
        f1 = np.matrix(self.F(x0))
        while res > self.tol and self.maxx > i:
            i = i + 1
            j1 = self.J(x0)
            h = np.array(np.linalg.solve(j1, f1.T).flatten())[0]
            x0 -= h
            f1 = np.matrix(self.F(x0))
            res = np.linalg.norm(f1)
            print i, ': ', res

        self.sol = x0

    def gauss(self):
        i = 0
        x = self.x0
        res = 1
        res_alt = 100000000000.0
        while res > self.tol and self.maxx > i and abs(res - res_alt) > self.tol:
            i += 1
            r = np.matrix(self.F(x))
            D = np.matrix(self.J(x))
            DD = np.linalg.solve(D.T * D, D.T * r.T)
            x = np.matrix(x).T - DD
            x = np.array(x.flatten())[0]
            res_alt = res
            res = norm(r)
            print i, ': ', res

        self.sol = x

    def leven(self):
        i = 0
        x = self.x0
        res = 1
        res_alt = 100000000000.0
        ny = 0.1
        b0 = 0.2
        b1 = 0.8
        roh = 0.0
        n = len(self.x0)
        while res > self.tol and self.maxx > i and abs(res - res_alt) > self.tol:
            i += 1
            while roh < b0:
                J = np.matrix(self.J(x))
                F = np.matrix(self.foo_ad.F).T
                normFx = norm(F)
                s = -np.linalg.solve(J.T * J + ny ** 2 * np.eye(n), J.T * F)
                Fxs = self.F(x + np.array(s).flatten())
                roh = (normFx ** 2 - norm(Fxs) ** 2) / (normFx ** 2 - norm(F + J * s) ** 2)
                print 'Roh:', roh
                if roh <= b0:
                    ny = 1.5 * ny
                if roh >= b1:
                    ny = 0.75 * ny
                print 'ny:', ny

            roh = 0.0
            x += np.array(s).flatten()
            res_alt = res
            res = normFx
            print i, ': ', res

        self.sol = x