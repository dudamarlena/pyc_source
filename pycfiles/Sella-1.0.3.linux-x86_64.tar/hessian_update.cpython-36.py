# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/sella/hessian_update.py
# Compiled at: 2020-01-27 12:54:08
# Size of source mod 2**32: 3567 bytes
from __future__ import division
import numpy as np
from scipy.linalg import eigh, lstsq, solve

def symmetrize_Y2(S, Y):
    _, nvecs = S.shape
    dY = np.zeros_like(Y)
    YTS = Y.T @ S
    dYTS = np.zeros_like(YTS)
    STS = S.T @ S
    for i in range(1, nvecs):
        RHS = np.linalg.lstsq((STS[:i, :i]), (YTS[i, :i].T - YTS[:i, i] - dYTS[:i, i]),
          rcond=None)[0]
        dY[:, i] = -S[:, :i] @ RHS
        dYTS[i, :] = -STS[:, :i] @ RHS

    return dY


def symmetrize_Y(S, Y, symm):
    if symm is None or S.shape[1] == 1:
        return Y
    else:
        if symm == 0:
            return Y + S @ lstsq(S.T @ S, np.tril(S.T @ Y - Y.T @ S, -1).T)[0]
        if symm == 1:
            return Y + Y @ lstsq(S.T @ Y, np.tril(S.T @ Y - Y.T @ S, -1).T)[0]
        if symm == 2:
            return Y + symmetrize_Y2(S, Y)
    raise ValueError('Unknown symmetrization method {}'.format(symm))


def update_H(B, S, Y, method='TS-BFGS', symm=2, lams=None, vecs=None):
    if len(S.shape) == 1:
        if np.linalg.norm(S) < 1e-08:
            return B
        S = S[:, np.newaxis]
    elif len(Y.shape) == 1:
        Y = Y[:, np.newaxis]
    else:
        Ytilde = symmetrize_Y(S, Y, symm)
        if B is None:
            thetas, _ = eigh(S.T @ Ytilde, S.T @ S)
            lam0 = np.exp(np.average(np.log(np.abs(thetas))))
            d, _ = S.shape
            B = lam0 * np.eye(d)
        if lams is None or vecs is None:
            lams, vecs = eigh(B)
        if method == 'BFGS_auto':
            method = 'TS-BFGS'
            if np.all(lams > 0):
                lams_STY, vecs_STY = eigh(S.T @ Ytilde, S.T @ S)
                if np.all(lams_STY > 0):
                    method = 'BFGS'
        if method == 'BFGS':
            Bplus = _MS_BFGS(B, S, Ytilde)
        else:
            if method == 'TS-BFGS':
                Bplus = _MS_TS_BFGS(B, S, Ytilde, lams, vecs)
            else:
                if method == 'PSB':
                    Bplus = _MS_PSB(B, S, Ytilde)
                else:
                    if method == 'DFP':
                        Bplus = _MS_DFP(B, S, Ytilde)
                    else:
                        if method == 'SR1':
                            Bplus = _MS_SR1(B, S, Ytilde)
                        else:
                            if method == 'Greenstadt':
                                Bplus = _MS_Greenstadt(B, S, Ytilde)
                            else:
                                raise ValueError('Unknown update method {}'.format(method))
    Bplus += B
    Bplus -= np.tril(Bplus.T - Bplus, -1).T
    return Bplus


def _MS_BFGS(B, S, Y):
    return Y @ solve(Y.T @ S, Y.T) - B @ S @ solve(S.T @ B @ S, S.T @ B)


def _MS_TS_BFGS(B, S, Y, lams, vecs):
    J = Y - B @ S
    X1 = S.T @ Y @ Y.T
    absBS = vecs @ (np.abs(lams[:, np.newaxis]) * (vecs.T @ S))
    X2 = S.T @ absBS @ absBS.T
    U = solve((X1 + X2) @ S, X1 + X2).T
    UJT = U @ J.T
    return UJT + UJT.T - U @ (J.T @ S) @ U.T


def _MS_PSB(B, S, Y):
    J = Y - B @ S
    U = solve(S.T @ S, S.T).T
    UJT = U @ J.T
    return UJT + UJT.T - U @ (J.T @ S) @ U.T


def _MS_DFP(B, S, Y):
    J = Y - B @ S
    U = solve(S.T @ Y, Y.T).T
    UJT = U @ J.T
    return UJT + UJT.T - U @ (J.T @ S) @ U.T


def _MS_SR1(B, S, Y):
    YBS = Y - B @ S
    return YBS @ solve(YBS.T @ S, YBS.T)


def _MS_Greenstadt(B, S, Y):
    J = Y - B @ S
    MS = B @ S
    U = solve(S.T @ MS, MS.T).T
    UJT = U @ J.T
    return UJT + UJT.T - U @ (J.T @ S) @ U.T


def _MS_Powell(B, S, Y):
    return (Y - B @ S) @ S.T