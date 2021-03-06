# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\chirp\pitch\template.py
# Compiled at: 2013-12-11 23:17:46
"""
harmonic template matching for pitch detection

Copyright (C) 2011 Daniel Meliza <dan // meliza.org>
Created 2011-07-29
"""
import numpy as nx, libtfr

class harmonic(object):
    """
    Performs harmonic template matching for pitch detection.  The
    template has positive and negative lobes with constant spacing.
    Template matching consists of cross-correlating the template
    against the spectrum of a sound; when the correlation is high then
    this indicates a high likelihood for that pitch.  The algorithm
    optimizes speed over memory consumption, so the template is stored
    in a 2D array with the template shifted by a different amount in
    each column.  Thus, each column corresponds to a different pitch
    value.

    Instantiating the object creates the template, which can then be
    used to analyze any number of spectrograms; however, the frequency
    grid of the template must match the grid of the spectrograms.
    """

    def __init__(self, **kwargs):
        """
        Initialize the object with the harmonic template. Frequency
        parameters are in relative units (1.0 is the sampling rate).
        Decay, neg_ampl, and neg_width help to reduce pitch doubling
        errors; see Wang et al 2000.  Options:

        pitch_range:  the range (2-ple) of pitches to search for (relative units)
        freq_range:   the range of frequencies in the input spectrogram
        nfreq:        the number of frequency points in the input spectrogram
        lobes:        the number of lobes to include in the template
        lobe_decay:   each successive lobe is scaled by decay^(n-1)
        neg_ampl:     the amplitude of interspaced negative lobes
        neg_width:    the width of negative lobes
        """
        pitch_range = kwargs.get('pitch_range')
        freq_range = kwargs.get('freq_range')
        nfreq = kwargs.get('nfft')
        lobes = kwargs.get('lobes', 7)
        decay = kwargs.get('lobe_decay', 0.85)
        neg_ampl = kwargs.get('neg_ampl', 0.35)
        neg_width = kwargs.get('neg_width', 9)
        self.fgrid = loggrid(freq_range[0], freq_range[1], nfreq)
        self.pgrid = self.fgrid[((self.fgrid >= pitch_range[0]) & (self.fgrid <= pitch_range[1]))]
        self.template = nx.zeros((self.fgrid.size, self.pgrid.size))
        T = self.make_template(lobes, decay, neg_ampl, neg_width)
        for i in xrange(self.pgrid.size):
            self.template[i:T.size, i] = T[:T.size - i]

    def make_template(self, lobes, decay, neg_ampl, neg_width):
        """
        Generate the base template.
        """
        N = int(1 / self.pgrid[0] * 50)
        pt = pulse_train(self.pgrid[0], N)
        A = libtfr.tfr_spec(pt, N, 1, N, fgrid=self.fgrid)[:, 0]
        A, p = normalize_lobes(A, lobes, decay)
        B = libtfr.tfr_spec(pt, N, 1, N, fgrid=self.fgrid * 2)[:, 0]
        B = normalize_lobes(B, lobes, 1.0, between=p)[0] * -neg_ampl
        B = nx.convolve(B, nx.hanning(neg_width), 'same')
        C = A + B
        return C / nx.sqrt(nx.sum(C ** 2))

    def xcorr(self, spectrogram, pow_thresh=0.0, **kwargs):
        """
        Calculate the cross-correlation between the template and a
        spectrogram.  The spectrogram must have the same frequency
        resolution as the template.

        pow_thresh:   Each frame is normalized by signal power;
                      if the power is < power_thresh then the
                      entire cross-correlation is replaced with 1/N
        """
        Z = nx.maximum(nx.dot(spectrogram.T, self.template), 0.0).T
        specpow = nx.sqrt((spectrogram ** 2).sum(0))
        ind = specpow > pow_thresh
        Z[:, nx.nonzero(ind)[0]] /= specpow[ind]
        Z[:, nx.nonzero(~ind)[0]] = 1.0 / Z.shape[0]
        return Z


def loggrid(fmin, fmax, N):
    """
    Generates a logarithmic frequency grid between fmin and fmax

    fmin - first frequency
    fmax  - last frequency
    N      - number of points
    base   - log base
    """
    from numpy import log, logspace, e
    lfmin, lfmax = log((fmin, fmax))
    return logspace(lfmin, lfmax, N, base=e)


def pulse_train(freq, N):
    """ Create a pulse train consisting of N pulses at freq """
    dt = int(1 / freq)
    Np = max(N, dt * 2)
    out = nx.zeros(Np)
    out[dt / 2:Np:dt] = 1
    out[dt / 2 + 1:Np:dt] = -1
    return out


def normalize_lobes(psd, lobes, decay, thresh=1e-10, between=None):
    """
    For a psd consisting of harmonically spaced lobes, this function
    will iterate through the psd, find each lobe, calculate the area
    under it, and normalize it so the area sums to decay^(n-1).

    lobes:  max number of lobes to keep
    decay:  exponential decay factor (1 for no decay)
    between: if not None, only keep lobes that are between the values in this list
    """
    out = nx.zeros_like(psd)
    lobepos = []
    csum = lobestart = lobecount = 0
    for i, val in enumerate(psd):
        if lobecount >= lobes:
            break
        if csum > thresh:
            if val > thresh:
                csum += val
            else:
                R = slice(lobestart, i)
                P = (i + lobestart) / 2
                if between is None or all(nx.abs(P - p) > 5 for p in between):
                    out[R] = psd[R] / csum * decay ** lobecount
                    lobecount += 1
                    lobepos.append(P)
                csum = 0
        elif val > thresh:
            lobestart = i
            csum = val

    return (
     out, lobepos)


def frame_xcorr(spec, max_jump, **kwargs):
    """
    Calculate cross-correlation between successive frames of a
    spectrogram. Uses FFT for efficiency.
    """
    from numpy.fft import fft, ifft
    rows, cols = spec.shape
    S = fft(spec, n=rows * 2, axis=0)
    Sx = nx.conj(S[:, :-1]) * S[:, 1:]
    sx = ifft(Sx, axis=0).real
    return nx.concatenate((sx[-max_jump:, :], sx[:max_jump, :]))