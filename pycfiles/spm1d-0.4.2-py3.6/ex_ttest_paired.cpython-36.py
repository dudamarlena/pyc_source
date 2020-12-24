# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/spm1d/examples/stats1d_roi/ex_ttest_paired.py
# Compiled at: 2019-08-22 04:37:04
# Size of source mod 2**32: 1038 bytes
import numpy as np
from matplotlib import pyplot
import spm1d
dataset = spm1d.data.uv1d.t2.PlantarArchAngle()
YA, YB = dataset.get_data()
roi = np.array([False] * YA.shape[1])
roi[0:10] = True
alpha = 0.05
t = spm1d.stats.ttest_paired(YA, YB, roi=roi)
ti = t.inference(alpha, two_tailed=False, interp=True)
pyplot.close('all')
pyplot.figure(figsize=(8, 3.5))
ax = pyplot.axes((0.1, 0.15, 0.35, 0.8))
spm1d.plot.plot_mean_sd(YA)
spm1d.plot.plot_mean_sd(YB, linecolor='r', facecolor='r')
spm1d.plot.plot_roi(roi, facecolor='b', alpha=0.3)
ax.axhline(y=0, color='k', linestyle=':')
ax.set_xlabel('Time (%)')
ax.set_ylabel('Plantar arch angle  (deg)')
ax = pyplot.axes((0.55, 0.15, 0.35, 0.8))
ti.plot()
ti.plot_threshold_label(fontsize=8)
ti.plot_p_values(size=10, offsets=[(0, 0.3)])
ax.set_xlabel('Time (%)')
pyplot.show()