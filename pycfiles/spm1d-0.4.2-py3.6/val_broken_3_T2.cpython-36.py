# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/spm1d/rft1d/examples/val_broken_3_T2.py
# Compiled at: 2019-08-22 04:37:04
# Size of source mod 2**32: 1887 bytes
import numpy as np
from matplotlib import pyplot
from spm1d import rft1d

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
nResponses = 25
nNodes = 101
nComponents = 2
nIterations = 200
FWHM = 12.0
W0 = np.eye(nComponents)
df = (
 nComponents, nResponses - 1)
nodes = np.array([True] * nNodes)
nodes[10:30] = False
nodes[60:85] = False
generator = rft1d.random.GeneratorMulti1D(nResponses, nodes, nComponents, FWHM, W0)
T2 = []
for i in range(nIterations):
    y = generator.generate_sample()
    t2 = here_hotellingsT2(y)
    T2.append(np.nanmax(t2))

T2 = np.array(T2)
heights = np.linspace(8.0, 15, 21)
sf = np.array([(T2 >= h).mean() for h in heights])
sfE_full = rft1d.T2.sf(heights, df, nNodes, FWHM)
sfE_broken = rft1d.T2.sf(heights, df, nodes, FWHM)
pyplot.close('all')
ax = pyplot.axes()
ax.plot(heights, sfE_full, 'b-', label='Theoretical (full)')
ax.plot(heights, sfE_broken, 'r-', label='Theoretical (broken)')
ax.plot(heights, sf, 'ro', label='Simulated (broken)')
ax.set_xlabel('x', size=16)
ax.set_ylabel('$P (T^2_\\mathrm{max} > x)$', size=20)
ax.legend()
ax.set_title('Broken field validation ($T^2$)', size=20)
pyplot.show()