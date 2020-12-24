# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/spm1d/rft1d/examples/val_max_6_twosample_T2_0d.py
# Compiled at: 2019-08-22 04:37:04
# Size of source mod 2**32: 1512 bytes
import numpy as np
from matplotlib import pyplot
from spm1d import rft1d
np.random.seed(1)
nResponsesA = 8
nResponsesB = 13
nComponents = 3
nIterations = 5000
W0 = np.eye(nComponents)
nTotal = nResponsesA + nResponsesB
df = (nComponents, float(nTotal - 2))
T2 = []
JA, JB = nResponsesA, nResponsesB
for i in range(nIterations):
    yA = np.random.multivariate_normal(np.zeros(nComponents), W0, JA)
    yB = np.random.multivariate_normal(np.zeros(nComponents), W0, JB)
    yA, yB = np.matrix(yA), np.matrix(yB)
    mA, mB = yA.mean(axis=0), yB.mean(axis=0)
    WA, WB = np.cov(yA.T), np.cov(yB.T)
    W = ((JA - 1) * WA + (JB - 1) * WB) / (JA + JB - 2)
    t2 = JA * JB / float(JA + JB) * (mB - mA) * np.linalg.inv(W) * (mB - mA).T
    T2.append(float(t2))

T2 = np.asarray(T2)
heights = np.linspace(4, 20, 21)
sf = np.array([(T2 > h).mean() for h in heights])
sfE = rft1d.T2.sf0d(heights, df)
pyplot.close('all')
ax = pyplot.axes()
ax.plot(heights, sf, 'o', label='Simulated')
ax.plot(heights, sfE, '-', label='Theoretical')
ax.set_xlabel('x', size=16)
ax.set_ylabel('P (T $^2$ > x)', size=16)
ax.legend()
ax.set_title("Two-sample Hotelling's T2 validation (0D)", size=20)
pyplot.show()