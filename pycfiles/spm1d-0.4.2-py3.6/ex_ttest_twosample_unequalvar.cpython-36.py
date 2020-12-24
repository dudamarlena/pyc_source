# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/spm1d/examples/stats0d/ex_ttest_twosample_unequalvar.py
# Compiled at: 2019-08-22 04:37:03
# Size of source mod 2**32: 364 bytes
import numpy as np, spm1d
dataset = spm1d.data.uv0d.t2nonspher.RSFlavor()
yA, yB = dataset.get_data()
print(dataset)
spmt = spm1d.stats.ttest2(yA, yB, equal_var=False)
spmti = spmt.inference(0.05, two_tailed=False)
print(spmti)