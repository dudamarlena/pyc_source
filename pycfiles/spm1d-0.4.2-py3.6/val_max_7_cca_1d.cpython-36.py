# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/spm1d/rft1d/examples/val_max_7_cca_1d.py
# Compiled at: 2019-08-22 04:37:04
# Size of source mod 2**32: 2436 bytes
from math import sqrt, log
import numpy as np
from matplotlib import pyplot
from spm1d import rft1d

def here_cca_single_node(y, x):
    N = y.shape[0]
    X, Y = np.matrix(x.T).T, np.matrix(y)
    Z = np.matrix(np.ones(N)).T
    Rz = np.eye(N) - Z * np.linalg.inv(Z.T * Z) * Z.T
    XStar = Rz * X
    YStar = Rz * Y
    p, r = (1.0, 1.0)
    m = N - p - r
    H = YStar.T * XStar * np.linalg.inv(XStar.T * XStar) * XStar.T * YStar / p
    W = YStar.T * (np.eye(nResponses) - XStar * np.linalg.inv(XStar.T * XStar) * XStar.T) * YStar / m
    F = np.linalg.inv(W) * H
    ff = np.linalg.eigvals(F)
    fmax = float(np.real(ff.max()))
    r2max = fmax * p / (m + fmax * p)
    rmax = sqrt(r2max)
    p, m = float(N), float(y.shape[1])
    x2 = -(p - 1 - 0.5 * (m + 2)) * log(1 - rmax ** 2)
    return x2


def here_cca(y, x):
    Q = y.shape[1]
    z = [here_cca_single_node(y[:, q, :], x) for q in range(Q)]
    return np.array(z)


np.random.seed(123456789)
nResponses = 20
nNodes = 101
nComponents = 2
nIterations = 100
FWHM = 15.0
W0 = np.eye(nComponents)
df = nComponents
x = np.linspace(0, 1, nResponses)
X2 = []
generator = rft1d.random.GeneratorMulti1D(nResponses, nNodes, nComponents, FWHM, W0)
for i in range(nIterations):
    y = generator.generate_sample()
    chi2 = here_cca(y, x)
    X2.append(chi2.max())

X2 = np.asarray(X2)
heights = np.linspace(7, 15, 21)
sf = np.array([(X2 > h).mean() for h in heights])
sfE = rft1d.chi2.sf(heights, df, nNodes, FWHM)
sf0D = rft1d.chi2.sf0d(heights, df)
pyplot.close('all')
ax = pyplot.axes()
ax.plot(heights, sf, 'o', label='Simulated')
ax.plot(heights, sfE, '-', label='Theoretical')
ax.plot(heights, sf0D, 'r-', label='Theoretical (0D)')
ax.set_xlabel('$u$', size=20)
ax.set_ylabel('$P (\\chi^2_\\mathrm{max} > u)$', size=20)
ax.legend()
ax.set_title('CCA validation (1D)', size=20)
pyplot.show()