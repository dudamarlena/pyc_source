# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/examples/python/credit_curves.py
# Compiled at: 2018-10-22 08:03:33
# Size of source mod 2**32: 2747 bytes
""" Compute and Visuzalize credit curves

"""
import matplotlib.pyplot as plt, transitionMatrix as tm
from datasets import Generic
print('> Load the generic transition matrix')
M = tm.TransitionMatrix(values=Generic)
Ratings = M.dimension
Default = Ratings - 1
Periods = 10
print('> Extend the matrix into 10 periods using the power method')
T = tm.TransitionMatrixSet(values=M, periods=Periods, method='Power', temporal_type='Cumulative')
print('> Display the calculated transition matrix set')
T.print()
print('> Compute the default curves')
incremental_PD, cumulative_PD, hazard_Rate, survival_Rate = T.default_curves(0)
print('> Plot the default curves')
curves = []
periods = range(0, Periods)
for ri in range(0, Ratings - 1):
    print('RI: ', ri)
    iPD, cPD, hR, sR = T.default_curves(ri)
    curves.append(cPD)

fig, ax = plt.subplots()
for ri in range(0, Ratings - 1):
    ax.plot(periods, curves[ri], label='RI=%d' % (ri,))

ax.autoscale()
ax.margins(0.1)
ax.set_xlabel('Periods')
ax.set_ylabel('Cumulative Default Probability')
ax.grid(True)
plt.title('Credit Curves of Generic Transition Matrix')
leg = plt.legend(loc='best', ncol=2, mode='expand', shadow=True, fancybox=True)
leg.get_frame().set_alpha(0.5)
plt.savefig('credit_curves.png')