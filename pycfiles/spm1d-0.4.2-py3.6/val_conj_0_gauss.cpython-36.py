# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/spm1d/rft1d/examples/val_conj_0_gauss.py
# Compiled at: 2019-08-22 04:37:04
# Size of source mod 2**32: 1170 bytes
import numpy as np
from matplotlib import pyplot
from spm1d import rft1d
np.random.seed(0)
nTestStatFields = 3
nNodes = 101
nIterations = 10000
FWHM = 10.0
rftcalc = rft1d.prob.RFTCalculator(STAT='Z', nodes=nNodes, FWHM=FWHM, n=nTestStatFields)
generator = rft1d.random.Generator1D(nTestStatFields, nNodes, FWHM)
Zmax = []
for i in range(nIterations):
    y = generator.generate_sample()
    Zconj = y.min(axis=0)
    Zmax.append(Zconj.max())

Zmax = np.array(Zmax)
heights = np.linspace(0.5, 2, 21)
sf = np.array([(Zmax > h).mean() for h in heights])
sfE = rftcalc.sf(heights)
pyplot.close('all')
ax = pyplot.axes()
ax.plot(heights, sf, 'o', label='Simulated')
ax.plot(heights, sfE, '-', label='Theoretical')
ax.set_xlabel('$u$', size=20)
ax.set_ylabel('$P(z_\\mathrm{conj} > u)$', size=20)
ax.legend()
ax.set_title('Conjunction validation (Gaussian fields)', size=20)
pyplot.show()