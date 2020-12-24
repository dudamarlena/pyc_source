# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/spm1d/rft1d/examples/val_max_5_onesample_T2_1d.py
# Compiled at: 2019-08-22 04:37:04
# Size of source mod 2**32: 1663 bytes
import numpy as np
from matplotlib import pyplot
from spm1d import rft1d

def here_hotellingsT2(y):
    N = y.shape[0]
    m = np.matrix(y.mean(axis=0))
    T2 = []
    for ii, mm in enumerate(m):
        W = np.matrix(np.cov((y[:, ii, :].T), ddof=1))
        t2 = N * mm * np.linalg.inv(W) * mm.T
        T2.append(float(t2))

    return np.asarray(T2)


np.random.seed(123456789)
nResponses = 20
nNodes = 101
nComponents = 3
nIterations = 50
FWHM = 15.0
W0 = np.eye(nComponents)
df = (
 nComponents, nResponses - 1)
T2 = []
generator = rft1d.random.GeneratorMulti1D(nResponses, nNodes, nComponents, FWHM, W0)
for i in range(nIterations):
    y = generator.generate_sample()
    t2 = here_hotellingsT2(y)
    T2.append(t2.max())

T2 = np.asarray(T2)
heights = np.linspace(10, 40, 21)
sf = np.array([(T2 > h).mean() for h in heights])
sfE = rft1d.T2.sf(heights, df, nNodes, FWHM)
sf0D = rft1d.T2.sf0d(heights, df)
pyplot.close('all')
ax = pyplot.axes()
ax.plot(heights, sf, 'o', label='Simulated')
ax.plot(heights, sfE, '-', label='Theoretical')
ax.plot(heights, sf0D, 'r-', label='Theoretical (0D)')
ax.set_xlabel('$u$', size=20)
ax.set_ylabel('$P (T^2_\\mathrm{max} > u)$', size=20)
ax.legend()
ax.set_title("One-sample Hotelling's T2 validation (1D)", size=20)
pyplot.show()