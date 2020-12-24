# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/spm1d/rft1d/examples/val_broken_1_t.py
# Compiled at: 2019-08-22 04:37:04
# Size of source mod 2**32: 1468 bytes
import numpy as np
from matplotlib import pyplot
from spm1d import rft1d
np.random.seed(0)
nResponses = 12
nIterations = 5000
nNodes = 101
FWHM = 11.5
df = nResponses - 1
sqrtN = np.sqrt(nResponses)
nodes = np.array([True] * nNodes)
nodes[10:25] = False
nodes[50:75] = False
generator = rft1d.random.Generator1D(nResponses, nodes, FWHM)
T = []
for i in range(nIterations):
    y = generator.generate_sample()
    t = y.mean(axis=0) / y.std(ddof=1, axis=0) * sqrtN
    T.append(np.nanmax(t))

T = np.array(T)
heights = np.linspace(2.0, 4, 21)
sf = np.array([(T >= h).mean() for h in heights])
sfE_full = rft1d.t.sf(heights, df, nNodes, FWHM)
sfE_broken = rft1d.t.sf(heights, df, nodes, FWHM)
pyplot.close('all')
ax = pyplot.axes()
ax.plot(heights, sfE_full, 'b-', label='Theoretical (full)')
ax.plot(heights, sfE_broken, 'r-', label='Theoretical (broken)')
ax.plot(heights, sf, 'ro', label='Simulated (broken)')
ax.set_xlabel('x', size=16)
ax.set_ylabel('$P (t_\\mathrm{max} > x)$', size=20)
ax.legend()
ax.set_title('Broken field validation (t)', size=20)
pyplot.show()