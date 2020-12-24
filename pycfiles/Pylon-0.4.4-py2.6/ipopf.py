# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\pylon\ipopf.py
# Compiled at: 2010-12-26 13:36:33
""" Defines an IPOPT OPF solver.
"""
import pyipopt
from numpy import Inf, ones, r_, zeros
from scipy.sparse import vstack, tril
from pylon.solver import PIPSSolver

class IPOPFSolver(PIPSSolver):
    """ Solves AC optimal power flow using IPOPT.
    """

    def _solve(self, x0, A, l, u, xmin, xmax):
        """ Solves using the Interior Point OPTimizer.
        """
        il = [ i for (i, ln) in enumerate(self._ln) if 0.0 < ln.rate_a < 10000000000.0 ]
        nl2 = len(il)
        neqnln = 2 * self._nb
        niqnln = 2 * len(il)
        user_data = {'A': A, 'neqnln': neqnln, 'niqnln': niqnln}
        self._f(x0)
        Jdata = self._dg(x0, False, user_data)
        lmbda = {'eqnonlin': ones(neqnln), 'ineqnonlin': ones(niqnln)}
        H = tril(self._hessfcn(x0, lmbda), format='coo')
        self._Hrow, self._Hcol = H.row, H.col
        n = len(x0)
        xl = xmin
        xu = xmax
        gl = r_[(zeros(2 * self._nb), -Inf * ones(2 * nl2), l)]
        gu = r_[(zeros(2 * self._nb), zeros(2 * nl2), u)]
        m = len(gl)
        nnzj = len(Jdata)
        nnzh = 0
        (f_fcn, df_fcn, g_fcn, dg_fcn, h_fcn) = (
         self._f, self._df, self._g, self._dg, self._h)
        nlp = pyipopt.create(n, xl, xu, m, gl, gu, nnzj, nnzh, f_fcn, df_fcn, g_fcn, dg_fcn)
        success = nlp.solve(x0, user_data)
        nlp.close()

    def _g(self, x, user_data):
        A = user_data['A']
        (h, g) = self._gh(x)
        if A is None:
            b = r_[(g, h)]
        else:
            b = r_[(g, h, A * x)]
        return b

    def _dg(self, x, flag, user_data):
        A = user_data['A']
        (dh, dg) = self._dgh(x)
        if A is None:
            J = vstack([dg.T, dh.T], 'coo')
        else:
            J = vstack([dg.T, dh.T, A], 'coo')
        if flag:
            return (
             J.col, J.row)
        else:
            return J.data
            return

    def _h(self, x, lagrange, obj_factor, flag, user_data=None):
        if flag:
            return (
             self._Hcol, self._Hrow)
        else:
            neqnln = user_data['neqnln']
            niqnln = user_data['niqnln']
            lmbda = {'eqnonlin': lagrange[:neqnln], 'ineqnonlin': lagrange[neqnln:neqnln + niqnln]}
            H = tril(self._hessfcn(x, lmbda), format='coo')
            return H.data