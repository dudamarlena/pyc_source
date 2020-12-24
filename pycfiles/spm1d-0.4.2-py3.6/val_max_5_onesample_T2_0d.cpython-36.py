# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/spm1d/rft1d/examples/val_max_5_onesample_T2_0d.py
# Compiled at: 2019-08-22 04:37:04
# Size of source mod 2**32: 1265 bytes
import numpy as np
from matplotlib import pyplot
from spm1d import rft1d
np.random.seed(1)
nResponses = 8
nComponents = 2
nIterations = 5000
W0 = np.array([[1, 0.2], [0.2, 1]])
df = (
 nComponents, nResponses - 1)
T2 = []
for i in range(nIterations):
    y = np.random.multivariate_normal(np.zeros(nComponents), W0, nResponses)
    y = np.matrix(y)
    m = y.mean(axis=0)
    W = np.matrix(np.cov((y.T), ddof=1))
    t2 = nResponses * m * np.linalg.inv(W) * m.T
    T2.append(float(t2))

T2 = np.asarray(T2)
heights = np.linspace(2, 10, 21)
sf = np.array([(T2 > h).mean() for h in heights])
sfE = rft1d.T2.sf0d(heights, df)
pyplot.close('all')
ax = pyplot.axes()
ax.plot(heights, sf, 'o', label='Simulated')
ax.plot(heights, sfE, '-', label='Theoretical')
ax.set_xlabel('$u$', size=20)
ax.set_ylabel('$P (T^2 > u)$', size=20)
ax.legend()
ax.set_title("One-sample Hotelling's T2 validation (0D)", size=20)
pyplot.show()