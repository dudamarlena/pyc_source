# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/spm1d/examples/stats1d_roi/ex_anova1.py
# Compiled at: 2019-08-22 04:37:03
# Size of source mod 2**32: 716 bytes
import numpy as np
from matplotlib import pyplot
import spm1d
dataset = spm1d.data.uv1d.anova1.SpeedGRFcategorical()
Y, A = dataset.get_data()
roi = np.array([False] * Y.shape[1])
roi[85:] = True
alpha = 0.05
F = spm1d.stats.anova1(Y, A, equal_var=True, roi=roi)
Fi = F.inference(alpha, interp=True)
print(Fi)
pyplot.close('all')
Fi.plot()
Fi.plot_threshold_label(bbox=dict(facecolor='w'))
pyplot.xlabel('Time (%)', size=20)
pyplot.title('Critical threshold at $\\alpha$=%.2f:  $F^*$=%.3f' % (alpha, Fi.zstar))
pyplot.show()