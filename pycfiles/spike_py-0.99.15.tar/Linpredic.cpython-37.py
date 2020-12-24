# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mad/Documents/spike/spike/Algo/Linpredic.py
# Compiled at: 2018-03-06 06:50:32
# Size of source mod 2**32: 6646 bytes
"""
Adaptation of code from :

file              CollombBurg.py
author/translator Ernesto P. Adorio
                  UPDEPP (UP Clark)
                  ernesto.adorio@gmail.com

Version           0.0.1 jun 11, 2010 # first release.
References        Burg's Method, Algorithm and Recursion, pp. 9-11

Created by Lionel on 2011-09-18.
Removed the "for loops" so as to speed up using numpy capabilities.
Copyright (c) 2010 IGBMC. All rights reserved.
"""
from __future__ import print_function
from __future__ import division
import numpy as np, random, time, unittest, sys
if sys.version_info[0] < 3:
    pass
else:
    xrange = range

def predict(data, ar, length):
    """
    returns a vector with additional points, predicted at the end of "data" up to total size "length", using "ar" polynomial
    """
    m = len(ar)
    n = len(data)
    if length <= n:
        raise Exception('values do not allow data extention')
    pred = np.zeros(length, dtype=(data.dtype))
    pred[0:n] = data[0:n]
    for i in xrange(n, length):
        x = np.sum(-ar * pred[i - 1:i - m - 1:-1])
        pred[i] = x

    return pred


def denoise(data, ar):
    """
    returned a denoised version of "data", using "ar" polynomial
    first len(ar) points are untouched.
    """
    m = len(ar)
    filtered = data.copy()
    for i in xrange(m + 1, len(data)):
        filtered[i] = predict(data[:i], ar, i + 1)[i]

    return filtered


def norme(v):
    """simple norme definition"""
    return np.dot(v, v.conjugate()).real


def burgr(m, x):
    """
    Based on Collomb's C++ code, pp. 10-11
    Burgs Method, algorithm and recursion
      m - number of lags in autoregressive model.
      x  - real data vector to approximate.
    """
    N = len(x) - 1
    f = np.array(x[:])
    b = np.array(x[:])
    Ak = np.zeros(m + 1)
    Ak[0] = 1.0
    Dk = 2.0 * (f[:N + 1] ** 2).sum() - (f[0] ** 2 + b[N] ** 2)
    for k in range(m):
        mu = (np.roll(f, -(k + 1)) * b)[:N - k].sum()
        mu *= -2.0 / Dk
        t1 = Ak + mu * np.roll(Ak[::-1], k + 2)
        t2 = mu * Ak + np.roll(Ak[::-1], k + 2)
        limk = (k + 1) // 2
        limkr = k // 2 + 1
        Ak[:limk + 1] = t1[:limk + 1]
        Ak[limk + 1:k + 2] = np.roll(t2[::-1], limkr)[:len(Ak[limk:k + 1])]
        t1 = (np.roll(f, -(k + 1)) + mu * b)[:N - k]
        t2 = (b + mu * np.roll(f, -(k + 1)))[:N - k]
        f[k + 1:N + 1] = t1
        b[:N - k] = t2
        Dk = (1.0 - mu ** 2) * Dk - f[(k + 1)] ** 2 - b[(N - k - 1)] ** 2

    return Ak[1:]


def burgc(lprank, data):
    """
    Based on Gifa code
    Burgs Method, algorithm and recursion
      lprank - number of lags in autoregressive model.
      data  - complex data vector to approximate.
    returns ar, pow1, error
    """
    if lprank == 0:
        raise Exception('lprank cannot be 0')
    m = lprank
    epsilon = 1e-07
    n = len(data)
    ar_ = np.zeros(m, dtype=complex)
    error = 0.0
    pow1 = norme(data)
    den = pow1 * 2
    pow1 = pow1 / n
    if lprank == 0:
        raise Exception('lprank cannot be 0')
    wk1_ = data.copy()
    wk2_ = data.copy()
    ww1 = wk1_.copy()
    ww2 = wk2_.copy()
    temp = 1.0
    for k in range(m):
        num = complex(0.0, 0.0)
        num = np.dot(wk1_[k + 1:n], wk2_[k:n - 1].conjugate())
        den = temp * den - norme(wk1_[k]) - norme(wk2_[(-1)])
        if den == 0.0:
            print('*** Pb with burg : your data may be null')
            return ar_
            save1 = -2.0 * num / den
            temp = 1.0 - norme(save1)
            if temp < epsilon:
                if temp < -epsilon:
                    raise Exception('*** Pb with burg : temp is negative or null')
        else:
            temp = epsilon
        pow1 = pow1 * temp
        ar_[k] = save1
        khalf = (k + 1) // 2
        for j in range(1, khalf + 1):
            kj = k + 1 - j
            save2 = ar_[(j - 1)]
            ar_[j - 1] = save2 + save1 * ar_[(kj - 1)].conjugate()
            if j == kj:
                break
            ar_[kj - 1] = ar_[(kj - 1)] + save1 * save2.conjugate()

        ww1[:] = wk1_[:]
        ww2[:] = wk2_[:]
        wk1_[k:n] = ww1[k:n] + save1 * np.roll(ww2[k:n], 1)
        wk2_[k:n] = np.roll(ww2[k:n], 1) + save1.conjugate() * ww1[k:n]

    return ar_


class LinpredTests(unittest.TestCase):
    __doc__ = ' - Testing linear prediction , Burg algorithm- '

    def setUp(self):
        self.verbose = 1

    def announce(self):
        if self.verbose > 0:
            print('\n========', self.shortDescription(), '===============')

    def curvetest(self):
        longtest = 128
        x = np.arange(longtest)
        original = np.cos(x * 0.01) + 0.75 * np.cos(x * 0.2) + 0.5 * np.cos(x * 0.05) + 0.25 * np.cos(x * 0.11) + 0.1 * np.random.randn(longtest)
        originalj = original + complex(0.0, 1.0) * np.sin(x * 0.01) + complex(0.0, 0.75) * np.sin(x * 0.2) + complex(0.0, 0.5) * np.sin(x * 0.05) + complex(0.0, 0.25) * np.sin(x * 0.11) + complex(0.0, 0.1) * np.random.randn(longtest)
        return (original, originalj)

    def test_burg(self):
        """ - testing burg algo - """
        from ..Display import testplot
        plt = testplot.plot()
        self.announce()
        mlength = 12
        original, originalj = self.curvetest()
        plt.plot(original, label='noisy original')
        coeffs = burgr(mlength, original)
        m = len(coeffs)
        predicted = predict(original, coeffs, 180)
        self.assertEqual(180, len(predicted))
        plt.plot(predicted, label='extended')
        denoised = denoise(original, coeffs)
        self.assertTrue(np.sum(abs(original - denoised)) / np.sum(abs(original)) < 0.2)
        print(np.sum(abs(original - denoised)) / np.sum(abs(original)))
        plt.plot(denoised, label='denoised')
        plt.title('Real')
        plt.legend()
        plt.figure()
        plt.plot((originalj.real), label='noisy original')
        coeffs = burgc(mlength, originalj)
        m = len(coeffs)
        predicted = predict(originalj, coeffs, 180)
        self.assertEqual(180, len(predicted))
        plt.plot((predicted.real), label='extended')
        denoised = denoise(originalj, coeffs)
        self.assertTrue(np.sum(abs(originalj - denoised)) / np.sum(abs(originalj)) < 0.2)
        print(np.sum(abs(originalj - denoised)) / np.sum(abs(originalj)))
        plt.plot((denoised.real), label='denoised')
        plt.title('Complex')
        plt.legend()
        plt.show()


if __name__ == '__main__':
    unittest.main()