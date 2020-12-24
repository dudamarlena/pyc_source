# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-x86_64/egg/bird/mdct_tools.py
# Compiled at: 2014-10-01 09:19:26
import math, numpy as np
from scipy import linalg
from scipy.fftpack import fft, ifft
import six

def _framing(a, L):
    shape = a.shape[:-1] + (a.shape[(-1)] - L + 1, L)
    strides = a.strides + (a.strides[(-1)],)
    return np.lib.stride_tricks.as_strided(a, shape=shape, strides=strides)[::L // 2].T.copy()


def mdct_waveform(scale, freq_bin):
    L = float(scale)
    K = L / 2.0
    fact = math.sqrt(2.0 / K)
    const_fact = np.pi / K * (float(freq_bin) + 0.5)
    const_offset = (L + 1.0) / 2.0
    f = np.pi / L
    i = np.arange(scale, dtype=np.float)
    wf = fact * np.sin(f * (i + 0.5)) * np.cos(const_fact * (i - K / 2.0 + const_offset))
    return wf / linalg.norm(wf)


def mdct(x, L):
    """Modified Discrete Cosine Transform (MDCT)

    Returns the Modified Discrete Cosine Transform with fixed
    window size L of the signal x.

    The window is based on a sine window.

    Parameters
    ----------
    x : ndarray, shape (N,)
        The signal
    L : int
        The window length

    Returns
    -------
    y : ndarray, shape (L/2, 2 * N / L)
        The MDCT coefficients

    See also
    --------
    imdct
    """
    x = np.asarray(x, dtype=np.float)
    N = x.size
    K = L // 2
    if N % K != 0:
        raise RuntimeError('Input length must be a multiple of the half of the window size')
    xx = np.zeros(L // 4 + N + L // 4)
    xx[(L // 4):(-L // 4)] = x
    x = xx
    del xx
    P = N // K
    if P < 2:
        raise ValueError('Signal too short')
    x = _framing(x, L)
    aL = np.arange(L, dtype=np.float)
    w_long = np.sin(np.pi / L * (aL + 0.5))
    w_edge_L = w_long.copy()
    w_edge_L[:(L // 4)] = 0.0
    w_edge_L[(L // 4):(L // 2)] = 1.0
    w_edge_R = w_long.copy()
    w_edge_R[(L // 2):(L // 2 + L // 4)] = 1.0
    w_edge_R[(L // 2 + L // 4):] = 0.0
    x[:, 0] *= w_edge_L
    x[:, 1:-1] *= w_long[:, None]
    x[:, -1] *= w_edge_R
    x = x.astype(np.complex)
    x *= np.exp(complex(0.0, -1.0) * np.pi / L * aL)[:, None]
    y = fft(x, axis=0)
    y = y[:L // 2, :]
    y *= np.exp(complex(0.0, -1.0) * np.pi * (L // 2 + 1.0) / L * (0.5 + aL[:L // 2]))[:, None]
    y = math.sqrt(2.0 / K) * np.real(y)
    return y


def imdct(y, L):
    """Inverse Modified Discrete Cosine Transform (MDCT)

    Returns the Inverse Modified Discrete Cosine Transform
    with fixed window size L of the vector of coefficients y.

    The window is based on a sine window.

    Parameters
    ----------
    y : ndarray, shape (L/2, 2 * N / L)
        The MDCT coefficients
    L : int
        The window length

    Returns
    -------
    x : ndarray, shape (N,)
        The reconstructed signal

    See also
    --------
    mdct
    """
    N = y.size
    K = L // 2
    if N % K != 0:
        raise ValueError('Input length must be a multiple of the half of the window size')
    P = N // K
    if P < 2:
        raise ValueError('Signal too short')
    temp = y
    y = np.zeros((L, P), dtype=np.float)
    y[:K, :] = temp
    del temp
    aL = np.arange(L, dtype=np.float)
    y = y * np.exp(complex(0.0, 1.0) * np.pi * (L / 2.0 + 1.0) / L * aL)[:, None]
    x = ifft(y, axis=0)
    x *= np.exp(complex(0.0, 1.0) * np.pi / L * (aL + (L / 2.0 + 1.0) / 2.0))[:, None]
    w_long = np.sin(np.pi / L * (aL + 0.5))
    w_edge_L = w_long.copy()
    w_edge_L[:(L // 4)] = 0.0
    w_edge_L[(L // 4):(L // 2)] = 1.0
    w_edge_R = w_long.copy()
    w_edge_R[(L // 2):(L // 2 + L // 4)] = 1.0
    w_edge_R[(L // 2 + L // 4):L] = 0.0
    x[:, 0] *= w_edge_L
    x[:, 1:-1] *= w_long[:, None]
    x[:, -1] *= w_edge_R
    x = math.sqrt(2.0 / K) * L * np.real(x)

    def overlap_add(y, x):
        z = np.concatenate((y, np.zeros((K,))))
        z[-2 * K:] += x
        return z

    x = six.moves.reduce(overlap_add, [ x[:, i] for i in range(x.shape[1]) ])
    x = x[K // 2:-K // 2].copy()
    return x


class MDCT(object):
    """Modified Discrete Cosine Transform (MDCT)

    Supports multiple MDCT dictionaries.

    Parameters
    ----------
    sizes : list of int
        The sizes of MDCT windows e.g. [256, 1024]
    """

    def __init__(self, sizes):
        self.sizes = sizes

    def _dot(self, y):
        cnt = 0
        N = y.size / len(self.sizes)
        x = np.zeros(N)
        for L in self.sizes:
            this_y = y[cnt:cnt + N]
            if np.count_nonzero(this_y) > 0:
                this_x = imdct(np.reshape(this_y, (L // 2, -1)), L)
                x += this_x
            cnt += N

        return x

    def dot(self, y):
        if y.ndim == 1:
            return self._dot(y)
        else:
            return np.array([ self._dot(this_y) for this_y in y ])

    def _doth(self, x):
        return np.concatenate([ mdct(x, L).ravel() for L in self.sizes ])

    def doth(self, x):
        if x.ndim == 1:
            return self._doth(x)
        else:
            return np.array([ self._doth(this_x) for this_x in x ])