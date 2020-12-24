# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/spm1d/rft1d/examples/val_broken_2_F.py
# Compiled at: 2019-08-22 04:37:04
# Size of source mod 2**32: 2351 bytes
import numpy as np
from matplotlib import pyplot
from spm1d import rft1d
eps = np.finfo(float).eps

def here_anova1(Y, X, X0, Xi, X0i, df):
    Y = np.matrix(Y)
    b = Xi * Y
    eij = Y - X * b
    R = eij.T * eij
    b0 = X0i * Y
    eij0 = Y - X0 * b0
    R0 = eij0.T * eij0
    F = (np.diag(R0) - np.diag(R)) / df[0] / (np.diag(R + eps) / df[1])
    return F


def here_design_matrices(nResponses, nGroups):
    nTotal = sum(nResponses)
    X = np.zeros((nTotal, nGroups))
    i0 = 0
    for i, n in enumerate(nResponses):
        X[i0:i0 + n, i] = 1
        i0 += n

    X = np.matrix(X)
    X0 = np.matrix(np.ones(nTotal)).T
    Xi, X0i = np.linalg.pinv(X), np.linalg.pinv(X0)
    return (X, X0, Xi, X0i)


np.random.seed(0)
nResponses = (9, 8, 9)
nNodes = 101
nIterations = 2000
FWHM = 8.0
nGroups = len(nResponses)
nTotal = sum(nResponses)
df = (nGroups - 1, nTotal - nGroups)
X, X0, Xi, X0i = here_design_matrices(nResponses, nGroups)
nodes = np.array([True] * nNodes)
nodes[10:25] = False
nodes[60:85] = False
generator = rft1d.random.Generator1D(nTotal, nodes, FWHM)
F = []
for i in range(nIterations):
    y = generator.generate_sample()
    f = here_anova1(y, X, X0, Xi, X0i, df)
    F.append(np.nanmax(f))

F = np.array(F)
heights = np.linspace(2.0, 8, 21)
sf = np.array([(F >= h).mean() for h in heights])
sfE_full = rft1d.f.sf(heights, df, nNodes, FWHM)
sfE_broken = rft1d.f.sf(heights, df, nodes, FWHM)
pyplot.close('all')
ax = pyplot.axes()
ax.plot(heights, sfE_full, 'b-', label='Theoretical (full)')
ax.plot(heights, sfE_broken, 'r-', label='Theoretical (broken)')
ax.plot(heights, sf, 'ro', label='Simulated (broken)')
ax.set_xlabel('x', size=16)
ax.set_ylabel('$P (F_\\mathrm{max} > x)$', size=20)
ax.legend()
ax.set_title('Broken field validation (F)', size=20)
pyplot.show()