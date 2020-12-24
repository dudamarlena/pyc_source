# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/spm1d/examples/stats1d_roi/ex_ttest2.py
# Compiled at: 2019-08-22 04:37:04
# Size of source mod 2**32: 1033 bytes
import numpy as np
from matplotlib import pyplot
import spm1d
dataset = spm1d.data.uv1d.t2.SimulatedTwoLocalMax()
YA, YB = dataset.get_data()
roi = np.array([False] * YA.shape[1])
roi[15:35] = True
roi[65:85] = True
alpha = 0.05
t = spm1d.stats.ttest2(YB, YA, equal_var=True, roi=roi)
ti = t.inference(alpha, two_tailed=False, interp=True)
print(ti)
pyplot.close('all')
pyplot.figure(figsize=(8, 3.5))
ax = pyplot.axes((0.1, 0.15, 0.35, 0.8))
spm1d.plot.plot_mean_sd(YA, roi=roi)
spm1d.plot.plot_mean_sd(YB, linecolor='r', facecolor='r', roi=roi)
ax.axhline(y=0, color='k', linestyle=':')
ax.set_xlabel('Time (%)')
ax.set_ylabel('Plantar arch angle  (deg)')
ax = pyplot.axes((0.55, 0.15, 0.35, 0.8))
ti.plot()
ti.plot_threshold_label(fontsize=8)
ti.plot_p_values(size=10, offset_all_clusters=(0, 0.9))
ax.set_xlabel('Time (%)')
pyplot.show()