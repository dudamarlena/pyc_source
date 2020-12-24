# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/spm1d/rft1d/examples/weather_1_rft.py
# Compiled at: 2019-08-22 04:37:04
# Size of source mod 2**32: 2199 bytes
import numpy as np
from scipy.ndimage.filters import gaussian_filter1d
from matplotlib import pyplot
from spm1d import rft1d
weather = rft1d.data.weather()
yA, yB = weather['Atlantic'], weather['Continental']
yA = gaussian_filter1d(yA, 8.0, axis=1, mode='wrap')
yB = gaussian_filter1d(yB, 8.0, axis=1, mode='wrap')
nA, nB = yA.shape[0], yB.shape[0]
mA, mB = yA.mean(axis=0), yB.mean(axis=0)
sA, sB = yA.std(ddof=1, axis=0), yB.std(ddof=1, axis=0)
s = np.sqrt(((nA - 1) * sA * sA + (nB - 1) * sB * sB) / (nA + nB - 2))
t = (mA - mB) / (s * np.sqrt(1.0 / nA + 1.0 / nB))
rA, rB = yA - mA, yB - mB
r = np.vstack([rA, rB])
FWHM = rft1d.geom.estimate_fwhm(r)
alpha = 0.05
df = nA + nB - 2
Q = yA.shape[1]
tstar = rft1d.t.isf(alpha, df, Q, FWHM)
calc = rft1d.geom.ClusterMetricCalculator()
k = calc.cluster_extents(t, tstar, interp=True)
k_resels = [kk / FWHM for kk in k]
nClusters = len(k)
rftcalc = rft1d.prob.RFTCalculator(STAT='T', df=(1, df), nodes=Q, FWHM=FWHM)
Pset = rftcalc.p.set(nClusters, min(k_resels), tstar)
Pcluster = [rftcalc.p.cluster(kk, tstar) for kk in k_resels]
pyplot.close('all')
ax = pyplot.axes()
ax.plot(t, 'k', lw=3, label='t field')
ax.plot([0, Q], ([tstar] * 2), 'r--', label='Critical threshold')
ax.legend(loc='upper left')
ax.text(10, 3.0, 'p = %.3f' % Pcluster[0])
ax.text(300, 3.6, 'p = %.3f' % Pcluster[1])
ax.text(280, 2.3, ('$\\alpha$ = %.3f' % alpha), color='r')
ax.set_xlabel('Day', size=16)
ax.set_ylabel('t value', size=16)
ax.set_title('RFT-based inference of weather dataset', size=20)
pyplot.show()