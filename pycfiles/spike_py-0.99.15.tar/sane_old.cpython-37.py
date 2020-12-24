# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mad/Documents/spike/spike/Algo/sane_old.py
# Compiled at: 2018-11-26 15:09:15
# Size of source mod 2**32: 26373 bytes
"""
sane.py
#########
Algorithm for denoising time series, named sane (standing for "Support Selection for Noise Elimination")

main function is 
sane(data, rank)
data : the series to be denoised
rank : the rank of the analysis

Copyright (c) 2015 IGBMC. All rights reserved.
Marc-Andr'e Delsuc <madelsuc@unistra.fr>
Lionel Chiron <lionel.chiron@gmail.com>

This software is a computer program whose purpose is to compute sane denoising.

This software is governed by the CeCILL  license under French law and
abiding by the rules of distribution of free software.  You can  use, 
modify and/ or redistribute the software under the terms of the CeCILL
license as circulated by CEA, CNRS and INRIA at the following URL
"http://www.cecill.info". 

As a counterpart to the access to the source code and  rights to copy,
modify and redistribute granted by the license, users are provided only
with a limited warranty  and the software's author,  the holder of the
economic rights,  and the successive licensors  have only  limited
liability. 

In this respect, the user's attention is drawn to the risks associated
with loading,  using,  modifying and/or developing or reproducing the
software by the user in light of its specific status of free software,
that may mean  that it is complicated to manipulate,  and  that  also
therefore means  that it is reserved for developers  and  experienced
professionals having in-depth computer knowledge. Users are therefore
encouraged to load and test the software's suitability as regards their
requirements in conditions enabling the security of their systems and/or 
data to be ensured and,  more generally, to use and operate it in the 
same conditions as regards security. 

The fact that you are presently reading this means that you have had
knowledge of the CeCILL license and that you accept its terms.

First Created by Lionel Chiron and Marc-Andr'e on september 2015.

associated publications
- Bray, F., Bouclon, J., Chiron, L., Witt, M., Delsuc, M.-A., & Rolando, C. (2017).
  Nonuniform Sampling Acquisition of Two-Dimensional Fourier Transform Ion Cyclotron Resonance Mass Spectrometry for Increased Mass Resolution of Tandem Mass Spectrometry Precursor Ions.
  Analytical Chemistry, acs.analchem.7b01850. http://doi.org/10.1021/acs.analchem.7b01850

"""
from __future__ import print_function, division
import numpy as np
import numpy.linalg as linalg
from numpy.fft import fft, ifft
import unittest, time
from scipy.linalg import norm
from math import sqrt
from util.signal_tools import findnoiselevel, mfft, mrfft
debug = 0

def _next_regular(target):
    """
    Find the next regular number greater than or equal to target.
    Regular numbers are composites of the prime factors 2, 3, and 5.
    Also known as 5-smooth numbers or Hamming numbers, these are the optimal
    size for inputs to FFTPACK.

    Target must be a positive integer.
    """
    if target <= 6:
        return target
    else:
        return target & target - 1 or target
    match = float('inf')
    p5 = 1
    while p5 < target:
        p35 = p5
        while p35 < target:
            quotient = -(-target // p35)
            try:
                p2 = 2 ** (quotient - 1).bit_length()
            except AttributeError:
                p2 = 2 ** (len(bin(quotient - 1)) - 2)

            N = p2 * p35
            if N == target:
                return N
            if N < match:
                match = N
            p35 *= 3
            if p35 == target:
                return p35

        if p35 < match:
            match = p35
        p5 *= 5
        if p5 == target:
            return p5

    if p5 < match:
        match = p5
    return match


def sane(data, k, orda=None, iterations=1, trick=True, optk=False, ktrick=False):
    """ 
    sane algorithm. Name stands for Support Selection for Noise Elimination.
    From a data series return a denoised series denoised
    data : the series to be denoised - a (normally complex) numpy buffer
    k : the rank of the analysis
    orda : is the order of the analysis
        internally, a Hankel matrix (M,N) is constructed, with M = orda and N = len(data)-orda+1
        if None (default) orda = (len(data)+1)/2
    iterations : the number of time the operation should be repeated
    optk : if set to True will calculate the rank giving the best recovery for an automatic estimated noise level. 
    trick : permits to enhanced the denoising by using a cleaned signal as the projective space. "Support Selection"
    ktrick : if a value is given, it permits to change the rank on the second pass.
             The idea is that for the first pass a rank large enough as to be used to compensate for the noise while
             for the second pass a lower rank can be used. 
    
    ########
    values are such that
    orda <= (len(data)+1)//2
    k < orda
    N = len(data)-orda+1
    Omega is (N x k)
    
    Sane is based on the same idea than urQRd, however, there is a much clever selection of the basis on which the random projection is performed.
    This allows a much better recovery of small signals buried into the noise, compared to urQRd.
    
    the flags trick, optk, ktrick control the program
    when all are false, sane folds back to urQRd algorithm.
    Optimal is certainly trick = True, optk = True, ktrick = True  but not fully tested yet.

    ##########
    sane uses a new trick for performing a better denoising.
    A rank a little above the number of peaks as to be given. 
    this permit to make a filtering matrix containing the signal quasi only after a first pass.
    On a second pass the full signal is projected on a new filtering subspace done from preceding denoising.
    A higher number of iterations will decrease even more the smallest amplitudes. 
    ##########
    """
    if not orda:
        orda = data.size // 2
    else:
        if optk:
            optrank = OPTK(data, orda)
            k = optrank.find_best_rank()
        if np.allclose(data, 0.0):
            return data
        L = len(data)
        if L > 340:
            Lr = _next_regular(L)
            orda_r = 2 * Lr - _next_regular(2 * Lr - orda)
            if debug > 0:
                if L != Lr or orda != orda_r:
                    print('SANE regularisation %d %d => %d %d' % (L, orda, Lr, orda_r))
                else:
                    Lr = L
                    orda_r = orda
            if L != Lr:
                data_r = np.concatenate((data, np.zeros(Lr - L)))
        else:
            data_r = data
    if 2 * orda_r > data_r.size:
        raise Exception('order is too large')
    if k >= orda_r:
        raise Exception('rank is too large, or orda is too small')
    N = len(data_r) - orda_r + 1
    dd = data_r.copy()
    for i in range(iterations + 1):
        if i == 1:
            if ktrick:
                Omega = np.random.normal(size=(N, ktrick))
            else:
                Omega = np.random.normal(size=(N, k))
            if i == 1:
                if trick:
                    dataproj = data_r.copy()
                else:
                    dataproj = dd.copy()
                if trick:
                    Q, QstarH = saneCore(dd, dataproj, Omega)
                    dd = Fast_Hankel2dt(Q, QstarH)
            elif i != 1:
                Q, QstarH = trick or saneCore(dd, dataproj, Omega)
                dd = Fast_Hankel2dt(Q, QstarH)

    denoised = dd
    if data.dtype == 'float':
        denoised = np.real(denoised)
    return denoised[:L]


def saneCore(dd, data, Omega):
    """
    Core of sane algorithm
    """
    Y = FastHankel_prod_mat_mat(dd, Omega)
    Q, r = linalg.qr(Y)
    del r
    QstarH = FastHankel_prod_mat_mat(data.conj(), Q).conj().T
    return (Q, QstarH)


def vec_mean(M, L):
    """
    Vector for calculating the mean from the sum on the antidiagonal.
    data = vec_sum*vec_mean
    """
    vec_prod_diag = [1 / float(i + 1) for i in range(M)]
    vec_prod_middle = [1 / float(M) for i in range(L - 2 * M)]
    vec_mean_prod_tot = vec_prod_diag + vec_prod_middle + vec_prod_diag[::-1]
    return np.array(vec_mean_prod_tot)


def FastHankel_prod_mat_mat(gene_vect, matrix):
    """
    Fast Hankel structured matrix matrix product based on FastHankel_prod_mat_vec
    """
    N, K = matrix.shape
    L = len(gene_vect)
    M = L - N + 1
    data = np.zeros(shape=(M, K), dtype=complex)
    for k in range(K):
        prod_vect = matrix[:, k]
        data[:, k] = FastHankel_prod_mat_vec(gene_vect, prod_vect)

    return data


def FastHankel_prod_mat_vec(gene_vect, prod_vect):
    """
    Compute product of Hankel matrix (gene_vect)  by vector prod_vect.
    H is not computed
    M is the length of the result
    """
    L = len(gene_vect)
    N = len(prod_vect)
    M = L - N + 1
    prod_vect_zero = np.concatenate((np.zeros(M - 1), prod_vect[::-1]))
    fft0, fft1 = fft(gene_vect), fft(prod_vect_zero)
    prod = fft0 * fft1
    c = ifft(prod)
    return np.roll(c, 1)[:M]


def Fast_Hankel2dt(Q, QH):
    """
    returning to data from Q and QstarH
    Based on FastHankel_prod_mat_vec.
    """
    M, K = Q.shape
    K, N = QH.shape
    L = M + N - 1
    vec_sum = np.zeros((L,), dtype=complex)
    for k in range(K):
        prod_vect = QH[k, :]
        gene_vect = np.concatenate((np.zeros(N - 1), Q[:, k], np.zeros(N - 1)))
        vec_k = FastHankel_prod_mat_vec(gene_vect, prod_vect[::-1])
        vec_sum += vec_k

    datadenoised = vec_sum * vec_mean(M, L)
    return datadenoised


class OPTK(object):
    __doc__ = '\n    Class for finding the best rank for classical sane.\n    The rank is calculated so as to permit the retrieving of the signal power at high enough level.\n    Passed parameters are the Fid "fid", the estimated number of lines "estim_nbpeaks" and the order "orda"\n    '

    def __init__(self, fid, orda, prec=0.9, debug=False):
        self.norm_show = False
        self.list_xis = []
        self.list_xin = []
        self.psig = 0
        self.pnoise = 0
        self.fid = fid
        self.xis = 0
        self.xin = 0
        self.above_noise = 4
        self.step_k = 20
        self.list_sane_norm = []
        self.estim_nbpeaks = None
        self.orda = orda
        self.prec = prec
        self.debug = debug

    def subspace_filling_with_rank(self):
        """
        Estimation of the signal and noise subspace filling in function of the rank.
        """
        self.separate_signal_from_noise()
        M = self.orda - self.estim_nbpeaks
        self.psig = norm(self.spec_trunc) ** 2
        self.pnoise = norm(self.spec - self.spec_trunc) ** 2
        for i in range(self.orda):
            empty = self.psig * (1 - self.xis) ** 2 + self.pnoise * (1 - self.xin) ** 2
            self.xis += self.psig * (1 - self.xis) ** 2 // empty // self.estim_nbpeaks
            self.xin += self.pnoise * (1 - self.xin) ** 2 // empty // M
            self.list_xis.append(self.xis)
            self.list_xin.append(self.xin)

    def separate_signal_from_noise(self):
        """
        Signal is separated from Noise and kept in self.spec
        self.noiselev : level of the noise
        self.estim_nbpeaks : estimation of the number of peaks in the spectrum
        """
        if self.fid.dtype == 'complex':
            self.spec = mfft(self.fid)
            if self.debug:
                print('complex fid')
        elif self.fid.dtype == 'float':
            self.spec = mrfft(self.fid)
            if self.debug:
                print('real fid')
        self.spec_trunc = self.spec.copy()
        self.noiselev = findnoiselevel((self.spec), nbseg=10)
        nbseg = 20
        less = len(self.spec) % nbseg
        restpeaks = self.spec[less:]
        mean_level = restpeaks.mean()
        self.noiselev += mean_level
        if self.debug:
            print('noiseleve found is ', self.noiselev)
        self.spec_trunc[self.spec < self.above_noise * self.noiselev] = 0
        peaks = self.peaks1d((self.spec), threshold=(self.above_noise * self.noiselev))
        self.estim_nbpeaks = len(peaks)
        if self.debug:
            print('self.estim_nbpeaks ', self.estim_nbpeaks)
            print('self.above_noise*self.noiselev ', self.above_noise * self.noiselev)

    def find_best_rank(self):
        """
        Finds the optimal rank
        optk : optimal rank
        """
        self.subspace_filling_with_rank()
        diff = abs(np.array(self.list_xis) - self.prec)
        minval = diff.min()
        optk = list(diff).index(minval)
        if self.debug:
            print('optimal rank is ', optk)
        return optk

    def peaks1d(self, fid, threshold=0.1):
        """
        Extracts peaks from 1d from FID
        Returns listpk[0]
        """
        listpk = np.where((fid > threshold * np.ones(fid.shape)) & (fid > np.roll(fid, 1, 0)) & (fid > np.roll(fid, -1, 0)))
        return listpk[0]


def test_sane_gene(lendata=10000, rank=100, orda=4000, nbpeaks=2, noise=50.0, noisetype='additive', nb_iterat=1, trick=False):
    """
    ============== example of use of sane on a synthetic data-set ===============
    """
    from ..Display import testplot
    plt = testplot.plot()
    from util.dynsubplot import subpl
    from util.signal_tools import fid_signoise, fid_signoise_type, SNR_dB, mfft
    superimpose = False
    nb_iterat = nb_iterat
    print('=== Running rQR algo ===', end=' ')
    print('lendata:', lendata, end=' ')
    print(' orda:', orda, end=' ')
    print(' rank:', rank)
    data = fid_signoise_type(nbpeaks, lendata, noise, noisetype)
    fdatanoise = mfft(data)
    noise = 0
    data0 = fid_signoise_type(nbpeaks, lendata, noise, noisetype)
    fdata = mfft(data0)
    iSNR = SNR_dB(data, data0)
    print('Initial Noisy Data SNR: %.2f dB - noise type : %s' % (iSNR, noisetype))
    t0 = time.time()
    datasane = sane(data, k=rank, orda=orda, optk=False, iterations=nb_iterat, trick=trick)
    tsane = time.time() - t0
    fdatasane = mfft(datasane)
    print('=== Result ===')
    fSNR = SNR_dB(datasane, data0)
    print('Denoised SNR: %.2f dB  - processing gain : %.2f dB' % (fSNR, fSNR - iSNR))
    print('processing time for sane : %f sec' % tsane)
    print(fSNR - iSNR)
    sub = subpl(2, plt)
    sub.next()
    sub.plot(data0, 'b', label='clean signal')
    sub.title('data series')
    sub.next()
    sub.plot(fdata, 'b', label='clean spectrum')
    sub.title('FFT spectrum')
    sub.next()
    sub.plot(data, 'k', label='noisy signal')
    sub.next()
    if superimpose:
        sub.plot(fdatasane, 'r', label=('sane {} iteration(s)'.format(nb_iterat)))
    sub.plot(fdatanoise, 'k', label='noisy spectrum')
    sub.next()
    sub.plot(datasane, 'r', label='sane filtered signal')
    sub.next()
    sub.plot(fdatasane, 'r', label='sane filtered spectrum')
    sub.title('Noise type : ' + noisetype)
    sub.show()
    return (iSNR, fSNR)


def test_sane(lendata=10000, rank=100, orda=4000, noise=200.0, iterations=1, noisetype='additive'):
    """
    ============== example of use of Sane on a synthetic data-set ===============
    """
    import time
    import matplotlib.pyplot as plt
    from matplotlib.ticker import MaxNLocator

    def plot_param(fig, fignumb):
        ax = fig.add_subplot(fignumb)
        ax.xaxis.set_major_locator(MaxNLocator(4))
        ax.yaxis.set_major_locator(MaxNLocator(4))

    def mfft(v):
        """utility that returns the modulus of the fft of v"""
        import scipy.fftpack as fft
        s0 = fft.fft(v)
        s0 = np.real(np.sqrt(s0 * s0.conj()))
        return s0

    def SNR(noisy, target):
        """computes and return SNR value, in dB"""
        return 10 * np.log10(sum(abs(target) ** 2) / sum(abs(noisy - target) ** 2))

    nbpeaks = 8
    LB = 1.11
    Freq = [(i + 1 + np.sqrt(10)) * np.pi * complex(0.0, 500.0) for i in range(nbpeaks)]
    Amp = [(i + 1) * 20 for i in range(nbpeaks)]
    data0 = np.zeros(lendata, dtype=complex)
    if noisetype == 'additive':
        x = np.arange(lendata * 1.0) / lendata
        for i in range(nbpeaks):
            data0 += Amp[i] * np.exp(Freq[i] * x) * np.exp(-LB * x)

        dataadd = data0 + noise * (np.random.randn(x.size) + complex(0.0, 1.0) * np.random.randn(x.size))
        data = dataadd
    else:
        if noisetype == 'multiplicative':
            x = np.arange(lendata * 1.0) / lendata
            for i in range(nbpeaks):
                data0 += Amp[i] * np.exp(Freq[i] * x) * np.exp(-LB * x)

            data = np.zeros(lendata, dtype=complex)
            Anoise = noise / 2
            Fnoise = noise / 200
            for i in range(nbpeaks):
                nAmp = Amp[i] + Anoise * np.random.randn(x.size)
                nFreq = Freq[i] + Fnoise * np.random.randn(x.size)
                data += nAmp * np.exp(nFreq * x) * np.exp(-LB * x)

        else:
            if noisetype == 'sampling':
                x = np.arange(lendata * 1.0) / lendata
                xn = x + 0.5 * np.random.randn(x.size) / lendata
                for i in range(nbpeaks):
                    data0 += Amp[i] * np.exp(Freq[i] * x) * np.exp(-LB * x)

                data = np.zeros(lendata, dtype=complex)
                for i in range(nbpeaks):
                    data += Amp[i] * np.exp(Freq[i] * xn) * np.exp(-LB * xn)

            else:
                if noisetype == 'missing points':
                    x = np.arange(lendata * 1.0) / lendata
                    for i in range(nbpeaks):
                        data0 += Amp[i] * np.exp(Freq[i] * x) * np.exp(-LB * x)

                    miss = np.random.randint(2, size=(len(x)))
                    dataadd = data0 * miss
                    data = dataadd
                else:
                    raise Exception('unknown noise type')
    iSNR = SNR(data, data0)
    print('Initial Noisy Data SNR: %.2f dB - noise type : %s' % (iSNR, noisetype))
    fdata = mfft(data0)
    fdatanoise = mfft(data)
    print('=== Running Sane algo ===')
    print('lendata:', lendata)
    print(' orda:', orda)
    print(' rank:', rank)
    t0 = time.time()
    datasane = sane(data, k=rank, orda=orda, iterations=iterations)
    tsane = time.time() - t0
    fdatasane = mfft(datasane)
    print('=== Result ===')
    fSNR = SNR(datasane, data0)
    print('Denoised SNR: %.2f dB  - processing gain : %.2f dB' % (fSNR, fSNR - iSNR))
    print('processing time for sane : %.2f sec' % tsane)
    fig = plt.figure()
    plot_param(fig, 321)
    plt.plot((data0.real), 'b', label='clean signal')
    plt.legend()
    plt.title('data series')
    plot_param(fig, 323)
    plt.plot((data.real), 'k', label='noisy signal')
    plt.legend()
    plot_param(fig, 325)
    plt.plot((datasane.real), 'r', label='sane filtered signal')
    plt.legend()
    plot_param(fig, 322)
    plt.plot(fdata, 'b', label='clean spectrum')
    plt.legend()
    plt.title('FFT spectrum')
    plot_param(fig, 324)
    plt.plot(fdatanoise, 'k', label='noisy spectrum')
    plt.legend()
    plot_param(fig, 326)
    plt.plot(fdatasane, 'r', label='sane filtered spectrum')
    plt.suptitle('Noise type : ' + noisetype)
    plt.legend()
    plt.show()


class sane_Tests(unittest.TestCase):

    def test_sane(self):
        """
        Makes sane without trick and 1 iteration.
        """
        iSNR, fSNR = test_sane_gene(lendata=10000, rank=30,
          orda=4000,
          nbpeaks=2,
          noise=10.0,
          noisetype='additive',
          nb_iterat=1)
        self.assertAlmostEqual(iSNR, 6, 0)
        self.assertTrue(fSNR > 28)

    def test_sane_iter_trick(self):
        """
        Makes sane with trick and varying the number of iterations.
        """
        for it in range(1, 4):
            test_sane_gene(lendata=10000, rank=4,
              orda=4000,
              nbpeaks=2,
              noise=50.0,
              noisetype='additive',
              nb_iterat=it,
              trick=True)

    def _test_optim(self):
        """
        Test of the rank optimization.
        The algorithm finds the minimal rank restituting the signal with complete power. 
        """
        from ..Display import testplot
        import numpy.fft as fft
        plt = testplot.plot()
        from util.signal_tools import fid_signoise
        nbpeaks = 15
        ampl = 2
        lengthfid = 10000
        noise = 20
        fid = fid_signoise(nbpeaks, ampl, lengthfid=lengthfid, noise=noise)
        plt.plot(abs(fft(fid)))
        orda = lengthfid // 4
        optrk = OPTK(fid, orda=orda, debug=True)
        optk = optrk.find_best_rank()
        print('optk', optk)
        self.assertAlmostEqual(optk, 66, 0)
        plt.show()