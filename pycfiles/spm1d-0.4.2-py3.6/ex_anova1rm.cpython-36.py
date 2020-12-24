# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/spm1d/examples/stats1d_roi/ex_anova1rm.py
# Compiled at: 2019-08-22 04:37:03
# Size of source mod 2**32: 1020 bytes
import numpy as np
from matplotlib import pyplot
import spm1d
dataset = spm1d.data.uv1d.anova1rm.SpeedGRFcategoricalRM()
Y, A, SUBJ = dataset.get_data()
roi = np.array([False] * Y.shape[1])
roi[70:] = True
alpha = 0.05
equal_var = True
F = spm1d.stats.anova1(Y, A, equal_var, roi=roi)
Frm = spm1d.stats.anova1rm(Y, A, SUBJ, equal_var, roi=roi)
Fi = F.inference(alpha)
Firm = Frm.inference(alpha)
pyplot.close('all')
pyplot.figure(figsize=(8, 3.5))
ax0 = pyplot.axes((0.1, 0.15, 0.35, 0.8))
ax1 = pyplot.axes((0.55, 0.15, 0.35, 0.8))
ax0.plot(Y[(A == 0)].T, 'b')
ax0.plot(Y[(A == 1)].T, 'k')
ax0.plot(Y[(A == 2)].T, 'r')
Firm.plot(ax=ax1, color='r', facecolor=(0.8, 0.3, 0.3), label='Within-subjects analysis')
Fi.plot(ax=ax1, label='Between-subjects analysis')
ax1.legend(fontsize=8)
pyplot.show()