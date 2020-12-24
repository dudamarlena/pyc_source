# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/spm1d/examples/stats0d/ex_manova1.py
# Compiled at: 2019-08-22 04:37:03
# Size of source mod 2**32: 306 bytes
import spm1d
dataset = spm1d.data.mv0d.manova1.AnimalDepression()
y, A = dataset.Y, dataset.A
print(dataset)
X2 = spm1d.stats.manova1(y, A)
X2i = X2.inference(alpha=0.05)
print(X2i)