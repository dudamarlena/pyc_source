# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/spm1d/examples/normality/0d/ex_regress.py
# Compiled at: 2019-08-22 04:37:03
# Size of source mod 2**32: 311 bytes
import spm1d
dataset = spm1d.data.uv0d.regress.RSRegression()
dataset = spm1d.data.uv0d.regress.ColumbiaHeadCircumference()
y, x = dataset.get_data()
alpha = 0.05
spmi = spm1d.stats.normality.k2.regress(y, x).inference(alpha)
print(spmi)