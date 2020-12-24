# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
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


def cadzow--- This code section failed: ---

 L.  48         0  LOAD_FAST                'data_arg'
                2  STORE_FAST               'data'

 L.  49         4  LOAD_GLOBAL              np
                6  LOAD_METHOD              allclose
                8  LOAD_FAST                'data'
               10  LOAD_CONST               0.0
               12  CALL_METHOD_2         2  ''
               14  POP_JUMP_IF_FALSE    20  'to 20'

 L.  50        16  LOAD_FAST                'data'
               18  RETURN_VALUE     
             20_0  COME_FROM            14  '14'

 L.  51        20  LOAD_GLOBAL              min
               22  LOAD_FAST                'orda'
               24  LOAD_FAST                'data'
               26  LOAD_ATTR                size
               28  LOAD_CONST               1
               30  BINARY_ADD       
               32  LOAD_CONST               2
               34  BINARY_TRUE_DIVIDE
               36  LOAD_CONST               4000
               38  CALL_FUNCTION_3       3  ''
               40  STORE_FAST               'orda'

 L.  52        42  LOAD_GLOBAL              debug
               44  POP_JUMP_IF_FALSE    68  'to 68'

 L.  53        46  LOAD_GLOBAL              print
               48  LOAD_STR                 'orda :'
               50  LOAD_FAST                'orda'
               52  CALL_FUNCTION_2       2  ''
               54  POP_TOP          

 L.  54        56  LOAD_GLOBAL              print
               58  LOAD_STR                 'processing'
               60  LOAD_FAST                'data'
               62  LOAD_ATTR                dtype
               64  CALL_FUNCTION_2       2  ''
               66  POP_TOP          
             68_0  COME_FROM            44  '44'

 L.  55        68  LOAD_FAST                'data'
               70  STORE_FAST               'fid1'

 L.  56        72  LOAD_GLOBAL              xrange
               74  LOAD_FAST                'n_of_iter'
               76  CALL_FUNCTION_1       1  ''
               78  GET_ITER         
             80_0  COME_FROM           234  '234'
               80  FOR_ITER            254  'to 254'
               82  STORE_FAST               'i'

 L.  57        84  LOAD_GLOBAL              debug
               86  POP_JUMP_IF_FALSE   104  'to 104'

 L.  57        88  LOAD_GLOBAL              print
               90  LOAD_STR                 'fid1'
               92  LOAD_FAST                'fid1'
               94  LOAD_ATTR                dtype
               96  LOAD_FAST                'fid1'
               98  LOAD_ATTR                shape
              100  CALL_FUNCTION_3       3  ''
              102  POP_TOP          
            104_0  COME_FROM            86  '86'

 L.  58       104  SETUP_FINALLY       128  'to 128'

 L.  59       106  LOAD_GLOBAL              dt2svd
              108  LOAD_FAST                'fid1'
              110  LOAD_FAST                'orda'
              112  LOAD_CONST               ('orda',)
              114  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              116  UNPACK_SEQUENCE_3     3 
              118  STORE_FAST               'U'
              120  STORE_FAST               'S'
              122  STORE_FAST               'Vh'
              124  POP_BLOCK        
              126  JUMP_FORWARD        166  'to 166'
            128_0  COME_FROM_FINALLY   104  '104'

 L.  60       128  DUP_TOP          
              130  LOAD_GLOBAL              np
              132  LOAD_ATTR                linalg
              134  LOAD_ATTR                LinAlgError
              136  COMPARE_OP               exception-match
              138  POP_JUMP_IF_FALSE   164  'to 164'
              140  POP_TOP          
              142  POP_TOP          
              144  POP_TOP          

 L.  61       146  LOAD_GLOBAL              print
              148  LOAD_STR                 'SVD error, exiting iteration loop'
              150  CALL_FUNCTION_1       1  ''
              152  POP_TOP          

 L.  62       154  POP_EXCEPT       
              156  POP_TOP          
              158  BREAK_LOOP          254  'to 254'
              160  POP_EXCEPT       
              162  JUMP_FORWARD        166  'to 166'
            164_0  COME_FROM           138  '138'
              164  END_FINALLY      
            166_0  COME_FROM           162  '162'
            166_1  COME_FROM           126  '126'

 L.  63       166  LOAD_GLOBAL              debug
              168  POP_JUMP_IF_FALSE   190  'to 190'

 L.  63       170  LOAD_GLOBAL              print
              172  LOAD_STR                 'U S V'
              174  LOAD_FAST                'U'
              176  LOAD_ATTR                dtype
              178  LOAD_FAST                'S'
              180  LOAD_ATTR                dtype
              182  LOAD_FAST                'Vh'
              184  LOAD_ATTR                dtype
              186  CALL_FUNCTION_4       4  ''
              188  POP_TOP          
            190_0  COME_FROM           168  '168'

 L.  64       190  LOAD_GLOBAL              svdclean
              192  LOAD_FAST                'S'
              194  LOAD_FAST                'n_of_line'
              196  LOAD_CONST               1
              198  LOAD_CONST               ('keep', 'remove')
              200  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              202  STORE_FAST               'S1'

 L.  65       204  LOAD_GLOBAL              debug
              206  POP_JUMP_IF_FALSE   220  'to 220'

 L.  65       208  LOAD_GLOBAL              print
              210  LOAD_STR                 'S1'
              212  LOAD_FAST                'S1'
              214  LOAD_ATTR                dtype
              216  CALL_FUNCTION_2       2  ''
              218  POP_TOP          
            220_0  COME_FROM           206  '206'

 L.  66       220  LOAD_GLOBAL              svd2dt
              222  LOAD_FAST                'U'
              224  LOAD_FAST                'S1'
              226  LOAD_FAST                'Vh'
              228  CALL_FUNCTION_3       3  ''
              230  STORE_FAST               'fid1'

 L.  67       232  LOAD_GLOBAL              debug
              234  POP_JUMP_IF_FALSE    80  'to 80'

 L.  67       236  LOAD_GLOBAL              print
              238  LOAD_STR                 'fid1'
              240  LOAD_FAST                'fid1'
              242  LOAD_ATTR                dtype
              244  LOAD_FAST                'fid1'
              246  LOAD_ATTR                shape
              248  CALL_FUNCTION_3       3  ''
              250  POP_TOP          
              252  JUMP_BACK            80  'to 80'

 L.  69       254  LOAD_FAST                'data'
              256  LOAD_ATTR                dtype
              258  LOAD_STR                 'float'
              260  COMPARE_OP               ==
          262_264  POP_JUMP_IF_FALSE   276  'to 276'

 L.  70       266  LOAD_GLOBAL              np
              268  LOAD_METHOD              real
              270  LOAD_FAST                'fid1'
              272  CALL_METHOD_1         1  ''
              274  STORE_FAST               'fid1'
            276_0  COME_FROM           262  '262'

 L.  72       276  LOAD_FAST                'fid1'
              278  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_TOP' instruction at offset 156


def cadzow1d(d1D, n_of_line=5, n_of_iter=5, orda=100):
    """
    applies the cadzow procedure to a 1D dataset
    """
    if d1D.axis1.itype == 0:
        d1D.buffer = cadzowd1D.buffern_of_linen_of_iterorda
    else:
        d1D.buffer = as_float(cadzowas_cpx(d1D.buffer)n_of_linen_of_iterorda)


def cadfun(iterelem):
    """utility for cadzow2d - has to be at top level"""
    fid, n_of_line, n_of_iter, orda = iterelem
    if fid.axis1.itype == 0:
        corr = cadzowfid.buffern_of_linen_of_iterorda
    else:
        corr = as_float(cadzowas_cpx(fid.buffer)n_of_linen_of_iterorda)
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
        d1D = d2D.col0
        iterlist = it.izip(d2D.xcol(), it.repeatn_of_line, it.repeatn_of_iter, it.repeatorda)
        if mp:
            pool = mproc.Pool(processes=N_proc)
            result = pool.imapcadfuniterlist
        else:
            result = it.imapcadfuniterlist
    for i in xrange(d2D.size2):
        if verbose > 0:
            print('processing column %d / %d' % (i + 1, d2D.size2))
        d1D.buffer = as_float(result.next())
        d1D.check()
        d2D.set_colid1D
    else:
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
    X = np.empty(n1, orda)'complex_'
    if debug:
        print('Hankel matrix (%d,%d)' % X.shape)
    for i in xrange(n1):
        X[i, :] = data[i:i + orda].copy()
    else:
        if truncated:
            U, S, Vh = lin.svd(X, full_matrices=False)
        else:
            U, S, Vh = lin.svdX
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
            print'M, N, size'MNsize
        if truncated:
            MN = minMN
            Sig = np.matlin.diagsvd(S, MN, MN)
        else:
            Sig = np.matlin.diagsvd(S, M, N)
    if debug:
        print('U S V : (%d x %d)  (%d x %d) (%d x %d)' % (U.shape + Sig.shape + V.shape))
    X = U * Sig * V
    Xt = X[::-1, :]
    for k in xrange(size):
        data[k] = np.diagXt(k - M + 1).mean()
    else:
        if debug:
            print'len(data) at the end of svd2dt 'len(data)
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
        n = len(svd) - len(np.nonzerosvdn[0])
        if debug:
            print('reduced power : %f' % math.sqrt(power / n))
        if n > 0:
            svdn = np.sqrt(svdn ** 2 - power / n).clip0.0(svd[0] ** 2)
    return svdn


class CadzowTest(unittest.TestCase):
    __doc__ = '  - Testing Cadzow mathematics - '

    def assertAlmostList(self, a, b, places=7):
        """apply asserAlmostEqual on two list of numbers"""
        for ia, ib in zipab:
            self.assertAlmostEqual(ia, ib, places=places)

    def mfft(self, v):
        """utility that returns the modulus of the fft of v"""
        import scipy.fftpack as fft
        s0 = fft.fftv
        s0 = np.realnp.sqrt(s0 * s0.conj())
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
        fid0 = complex(0.0, 1.0) * np.zeros_likex
        for i in range16:
            fid0 += i * 20 * np.exp(2 * i * complex(0.0, 432.1) * x) * np.exp(-LB * x)
        else:
            s0 = self.mfftfid0
            plt.subplot(3, 1, 1)
            plt.plot(s0, label='initial spectrum')
            plt.legend()
            fid = fid0 + noise * np.random.randnx.size
            plt.subplot(3, 1, 2)
            plt.plot((self.mfft(np.exp(-LB * x) * fid)), label='noised (filtered) spectrum')
            plt.legend()
            fidn = np.zeros_likefid
            NN = 1
            for i in range1(NN + 1):
                o = N // 4
                fid1 = cadzow(fid, n_of_line=10, n_of_iter=2, orda=o)
                fidn = fidn + fid1
            else:
                spn = self.mfftfidn * (1.0 / NN)
                plt.subplot(3, 1, 3)
                plt.plot(spn, label='Cadzow cleaned')
                plt.legend()
                plt.show()
                diff = np.abs(s0 - spn)
                self.assertTrue(np.sumdiff / N < 2 * noise)
                self.assertTrue(max(diff) < 10000)

    def _test2D(self):
        """
        ==============test for multiprocessing in cazow2d()===============
        This test might fail because svd is multithreaded on MKL, so mp version may actually be slower !!!!
        """
        from .. import NPKData
        import multiprocessing as mproc
        print(self.test2D.__doc__)
        d1 = NPKData._NPKData(buffer=(np.random.rand500200))
        d1.axis1.itype = 1
        d2 = d1.copy()
        print('one processor')
        t0 = time.time()
        cadzow2d(d2, n_of_line=5, n_of_iter=3, orda=20, mp=False, verbose=0)
        tmono = time.time() - t0
        print'Time : 'tmono
        d2 = d1.copy()
        N = mproc.cpu_count()
        if N > 1:
            printN'processors'
            if N > 8:
                print('Limiting to 8 proc')
                N = 8
            t0 = time.time()
            cadzow2d(d2, n_of_line=5, n_of_iter=3, orda=20, mp=True, verbose=0, N_proc=N)
            tduo = time.time() - t0
            print'Time : 'tduo
            self.assertTrue(tduo < tmono)
        else:
            print('test not valid as you have only one processor !')


if __name__ == '__main__':
    unittest.main()