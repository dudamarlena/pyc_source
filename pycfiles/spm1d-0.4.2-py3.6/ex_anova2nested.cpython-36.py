# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/spm1d/examples/stats1d_roi/ex_anova2nested.py
# Compiled at: 2019-08-22 04:37:04
# Size of source mod 2**32: 662 bytes
import numpy as np
from matplotlib import pyplot
import spm1d
dataset = spm1d.data.uv1d.anova2nested.SPM1D_ANOVA2NESTED_2x2()
Y, A, B = dataset.get_data()
roi = np.array([False] * Y.shape[1])
roi[40:55] = True
alpha = 0.05
FF = spm1d.stats.anova2nested(Y, A, B, equal_var=True, roi=roi)
FFi = [F.inference(alpha, interp=True) for F in FF]
pyplot.close('all')
pyplot.subplot(221)
FFi[0].plot()
pyplot.title('Main effect A')
pyplot.subplot(222)
FFi[1].plot()
pyplot.title('Main effect B')
pyplot.show()