# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/spm1d/examples/scipy/ex_ttest_normality.py
# Compiled at: 2019-08-22 04:37:03
# Size of source mod 2**32: 693 bytes
import numpy as np, scipy.stats, spm1d
dataset = spm1d.data.uv0d.normality.ZarBiostatisticalAnalysis68()
dataset = spm1d.data.uv0d.normality.KendallRandomNumbers()
y = dataset.get_data()
print(dataset)
np.random.seed(0)
alpha = 0.05
spm = spm1d.stats.normality.ttest(y)
spmi = spm.inference(alpha)
print(spmi)
results = scipy.stats.normaltest(y)
print
print('scipy.stats.normaltest result:')
print('   K2=%.5f, p=%.5f' % (results.statistic, results.pvalue))
print
print('spm1d result:')
print('   K2=%.5f, p=%.5f' % (spmi.z, spmi.p))
print