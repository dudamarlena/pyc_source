# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/spm1d/rft1d/examples/val_max_3_regress_0d.py
# Compiled at: 2019-08-22 04:37:04
# Size of source mod 2**32: 1728 bytes
from math import sqrt
import numpy as np
from scipy import stats
from matplotlib import pyplot

def tstat_regress(Y, x):
    Y = np.array([Y]).T
    X = np.ones((Y.shape[0], 2))
    X[:, 0] = x
    Y = np.matrix(Y)
    X = np.matrix(X)
    c = np.matrix([1, 0]).T
    b = np.linalg.pinv(X) * Y
    eij = Y - X * b
    R = eij.T * eij
    df = Y.shape[0] - 2
    sigma2 = np.diag(R) / df
    return np.array(c.T * b).flatten() / np.sqrt(sigma2 * float(c.T * np.linalg.inv(X.T * X) * c))


np.random.seed(0)
nResponses = 10
nIterations = 5000
x = np.arange(nResponses)
df = nResponses - 2
T = []
for i in range(nIterations):
    y = np.random.randn(nResponses)
    t = tstat_regress(y, x)
    T.append(t)

T = np.asarray(T)
heights = np.linspace(1, 4, 21)
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
ax.set_title('Linear regression validation (0D)', size=20)
pyplot.show()