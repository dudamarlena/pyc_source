# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mad/Documents/spike/spike/Algo/BC.py
# Compiled at: 2018-03-06 06:50:32
# Size of source mod 2**32: 9215 bytes
"""
This module contains several utilities for baseline correction of spectra

Created by Marc-Andre on 2015-03-26.

Modification by Lionel 2015-07-10

"""
from __future__ import print_function, division
from scipy.optimize import minimize
import numpy as np
from numpy import pi
import unittest, multiprocessing as mp
from scipy import interpolate

def poly(x, coeff):
    """computes the polynomial over x with coeff"""
    lcoeff = list(coeff)
    y = np.zeros_like(x)
    y += lcoeff.pop()
    while lcoeff:
        y *= x
        y += lcoeff.pop()

    return y


def fitpolyL1(x, y, degree=2, power=1, method='Powell'):
    """fit with L1 norm a polynome to a function y over x, returns coefficients"""
    coeff0 = [
     0] * (degree + 1)
    pmin = lambda c, x, y: np.sum(np.power(np.abs(y - poly(x, c)), power))
    res = minimize(pmin, coeff0, args=(x, y), method=method)
    return res.x


def bcL1(y, degree=2, power=1, method='Powell'):
    """compute a baseline on y using fitpolyL1"""
    x = np.arange(1.0 * y.size)
    coeff = fitpolyL1(x, y, degree=degree, power=power, method=method)
    return poly(x, coeff)


def bcL1_paral(args):
    """
    compute a baseline on y using fitpolyL1 for the parallel case.
    """
    y, degree, power, method = args
    x = np.arange(1.0 * y.size)
    coeff = fitpolyL1(x, y, degree=degree, power=power, method=method)
    return poly(x, coeff)


def baseline0(y, degree=2, power=1, method='Powell', chunksize=2000, nbcores=None, ratiocov=0.7):
    """
    compute a piece-wise baseline on y using fitpolyL1
    degree :  is the degree of the underlying polynome
    power : norm for the approximation
    chunksize :  defines the size of the pieces. 
    nbcores : number of cores used for parallelization of the calculations.
    ratiocov : covering ratio of the chunks
    y - baseline(y) produces a baseline corrected spectrum
    """

    def approx_BL_parallel():
        for k, estimate in enumerate(res):
            s0 = slice((k + 1) * lsize - cov, (k + 2) * lsize + cov)
            scov0 = slice((k + 1) * lsize - cov, (k + 1) * lsize + cov)
            scov1 = slice((k + 1) * lsize + cov, (k + 2) * lsize + cov)
            tbl = estimate
            bl[scov0] = tbl[:2 * cov] * corr + bl[scov0] * corrm1
            bl[scov1] = tbl[2 * cov:]

    def approx_BL_serial():
        for i in range(1, nchunk - 1):
            tbl = bcL1((y[i * lsize - cov:(i + 1) * lsize + cov]), degree=degree, power=power)
            bl[i * lsize - cov:i * lsize + cov] = bl[i * lsize - cov:i * lsize + cov] * corrm1 + tbl[:2 * cov] * corr
            bl[i * lsize + cov:(i + 1) * lsize + cov] = tbl[2 * cov:]

    nchunk = y.size // chunksize
    if nchunk < 2:
        bl = bcL1(y, degree=degree, power=power, method=method)
    else:
        lsize = y.size // nchunk
        cov = int(lsize * ratiocov)
        corr = np.linspace(0.0, 1.0, 2 * cov)
        corrm1 = 1.0 - corr
        bl = np.zeros_like(y)
        bl[0:lsize + cov] = bcL1((y[0:lsize + cov]), degree=degree, power=power)
        i = 0
        if nbcores:
            p = mp.Pool(nbcores)
            args = iter([[y[i * lsize - cov:(i + 1) * lsize + cov], degree, power, method] for i in range(1, nchunk - 1)])
            res = p.imap(bcL1_paral, args)
            approx_BL_parallel()
            p.close()
        else:
            approx_BL_serial()
        i = nchunk - 1
        tbl = bcL1((y[i * lsize - cov:-1]), degree=degree, power=power)
        bl[i * lsize - cov:i * lsize + cov] = bl[i * lsize - cov:i * lsize + cov] * corrm1 + tbl[:2 * cov] * corr
        bl[i * lsize + cov:] = tbl[2 * cov - 1:]
    return bl


def baseline1(y, degree=2, chunksize=2000):
    """
    compute a piece-wise baseline on y using fitpolyL1
    degree is the degree of the underlying polynome
    chunksize defines the size of the pieces
    a cosine roll-off is used to smooth out chunks junctions

    y - baseline(y) produces a baseline corrected spectrum
    """
    nchunk = y.size // chunksize
    if nchunk < 2:
        bl = bcL1(y, degree=degree)
    else:
        lsize = y.size // nchunk
        recov = lsize // 10
        corr = np.linspace(0.0, 1.0, 2 * recov)
        corr = np.sin(np.linspace(0, np.pi / 2, 2 * recov)) ** 2
        corrm1 = 1.0 - corr
        bl = np.zeros_like(y)
        bl[0:lsize + recov] = bcL1((y[0:lsize + recov]), degree=degree)
        i = 0
        for i in range(1, nchunk - 1):
            tbl = bcL1((y[i * lsize - recov:(i + 1) * lsize + recov]), degree=degree)
            bl[i * lsize - recov:i * lsize + recov] = bl[i * lsize - recov:i * lsize + recov] * corrm1 + tbl[:2 * recov] * corr
            bl[i * lsize + recov:(i + 1) * lsize + recov] = tbl[2 * recov:]

        i = i + 1
        tbl = bcL1((y[i * lsize - recov:-1]), degree=degree)
        bl[i * lsize - recov:i * lsize + recov] = bl[i * lsize - recov:i * lsize + recov] * corrm1 + tbl[:2 * recov] * corr
        bl[i * lsize + recov:] = tbl[2 * recov - 1:]
    return bl


def correctbaseline(y, iterations=1, nbchunks=100, firstpower=0.3, secondpower=7, degree=1, chunkratio=1.0, interv_ignore=None, method='Powell', nbcores=None, debug=False, choiceBL=0, ratiocov=0.7):
    """
    Find baseline by using low norm value and then high norm value to attract the baseline on the small values.
    Parameters : 
    iterations : number of iterations for convergence toward the small values. 
    nbchunks : number of chunks on which is done the minimization. Typically, each chunk must be larger than the peaks. 
    firstpower : norm used for the first iterate
    secondpower : norm used for attracting the curve toward the lowest values. 
    firstdeg : degree used for the first minimization 
    degree : degree of the polynome used for approaching each signal chunk. 
    chunkratio : ratio for changing the chunksize inside main loop
    interv_ignore : ignore a given intervall in the spectrum (eg : avoids issues with water pick)
    method : Algorithm used for minimization on each chunk
    nbcores : number of cores used for minimizing in parallel on many chunks (if not None)
    debug : if debug is set to True, the dictionary bls is built
    ratiocov : covering ratio of the chunks. High recovering ratios seem to give better results. By default ratiocov = 0.7
    """
    if choiceBL == 0:
        baseline = baseline0
    else:
        if choiceBL == 1:
            baseline = baseline1
        else:
            raise Exception('error with choiceBL')
    if interv_ignore:
        ii = interv_ignore
        delta = ii[1] - ii[0]
        y[ii[0]:ii[1]] = y[ii[0]] + np.arange(delta) / float(delta) * (y[ii[1]] - y[ii[0]])
    chunksize = y.size // nbchunks
    bl = baseline(y, degree=degree, power=firstpower, chunksize=chunksize, nbcores=nbcores, method='Powell', ratiocov=ratiocov)
    bls = {'bl':[],  'blmin':[]}
    for i in range(iterations):
        blmin = np.minimum.reduce([bl, y])
        bl = baseline(blmin, degree=degree, power=secondpower, chunksize=(int(chunksize * chunkratio)),
          nbcores=nbcores,
          method=method,
          ratiocov=ratiocov)
        bls['bl'].append(bl)
        bls['blmin'].append(blmin)

    if debug:
        return (
         bl, bls)
    return bl


class BC_Tests(unittest.TestCase):

    def test_poly(self):
        """tests the poly function"""
        p = poly(np.arange(10.0), (0.1, 0.2, 0.3, 0.4))
        self.assertEqual(p[6], 98.5)
        self.assertAlmostEqual(sum(p), 905.5)

    def test_baseline0(self):
        N = 100000
        x = np.linspace(0, 10, N)
        y = np.sin(x / 2) + 0.2 * np.random.randn(N)
        b = baseline0(y, chunksize=(N // 20))
        corr = y - b
        self.assertTrue(np.std(corr) < 0.21)

    def test_baseline1(self):
        N = 100000
        x = np.linspace(0, 10, N)
        y = np.sin(x / 2) + 0.2 * np.random.randn(N)
        b = baseline1(y, chunksize=(N // 20))
        corr = y - b
        self.assertTrue(np.std(corr) < 0.21)

    def _test_correctbaseline(self):
        N = 100000
        x = np.linspace(0, 10, N)
        y = np.sin(x / 2) + 0.2 * np.random.randn(N)
        b = correctbaseline(y, iterations=10, nbchunks=20)
        corr = y - b
        self.assertTrue(np.std(corr) < 0.25)


if __name__ == '__main__':
    unittest.main()