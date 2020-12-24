# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/spm1d/examples/stats1d/rfx_2_level2.py
# Compiled at: 2019-08-22 04:37:03
# Size of source mod 2**32: 782 bytes
import os, numpy as np
from matplotlib import pyplot
import spm1d
nSubj = 10
BETA = []
for subj in range(nSubj):
    dataset = spm1d.data.uv1d.regress.SpeedGRF(subj=subj)
    Y, x = dataset.get_data()
    t = spm1d.stats.regress(Y, x)
    BETA.append(t.beta[0])

BETA = np.array(BETA)
alpha = 0.05
t = spm1d.stats.ttest(BETA)
ti = t.inference(alpha, two_tailed=True)
pyplot.close('all')
ti.plot()
ti.plot_threshold_label(fontsize=12)
ti.plot_p_values()
pyplot.xlabel('Time (% stance)', size=16)
pyplot.show()