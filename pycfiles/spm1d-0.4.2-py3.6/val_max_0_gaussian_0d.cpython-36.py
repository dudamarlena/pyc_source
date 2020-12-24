# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/spm1d/rft1d/examples/val_max_0_gaussian_0d.py
# Compiled at: 2019-08-22 04:37:04
# Size of source mod 2**32: 714 bytes
import numpy as np
from scipy import stats
from matplotlib import pyplot
np.random.seed(0)
nResponses = 10000
y = np.random.randn(nResponses)
heights = np.linspace(0, 5, 21)
sf = np.array([(y > h).mean() for h in heights])
sfE = stats.norm.sf(heights)
pyplot.close('all')
ax = pyplot.axes()
ax.plot(heights, sf, 'o', label='Simulated')
ax.plot(heights, sfE, '-', label='Theoretical')
ax.set_xlabel('$u$', size=20)
ax.set_ylabel('$P (z > u)$', size=20)
ax.legend()
ax.set_title('Gaussian univariate validation (0D)', size=20)
pyplot.show()