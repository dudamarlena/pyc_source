# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/spm1d/examples/nonparam/1d/ex_ttest_other_metrics.py
# Compiled at: 2019-08-22 04:37:03
# Size of source mod 2**32: 1174 bytes
import numpy as np
from matplotlib import pyplot
import spm1d
dataset = spm1d.data.uv1d.t1.SimulatedPataky2015b()
y, mu = dataset.get_data()
metrics = ('MaxClusterIntegral', 'MaxClusterExtent', 'MaxClusterHeight')
metric = metrics[1]
np.random.seed(0)
alpha = 0.05
two_tailed = False
snpm = spm1d.stats.nonparam.ttest(y, mu)
snpmi = snpm.inference(alpha, two_tailed=two_tailed, iterations=(-1), cluster_metric=metric)
print(snpmi)
print(snpmi.clusters)
spm = spm1d.stats.ttest(y, mu)
spmi = spm.inference(alpha, two_tailed=two_tailed)
print(spmi)
print(spmi.clusters)
pyplot.close('all')
pyplot.figure(figsize=(12, 4))
ax0 = pyplot.subplot(121)
ax1 = pyplot.subplot(122)
labels = ('Parametric', 'Non-parametric')
for ax, zi, label in zip([ax0, ax1], [spmi, snpmi], labels):
    zi.plot(ax=ax)
    zi.plot_threshold_label(ax=ax, fontsize=8)
    zi.plot_p_values(ax=ax, size=10)
    ax.set_title(label)

pyplot.show()