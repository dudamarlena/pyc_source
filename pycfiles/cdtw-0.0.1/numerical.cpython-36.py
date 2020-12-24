# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cdt/independence/stats/numerical.py
# Compiled at: 2020-02-05 06:32:12
# Size of source mod 2**32: 7415 bytes
__doc__ = 'Dependency criteria for Numerical data.\n\nAuthor: Diviyan Kalainathan\nDate: 1/06/2017\n\n.. MIT License\n..\n.. Copyright (c) 2018 Diviyan Kalainathan\n..\n.. Permission is hereby granted, free of charge, to any person obtaining a copy\n.. of this software and associated documentation files (the "Software"), to deal\n.. in the Software without restriction, including without limitation the rights\n.. to use, copy, modify, merge, publish, distribute, sublicense, and/or sell\n.. copies of the Software, and to permit persons to whom the Software is\n.. furnished to do so, subject to the following conditions:\n..\n.. The above copyright notice and this permission notice shall be included in all\n.. copies or substantial portions of the Software.\n..\n.. THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\n.. IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\n.. FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\n.. AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\n.. LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\n.. OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\n.. SOFTWARE.\n'
import numpy as np, scipy.stats as sp
from .model import IndependenceModel
from sklearn.feature_selection import mutual_info_regression

def rbf_dot2(p1, p2, deg):
    if p1.ndim == 1:
        p1 = p1[:, np.newaxis]
        p2 = p2[:, np.newaxis]
    size1 = p1.shape
    size2 = p2.shape
    G = np.sum((p1 * p1), axis=1)[:, np.newaxis]
    H = np.sum((p2 * p2), axis=1)[:, np.newaxis]
    Q = np.tile(G, (1, size2[0]))
    R = np.tile(H.T, (size1[0], 1))
    H = Q + R - 2.0 * np.dot(p1, p2.T)
    H = np.exp(-H / 2.0 / deg ** 2)
    return H


def rbf_dot(X, deg):
    if X.ndim == 1:
        X = X[:, np.newaxis]
    m = X.shape[0]
    G = np.sum((X * X), axis=1)[:, np.newaxis]
    Q = np.tile(G, (1, m))
    H = Q + Q.T - 2.0 * np.dot(X, X.T)
    if deg == -1:
        dists = (H - np.tril(H)).flatten()
        deg = np.sqrt(0.5 * np.median(dists[(dists > 0)]))
    H = np.exp(-H / 2.0 / deg ** 2)
    return H


def FastHsicTestGamma(X, Y, sig=[
 -1, -1], maxpnt=200):
    """This function implements the HSIC independence test using a Gamma approximation
     to the test threshold. Use at most maxpnt points to save time.

    :param X: contains dx columns, m rows. Each row is an i.i.d sample
    :param Y: contains dy columns, m rows. Each row is an i.i.d sample
    :param sig: [0] (resp [1]) is kernel size for x(resp y) (set to median distance if -1)
    :return: test statistic

    """
    m = X.shape[0]
    if m > maxpnt:
        indx = np.floor(np.r_[0:m:float(m - 1) / (maxpnt - 1)]).astype(int)
        Xm = X[indx].astype(float)
        Ym = Y[indx].astype(float)
        m = Xm.shape[0]
    else:
        Xm = X.astype(float)
        Ym = Y.astype(float)
    H = np.eye(m) - 1.0 / m * np.ones((m, m))
    K = rbf_dot(Xm, sig[0])
    L = rbf_dot(Ym, sig[1])
    Kc = np.dot(H, np.dot(K, H))
    Lc = np.dot(H, np.dot(L, H))
    testStat = 1.0 / m * (Kc.T * Lc).sum()
    if ~np.isfinite(testStat):
        testStat = 0
    return testStat


class PearsonCorrelation(IndependenceModel):
    """PearsonCorrelation"""

    def __init__(self):
        super(PearsonCorrelation, self).__init__()

    def predict(self, a, b):
        """ Compute the test statistic

        Args:
            a (array-like): Variable 1
            b (array-like): Variable 2

        Returns:
            float: test statistic
        """
        return sp.pearsonr(a, b)[0]


class SpearmanCorrelation(IndependenceModel):
    """SpearmanCorrelation"""

    def __init__(self):
        super(SpearmanCorrelation, self).__init__()

    def predict(self, a, b):
        """ Compute the test statistic

        Args:
            a (array-like): Variable 1
            b (array-like): Variable 2

        Returns:
            float: test statistic
        """
        return sp.spearmanr(a, b)[0]


class MIRegression(IndependenceModel):
    """MIRegression"""

    def __init__(self):
        super(MIRegression, self).__init__()

    def predict(self, a, b):
        """ Compute the test statistic

        Args:
            a (array-like): Variable 1
            b (array-like): Variable 2

        Returns:
            float: test statistic
        """
        a = np.array(a).reshape((-1, 1))
        b = np.array(b).reshape((-1, 1))
        return (mutual_info_regression(a, b.reshape((-1, ))) + mutual_info_regression(b, a.reshape((-1, )))) / 2


class KendallTau(IndependenceModel):
    """KendallTau"""

    def __init__(self):
        super(KendallTau, self).__init__()

    def predict(self, a, b):
        """ Compute the test statistic

        Args:
            a (array-like): Variable 1
            b (array-like): Variable 2

        Returns:
            float: test statistic
        """
        a = np.array(a).reshape((-1, 1))
        b = np.array(b).reshape((-1, 1))
        return sp.kendalltau(a, b)[0]


class NormalizedHSIC(IndependenceModel):
    """NormalizedHSIC"""

    def __init__(self):
        super(NormalizedHSIC, self).__init__()

    def predict(self, a, b, sig=[
 -1, -1], maxpnt=500):
        """ Compute the test statistic

        Args:
            a (array-like): Variable 1
            b (array-like): Variable 2
            sig (list): [0] (resp [1]) is kernel size for a(resp b) (set to median distance if -1)
            maxpnt (int): maximum number of points used, for computational time

        Returns:
            float: test statistic
        """
        a = (a - np.mean(a)) / np.std(a)
        b = (b - np.mean(b)) / np.std(b)
        return FastHsicTestGamma(a, b, sig, maxpnt)