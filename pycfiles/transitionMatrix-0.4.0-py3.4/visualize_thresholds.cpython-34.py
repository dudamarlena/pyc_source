# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/examples/python/visualize_thresholds.py
# Compiled at: 2018-10-21 10:35:49
# Size of source mod 2**32: 2125 bytes
""" Visualize Calculated Thresholds

"""
import matplotlib.pyplot as plt
from matplotlib import collections as mc
import transitionMatrix as tm
from datasets import Generic
from transitionMatrix.thresholds.model import ThresholdSet
from transitionMatrix.thresholds.settings import AR_Model
M = tm.TransitionMatrix(values=Generic)
Ratings = M.dimension
Default = Ratings - 1
Periods = 10
T = tm.TransitionMatrixSet(values=M, periods=Periods, method='Power', temporal_type='Cumulative')
As = ThresholdSet(TMSet=T)
for ri in range(0, Ratings):
    print('RI: ', ri)
    As.fit(AR_Model, ri)

lines = []
ri = 3
for rf in range(0, Ratings):
    for k in range(0, Periods):
        if rf != ri:
            value = As.A[(ri, rf, k)]
            line = [(k, value), (k + 1.0, value)]
            lines.append(line)
            continue

lc = mc.LineCollection(lines, linewidths=2)
fig, ax = plt.subplots()
ax.add_collection(lc)
ax.autoscale()
ax.margins(0.1)
ax.set_xlabel('Periods')
ax.set_ylabel('Normalized Z Level')
plt.title('Rating Transition Thresholds')
plt.savefig('Thresholds.png')