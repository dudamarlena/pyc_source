# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/spm1d/examples/stats1d_roi/ex_regression_directional.py
# Compiled at: 2019-08-22 04:37:04
# Size of source mod 2**32: 661 bytes
import numpy as np
from matplotlib import pyplot
import spm1d
dataset = spm1d.data.uv1d.regress.SpeedGRF()
Y, x = dataset.get_data()
roi = np.array([0] * Y.shape[1])
roi[0:20] = 1
roi[30:65] = -1
alpha = 0.05
t = spm1d.stats.regress(Y, x, roi=roi)
ti = t.inference(alpha, two_tailed=False, interp=True)
print(ti)
pyplot.close('all')
pyplot.figure(figsize=(7.5, 5))
ax = pyplot.axes()
ti.plot()
ti.plot_threshold_label(fontsize=8)
ti.plot_p_values(size=10)
ax.set_xlabel('Time (%)')
pyplot.show()