# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/obpds/solution.py
# Compiled at: 2015-11-15 13:26:55
import numpy
__all__ = [
 'Solution', 'EquilibriumSolution']

class Solution(object):
    pass


class ParametersSolution(Solution):
    pass


class FlatbandSolution(Solution):

    def __init__(self, T, N, x, Ev, Ec_Gamma, Ec_L, Ec_X, Ec, Ei):
        self.T = T
        self.N = N
        self.x = x
        self.Ev = Ev
        self.Ec_Gamma = Ec_Gamma
        self.Ec_L = Ec_L
        self.Ec_X = Ec_X
        self.Ec = Ec
        self.Ei = Ei


class ZeroCurrentSolution(Solution):

    def __init__(self, V, T, N, x, Na, Nd, Fp, Fn, Ev, Ec_Gamma, Ec_L, Ec_X, Ec, Ei, dEv_dx, dEc_Gamma_dx, dEc_L_dx, dEc_X_dx, dEc_dx, psi, field, n_Gamma, n_L, n_X, n, p):
        self.V = V
        self.T = T
        self.N = N
        self.x = x
        self.Na = Na
        self.Nd = Nd
        self.Fp = Fp
        self.Fn = Fn
        self.Ev = Ev
        self.Ec_Gamma = Ec_Gamma
        self.Ec_L = Ec_L
        self.Ec_X = Ec_X
        self.Ec = Ec
        self.Ei = Ei
        self.dEv_dx = dEv_dx
        self.dEc_Gamma_dx = dEc_Gamma_dx
        self.dEc_L_dx = dEc_L_dx
        self.dEc_X_dx = dEc_X_dx
        self.dEc_dx = dEc_dx
        self.psi = psi
        self.field = field
        self.n_Gamma = n_Gamma
        self.n_L = n_L
        self.n_X = n_X
        self.n = n
        self.p = p


class EquilibriumSolution(ZeroCurrentSolution):

    def __new__(self, zcs):
        zcs.Ef = numpy.zeros(zcs.N)
        return zcs