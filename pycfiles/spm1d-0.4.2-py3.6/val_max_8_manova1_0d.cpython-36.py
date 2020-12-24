# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/spm1d/rft1d/examples/val_max_8_manova1_0d.py
# Compiled at: 2019-08-22 04:37:04
# Size of source mod 2**32: 2070 bytes
from math import log
import numpy as np
from scipy import stats
from matplotlib import pyplot

def here_manova1(Y, GROUP):
    u = np.unique(GROUP)
    nGroups = u.size
    nResponses = Y.shape[0]
    nComponents = Y.shape[1]
    X = np.zeros((nResponses, nGroups))
    ind0 = 0
    for i, uu in enumerate(u):
        n = (GROUP == uu).sum()
        X[ind0:ind0 + n, i] = 1
        ind0 += n

    Y, X = np.matrix(Y), np.matrix(X)
    b = np.linalg.pinv(X) * Y
    R = Y - X * b
    R = R.T * R
    X0 = np.matrix(np.ones(Y.shape[0])).T
    b0 = np.linalg.pinv(X0) * Y
    R0 = Y - X0 * b0
    R0 = R0.T * R0
    lam = np.linalg.det(R) / np.linalg.det(R0)
    N, p, k = float(nResponses), float(nComponents), float(nGroups)
    x2 = -(N - 1 - 0.5 * (p + k)) * log(lam)
    return x2


def here_get_groups(nResponses):
    GROUP = []
    for i, n in enumerate(nResponses):
        GROUP += [i] * n

    return np.array(GROUP)


np.random.seed(1)
nResponses = (10, 3, 4)
nComponents = 3
nGroups = len(nResponses)
nIterations = 5000
W0 = np.eye(nComponents)
GROUP = here_get_groups(nResponses)
nTotal = sum(nResponses)
df = nComponents * (nGroups - 1)
X2 = []
for i in range(nIterations):
    y = np.random.multivariate_normal(np.zeros(nComponents), W0, nTotal)
    chi2 = here_manova1(y, GROUP)
    X2.append(chi2)

X2 = np.asarray(X2)
heights = np.linspace(5, 15, 21)
sf = np.array([(X2 > h).mean() for h in heights])
sfE = stats.chi2.sf(heights, df)
pyplot.close('all')
ax = pyplot.axes()
ax.plot(heights, sf, 'o', label='Simulated')
ax.plot(heights, sfE, '-', label='Theoretical')
ax.set_xlabel('$u$', size=20)
ax.set_ylabel('$P (\\chi^2 > u)$', size=20)
ax.legend()
ax.set_title('MANOVA validation (0D)', size=20)
pyplot.show()