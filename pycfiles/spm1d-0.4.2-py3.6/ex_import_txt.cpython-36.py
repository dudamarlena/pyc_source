# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/spm1d/examples/io/ex_import_txt.py
# Compiled at: 2019-08-22 04:37:03
# Size of source mod 2**32: 421 bytes
import os, numpy as np
from matplotlib import pyplot
dir0 = os.path.dirname(__file__)
fname = os.path.join(dir0, 'data', 'ex_kinematics.txt')
Y = np.loadtxt(fname)
pyplot.close('all')
pyplot.plot((Y.T), color='k')
pyplot.xlabel('Time (%)', size=20)
pyplot.ylabel('$\\theta$ (deg)', size=20)
pyplot.show()