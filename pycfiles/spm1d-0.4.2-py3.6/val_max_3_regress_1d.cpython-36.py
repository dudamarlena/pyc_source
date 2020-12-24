# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/spm1d/rft1d/examples/val_max_3_regress_1d.py
# Compiled at: 2019-08-22 04:37:04
# Size of source mod 2**32: 1838 bytes
import numpy as np
from matplotlib import pyplot
from spm1d import rft1d

def tstat_regress(Y, x):
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
    t = np.array(c.T * b).flatten() / np.sqrt(sigma2 * float(c.T * np.linalg.inv(X.T * X) * c))
    return t


np.random.seed(123456789)
nResponses = 12
nIterations = 2000
nNodes = 101
FWHM = 10.0
x = np.arange(nResponses)
df = nResponses - 2
T = []
generator = rft1d.random.Generator1D(nResponses, nNodes, FWHM)
for i in range(nIterations):
    y = generator.generate_sample()
    t = tstat_regress(y, x)
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
ax.set_title('Linear regression validation (1D)', size=20)
pyplot.show()