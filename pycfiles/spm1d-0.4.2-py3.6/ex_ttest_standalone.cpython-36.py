# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/spm1d/examples/nonparam/0d/ex_ttest_standalone.py
# Compiled at: 2019-08-22 04:37:03
# Size of source mod 2**32: 1090 bytes
from math import sqrt
import itertools, numpy as np
from scipy import stats
y = np.array([0.4, 0.2, 0.5, 0.3, -0.1])
n, df = y.size, y.size - 1
alpha = 0.05
sqrtN = sqrt(n)
t0 = y.mean() / y.std(ddof=1) * sqrtN
LABELS = list(itertools.product([0, 1], repeat=n))
T = []
for labels in LABELS:
    signs = -2 * np.array(labels) + 1
    yy = y.copy() * signs
    t = yy.mean() / yy.std(ddof=1) * sqrtN
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