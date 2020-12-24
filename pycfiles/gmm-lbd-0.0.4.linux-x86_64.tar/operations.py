# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/theo/miniconda/lib/python2.7/site-packages/gmm_lbd/operations.py
# Compiled at: 2015-09-21 19:39:09
import numpy as np
from sklearn.utils.extmath import pinvh
from gmm import LbdGMM

def conc(X=None, *gmms):
    """Predict a generalized trajectory from multiple independant constraints.

    Parameters
    ----------
    X : array-like, shape (n_samples, n_features)
        Range of,  regression values
    gmms :

    """
    if 'LbdGMM' in str(type(X)):
        gmms += (X,)
        X = np.empty(0)
        for gmm in gmms:
            X = X if gmm.X_.shape[0] < X.shape[0] else np.linspace(min(gmm.X_[:, 0]), max(gmm.X_[:, 0]), 200)

    all_means = []
    all_covars = []
    for gmm in gmms:
        _, m, c = gmm.regression(X)
        all_means.append(m)
        all_covars.append(c)

    generalized_mean = np.empty_like(all_means[0])
    generalized_covar = np.empty_like(all_covars[0])
    for k in range(X.shape[0]):
        generalized_covar[k] = pinvh(sum([ pinvh(cov[k]) for cov in all_covars ]))
        generalized_mean[k] = generalized_covar[k].dot(sum([ pinvh(cov[k]).dot(means[k]) for cov, means in zip(all_covars, all_means) ]))

    return (X, generalized_mean, generalized_covar)


def influence_gmm(gmm, coef=1.0):
    gmm = gmm.copy()
    gmm.covars_ /= coef
    return gmm


def seq(gmm1, gmm2, wait=0, ver='add'):
    gmm1 = gmm1.copy()
    gmm2 = gmm2.copy()
    if ver == 'add':
        delta = max(gmm1.X_[:, 0]) - min(gmm2.X_[:, 0])
        delta += wait
        gmm2.X_[:, 0] += delta
        gmm2.means_[:, 0] += delta
    elif ver == 'align':
        delta = min(gmm1.X_[:, 0]) - min(gmm2.X_[:, 0])
        delta += wait
        gmm2.X_[:, 0] += delta
        gmm2.means_[:, 0] += delta
    gmm_output = LbdGMM(n_components=gmm1.n_components + gmm2.n_components)
    gmm_output._set_covars(np.concatenate((gmm1._get_covars(), gmm2._get_covars())))
    gmm_output.means_ = np.concatenate((gmm1.means_, gmm2.means_))
    gmm_output.weights_ = np.concatenate((
     gmm1.weights_ * gmm1.n_components / (gmm1.n_components + gmm2.n_components),
     gmm2.weights_ * gmm2.n_components / (gmm1.n_components + gmm2.n_components)))
    gmm_output.X_ = np.concatenate((gmm1.X_, gmm2.X_))
    return gmm_output