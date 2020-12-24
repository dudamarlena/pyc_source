# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/spm1d/rft1d/examples/val_broken_0_gauss.py
# Compiled at: 2019-08-22 04:37:04
# Size of source mod 2**32: 1497 bytes
import numpy as np
from matplotlib import pyplot
from spm1d import rft1d
np.random.seed(0)
nResponses = 10000
nNodes = 101
FWHM = 13.1877
nodes_full = np.array([True] * nNodes)
nodes = nodes_full.copy()
nodes[20:45] = False
nodes[60:80] = False
y_full = rft1d.randn1d(nResponses, nNodes, FWHM)
np.random.seed(0)
y_broken = rft1d.randn1d(nResponses, nodes, FWHM)
ymax_full = y_full.max(axis=1)
ymax_broken = np.nanmax(y_broken, axis=1)
heights = np.linspace(2.0, 4, 21)
sf_full = np.array([(ymax_full >= h).mean() for h in heights])
sf_broken = np.array([(ymax_broken >= h).mean() for h in heights])
sfE_full = rft1d.norm.sf(heights, nNodes, FWHM)
sfE_broken = rft1d.norm.sf(heights, nodes, FWHM)
pyplot.close('all')
ax = pyplot.axes()
ax.plot(heights, sfE_full, 'b-', label='Theoretical (full)')
ax.plot(heights, sfE_broken, 'r-', label='Theoretical (broken)')
ax.plot(heights, sf_full, 'bo', label='Simulated (full)')
ax.plot(heights, sf_broken, 'ro', label='Simulated (broken)')
ax.set_xlabel('x', size=16)
ax.set_ylabel('$P (z_\\mathrm{max} > x)$', size=20)
ax.legend()
ax.set_title('Broken field validation (Gaussian)', size=20)
pyplot.show()