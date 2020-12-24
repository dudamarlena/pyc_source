# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/examples/python/matrix_lendingclub.py
# Compiled at: 2018-10-21 08:59:12
# Size of source mod 2**32: 2840 bytes
"""
Example workflow using transitionMatrix to estimate a matrix from LendingClub data
Input data are in a special cohort format as the published datasets have some limitations

"""
import pandas as pd, transitionMatrix as tm
from transitionMatrix import source_path
from transitionMatrix.estimators import simple_estimator as es
dataset_path = source_path + 'datasets/'
print('Step 1')
data = pd.read_csv(dataset_path + 'LoanStats3a_Step2.csv')
print(data.describe())
print('Step 2')
description = [('A', 'Grade A'), ('B', 'Grade B'), ('C', 'Grade C'),
 ('D', 'Grade D'), ('E', 'Grade E'), ('F', 'Grade F'),
 ('G', 'Grade G'), ('H', 'Delinquent'), ('I', 'Charged Off'),
 ('J', 'Repaid')]
myState = tm.StateSpace(description)
myState.describe()
labels = {'State': 'State_IN'}
print(myState.validate_dataset(dataset=data, labels=labels))
labels = {'State': 'State_OUT'}
print(myState.validate_dataset(dataset=data, labels=labels))
print('Step 3')
myEstimator = es.SimpleEstimator(states=myState, ci={'method': 'goodman',  'alpha': 0.05})
result = myEstimator.fit(data)
myEstimator.summary()
print('Step 4')
myMatrix = tm.TransitionMatrix(result)
myMatrix.print()
myMatrix[(7, 9)] = 1.0
myMatrix[(8, 9)] = 1.0
myMatrix[(9, 9)] = 1.0
print(myMatrix.validate())
print(myMatrix.characterize())
myMatrix.print()