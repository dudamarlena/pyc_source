# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/tom/.local/miniconda/lib/python3.6/site-packages/alphacsc/utils/arma.py
# Compiled at: 2019-06-04 04:10:26
# Size of source mod 2**32: 7854 bytes
import numpy as np
from scipy import signal, linalg, fftpack, fft

class Arma(object):
    """Arma"""

    def __init__(self, ordar=2, ordma=0, block_length=1024, fft_length=None, step=None, wfunc=np.hamming, fs=1.0, donorm=True):
        self.ordar = ordar
        self.ordma = ordma
        self.block_length = block_length
        self.fft_length = fft_length
        self.step = step
        self.wfunc = wfunc
        self.fs = fs
        self.donorm = donorm
        self.psd = []

    def check_params(self):
        if self.block_length <= 0:
            raise ValueError('Block length is negative: %s' % (
             self.block_length,))
        else:
            self.block_length = int(self.block_length)
            if self.fft_length is None:
                fft_length = next_power2(self.block_length)
            else:
                fft_length = int(self.fft_length)
            if not is_power2(fft_length):
                raise ValueError('FFT length should be a power of 2')
            if fft_length < self.block_length:
                raise ValueError('Block length is greater than FFT length')
            if self.step is None:
                step = max(int(self.block_length // 2), 1)
            else:
                step = int(self.step)
            if step <= 0 or step > self.block_length:
                raise ValueError('Invalid step between blocks: %s' % (step,))
        return (fft_length, step)

    def periodogram(self, signals, hold=False, mean_psd=False):
        """
        Computes the estimation (in dB) for each epoch in a signal

        Parameters
        ----------
        signals : array, shape (n_epochs, n_points)
            Signals from which one computes the power spectrum

        hold : boolean, default = False
            If True, the estimation is appended to the list of previous
            estimations, else, the list is emptied and only the current
            estimation is stored.

        mean_psd : boolean, default = False
            If True, the PSD is the mean PSD over all epochs.

        Returns
        -------
        psd : array, shape (n_epochs, n_freq) or (1, n_freq) if mean_psd
            Power spectrum estimated with a Welsh method on each epoch
            n_freq = fft_length // 2 + 1
        """
        fft_length, step = self.check_params()
        signals = np.atleast_2d(signals)
        n_epochs, n_points = signals.shape
        block_length = min(self.block_length, n_points)
        window = self.wfunc(block_length)
        n_epochs, tmax = signals.shape
        n_freq = fft_length // 2 + 1
        psd = np.zeros((n_epochs, n_freq))
        for i, sig in enumerate(signals):
            block = np.arange(block_length)
            count = 0
            while block[(-1)] < sig.size:
                psd[i] += np.abs(fft(window * sig[block], fft_length, 0))[:n_freq] ** 2
                count = count + 1
                block = block + step

            if count == 0:
                raise IndexError('spectrum: first block has %d samples but sig has %d samples' % (
                 block[(-1)] + 1, sig.size))
            if self.donorm:
                scale = 1.0 / (count * np.sum(window) ** 2)
            else:
                scale = 1.0 / count
            psd[i] *= scale

        if mean_psd:
            psd = np.mean(psd, axis=0)[None, :]
        if not hold:
            self.psd = []
        self.psd.append(psd)
        return psd

    def estimate(self, nbcorr=np.nan, numpsd=-1):
        fft_length, _ = self.check_params()
        if np.isnan(nbcorr):
            nbcorr = self.ordar
        else:
            full_psd = self.psd[numpsd]
            full_psd = np.c_[(full_psd, np.conjugate(full_psd[:, :0:-1]))]
            correl = fftpack.ifft(full_psd[0], fft_length, 0).real
            col1 = correl[self.ordma:self.ordma + nbcorr]
            row1 = correl[np.abs(np.arange(self.ordma, self.ordma - self.ordar, -1))]
            R = linalg.toeplitz(col1, row1)
            r = -correl[self.ordma + 1:self.ordma + nbcorr + 1]
            AR = linalg.solve(R, r)
            self.AR_ = AR
            if self.ordma == 0:
                sigma2 = correl[0] + np.dot(AR, correl[1:self.ordar + 1])
                self.MA = np.ones(1) * np.sqrt(sigma2)
            else:
                raise NotImplementedError('arma: estimation of the MA part not yet implemented')

    def arma2psd(self, hold=False):
        """Compute the power spectral density of the ARMA model

        """
        fft_length, _ = self.check_params()
        arpart = np.concatenate((np.ones(1), self.AR_))
        psdar = np.abs(fftpack.fft(arpart, fft_length, 0)) ** 2
        psdma = np.abs(fftpack.fft(self.MA, fft_length, 0)) ** 2
        psd = psdma / psdar
        if not hold:
            self.psd = []
        self.psd.append(psd[None, :fft_length // 2 + 1])

    def inverse(self, sigin):
        """Apply the inverse ARMA filter to a signal

        sigin : input signal (ndarray)

        returns the filtered signal(ndarray)

        """
        arpart = np.concatenate((np.ones(1), self.AR_))
        return signal.fftconvolve(sigin, arpart, 'same')


def ai2ki(ar):
    """Convert AR coefficients to partial correlations
    (inverse Levinson recurrence)

    ar : AR models stored by columns

    returns the partial correlations (one model by column)

    """
    parcor = np.copy(ar)
    ordar, n_epochs, n_points = ar.shape
    for i in range(ordar - 1, -1, -1):
        if i > 0:
            parcor[0:i, :, :] -= parcor[i:i + 1, :, :] * np.flipud(parcor[0:i, :, :])
            parcor[0:i, :, :] *= 1.0 / (1.0 - parcor[i:i + 1, :, :] ** 2)

    return parcor


def ki2ai(parcor):
    """Convert parcor coefficients to autoregressive ones
    (Levinson recurrence)

    parcor : partial correlations stored by columns

    returns the AR models by columns

    """
    ar = np.zeros_like(parcor)
    ordar, n_epochs, n_points = parcor.shape
    for i in range(ordar):
        if i > 0:
            ar[0:i, :, :] += parcor[i:i + 1, :, :] * np.flipud(ar[0:i, :, :])
        ar[i, :, :] = parcor[i, :, :]

    return ar


def is_power2(num):
    """Test if num is a power of 2. (int -> bool)"""
    num = int(num)
    return num != 0 and num & num - 1 == 0


def next_power2(num):
    """Compute the smallest power of 2 >= to num.(float -> int)"""
    return 2 ** int(np.ceil(np.log2(num)))