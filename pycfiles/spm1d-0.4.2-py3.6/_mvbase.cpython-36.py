# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/spm1d/stats/_mvbase.py
# Compiled at: 2019-08-22 04:37:04
# Size of source mod 2**32: 2097 bytes
from math import sqrt, log
import numpy as np
from scipy import ndimage
from . import _spm
from .. import rft1d
eps = np.finfo(float).eps

def _fwhm(R):
    nComp = R.shape[2]
    W = [rft1d.geom.estimate_fwhm(R[:, :, i]) for i in range(nComp)]
    return np.mean(W)


def _get_residuals_onesample(Y):
    N = Y.shape[0]
    m = Y.mean(axis=0)
    R = Y - np.array([m] * N)
    return R


def _get_residuals_twosample(YA, YB):
    RA = _get_residuals_onesample(YA)
    RB = _get_residuals_onesample(YB)
    return np.vstack((RA, RB))


def _get_residuals_regression(y, x):
    J, Q, I = y.shape
    Z = np.matrix(np.ones(J)).T
    X = np.hstack([np.matrix(x.T).T, Z])
    Xi = np.linalg.pinv(X)
    R = np.zeros(y.shape)
    for i in range(Q):
        for ii in range(I):
            yy = np.matrix(y[:, i, ii]).T
            b = Xi * yy
            eij = yy - X * b
            R[:, i, ii] = np.asarray(eij).flatten()

    return R


def _get_residuals_manova1(Y, GROUP):
    u = np.unique(GROUP)
    R = []
    for uu in u:
        R.append(_get_residuals_onesample(Y[(GROUP == uu)]))

    return np.vstack(R)


def _normalize_residuals(R):
    nCurves, nNodes, nVectDim = R.shape
    for i in range(nCurves):
        mag = np.sqrt((R[i, :, :] ** 2).sum(axis=0))
        R[i, :, :] /= mag
        mag = np.sqrt((R[i, :, :] ** 2).sum(axis=1))
        R[i, :, :] /= np.vstack([mag] * nVectDim).T

    return R


def _resel_counts(R, W, roi=None):
    B = np.any(np.any((np.abs(R) > 0), axis=0), axis=1)
    if roi is not None:
        B = np.logical_and(B, roi)
    mNodes = B.sum()
    mClusters = ndimage.label(B)[1]
    rCounts = []
    rCounts.append(mClusters)
    rCounts.append((mNodes - mClusters) / float(W))
    return rCounts