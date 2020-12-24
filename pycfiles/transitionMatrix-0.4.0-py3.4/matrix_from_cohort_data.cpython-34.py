# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/examples/python/matrix_from_cohort_data.py
# Compiled at: 2018-10-21 08:46:16
# Size of source mod 2**32: 4695 bytes
"""
Example workflows using transitionMatrix to estimate a transition matrix from data in cohort format

"""
import pandas as pd, transitionMatrix as tm
from transitionMatrix import source_path
from transitionMatrix.estimators import cohort_estimator as es
dataset_path = source_path + 'datasets/'
example = 2
if example == 1:
    description = [
     ('0', 'AAA'), ('1', 'AA'), ('2', 'A'), ('3', 'BBB'),
     ('4', 'BB'), ('5', 'B'), ('6', 'CCC'), ('7', 'D')]
    myState = tm.StateSpace(description)
    print('> Describe state space')
    myState.describe()
    print('> List of states')
    print(myState.get_states())
    print('> List of state labels')
    print(myState.get_state_labels())
    print('> Load and validate dataset')
    data = pd.read_csv(dataset_path + 'synthetic_data4.csv', dtype={'State': str})
    sorted_data = data.sort_values(['ID', 'Timestep'], ascending=[True, True])
    print(myState.validate_dataset(dataset=sorted_data))
    myEstimator = es.CohortEstimator(states=myState, ci={'method': 'goodman',  'alpha': 0.05})
    result = myEstimator.fit(sorted_data)
    print('> Compute confidence interval using goodman method at 95% confidence level')
    myEstimator.summary()
    myMatrixSet = tm.TransitionMatrixSet(values=result, temporal_type='Incremental')
    print('> Print Estimated Matrix Set')
    myMatrixSet.print()
else:
    if example == 2:
        print('>>> Step 1')
        data = pd.read_csv(dataset_path + 'synthetic_data5.csv', dtype={'State': str})
        sorted_data = data.sort_values(['ID', 'Timestep'], ascending=[True, True])
        print(sorted_data.describe())
        print('>>> Step 2')
        description = [('0', 'Stage 1'), ('1', 'Stage 2'), ('2', 'Stage 3')]
        myState = tm.StateSpace(description)
        myState.describe()
        print(myState.validate_dataset(dataset=sorted_data))
        print('>>> Step 3')
        myEstimator = es.CohortEstimator(states=myState, ci={'method': 'goodman',  'alpha': 0.05})
        result = myEstimator.fit(sorted_data)
        myEstimator.summary()
        print('>>> Step 4')
        myMatrixSet = tm.TransitionMatrixSet(values=result, temporal_type='Incremental')
        print(myMatrixSet.temporal_type)
        myMatrixSet.print()
    elif example == 3:
        data = pd.read_csv(dataset_path + 'synthetic_data6.csv', dtype={'State': str})
        sorted_data = data.sort_values(['ID', 'Timestep'], ascending=[True, True])
        myState = tm.StateSpace()
        myState.generic(2)
        print(myState.validate_dataset(dataset=sorted_data))
        myEstimator = es.CohortEstimator(states=myState, ci={'method': 'goodman',  'alpha': 0.05})
        result = myEstimator.fit(sorted_data)
        myMatrixSet = tm.TransitionMatrixSet(values=result, temporal_type='Incremental')
        myEstimator.print(select='Counts', period=0)
        myEstimator.print(select='Frequencies', period=18)