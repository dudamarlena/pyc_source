# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/spm1d/rft1d/examples/random_fields_0.py
# Compiled at: 2019-08-22 04:37:04
# Size of source mod 2**32: 1440 bytes
"""
Verbose random field generation.

Note:
When FWHM gets large (2FWHM>nNodes), the data should be padded prior to filtering.
Use **rft1d.random.randn1d** for optional padding.
"""
import numpy as np
from scipy.ndimage import gaussian_filter1d
from matplotlib import pyplot
np.random.seed(12345)
nResponses = 5
nNodes = 101
FWHM = 20.0
y = np.random.randn(nResponses, nNodes)
sd = FWHM / np.sqrt(8 * np.log(2))
y = gaussian_filter1d(y, sd, axis=1, mode='wrap')
t = np.arange(-0.5 * (nNodes - 1), 0.5 * (nNodes - 1) + 1)
gf = np.exp(-t ** 2 / (2 * sd ** 2))
gf /= gf.sum()
AG = np.fft.fft(gf)
Pag = AG * np.conj(AG)
COV = np.real(np.fft.ifft(Pag))
svar = COV[0]
scale = np.sqrt(1.0 / svar)
y *= scale
pyplot.close('all')
pyplot.plot(y.T)
pyplot.plot([0, 100], [0, 0], 'k:')
pyplot.xlabel('Field position', size=16)
pyplot.ylabel('z', size=20)
pyplot.title('Random (Gaussian) fields', size=20)
pyplot.show()