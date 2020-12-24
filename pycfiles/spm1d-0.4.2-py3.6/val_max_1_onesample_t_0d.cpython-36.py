# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/spm1d/rft1d/examples/val_max_1_onesample_t_0d.py
# Compiled at: 2019-08-22 04:37:04
# Size of source mod 2**32: 1113 bytes
from math import sqrt
import numpy as np
from scipy import stats
from matplotlib import pyplot
np.random.seed(0)
nResponses = 6
nIterations = 10000
df = nResponses - 1
sqrtN = sqrt(nResponses)
T = []
for i in range(nIterations):
    y = np.random.randn(nResponses)
    t = y.mean() / y.std(ddof=1) * sqrtN
    T.append(t)

T = np.asarray(T)
heights = np.linspace(0, 5, 21)
sf = np.array([(T > h).mean() for h in heights])
sfE = stats.t.sf(heights, df)
sfN = stats.norm.sf(heights)
pyplot.close('all')
ax = pyplot.axes()
ax.plot(heights, sf, 'o', label='Simulated')
ax.plot(heights, sfE, '-', label='Theoretical')
ax.plot(heights, sfN, 'r-', label='Standard normal')
ax.set_xlabel('$u$', size=20)
ax.set_ylabel('$P (t > u)$', size=20)
ax.legend()
ax.set_title('One-sample t validation (0D)', size=20)
pyplot.show()