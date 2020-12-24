# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/spm1d/rft1d/examples/val_upx_2_F_set.py
# Compiled at: 2019-08-22 04:37:04
# Size of source mod 2**32: 2524 bytes
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
nResponses = (7, 8, 9)
nNodes = 101
nIterations = 5000
FWHM = 10.0
interp = True
wrap = True
heights = [6, 7, 8]
c = 2
nGroups = len(nResponses)
nTotal = sum(nResponses)
df = (nGroups - 1, nTotal - nGroups)
X, X0, Xi, X0i = here_design_matrices(nResponses, nGroups)
calc = rft1d.geom.ClusterMetricCalculator()
rftcalc = rft1d.prob.RFTCalculator(STAT='F', df=df, nodes=nNodes, FWHM=FWHM)
F = []
generator = rft1d.random.Generator1D(nTotal, nNodes, FWHM)
for i in range(nIterations):
    y = generator.generate_sample()
    f = here_anova1(y, X, X0, Xi, X0i, df)
    F.append(f)

F = np.asarray(F)
K0 = np.linspace(eps, 8, 21)
K = [[calc.cluster_extents(yy, h, interp, wrap) for yy in F] for h in heights]
C = np.array([[[sum([kkk >= k0 for kkk in kk]) for kk in k] for k in K] for k0 in K0])
P = np.mean((C >= c), axis=2).T
P0 = np.array([[rftcalc.p.set(c, k0, h) for h in heights] for k0 in K0 / FWHM]).T
pyplot.close('all')
colors = ['b', 'g', 'r']
ax = pyplot.axes()
for color, p, p0, u in zip(colors, P, P0, heights):
    ax.plot(K0, p, 'o', color=color)
    ax.plot(K0, p0, '-', color=color, label=('u = %.1f' % u))

ax.set_xlabel('x', size=16)
ax.set_ylabel('P(c, k_min) > x', size=16)
ax.legend()
ax.set_title('Set-level inference validations (F fields)', size=20)
pyplot.show()