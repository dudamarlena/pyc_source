# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cdt/causality/pairwise/ANM.py
# Compiled at: 2020-02-05 06:32:12
# Size of source mod 2**32: 6493 bytes
__doc__ = 'Additive Noise Model.\n\nRef : Hoyer, Patrik O and Janzing, Dominik and Mooij, Joris M and Peters, Jonas and Schölkopf, Bernhard,\n  "Nonlinear causal discovery with additive noise models", NIPS 2009\n\n.. MIT License\n..\n.. Copyright (c) 2018 Diviyan Kalainathan\n..\n.. Permission is hereby granted, free of charge, to any person obtaining a copy\n.. of this software and associated documentation files (the "Software"), to deal\n.. in the Software without restriction, including without limitation the rights\n.. to use, copy, modify, merge, publish, distribute, sublicense, and/or sell\n.. copies of the Software, and to permit persons to whom the Software is\n.. furnished to do so, subject to the following conditions:\n..\n.. The above copyright notice and this permission notice shall be included in all\n.. copies or substantial portions of the Software.\n..\n.. THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\n.. IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\n.. FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\n.. AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\n.. LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\n.. OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\n.. SOFTWARE.\n'
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.preprocessing import scale
from .model import PairwiseModel
import numpy as np

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


def normalized_hsic(x, y):
    x = (x - np.mean(x)) / np.std(x)
    y = (y - np.mean(y)) / np.std(y)
    h = FastHsicTestGamma(x, y)
    return h


class ANM(PairwiseModel):
    """ANM"""

    def __init__(self):
        super(ANM, self).__init__()

    def predict_proba(self, data, **kwargs):
        """Prediction method for pairwise causal inference using the ANM model.

        Args:
            dataset (tuple): Couple of np.ndarray variables to classify

        Returns:
            float: Causation score (Value : 1 if a->b and -1 if b->a)
        """
        a, b = data
        a = scale(a).reshape((-1, 1))
        b = scale(b).reshape((-1, 1))
        return self.anm_score(b, a) - self.anm_score(a, b)

    def anm_score(self, x, y):
        """Compute the fitness score of the ANM model in the x->y direction.

        Args:
            a (numpy.ndarray): Variable seen as cause
            b (numpy.ndarray): Variable seen as effect

        Returns:
            float: ANM fit score
        """
        gp = GaussianProcessRegressor().fit(x, y)
        y_predict = gp.predict(x)
        indepscore = normalized_hsic(y_predict - y, x)
        return indepscore