# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/spm1d/rft1d/examples/val_upx_3_T2_cluster.py
# Compiled at: 2019-08-22 04:37:04
# Size of source mod 2**32: 2122 bytes
from math import sqrt, log
import numpy as np
from matplotlib import pyplot
from spm1d import rft1d
eps = np.finfo(float).eps

def here_hotellingsT2(y):
    N = y.shape[0]
    m = np.matrix(y.mean(axis=0))
    T2 = []
    for ii, mm in enumerate(m):
        W = np.matrix(np.cov((y[:, ii, :].T), ddof=1))
        t2 = N * mm * np.linalg.inv(W) * mm.T
        T2.append(float(t2))

    return np.asarray(T2)


np.random.seed(0)
nResponses = 30
nComponents = 2
nNodes = 101
nIterations = 500
FWHM = 10.0
W0 = np.eye(nComponents)
interp = True
wrap = True
heights = [8, 10, 12, 14]
df = (
 nComponents, nResponses - 1)
calc = rft1d.geom.ClusterMetricCalculator()
rftcalc = rft1d.prob.RFTCalculator(STAT='T2', df=df, nodes=nNodes, FWHM=FWHM)
T2 = []
generator = rft1d.random.GeneratorMulti1D(nResponses, nNodes, nComponents, FWHM, W0)
for i in range(nIterations):
    y = generator.generate_sample()
    t2 = here_hotellingsT2(y)
    T2.append(t2)

T2 = np.asarray(T2)
K0 = np.linspace(eps, 12, 21)
K = np.array([[calc.max_cluster_extent(yy, h, interp, wrap) for yy in T2] for h in heights])
P = np.array([(K >= k0).mean(axis=1) for k0 in K0]).T
P0 = np.array([[rftcalc.p.cluster(k0, h) for k0 in K0 / FWHM] for h in heights])
pyplot.close('all')
colors = ['b', 'g', 'r', 'orange']
labels = ['u = %.1f' % h for h in heights]
ax = pyplot.axes()
for color, p, p0, label in zip(colors, P, P0, labels):
    ax.plot(K0, p, 'o', color=color)
    ax.plot(K0, p0, '-', color=color, label=label)

ax.plot([0, 1], [10, 10], 'k-', label='Theoretical')
ax.plot([0, 1], [10, 10], 'ko-', label='Simulated')
ax.set_xlabel('x', size=16)
ax.set_ylabel('P(k_max) > x', size=16)
ax.set_ylim(0, 0.3)
ax.legend()
ax.set_title('Upcrossing extent validations ($T^2$ fields)', size=20)
pyplot.show()