# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/spm1d/rft1d/examples/val_conj_1_t.py
# Compiled at: 2019-08-22 04:37:04
# Size of source mod 2**32: 1445 bytes
import numpy as np
from matplotlib import pyplot
from spm1d import rft1d
np.random.seed(0)
nResponses = 12
nTestStatFields = 2
nNodes = 101
nIterations = 2000
FWHM = 10.0
df = nResponses - 1
sqrtN = np.sqrt(nResponses)
rftcalc = rft1d.prob.RFTCalculator(STAT='T', df=(1, df), nodes=nNodes, FWHM=FWHM, n=nTestStatFields)
generator = rft1d.random.Generator1D(nResponses, nNodes, FWHM)
Tmax = []
for i in range(nIterations):
    T = []
    for i in range(nTestStatFields):
        y = generator.generate_sample()
        t = y.mean(axis=0) / y.std(ddof=1, axis=0) * sqrtN
        T.append(t)

    Tconj = np.min(T, axis=0)
    Tmax.append(Tconj.max())

Tmax = np.array(Tmax)
heights = np.linspace(1, 3, 21)
sf = np.array([(Tmax > h).mean() for h in heights])
sfE = rftcalc.sf(heights)
pyplot.close('all')
ax = pyplot.axes()
ax.plot(heights, sf, 'o', label='Simulated')
ax.plot(heights, sfE, '-', label='Theoretical')
ax.set_xlabel('$u$', size=20)
ax.set_ylabel('$P(t_\\mathrm{conj} > u)$', size=20)
ax.legend()
ax.set_title('Conjunction validation (t fields)', size=20)
pyplot.show()