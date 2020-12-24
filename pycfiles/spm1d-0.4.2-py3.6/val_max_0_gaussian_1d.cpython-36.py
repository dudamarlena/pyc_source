# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/spm1d/rft1d/examples/val_max_0_gaussian_1d.py
# Compiled at: 2019-08-22 04:37:04
# Size of source mod 2**32: 956 bytes
import numpy as np
from matplotlib import pyplot
from spm1d import rft1d
np.random.seed(123456789)
nResponses = 10000
nNodes = 101
FWHM = 10.0
y = rft1d.randn1d(nResponses, nNodes, FWHM)
ymax = y.max(axis=1)
heights = np.linspace(2, 4, 21)
sf = np.array([(ymax > h).mean() for h in heights])
sfE = rft1d.norm.sf(heights, nNodes, FWHM)
sfN = rft1d.norm.sf0d(heights)
pyplot.close('all')
ax = pyplot.axes()
ax.plot(heights, sf, 'o', label='Simulated')
ax.plot(heights, sfE, '-', label='Theoretical')
ax.plot(heights, sfN, 'r-', label='Standard normal')
ax.set_xlabel('x', size=16)
ax.set_ylabel('$P (z_\\mathrm{max} > x)$', size=20)
ax.legend()
ax.set_title('Gaussian univariate validation (1D)', size=20)
pyplot.show()