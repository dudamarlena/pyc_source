# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/spm1d/examples/stats1d/ex_ci_onesample_standalone.py
# Compiled at: 2019-08-22 04:37:03
# Size of source mod 2**32: 1583 bytes
import numpy as np
from matplotlib import pyplot
import spm1d
from spm1d import rft1d
dataset = spm1d.data.uv1d.t1.SimulatedPataky2015b()
y, mu = dataset.get_data()
alpha = 0.05
J = y.shape[0]
df = J - 1
m = y.mean(axis=0)
s = y.std(axis=0, ddof=1)
residuals = y - m
fwhm = rft1d.geom.estimate_fwhm(residuals)
resels = rft1d.geom.resel_counts(residuals, fwhm, element_based=False)
zstar = rft1d.t.isf_resels(0.5 * alpha, df, resels)
hstar = zstar * s / J ** 0.5
ci = (m - hstar, m + hstar)
ci_spm1d = spm1d.stats.ci_onesample(y, alpha, mu)
pyplot.close('all')
pyplot.figure(figsize=(10, 4))
ax = pyplot.subplot(121)
ax.plot(m, color='b', lw=3)
ax.plot((ci[0]), color='b', lw=1, linestyle=':')
ax.plot((ci[1]), color='b', lw=1, linestyle=':')
ax.axhline(0, color='k', linestyle='--')
ax.set_title('Manually computed CI', size=10)
ax.set_ylim(-7, 13)
ax = pyplot.subplot(122)
ci_spm1d.plot(ax)
ax.set_title('spm1d result', size=10)
pyplot.suptitle('One-sample CIs')
ax.set_ylim(-7, 13)
pyplot.show()