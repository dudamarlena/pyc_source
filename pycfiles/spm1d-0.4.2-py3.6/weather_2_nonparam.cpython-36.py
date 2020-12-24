# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/spm1d/rft1d/examples/weather_2_nonparam.py
# Compiled at: 2019-08-22 04:37:04
# Size of source mod 2**32: 2452 bytes
import numpy as np
from scipy.ndimage.filters import gaussian_filter1d
from matplotlib import pyplot
from spm1d import rft1d

def here_tstat2(yA, yB):
    nA, nB = yA.shape[0], yB.shape[0]
    mA, mB = yA.mean(axis=0), yB.mean(axis=0)
    sA, sB = yA.std(ddof=1, axis=0), yB.std(ddof=1, axis=0)
    s = np.sqrt(((nA - 1) * sA * sA + (nB - 1) * sB * sB) / (nA + nB - 2))
    t = (mA - mB) / (s * np.sqrt(1.0 / nA + 1.0 / nB))
    return t


weather = rft1d.data.weather()
yA, yB = weather['Atlantic'], weather['Continental']
yA = gaussian_filter1d(yA, 8.0, axis=1, mode='wrap')
yB = gaussian_filter1d(yB, 8.0, axis=1, mode='wrap')
nA, nB = yA.shape[0], yB.shape[0]
N = nA + nB
t0 = here_tstat2(yA, yB)
np.random.seed(0)
nIter = 1000
T = []
y = np.vstack((yA, yB))
for iii in range(nIter):
    ind = np.random.permutation(N)
    i0, i1 = ind[:nA], ind[nA:]
    yyA, yyB = y[i0], y[i1]
    T.append(here_tstat2(yyA, yyB).max())

alpha = 0.05
tstar = np.percentile(T, 100 * (1 - alpha))
calc = rft1d.geom.ClusterMetricCalculator()
k0 = calc.cluster_extents(t0, tstar, interp=True)
nIter = 1000
K = []
for iii in range(nIter):
    ind = np.random.permutation(N)
    i0, i1 = ind[:nA], ind[nA:]
    yyA, yyB = y[i0], y[i1]
    t = here_tstat2(yyA, yyB)
    k = calc.cluster_extents(t, tstar, interp=True)
    K.append(max(k))

K = np.array(K)
Pcluster = [(K >= kk).mean() for kk in k0]
pyplot.close('all')
ax = pyplot.axes()
ax.plot(t0, 'k', lw=3, label='t field')
ax.plot([0, t.size], ([tstar] * 2), 'r--', label='Critical threshold')
ax.legend(loc='upper left')
ax.text(10, 3.0, 'p = %.3f' % Pcluster[0])
ax.text(300, 3.6, 'p = %.3f' % Pcluster[1])
ax.text(280, 2.1, ('$\\alpha$ = %.3f' % alpha), color='r')
ax.set_xlabel('Day', size=16)
ax.set_ylabel('t value', size=16)
ax.set_title('Non-parametric RFT-like inference of weather dataset', size=20)
pyplot.show()