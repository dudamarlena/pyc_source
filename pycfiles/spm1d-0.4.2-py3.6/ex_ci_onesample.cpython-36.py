# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/spm1d/examples/stats1d/ex_ci_onesample.py
# Compiled at: 2019-08-22 04:37:03
# Size of source mod 2**32: 2777 bytes
"""
One-sample confidence intervals for 1D data:

NOTES:
1.  If mu=None then explicit hypothesis testing is suppressed (i.e. exploratory analysis)
Note that the hypothesis test is still conducted implicitly (to compute the CI).
However, the explicit null hypothesis rejection decision will not appear when using either "print(ci)" or "ci.plot()".
Note especially that these one-sample CIs are invalid for two-sample, regression and ANOVA-like experiments.
Thus "mu=None" is generally useful only for exploratory purposes.

2.  If mu is a 0D scalar or a 1D scalar field then:
- Explicit null hypothesis testing is conducted
- The null hypothesis is rejected if mu lies outside the CI at any point in the 1D field
- A 0D scalar value for mu represents a constant 1D field
"""
import numpy as np
from matplotlib import pyplot
import spm1d
dataset = spm1d.data.uv1d.t1.SimulatedPataky2015b()
y, mu = dataset.get_data()
mu0 = 0
mu1 = 5 * np.sin(np.linspace(0, np.pi, y.shape[1]))
alpha = 0.05
ci0 = spm1d.stats.ci_onesample(y, alpha, mu=mu0)
ci1 = spm1d.stats.ci_onesample(y, alpha, mu=mu1)
print(ci0)
print(ci1)
pyplot.close('all')
pyplot.figure(figsize=(14, 7))
ax = pyplot.subplot(231)
spm1d.plot.plot_mean_sd((y - mu0), ax=ax)
ax.set_title('Mean and SD', size=10)
spm1d.plot.legend_manual(ax, labels=['Mean', 'SD'], colors=['k', '0.85'], linestyles=['-', '-'], linewidths=[3, 10], loc='upper left', fontsize=10)
ax = pyplot.subplot(232)
spmi = spm1d.stats.ttest(y, mu0).inference(alpha, two_tailed=True)
spmi.plot(ax=ax)
spmi.plot_p_values()
ax.set_title('Hypothesis test', size=10)
ax = pyplot.subplot(233)
ci0.plot(ax)
ax.set_title('CI  (criterion: mu=0)', size=10)
spm1d.plot.legend_manual(ax, labels=['Mean', 'CI', 'Criterion'], colors=['k', '0.85', 'r'], linestyles=['-', '-', '--'], linewidths=[3, 10, 1], loc='upper left', fontsize=10)
ax = pyplot.subplot(234)
spm1d.plot.plot_mean_sd((y - mu1), ax=ax)
ax.set_title('Mean and SD  (y - mu1)', size=10)
ax = pyplot.subplot(235)
spmi = spm1d.stats.ttest(y, mu1).inference(alpha, two_tailed=True)
spmi.plot(ax=ax)
spmi.plot_p_values()
ax.set_title('Hypothesis test (y - mu1)', size=10)
ax = pyplot.subplot(236)
ci1.plot(ax)
ax.set_title('CI  (criterion: mu1)', size=10)
pyplot.suptitle('One-sample analysis')
pyplot.show()