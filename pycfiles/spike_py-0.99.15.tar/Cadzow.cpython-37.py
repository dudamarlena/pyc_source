# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mad/Documents/spike/spike/Algo/Cadzow.py
# Compiled at: 2020-02-11 03:42:32
# Size of source mod 2**32: 11560 bytes
"""
cadzow.py

Created by Marc-André on 2010-03-18.
Copyright (c) 2010 IGBMC. All rights reserved.
"""
from __future__ import print_function, division
__version__ = '0.1.3'
import numpy as np
import scipy.linalg as lin
import math, sys
debug = False
import unittest, time
if sys.version_info[0] < 3:
    pass
else:
    xrange = range
truncated = True

def as_cpx(arr):
    return arr.view(dtype='complex')


def as_float(arr):
    return arr.view(dtype='float')


def cadzow(data_arg, n_of_line=5, n_of_iter=5, orda=10):
    """ apply the cadzow procedure to remove noise from the current FID.
    should be followed with an FT or an LP-SVD analysis
    
    will return a dataset of the same type (float or cpx) as the input
    
    will do nothing if the data is null
    """
    data = data_arg
    if np.allclose(data, 0.0):
        return data
    orda = min(orda, (data.size + 1) / 2, 4000)
    if debug:
        print('orda :', orda)
        print('processing', data.dtype)
    fid1 = data
    for i in xrange(n_of_iter):
        if debug:
            print('fid1', fid1.dtype, fid1.shape)
        try:
            U, S, Vh = dt2svd(fid1, orda=orda)
        except np.linalg.LinAlgError:
            print('SVD error, exiting iteration loop')
            break

        if debug:
            print('U S V', U.dtype, S.dtype, Vh.dtype)
        S1 = svdclean(S, keep=n_of_line, remove=1)
        if debug:
            print('S1', S1.dtype)
        fid1 = svd2dt(U, S1, Vh)
        if debug:
            print('fid1', fid1.dtype, fid1.shape)

    if data.dtype == 'float':
        fid1 = np.real(fid1)
    return fid1


def cadzow1d(d1D, n_of_line=5, n_of_iter=5, orda=100):
    """
    applies the cadzow procedure to a 1D dataset
    """
    if d1D.axis1.itype == 0:
        d1D.buffer = cadzow(d1D.buffer, n_of_line, n_of_iter, orda)
    else:
        d1D.buffer = as_float(cadzow(as_cpx(d1D.buffer), n_of_line, n_of_iter, orda))


def cadfun(iterelem):
    """utility for cadzow2d - has to be at top level"""
    fid, n_of_line, n_of_iter, orda = iterelem
    if fid.axis1.itype == 0:
        corr = cadzow(fid.buffer, n_of_line, n_of_iter, orda)
    else:
        corr = as_float(cadzow(as_cpx(fid.buffer), n_of_line, n_of_iter, orda))
    return corr


def cadzow2d(d2D, n_of_line=5, n_of_iter=5, orda=100, mp=True, N_proc=None, verbose=1):
    """
    applies the cadzow procedure to all columns of the 2D

    if mp,  does it in a multiprocessing fashion using multiprocessing.Pool()
    if N_proc is None, finds the optimum numer itself.
    verbose = 1 is minimum output, verbose 0 is no output
    """
    if mp:
        import multiprocessing as mproc
    else:
        import itertools as it
        d2D.check2D()
        d1D = d2D.col(0)
        iterlist = it.izip(d2D.xcol(), it.repeat(n_of_line), it.repeat(n_of_iter), it.repeat(orda))
        if mp:
            pool = mproc.Pool(processes=N_proc)
            result = pool.imap(cadfun, iterlist)
        else:
            result = it.imap(cadfun, iterlist)
    for i in xrange(d2D.size2):
        if verbose > 0:
            print('processing column %d / %d' % (i + 1, d2D.size2))
        d1D.buffer = as_float(result.next())
        d1D.check()
        d2D.set_col(i, d1D)

    if mp:
        pool.close()
        pool.join()


cadzow2dmp = cadzow2d

def dt2svd(data, orda=5):
    """computes SVD at order 'orda' from current 1D data (FID)
    data should be a numpy complex 1D array
    
    Calculates the rectangular matrix X(size-order,order) from the data and perform its singular value decomposition.
    This is the first step of the LP-SVD spectral analysis method.
    The same singular value decomposition can be used to perform forward and backward analysis.

    data is untouched

    returns (U, S, Vh)

    see also : svd2dt svdlist svdclean1 svd2ar
    """
    n, = data.shape
    n1 = n - orda + 1
    if n1 < orda:
        raise Exception('orda is too large for this data, orda max : %d' % n / 2)
    else:
        X = np.empty((n1, orda), 'complex_')
        if debug:
            print('Hankel matrix (%d,%d)' % X.shape)
        for i in xrange(n1):
            X[i, :] = data[i:i + orda].copy()

        if truncated:
            U, S, Vh = lin.svd(X, full_matrices=False)
        else:
            U, S, Vh = lin.svd(X)
    return (
     U, S, Vh)


def svd2dt(U, S, V):
    """
    Recalculate the data which would produce the SVD decomposition U S V,
    Does this by approximating the Hankel data matrix x from the svd and u,v

    U S V are untouched,
    
    return data

    see also : dt2svd svdclean svd2ar
    """
    if debug:
        print('########in svd2dt')
    else:
        M = U.shape[0]
        N = V.shape[0]
        size = M + N - 1
        data = np.empty((size,), dtype='complex_')
        if debug:
            print('M, N, size', M, N, size)
        if truncated:
            MN = min(M, N)
            Sig = np.mat(lin.diagsvd(S, MN, MN))
        else:
            Sig = np.mat(lin.diagsvd(S, M, N))
    if debug:
        print('U S V : (%d x %d)  (%d x %d) (%d x %d)' % (U.shape + Sig.shape + V.shape))
    X = U * Sig * V
    Xt = X[::-1, :]
    for k in xrange(size):
        data[k] = np.diag(Xt, k - M + 1).mean()

    if debug:
        print('len(data) at the end of svd2dt ', len(data))
    return data


def svdclean(svd, keep=0, threshold=0, remove=1):
    """
    removes noise related features from a svd spectrum
    two methods available (uses whichever is available (eventually both)):
    keep != 0 : the number of svd to keep
    threshold != 0 : the minimum value to keep
    when remove == 1, the mean power of the removed SVD is removed from the remaining ones
    
    svd is untouched
    """
    svdn = svd.copy()
    if keep != 0:
        svdn[keep:] = 0.0
    if threshold != 0:
        svdn = np.where(svdn < threshold, 0.0, svdn)
    if remove == 1:
        power = np.sum((svd - svdn) ** 2)
        n = len(svd) - len(np.nonzero(svdn)[0])
        if debug:
            print('reduced power : %f' % math.sqrt(power / n))
        if n > 0:
            svdn = np.sqrt((svdn ** 2 - power / n).clip(0.0, svd[0] ** 2))
    return svdn


class CadzowTest(unittest.TestCase):
    __doc__ = '  - Testing Cadzow mathematics - '

    def assertAlmostList(self, a, b, places=7):
        """apply asserAlmostEqual on two list of numbers"""
        for ia, ib in zip(a, b):
            self.assertAlmostEqual(ia, ib, places=places)

    def mfft(self, v):
        """utility that returns the modulus of the fft of v"""
        import scipy.fftpack as fft
        s0 = fft.fft(v)
        s0 = np.real(np.sqrt(s0 * s0.conj()))
        return s0

    def test1D(self):
        """
        ============= a  demo / test of cadzow noise cleaning technique ==============
        applied on an additive noise
        """
        from ..Display import testplot
        plt = testplot.plot()
        print(self.test1D.__doc__)
        LB = 3
        N = 2000
        noise = 30.0
        x = np.arange(N * 1.0) / N
        fid0 = complex(0.0, 1.0) * np.zeros_like(x)
        for i in range(1, 6):
            fid0 += i * 20 * np.exp(2 * i * complex(0.0, 432.1) * x) * np.exp(-LB * x)

        s0 = self.mfft(fid0)
        plt.subplot(3, 1, 1)
        plt.plot(s0, label='initial spectrum')
        plt.legend()
        fid = fid0 + noise * np.random.randn(x.size)
        plt.subplot(3, 1, 2)
        plt.plot((self.mfft(np.exp(-LB * x) * fid)), label='noised (filtered) spectrum')
        plt.legend()
        fidn = np.zeros_like(fid)
        NN = 1
        for i in range(1, NN + 1):
            o = N // 4
            fid1 = cadzow(fid, n_of_line=10, n_of_iter=2, orda=o)
            fidn = fidn + fid1

        spn = self.mfft(fidn) * (1.0 / NN)
        plt.subplot(3, 1, 3)
        plt.plot(spn, label='Cadzow cleaned')
        plt.legend()
        plt.show()
        diff = np.abs(s0 - spn)
        self.assertTrue(np.sum(diff) / N < 2 * noise)
        self.assertTrue(max(diff) < 10000)

    def _test2D(self):
        """
        ==============test for multiprocessing in cazow2d()===============
        This test might fail because svd is multithreaded on MKL, so mp version may actually be slower !!!!
        """
        from .. import NPKData
        import multiprocessing as mproc
        print(self.test2D.__doc__)
        d1 = NPKData._NPKData(buffer=(np.random.rand(500, 200)))
        d1.axis1.itype = 1
        d2 = d1.copy()
        print('one processor')
        t0 = time.time()
        cadzow2d(d2, n_of_line=5, n_of_iter=3, orda=20, mp=False, verbose=0)
        tmono = time.time() - t0
        print('Time : ', tmono)
        d2 = d1.copy()
        N = mproc.cpu_count()
        if N > 1:
            print(N, 'processors')
            if N > 8:
                print('Limiting to 8 proc')
                N = 8
            t0 = time.time()
            cadzow2d(d2, n_of_line=5, n_of_iter=3, orda=20, mp=True, verbose=0, N_proc=N)
            tduo = time.time() - t0
            print('Time : ', tduo)
            self.assertTrue(tduo < tmono)
        else:
            print('test not valid as you have only one processor !')


if __name__ == '__main__':
    unittest.main()