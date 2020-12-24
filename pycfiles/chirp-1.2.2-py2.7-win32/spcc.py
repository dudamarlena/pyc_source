# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\chirp\compare\spcc.py
# Compiled at: 2013-12-11 23:17:46
"""
compare signals using spectrographic cross-correlation.

Copyright (C) 2011 Daniel Meliza <dan // meliza.org>
Created 2011-08-30
"""
import os
from chirp.common.config import _configurable
from chirp.compare.base_comparison import base_comparison

class spcc(base_comparison, _configurable):
    """
    Compute pairwise distances between motifs using spectrographic
    cross-correlation (SPCC). Configurable options:

    nfreq:         the number of frequency bands to compare
    freq_range:    the range of frequencies to compare (in Hz)
    shift:         the number of time points to shift between analysis window
    window:        the windowing function to use
    subtract_mean: subtract mean of log spectrograms before doing CC
    biased_norm:   use a biased (but more robust) normalization
    """
    _descr = 'spectrographic crosscorrelation (requires wav; ebl optional)'
    file_extension = '.wav'
    options = dict(spec_method='hanning', nfreq=100, window_shift=1.5, freq_range=(750.0,
                                                                                   10000.0), powscale='linear', mask='box', subtract_mean=True, biased_norm=True)
    config_sections = ('spectrogram', 'spcc')

    def __init__(self, configfile=None, **kwargs):
        self.readconfig(configfile)
        self.options.update(kwargs)

    def load_signal(self, locator, dtype='d'):
        """
        Loads the signal and computes the spectrogram.

        dtype: the data type to store the output in. Use
               single-precision floats if needed to reduce storage
               requirements.
        """
        from ewave import wavfile
        from libtfr import fgrid, dynamic_range
        from chirp.common.signal import spectrogram
        from chirp.common.geom import elementlist, masker
        from numpy import linspace, log10
        fp = wavfile(locator)
        signal = fp.read()
        Fs = fp.sampling_rate
        speccr = spectrogram(**self.options)
        df = 1.0 * (self.options['freq_range'][1] - self.options['freq_range'][0]) / self.options['nfreq']
        nfft = int(Fs / df)
        spec, extent = speccr.linspect(signal, Fs / 1000, nfft=nfft)
        F, ind = fgrid(Fs, nfft, self.options['freq_range'])
        spec = spec[ind, :]
        T = linspace(extent[0], extent[1], spec.shape[1])
        if self.options['powscale'].startswith('log'):
            spec = log10(dynamic_range(spec, 96))
            if self.options['subtract_mean']:
                spec -= spec.mean()
        if self.options['mask'] != 'none':
            eblfile = os.path.splitext(locator)[0] + elementlist.default_extension
            if os.path.exists(eblfile):
                mask = elementlist.read(eblfile)
                spec = masker(boxmask=self.options['mask'] == 'box').cut(spec, mask, T, F / 1000.0)
        return spec.astype(dtype)

    def compare(self, ref, tgt):
        cc = spectcc(ref, tgt, self.options['biased_norm'])
        return (cc.sum(0).max(),)

    @property
    def compare_stat_fields(self):
        """ Return a tuple of the names for the statistics returned by compare() """
        return ('spcc', )

    def options_str(self):
        out = '* SPCC parameters:\n** Frequency bands = %(nfreq)d\n** Frequency range %(freq_range)s\n** Window shift = %(window_shift).2f\n** Spectrogram method = %(spec_method)s\n** Spectrogram power scale = %(powscale)s\n** Use biased norm = %(biased_norm)s\n** Spectrogram masking = %(mask)s' % self.options
        return out


def spectcc(ref, tgt, biased_norm=True):
    """
    Compute cross-correlation between two spectrograms.  This is
    essentially the mean of the cross-correlations for each of the
    frequency bands in the spectrograms.

    ref, tgt:  spectrograms of signals, nfreq x nframe

    returns the 2D cross-correlation, calculate sum of columns to get CC for each lag
    """
    from numpy import conj, sqrt, convolve, ones
    from numpy.fft import fft, ifft
    from numpy.linalg import norm
    assert ref.ndim == tgt.ndim
    if ref.ndim == 1:
        ref.shape = (
         1, ref.size)
        tgt.shape = (1, tgt.size)
    rfreq, rframes = ref.shape
    tfreq, tframes = tgt.shape
    assert tfreq == rfreq, 'Spectrograms must have same number of frequency bands'
    if tframes < rframes:
        tframes, rframes = rframes, tframes
        tgt, ref = ref, tgt
    sz = rframes + tframes - 1
    X = conj(fft(ref, sz, axis=1))
    X *= fft(tgt, sz, axis=1)
    num = ifft(X).real
    ind = abs(rframes - tframes) + 1
    num = num[:, :ind]
    d1 = norm(ref)
    if biased_norm:
        d2 = norm(tgt)
    else:
        d2 = sqrt(convolve((tgt ** 2).sum(0), ones(rframes), 'valid'))
    return num / d1 / d2