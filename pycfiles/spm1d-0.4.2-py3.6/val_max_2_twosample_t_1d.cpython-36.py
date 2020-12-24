# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/spm1d/rft1d/examples/val_max_2_twosample_t_1d.py
# Compiled at: 2019-08-22 04:37:04
# Size of source mod 2**32: 1413 bytes
import numpy as np
from matplotlib import pyplot
from spm1d import rft1d
np.random.seed(123456789)
nResponsesA = 5
nResponsesB = 5
nNodes = 101
FWHM = 10.0
nIterations = 5000
nA, nB = nResponsesA, nResponsesB
nTotal = nA + nB
df = nA + nB - 2
T = []
for i in range(nIterations):
    y = rft1d.randn1d(nTotal, nNodes, FWHM)
    yA, yB = y[:nA], y[nA:]
    mA, mB = yA.mean(axis=0), yB.mean(axis=0)
    sA, sB = yA.std(ddof=1, axis=0), yB.std(ddof=1, axis=0)
    s = np.sqrt(((nA - 1) * sA * sA + (nB - 1) * sB * sB) / df)
    t = (mA - mB) / (s * np.sqrt(1.0 / nA + 1.0 / nB))
    T.append(t.max())

T = np.asarray(T)
heights = np.linspace(2, 5, 21)
sf = np.array([(T > h).mean() for h in heights])
sfE = rft1d.t.sf(heights, df, nNodes, FWHM)
sf0D = rft1d.t.sf0d(heights, df)
pyplot.close('all')
ax = pyplot.axes()
ax.plot(heights, sf, 'o', label='Simulated')
ax.plot(heights, sfE, '-', label='Theoretical')
ax.plot(heights, sf0D, 'r-', label='Theoretical (0D)')
ax.set_xlabel('$u$', size=20)
ax.set_ylabel('$P (t_\\mathrm{max} > u)$', size=20)
ax.legend()
ax.set_title('Two-sample t validation (1D)', size=20)
pyplot.show()