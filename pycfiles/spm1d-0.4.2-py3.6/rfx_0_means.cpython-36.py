# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/spm1d/examples/stats1d/rfx_0_means.py
# Compiled at: 2019-08-22 04:37:03
# Size of source mod 2**32: 869 bytes
import numpy as np
from matplotlib import pyplot
import spm1d
nSubj = 10
Y1, Y2, Y3 = [], [], []
for subj in range(10):
    dataset = spm1d.data.uv1d.anova1.SpeedGRFcategorical(subj=subj)
    Y, A = dataset.get_data()
    y1, y2, y3 = Y[(A == 1)], Y[(A == 2)], Y[(A == 3)]
    Y1.append(y1.mean(axis=0))
    Y2.append(y2.mean(axis=0))
    Y3.append(y3.mean(axis=0))

Y1, Y2, Y3 = np.asarray(Y1), np.asarray(Y2), np.asarray(Y3)
pyplot.close('all')
h1 = pyplot.plot((Y1.T), color='b')
h2 = pyplot.plot((Y2.T), color='k')
h3 = pyplot.plot((Y3.T), color='r')
h1[0].set_label('Slow')
h2[0].set_label('Normal')
h3[0].set_label('Fast')
pyplot.legend(loc='lower center', fontsize=12)
pyplot.xlabel('Time (% stance)')
pyplot.ylabel('GRF (BW)')
pyplot.show()