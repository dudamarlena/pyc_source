# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cdt/independence/graph/HSICLasso.py
# Compiled at: 2020-02-05 06:32:12
# Size of source mod 2**32: 5010 bytes
__doc__ = 'Utils for the HSICLasso implementation.\n\n.. MIT License\n..\n.. Copyright (c) 2018 Diviyan Kalainathan\n..\n.. Permission is hereby granted, free of charge, to any person obtaining a copy\n.. of this software and associated documentation files (the "Software"), to deal\n.. in the Software without restriction, including without limitation the rights\n.. to use, copy, modify, merge, publish, distribute, sublicense, and/or sell\n.. copies of the Software, and to permit persons to whom the Software is\n.. furnished to do so, subject to the following conditions:\n..\n.. The above copyright notice and this permission notice shall be included in all\n.. copies or substantial portions of the Software.\n..\n.. THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\n.. IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\n.. FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\n.. AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\n.. LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\n.. OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\n.. SOFTWARE.\n'
__author__ = 'makotoy'
import numpy as np

def kernel_Delta_norm(xin1, xin2):
    n1 = xin1.shape[1]
    n2 = xin2.shape[1]
    K = np.zeros((n1, n2))
    ulist = np.unique(xin1)
    for ind in ulist:
        c1 = np.sqrt(np.sum(xin1 == ind))
        c2 = np.sqrt(np.sum(xin2 == ind))
        ind1 = np.where(xin1 == ind)[1]
        ind2 = np.where(xin2 == ind)[1]
        K[np.ix_(ind1, ind2)] = 1 / c1 / c2

    return K


def kernel_Delta(xin1, xin2):
    n1 = xin1.shape[1]
    n2 = xin2.shape[1]
    K = np.zeros((n1, n2))
    ulist = np.unique(xin1)
    for ind in ulist:
        ind1 = np.where(xin1 == ind)[1]
        ind2 = np.where(xin2 == ind)[1]
        K[np.ix_(ind1, ind2)] = 1

    return K


def kernel_Gaussian(xin1, xin2, sigma):
    n1 = xin1.shape[1]
    n2 = xin2.shape[1]
    xin12 = np.sum(np.power(xin1, 2), 0)
    xin22 = np.sum(np.power(xin2, 2), 0)
    dist2 = np.tile(xin22, (n1, 1)) + np.tile(xin12, (n2, 1)).transpose() - 2 * np.dot(xin1.T, xin2)
    K = np.exp(-dist2 / (2 * np.power(sigma, 2)))
    return K


def hsiclasso(Xin, Yin, numFeat=5, ykernel='Gauss'):
    d, n = Xin.shape
    H = np.eye(n) - 1.0 / float(n) * np.ones(n)
    XX = Xin / (Xin.std(1)[:, None] + 1e-05)
    if ykernel == 'Gauss':
        YY = Yin / (Yin.std(1)[:, None] + 1e-05)
        L = kernel_Gaussian(YY, YY, 1.0)
    else:
        L = kernel_Delta_norm(Yin, Yin)
    L = np.dot(H, np.dot(L, H))
    X = np.zeros((n * n, d))
    Xty = np.zeros((d, 1))
    for ii in range(0, d):
        Kx = kernel_Gaussian(XX[(ii, None)], XX[(ii, None)], 1.0)
        tmp = np.dot(np.dot(H, Kx), H)
        X[:, ii] = tmp.flatten()
        Xty[ii] = (tmp * L).sum()

    Il = list(range(0, d))
    A = []
    beta = np.zeros((d, 1))
    XtXbeta = np.dot(X.transpose(), np.dot(X, beta))
    c = Xty - XtXbeta
    j = c.argmax()
    C = c[j]
    A.append(j)
    Il.remove(j)
    inc_path = True
    k = 0
    if inc_path:
        path = np.zeros((d, 4 * d))
        lam = np.zeros((1, 4 * d))
        path[:, k] = beta.transpose()
    while float(sum(c[A])) / float(len(A)) >= 1e-09 and len(A) < numFeat + 1:
        tmp = float(sum(c[A])) / float(len(A))
        s = np.ones((len(A), 1))
        w = np.dot(np.linalg.pinv(np.dot(X[:, A].transpose(), X[:, A])), s)
        XtXw = np.dot(X.transpose(), np.dot(X[:, A], w))
        gamma1 = (C - c[Il]) / (XtXw[A[0]] - XtXw[Il])
        gamma2 = -beta[A] / (w + 1e-10)
        gamma3 = np.zeros((1, 1))
        gamma3[0] = c[A[0]] / (XtXw[A[0]] + 1e-10)
        gamma = np.concatenate((np.concatenate((gamma1, gamma2)), gamma3))
        gamma[gamma <= 1e-09] = np.inf
        t = gamma.argmin()
        mu = min(gamma)
        beta[A] = beta[A] + mu * w
        lassocond = 0
        XtXbeta = np.dot(X.transpose(), np.dot(X, beta))
        c = Xty - XtXbeta
        j = np.argmax(c[Il])
        C = max(c[Il])
        k += 1
        if inc_path:
            path[:, k] = beta.transpose()
            if len(C) == 0:
                lam[k] = 0
            else:
                lam[(0, k)] = C[0]
        if lassocond is 0:
            A.append(Il[j])
            Il.remove(Il[j])

    if inc_path:
        path_final = path[:, 0:k + 1]
        lam_final = lam[0:k + 1]
    return (
     path_final, beta, A, lam_final)