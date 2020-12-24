# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/spm1d/rft1d/examples/val_conj_3_T2.py
# Compiled at: 2019-08-22 04:37:04
# Size of source mod 2**32: 1807 bytes
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
nResponses = 21
nNodes = 101
nComponents = 2
nTestStatFields = 3
nIterations = 100
FWHM = 12.0
W0 = np.eye(nComponents)
df = (
 nComponents, nResponses - 1)
rftcalc = rft1d.prob.RFTCalculator(STAT='T2', df=df, nodes=nNodes, FWHM=FWHM, n=nTestStatFields)
T2max = []
generator = rft1d.random.GeneratorMulti1D(nResponses, nNodes, nComponents, FWHM, W0)
for i in range(nIterations):
    T2 = []
    for i in range(nTestStatFields):
        y = generator.generate_sample()
        t2 = here_hotellingsT2(y)
        T2.append(t2)

    T2conj = np.min(T2, axis=0)
    T2max.append(T2conj.max())

T2max = np.array(T2max)
heights = np.linspace(3, 7, 21)
sf = np.array([(T2max > h).mean() for h in heights])
sfE = rftcalc.sf(heights)
pyplot.close('all')
ax = pyplot.axes()
ax.plot(heights, sf, 'o', label='Simulated')
ax.plot(heights, sfE, '-', label='Theoretical')
ax.set_xlabel('$u$', size=20)
ax.set_ylabel('$P(T^2_\\mathrm{conj} > u)$', size=20)
ax.legend()
ax.set_title('Conjunction validation ($T^2$ fields)', size=20)
pyplot.show()