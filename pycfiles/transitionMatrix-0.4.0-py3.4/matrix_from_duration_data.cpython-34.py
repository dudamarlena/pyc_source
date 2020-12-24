# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/examples/python/matrix_from_duration_data.py
# Compiled at: 2018-10-21 08:54:24
# Size of source mod 2**32: 4466 bytes
"""
Example workflows using transitionMatrix to estimate a matrix from duration type data
The datasets are produced in examples/generate_synthetic_data.py

"""
import pandas as pd, transitionMatrix as tm
from transitionMatrix import source_path
from transitionMatrix.estimators import cohort_estimator as es
dataset_path = source_path + 'datasets/'
example = 3
if example == 1:
    data = pd.read_csv(dataset_path + 'synthetic_data1.csv', dtype={'State': str})
    sorted_data = data.sort_values(['ID', 'Time'], ascending=[True, True])
    myState = tm.StateSpace([('0', 'A'), ('1', 'B'), ('2', 'C'), ('3', 'D')])
    print('> Validate data set')
    print(myState.validate_dataset(dataset=sorted_data))
    cohort_data, cohort_intervals = tm.utils.bin_timestamps(data, cohorts=5)
    myEstimator = es.CohortEstimator(states=myState, ci={'method': 'goodman',  'alpha': 0.05})
    labels = {'Timestamp': 'Cohort',  'State': 'State',  'ID': 'ID'}
    result = myEstimator.fit(cohort_data, labels=labels)
    myEstimator.summary(k=0)
    myEstimator.summary(k=4)
else:
    if example == 2:
        print('> Step 1: Load the data')
        data = pd.read_csv(dataset_path + 'synthetic_data2.csv', dtype={'State': str})
        sorted_data = data.sort_values(['ID', 'Time'], ascending=[True, True])
        print(sorted_data.describe())
        print('> Step 2: Validate against state space')
        myState = tm.StateSpace([('0', 'Basic'), ('1', 'Default')])
        myState.describe()
        print(myState.validate_dataset(dataset=sorted_data))
        print('> Step 3: Arrange the data in period cohorts')
        cohort_data, cohort_intervals = tm.utils.bin_timestamps(data, cohorts=5)
        print('> Step 4: Estimate matrices')
        myEstimator = es.CohortEstimator(states=myState, ci={'method': 'goodman',  'alpha': 0.05})
        labels = {'Timestamp': 'Cohort',  'State': 'State',  'ID': 'ID'}
        result = myEstimator.fit(cohort_data, labels=labels)
        print('> Step 5: Display results')
        myMatrixSet = tm.TransitionMatrixSet(values=result, temporal_type='Incremental')
        print(myMatrixSet.temporal_type)
        myMatrixSet.print()
    elif example == 3:
        data = pd.read_csv(dataset_path + 'synthetic_data3.csv', dtype={'State': str})
        sorted_data = data.sort_values(['ID', 'Time'], ascending=[True, True])
        myState = tm.StateSpace([('0', 'A'), ('1', 'B'), ('2', 'C'), ('3', 'D'), ('4', 'E'), ('5', 'F'), ('6', 'G')])
        print(myState.validate_dataset(dataset=sorted_data))
        cohort_data, cohort_intervals = tm.utils.bin_timestamps(data, cohorts=5)
        myEstimator = es.CohortEstimator(states=myState, ci={'method': 'goodman',  'alpha': 0.05})
        labels = {'Timestamp': 'Cohort',  'State': 'State',  'ID': 'ID'}
        result = myEstimator.fit(cohort_data, labels=labels)
        myMatrixSet = tm.TransitionMatrixSet(values=result, temporal_type='Incremental')
        myMatrixSet.print()