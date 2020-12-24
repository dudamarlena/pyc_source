# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/examples/python/matrix_set_lendingclub.py
# Compiled at: 2018-10-21 09:56:17
# Size of source mod 2**32: 2230 bytes
"""
Example workflow using transitionMatrix to estimate a set of matrix from LendingClub data
Input data are in a special cohort format as the published datasets have some limitations

"""
import pandas as pd, transitionMatrix as tm
from transitionMatrix import source_path
from transitionMatrix.estimators import simple_estimator as es
dataset_path = source_path + 'datasets/'
description = [
 ('A', 'Grade A'), ('B', 'Grade B'), ('C', 'Grade C'),
 ('D', 'Grade D'), ('E', 'Grade E'), ('F', 'Grade F'),
 ('G', 'Grade G'), ('H', 'Delinquent'), ('I', 'Charged Off'),
 ('J', 'Repaid')]
myState = tm.StateSpace(description)
matrix_set = []
for letter in ['a', 'b', 'c', 'd']:
    data = pd.read_csv(dataset_path + 'LoanStats3' + letter + '_Step2.csv')
    myEstimator = es.SimpleEstimator(states=myState, ci={'method': 'goodman',  'alpha': 0.05})
    result = myEstimator.fit(data)
    myEstimator.summary()
    myMatrix = tm.TransitionMatrix(result)
    myMatrix[(7, 9)] = 1.0
    myMatrix[(8, 9)] = 1.0
    myMatrix[(9, 9)] = 1.0
    matrix_set.append(myMatrix)

LC_Set = tm.TransitionMatrixSet(values=matrix_set, temporal_type='Incremental')
LC_Set.print()