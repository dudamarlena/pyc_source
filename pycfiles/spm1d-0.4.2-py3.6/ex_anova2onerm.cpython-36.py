# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/spm1d/examples/stats1d_roi/ex_anova2onerm.py
# Compiled at: 2019-08-22 04:37:04
# Size of source mod 2**32: 741 bytes
import numpy as np
from matplotlib import pyplot
import spm1d
dataset = spm1d.data.uv1d.anova2onerm.SPM1D_ANOVA2ONERM_2x3()
Y, A, B, SUBJ = dataset.get_data()
roi = np.array([False] * Y.shape[1])
roi[60:] = True
alpha = 0.05
FF = spm1d.stats.anova2onerm(Y, A, B, SUBJ, equal_var=True, roi=roi)
FFi = [F.inference(alpha, interp=True) for F in FF]
pyplot.close('all')
pyplot.subplot(221)
FFi[0].plot()
pyplot.title('Main effect A')
pyplot.subplot(222)
FFi[1].plot()
pyplot.title('Main effect B')
pyplot.subplot(223)
FFi[2].plot()
pyplot.title('Interaction effect AB')
pyplot.show()