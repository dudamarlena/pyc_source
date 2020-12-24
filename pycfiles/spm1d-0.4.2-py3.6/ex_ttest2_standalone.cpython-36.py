# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/spm1d/examples/nonparam/0d/ex_ttest2_standalone.py
# Compiled at: 2019-08-22 04:37:03
# Size of source mod 2**32: 1524 bytes
from math import sqrt
import itertools, numpy as np
from scipy import stats
yA = np.array([0.7, 0.6, 0.5, 0.4, 0.5])
yB = np.array([0.4, 0.2, 0.5, 0.3, 0.4])
alpha = 0.05
nA, nB = yA.size, yB.size
df = nA + nB - 2
mA, mB = yA.mean(), yB.mean()
sA, sB = yA.std(ddof=1), yB.std(ddof=1)
s = np.sqrt(((nA - 1) * sA * sA + (nB - 1) * sB * sB) / (nA + nB - 2))
t0 = (mA - mB) / (s * sqrt(1.0 / nA + 1.0 / nB))
N = nA + nB
GROUPA = itertools.combinations(range(N), nA)
T = []
y = np.hstack([yA, yB])
for groupA in GROUPA:
    labels = np.zeros(N)
    labels[list(groupA)] = 1
    yyA = y[(labels == 1)]
    yyB = y[(labels == 0)]
    mA, mB = yyA.mean(), yyB.mean()
    sA, sB = yyA.std(ddof=1), yyB.std(ddof=1)
    s = np.sqrt(((nA - 1) * sA * sA + (nB - 1) * sB * sB) / (nA + nB - 2))
    t = (mA - mB) / (s * sqrt(1.0 / nA + 1.0 / nB))
    T.append(t)

T = np.array(T)
p = np.mean(T > t0)
tCrit = np.percentile(T, 100 * (1 - alpha))
p_para = stats.t.sf(t0, df)
tCrit_para = stats.t.isf(alpha, df)
print('Non-parametric test:')
print('   t=%.3f, p=%.5f, tCritical=%.3f' % (t0, p, tCrit))
print
print('Parametric test:')
print('   t=%.3f, p=%.5f, tCritical=%.3f' % (t0, p_para, tCrit_para))
print