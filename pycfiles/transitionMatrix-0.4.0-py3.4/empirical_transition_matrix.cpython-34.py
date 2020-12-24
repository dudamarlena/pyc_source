# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/examples/python/empirical_transition_matrix.py
# Compiled at: 2018-10-22 09:04:24
# Size of source mod 2**32: 4427 bytes
"""
Example workflows using transitionMatrix to estimate an empirical transition matrix from duration type data
The datasets are produced in examples/generate_synthetic_data.py

"""
import matplotlib.pyplot as plt, numpy as np, pandas as pd, transitionMatrix as tm
from transitionMatrix import source_path
from transitionMatrix.estimators import aalen_johansen_estimator as aj
dataset_path = source_path + 'datasets/'
example = 1
print('> Step 1: Load the data set into a pandas frame')
if example == 1:
    data = pd.read_csv(dataset_path + 'synthetic_data7.csv', dtype={'State': str})
else:
    if example == 2:
        data = pd.read_csv(dataset_path + 'synthetic_data8.csv', dtype={'State': str})
    sorted_data = data.sort_values(['Time', 'ID'], ascending=[True, True])
    print(sorted_data.describe())
    print('> Step 2: Describe and validate the State Space against the data')
    if example == 1:
        description = [
         ('0', 'AAA'), ('1', 'AA'), ('2', 'A'), ('3', 'BBB'),
         ('4', 'BB'), ('5', 'B'), ('6', 'CCC'), ('7', 'D')]
    elif example == 2:
        description = [
         ('0', 'G'), ('1', 'B')]
myState = tm.StateSpace(description)
myState.describe()
labels = {'State': 'From'}
print(myState.validate_dataset(dataset=sorted_data, labels=labels))
labels = {'State': 'To'}
print(myState.validate_dataset(dataset=sorted_data, labels=labels))
print('> Step 3: Estimate matrices using the Aalen-Johansen estimator')
myEstimator = aj.AalenJohansenEstimator(states=myState)
labels = {'Timestamp': 'Time',  'From_State': 'From',  'To_State': 'To',  'ID': 'ID'}
etm, times = myEstimator.fit(sorted_data, labels=labels)
print('> Step 4: Print the cumulative computed matrix')
print(etm[:, :, -1])
if example == 1:
    print('> Plot the transition curves')
    Periods = 10
    Ratings = 8
    periods = range(0, Periods)
    m = 4
    n = 2
    f, axarr = plt.subplots(m, n)
    f.subplots_adjust(left=0.05, bottom=0.05, right=0.95, top=0.9, wspace=0.0, hspace=0.1)
    for ri in range(0, Ratings):
        axj = int(ri / 2)
        axi = ri % 2
        print(ri, axj, axi)
        curves = []
        for rf in range(0, Ratings):
            cPD = etm[ri, rf, :]
            curves.append(cPD)
            axarr[(axj, axi)].set_aspect(5)
            axarr[(axj, axi)].set_ylabel('State ' + str(ri), fontsize=12)
            axarr[(axj, axi)].set_xlabel('Time')
            axarr[(axj, axi)].plot(times[1:], curves[rf], label='RI=%d' % (rf,))
            axarr[(axj, axi)].set_xticks(range(10), minor=False)
            axarr[(axj, axi)].set_yticks(np.linspace(0, 1, 5), minor=False)
            axarr[(axj, axi)].margins(y=0.05, x=0.05)
            axarr[(axj, axi)].grid(True)

    f.suptitle('Multi-period Transition Probabilities', fontsize=12)
    plt.savefig('transition_probabilities.png')
    plt.show()