# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mad/Documents/spike/spike/Algo/SL0_test.py
# Compiled at: 2017-08-31 16:40:33
# Size of source mod 2**32: 10558 bytes
"""

SL0 from http://ee.sharif.ir/~SLzero/

from http://nuit-blanche.blogspot.com/2011/11/how-to-wow-your-friends-in-high-places.html

code from Igor Carron

Authors: Massoud Babaie-Zadeh and Hossein Mohimani
Version: 1.3
Last modified: 4 August 2008.

adapted to numpy by Marc-André on 2011-11-18.
Copyright (c) 2011 IGBMC. All rights reserved.
"""
from __future__ import print_function
import numpy as np
from ..Display import testplot
plt = testplot.plot()
import scipy.fftpack as fft
from scipy.linalg import norm
import time, SL0

def norm(v):
    """frobenius norm"""
    return np.real(np.sqrt(np.sum(v * v.conj())))


def generate(LB=0.0, N=2000, NS=6, noise=30.0):
    x = np.arange(N * 1.0) / N
    fid0 = complex(0.0, 1.0) * np.zeros_like(x)
    for i in range(1, NS + 1):
        fid0 += i * 20 * np.exp(2 * i * complex(0.0, 432.1) * x) * np.exp(-LB * x)

    fidnoise = np.abs(fid0 + noise * np.random.randn(x.size))
    return (fid0, fidnoise)


def test_igor0():
    """
    igor1 modified for my own sake
    """
    M = 200
    N = 5000
    noise = 0.01
    A = np.random.rand(M, N)
    x = np.zeros(N)
    x[23] = 1
    x[140] = 1
    y1 = np.dot(A, x) + noise * np.random.randn(M)
    plt.plot(y1)
    plt.figure()
    plt.plot(x, 'x', label=' original')
    sigma_min = 4e-05
    sdf = 0.95
    x4 = SL0.SL0(A, y1, sigma_min, sdf, true_s=x)
    plt.plot(x4, '+', label='SL0 solution')
    plt.legend()
    plt.show()


def test_igor1():
    """
    from http://nuit-blanche.blogspot.com/2011/11/how-to-wow-your-friends-in-high-places.html
    code from Igor Carron
    """
    M = 200
    N = 5000
    noise = 0.1
    A = np.random.randn(M, N)
    x = np.zeros(N)
    x[23] = 1
    x[140] = 1
    y1 = np.dot(A, x) + noise * np.random.randn(M)
    plt.subplot(2, 2, 1)
    plt.plot(x, 'o')
    plt.title(' original')
    x2 = np.linalg.lstsq(A, y1)[0]
    plt.subplot(2, 2, 2)
    plt.plot(x2, '*')
    plt.title(' using lstsq')
    print(np.dot(A, A.T.conj()).shape)
    A3 = np.dot(A.T.conj(), np.linalg.inv(np.dot(A, A.T.conj())))
    print(A3.shape)
    x3 = np.dot(A3, y1)
    plt.subplot(2, 2, 3)
    plt.plot(x3, '*')
    plt.title(' using pinv')
    plt.subplot(2, 2, 4)
    sigma_min = 4e-05
    sdf = 0.95
    x4 = SL0.SL0(A, y1, sigma_min, sdf)
    plt.plot(x4, '*')
    plt.title(' using SL0 solver')
    plt.show()


def test_igor2():
    """from http://nuit-blanche.blogspot.com/2007/09/compressed-sensing-how-to-wow-your.html """
    n = 512
    x0 = np.zeros(n)
    x0[1] = 2
    x0[2] = 1
    x0[300] = 21
    xx = np.array([1, 4, 6, 12, 54, 69, 75, 80, 89, 132, 133, 152, 178, 230, 300, 340, 356, 400])
    C = np.zeros((len(xx), n))
    for i in range(n):
        C[:, i] = np.sin(i * xx)

    b = np.dot(C, x0)
    print(b)
    sigma_min = 4e-06
    sdf = 0.95
    L = 5
    sol = SL0.SL0(C, b, sigma_min, sdf, L)
    plt.plot(sol, '*', label='solved')
    plt.plot(x0, 'o', label='original')
    plt.legend()
    plt.show()


def build_sampling(N, M, trunc=False):
    if trunc:
        pm = np.arange(N)
    else:
        pm = np.random.permutation(N)
    sample = pm[:M]
    sample.sort()
    print(sample)
    A = np.zeros((M, N))
    for i, s in enumerate(sample):
        A[(i, s)] = 1.0

    return A


def generatesp(N, N_line=10, noise=0):
    spectrum0 = np.zeros(N)
    for i in range(N_line):
        spectrum0[np.random.randint(10, N)] = 1 + i
        s = N_line + 0.5 * N_line * (N_line + 1)

    if noise > 0:
        print('SNR data:', 10 * np.log10(s / noise))
    return (
     spectrum0, noise * np.random.randn(N) + spectrum0)


def generatefid(N, N_line=10, noise=0):
    spectrum0, spectrum = generatesp(N, N_line, noise)
    return (fft.ifft(spectrum0), fft.ifft(spectrum))


def generatefid2(N, N_line=10, noise=0, LB=3):
    x = np.arange(N * 1.0) / N
    fid0 = complex(0.0, 1.0) * np.zeros_like(x)
    for i in range(N_line):
        k = i + 1
        fid0 += k * 20 * np.exp(2 * k * complex(0.0, 432.1) * x) * np.exp(-LB * x)

    if noise > 0:
        print('SNR data:', 10 * np.log10(np.max(np.abs(fid0)) / noise))
    return (
     fid0, fid0 + noise * (np.random.randn(x.size) + complex(0.0, 1.0) * np.random.randn(x.size)))


def em(x, linebroad=1.0, sw=1000.0, limit=100.0):
    if linebroad == 0.0:
        return x
    else:
        size = len(x)
        if linebroad < 0.0:
            a = np.minimum(np.exp(-linebroad * np.arange(size) / sw), limit)
            a[np.where(a >= limit)] = 0.0
        else:
            if linebroad > 0.0:
                a = np.exp(-linebroad * np.arange(size) / sw)
    n = norm(a) / np.sqrt(size)
    print('em:', n)
    return x * a / n


def test_FT(N_line=10):
    M = 300
    N = 5120
    noise = 0.0001
    Mode = 'sampling'
    if Mode == 'random':
        A = np.random.randn(M, N)
    else:
        if Mode == 'truncate':
            A = build_sampling(N, M, trunc=True)
        else:
            if Mode == 'sampling':
                A = build_sampling(N, M)
            else:
                x0, x = generatefid(N, N_line, noise)
                plt.subplot(3, 1, 1)
                plt.plot(fft.fft(x))
                plt.title('noisy original, %d lines' % N_line)
                y1 = np.dot(A, x)
                plt.subplot(3, 1, 2)
                xx = np.zeros(N, 'complex128')
                xx[:M] = x[:M] * np.hanning(M)
                plt.plot(np.abs(fft.fft(xx)))
                plt.subplot(3, 1, 3)
                sigma_min = max(noise / 10, 0.0001)
                sdf = 0.9
                L = 2
                t0 = time.time()
                if Mode == 'random':
                    sol = SL0.SL0FT(A, y1, sigma_min, sdf, L)
                else:
                    sol = SL0.SL0FT(A, y1, sigma_min, sdf, L, A_pinv=(A.T), true_s=(fft.fft(x0)))
            print(time.time() - t0, 'sec')
            plt.plot(sol)
            plt.title('SL0 inversion, noise %.1f %% of smallest peak; sampled at %.1f %%' % (100 * noise, 100.0 * M / N))
            plt.show()


def test_FTgene(N_line=10):
    import functools
    M = 500
    N = 5120
    noise = 0.1
    x0, x = generatefid(N, N_line, noise)
    Mode = 'sampling'
    if Mode == 'random':
        raise 'a faire'
    else:
        if Mode == 'truncate':
            tr = SL0.transformations(N, M, debug=1)
            trans = tr.transform
            ttrans = tr.ttransform
            tr.check()
            y1 = x[0:M]
            print(x.shape, y1.shape, y1.dtype)
        else:
            if Mode == 'sampling':
                tr = SL0.transformations(N, M, debug=0)
                tr.sampling = np.array(sorted(np.random.permutation(N)[:M]))
                trans = tr.transform
                ttrans = tr.ttransform
                tr.check()
                y1 = tr.sample(x)
                print('#########', x.shape, y1.shape, y1.dtype)
            else:
                plt.subplot(3, 1, 1)
                plt.title('noisy original, %d lines, noise at %.1f %% of smallest peak, generated on %d points' % (N_line, 100 * noise, N))
                plt.plot(fft.fft(x))
                plt.subplot(3, 1, 2)
                xx = np.zeros(N, 'complex128')
                xx[:M] = x[:M] * np.hanning(M)
                plt.plot(np.abs(fft.fft(xx)))
                plt.title('best FT using %d points (truncated at %.1f %%)' % (M, 100.0 * M / N))
                plt.subplot(3, 1, 3)
                sigma_min = max(noise / 2, 0.0001)
                sdf = 0.9
                L = 2
                t0 = time.time()
                if Mode == 'random':
                    print('START')
                    sol = SL0.SL0gene(trans, ttrans, y1, sigma_min, sdf, L)
                else:
                    print('START')
                sol = SL0.SL0gene(trans, ttrans, y1, sigma_min, sdf, L, true_s=(fft.fft(x0)))
            print(time.time() - t0, 'sec')
            plt.subplot(3, 1, 3)
            plt.plot(sol)
            plt.title('SL0 inversion, using %d points (sampled at %.1f %% using %s mode)' % (M, 100.0 * M / N, Mode))
            plt.show()


def test_FTgene2(N_line=10):
    from functools import partial
    from util.SignalToNoise import findnoiselevel
    M = 500
    N = 5120
    noise = 0.01
    lb = 10.0
    fid0, fidN = generatefid2(N, N_line, noise=noise, LB=lb)
    Mode = 'sampling'
    tr = SL0.transformations(N, M, debug=0)
    tr.post_ft = partial(em, linebroad=lb)
    tr.tpost_ft = partial(em, linebroad=(-lb))
    if Mode == 'random':
        raise 'a faire'
    else:
        if Mode == 'truncate':
            fid = fidN[:M]
        else:
            if Mode == 'sampling':
                tr.sampling = np.array(sorted(np.random.permutation(N)[:M]))
                fid = tr.sample(fidN)
    tr.check()
    plt.subplot(3, 1, 1)
    plt.title('noisy original, %d lines, noise at %.1f %% of smallest peak, generated on %d points' % (N_line, 100 * noise, N))
    plt.plot(fft.fft(fidN))
    plt.subplot(3, 1, 2)
    plt.plot(fidN)
    plt.title('best FT using %d points (truncated at %.1f %%)' % (M, 100.0 * M / N))
    plt.subplot(3, 1, 3)
    sigma_min = 1
    sdf = 0.95
    L = 5
    t0 = time.time()
    print('START')
    sol = SL0.SL0gene(tr.transform, tr.ttransform, fid, sigma_min, sdf, L)
    print(time.time() - t0, 'sec')
    plt.subplot(3, 1, 3)
    plt.plot(sol)
    plt.title('SL0 inversion, using %d points (sampled at %.1f %% using %s mode)' % (M, 100.0 * M / N, Mode))
    plt.show()


if __name__ == '__main__':
    test_FT(100)