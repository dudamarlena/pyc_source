# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.5-x86_64/egg/PyGS/PowerSpectra.py
# Compiled at: 2013-07-01 18:36:24
__doc__ = '\nCreated on Dec 3, 2012\n\n@author: Steven\n'
import sys
try:
    import matplotlib.pyplot as plt
except:
    sys.exit('Please install Matplotlib')

try:
    import numpy as np
except:
    sys.exit('Please install Numpy')

try:
    from scipy.interpolate import griddata
except:
    sys.exit('Please install scipy')

import utils
try:
    from fort.DFT import dft
    fort_routines = True
except:
    print 'Warning: DFT fortran routines not found'
    fort_routines = False

def power_spec_1d_fast(quantity, bins=None, min_wave=0.0001, max_wave=0.02, pad=1, weight=None):
    """
    Computes the 1D power spectrum and plots it.
    
    This method uses the numpy fft algorithm to calculate the real to real 
    DFT of any quantity in the GS data, then converts this to a power
    spectrum (merely squares it). As such, it needs what I call 'density 
    values' as its input, which here are merely histogram values. It will 
    only calculate as many DFT points as there are bins in the histogram, 
    which is fine for frequency-based plots, but makes wavelength (inverse 
    frequency) plots very angular. To increase the number of points you can
    pad the original data with zeroes on either end, but even this does not
    ensure a smooth wavelength plot. To get a very nice looking wavelength 
    plot, use PowerSpec_1d_slow().
    
    
    INPUT PARAMETERS:
    quantity                  : the quantity type used for the dft. Generally 'redshift', 'c_dist', 'ra' or 'dec'
    bins        [None]        : the number of bins to use in the histogram to get 'densities'. 
                                If none, an 'optimal' bin number is used.
    min_wave    [0.0001]      : The minimum wavelength to plot.
    max_wave    [0.02]        : The maximum wavelength to plot
    pad         [1]           : How much the original data length is multiplied by (zeroes padded in the extra space).
                                The higher the padding, the longer the calculation, but the better the resolution.
    wavelength  [True]        : Whether to plot the power against wavelength. If False, plots against frequency.
    weight      [None]        :  An optional setting allowing a further weight to be applied to the bin densities before calculation.
                                0 - No extra weighting (each bin will be its number)
                                'weights_1' - Inverse of selection function (simple)
                                'weights_2' - Inverse of selection function +1 (simple)
    
    OUTPUT PARAMETERS:
    ps                        : array of power spectrum values
    freq                      : array of frequencies
    wvl                       : array of wavelengths
    """
    if not bins:
        bins = utils.FD_bins(quantity)
        print 'bins: ', bins
    if weight is not None:
        hist, edges = np.histogram(quantity, bins, weights=weight)
        print np.min(weight)
        print np.max(weight)
    else:
        hist, edges = np.histogram(quantity, bins)
    print np.min(quantity)
    print np.max(quantity)
    print 'hist: ', hist
    print 'edges: ', edges
    step = edges[2] - edges[1]
    n = pad * hist.size
    ps = np.abs(np.fft.rfft(hist, n=n) / np.sqrt(n)) ** 2
    freq = np.fft.fftfreq(n, step)
    wavelength = 1.0 / freq[:np.floor(n / 2 + 1)]
    print 'ps: ', ps
    print 'freq ', freq
    print 'wvl ', wavelength
    return (
     ps, freq * 2.0 * np.pi, wavelength)


def power_spec_1d_slow(quantity, bins=None, min_wave=0.0001, max_wave=0.02, n_waves=1000, weight=None):
    """
    Computes the 1D power spectrum and plots it.
    
    This method uses a slower DFT method, rather than an FFT. However, the bonus is that the increments in
    wavelength are regular and completely customizable (producing smooth plots). And also can do weights.
    
    INPUT PARAMETERS
    quantity    ['redshift']    : the quantity to analyse.
    bins        [None]          : the number of bins to use in the histogram , if None, performs a 'phase'
                                    DFT, which is to say each data point counts for 1.0 at its precise location.
    min_wave    [0.0001]        :the minimum wavelength to calculate
    max_wave    [0.02]        :the maximum wavelength ot calculate
    n_waves     [1000]          :the number of wavelengths to calculate
    
    OUTPUT PARAMETERS
    ps    : the power spectrum
    wvl   : the wavelengths
    """
    wavelengths = np.asfortranarray(np.linspace(min_wave, max_wave, n_waves))
    freq = 2 * np.pi / wavelengths
    if bins:
        if weight is not None:
            hist, edges = np.histogram(quantity, bins, weights=weight)
        else:
            hist, edges = np.histogram(quantity, bins)
        centres = np.asfortranarray(edges[:-1] + (edges[1] - edges[0]) / 2.0)
        ps = dft.dft_one(np.asfortranarray(hist), centres, wavelengths)
    elif weight is None:
        ps = dft.phasedft_one(np.asfortranarray(quantity), wavelengths)
    else:
        ps = dft.dft_one(np.asfortranarray(weight), np.asfortranarray(quantity), wavelengths)
    return (
     ps, freq, wavelengths)