# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/spm1d/examples/stats1d_roi/ex_glm.py
# Compiled at: 2019-08-22 04:37:04
# Size of source mod 2**32: 1008 bytes
import numpy as np
from matplotlib import pyplot
import spm1d
dataset = spm1d.data.uv1d.regress.SpeedGRF()
Y, x = dataset.get_data()
nCurves = x.size
nFactors = 4
X = np.zeros((nCurves, nFactors))
X[:, 0] = x
X[:, 1] = 1
X[:, 2] = np.linspace(0, 1, nCurves)
X[:, 3] = np.sin(np.linspace(0, np.pi, nCurves))
c = [
 1, 0, 0, 0]
roi = np.array([False] * Y.shape[1])
roi[60:] = True
alpha = 0.05
t = spm1d.stats.glm(Y, X, c, roi=roi)
ti = t.inference(alpha, two_tailed=False, interp=True)
print(ti)
pyplot.close('all')
ax = pyplot.axes()
ti.plot()
ti.plot_threshold_label(fontsize=8)
ti.plot_p_values(size=10)
ax.set_xlabel('Time (%)')
pyplot.show()