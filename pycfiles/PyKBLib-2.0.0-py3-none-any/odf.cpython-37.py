# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/pykbi/odf.py
# Compiled at: 2018-09-02 04:17:57
# Size of source mod 2**32: 765 bytes
__doc__ = '\nOscillatory decaying function.\n\nThis is the same function as is used in Kruger et al. J. Phys. Chem. Lett.\n2013, 4, 235-238 (dx.doi.org/10.1021/jz301992u)\n\nThe function acts as a radial distribution function, being zero initally, and\noscilating around 1.  The value r is the radial distance, chi is the intensity\nof the fluctuations, and sigma is the width of the fluctuations.\n\n'
import numpy as _np
__all__ = [
 'odf']

def odf(radius, chi, sigma=1.0):
    """
    Calculate the fluctuating decaying function

    """
    cut = 0.95
    rdata = radius / sigma
    function = lambda rin: 1.5 / rin * _np.exp((1.0 - rin) / chi) * _np.cos(2.0 * _np.pi * (rin - 1.05))
    return _np.where(rdata >= cut, function(rdata), -1.0) + 1.0