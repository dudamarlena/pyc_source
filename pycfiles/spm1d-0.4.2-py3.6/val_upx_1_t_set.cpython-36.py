# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/spm1d/rft1d/examples/val_upx_1_t_set.py
# Compiled at: 2019-08-22 04:37:04
# Size of source mod 2**32: 1698 bytes
import numpy as np
from matplotlib import pyplot
from spm1d import rft1d
eps = np.finfo(float).eps
np.random.seed(0)
nResponses = 12
nNodes = 101
nIterations = 2000
FWHM = 8.5
interp = True
wrap = True
heights = [2.0, 2.2, 2.4]
c = 2
df = nResponses - 1
sqrtN = np.sqrt(nResponses)
calc = rft1d.geom.ClusterMetricCalculator()
rftcalc = rft1d.prob.RFTCalculator(STAT='T', df=(1, df), nodes=nNodes, FWHM=FWHM)
T = []
generator = rft1d.random.Generator1D(nResponses, nNodes, FWHM)
for i in range(nIterations):
    y = generator.generate_sample()
    t = y.mean(axis=0) / y.std(ddof=1, axis=0) * sqrtN
    T.append(t)

T = np.asarray(T)
K0 = np.linspace(eps, 8, 21)
K = [[calc.cluster_extents(yy, h, interp, wrap) for yy in T] for h in heights]
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
ax.set_title('Set-level inference validations (t fields)', size=20)
pyplot.show()