# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/spm1d/examples/stats1d_roi/ex_cca_Dorn2012.py
# Compiled at: 2019-08-22 04:37:04
# Size of source mod 2**32: 545 bytes
import numpy as np
from matplotlib import pyplot
import spm1d
dataset = spm1d.data.mv1d.cca.Dorn2012()
Y, x = dataset.get_data()
print(dataset)
roi = np.array([False] * Y.shape[1])
roi[20:50] = True
roi[60:90] = True
alpha = 0.05
X2 = spm1d.stats.cca(Y, x, roi=roi)
X2i = X2.inference(0.05)
print(X2i)
pyplot.close('all')
X2i.plot()
X2i.plot_p_values()
pyplot.show()