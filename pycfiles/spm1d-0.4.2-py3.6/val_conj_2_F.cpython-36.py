# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/spm1d/rft1d/examples/val_conj_2_F.py
# Compiled at: 2019-08-22 04:37:04
# Size of source mod 2**32: 2269 bytes
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
nTestStatFields = 3
nNodes = 101
nIterations = 2000
FWHM = 8.0
nGroups = len(nResponses)
nTotal = sum(nResponses)
df = (nGroups - 1, nTotal - nGroups)
X, X0, Xi, X0i = here_design_matrices(nResponses, nGroups)
rftcalc = rft1d.prob.RFTCalculator(STAT='F', df=df, nodes=nNodes, FWHM=FWHM, n=nTestStatFields)
Fmax = []
generator = rft1d.random.Generator1D(nTotal, nNodes, FWHM)
for i in range(nIterations):
    F = []
    for i in range(nTestStatFields):
        y = generator.generate_sample()
        f = here_anova1(y, X, X0, Xi, X0i, df)
        F.append(f)

    Fconj = np.min(F, axis=0)
    Fmax.append(Fconj.max())

Fmax = np.array(Fmax)
heights = np.linspace(2, 5, 21)
sf = np.array([(Fmax > h).mean() for h in heights])
sfE = rftcalc.sf(heights)
pyplot.close('all')
ax = pyplot.axes()
ax.plot(heights, sf, 'o', label='Simulated')
ax.plot(heights, sfE, '-', label='Theoretical')
ax.set_xlabel('$u$', size=20)
ax.set_ylabel('$P(F_\\mathrm{conj} > u)$', size=20)
ax.legend()
ax.set_title('Conjunction validation (F fields)', size=20)
pyplot.show()