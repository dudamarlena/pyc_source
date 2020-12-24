# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/piwavelet/smooth.py
# Compiled at: 2020-03-19 11:26:12
# Size of source mod 2**32: 4128 bytes
from __future__ import division
__authors__ = 'Eduardo dos Santos Pereira'
__data__ = '16/06/2015'
__email__ = 'pereira.somoza@gmail.com'
import os
from oct2py import octave
from numpy import zeros, matrix, ceil, log2, pi, exp
from numpy import isreal, ndarray, ma, arange
from numpy.fft import fft, ifft, fftfreq
from scipy.signal import convolve2d
from .piwavelet import cwt, Morlet

def rect(x, normalize=False):
    if type(x) in [int, float]:
        shape = [
         x]
    else:
        if type(x) in [list, dict]:
            shape = x
        else:
            if type(x) in [ndarray, ma.core.MaskedArray]:
                shape = x.shape
    X = zeros(shape)
    X[0] = X[-1] = 0.5
    X[1:-1] = 1
    if normalize:
        X /= X.sum()
    return X


class smooth:
    __doc__ = '\n    This class is an Python interface for the Smoothing matlab\n    functions of the package for wavelet,\n    cross-wavelet and coherence-wavelet analises profided by\n    Aslak Grinsted, John C. Moore and Svetlana Jevrejeva.\n\n    http://noc.ac.uk/using-science/crosswavelet-wavelet-coherence\n\n    However, the Continuous wavelet transform of the signal,\n    in this class, is a pure python\n    function.\n\n    Smoothing as in the appendix of Torrence and Webster\n    "Inter decadal changes in the ENSO-Monsoon System" 1998\n    used in wavelet coherence calculations.\n    Only applicable for the Morlet wavelet.\n    '

    def __init__(self, wave, dt, freqs, dj, scale):
        self.wave = wave
        self.dt = dt
        self.period = 1.0 / freqs
        self.freqs = freqs
        self.dj = dj
        self.scale = scale
        HOME = os.path.expanduser('~')
        mFiles = HOME + '/.piwavelet/wtc/'
        self.wtcPath = octave.addpath(mFiles)

    def __call__(self):
        return self.smoothwavelet()

    def smoothwavelet(self):
        """
        Smoothing as in the appendix of Torrence and Webster
        "Inter decadal changes in the ENSO-Monsoon System" 1998
        used in wavelet coherence calculations.
         Only applicable for the Morlet wavelet.
        """
        swave = octave.smoothwavelet(self.wave, self.dt, self.period, self.dj, self.scale)
        return swave

    def smooth(self):
        """Smoothing function used in coherence analysis."""
        W = self.wave
        m, n = W.shape
        T = zeros([m, n])
        T = matrix(T)
        T = T + complex(0.0, 0.0)
        W = matrix(W)
        npad = int(2 ** ceil(log2(n)))
        k = zeros(npad + 1)
        x = arange(1, int(npad / 2), 1)
        k[1:int(npad / 2)] = x
        k[int(npad / 2) + 2:] = -1 * x[::-1]
        k = 2 * pi * k / npad
        k2 = k ** 2
        snorm = self.scale / self.dt
        for i in range(m):
            F = matrix(exp(-0.5 * snorm[i] ** 2 * k2))
            smooth = ifft(F.T * fft((W[i, :]), n=npad))
            T[i, :] = smooth[0:n]

        if isreal(W).all():
            T = T.real
        wsize = 0.6 / self.dj * 2
        win = rect((int(round(wsize))), normalize=True)
        T = convolve2d(T, win[:, None], 'same')
        return T


if __name__ == '__main__':
    sig = [
     10, 34, 25, 43, 54, 28, 36, 44, 33, 25, 18, 9, 20]
    wave, scales, freqs, coi, fftOut, fftfreqs = cwt(sig, 1, 0.25, -1, -1, Morlet(6.0))
    sm = smooth(wave, 1, freqs, 0.25, scales)
    a = sm.smoothwavelet()
    b = sm.smooth()
    print(a[0])
    print(b[0])