# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/spm1d/examples/stats0d/ex_anova2onermub.py
# Compiled at: 2019-08-22 04:37:03
# Size of source mod 2**32: 351 bytes
import spm1d
dataset = spm1d.data.uv0d.anova2onerm.Santa23UnequalSampleSizes()
dataset = spm1d.data.uv0d.anova2onerm.Southampton2onermUnequalSampleSizes()
y, A, B, SUBJ = dataset.get_data()
print(dataset)
FF = spm1d.stats.anova2onerm(y, A, B, SUBJ)
FFi = FF.inference(0.05)
print(FFi)