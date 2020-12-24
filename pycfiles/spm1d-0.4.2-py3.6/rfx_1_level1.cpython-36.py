# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/spm1d/examples/stats1d/rfx_1_level1.py
# Compiled at: 2019-08-22 04:37:03
# Size of source mod 2**32: 713 bytes
import numpy as np
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
pyplot.close('all')
ax = pyplot.axes((0.15, 0.15, 0.8, 0.8))
pyplot.plot((BETA.T), color='k')
ax.axhline(y=0, color='k', linewidth=1, linestyle=':')
ax.set_xlabel('Time (% stance)')
ax.set_ylabel('$\\beta_0$   $(BW / ms^{-1})$')
pyplot.show()