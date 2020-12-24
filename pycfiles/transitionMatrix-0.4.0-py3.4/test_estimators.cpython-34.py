# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/philippos/Desktop/Dev_OpenSource/transitionMatrix/tests/test_estimators.py
# Compiled at: 2018-10-22 07:00:59
# Size of source mod 2**32: 2803 bytes
import unittest, pandas as pd, transitionMatrix as tm
from transitionMatrix import source_path
from transitionMatrix.estimators import cohort_estimator as es
from transitionMatrix.estimators import aalen_johansen_estimator as aj
ACCURATE_DIGITS = 2

class TestSimpleEstimator(unittest.TestCase):
    pass


class TestCohortEstimator(unittest.TestCase):

    def test_cohort_estimator_counts(self):
        dataset_path = source_path + 'datasets/'
        data = pd.read_csv(dataset_path + 'synthetic_data5.csv')
        event_count = data[(data['Timestep'] < 4)]['ID'].count()
        description = [('0', 'Stage 1'), ('1', 'Stage 2'), ('2', 'Stage 3')]
        myState = tm.StateSpace(description)
        sorted_data = data.sort_values(['ID', 'Timestep'], ascending=[True, True])
        myEstimator = es.CohortEstimator(states=myState, ci={'method': 'goodman',  'alpha': 0.05})
        result = myEstimator.fit(sorted_data)
        self.assertEqual(event_count, myEstimator.counts)


class TestAalenJohansenEstimator(unittest.TestCase):
    __doc__ = '\n    Test the estimation of a simple 2x2 transition matrix with absorbing state\n\n    .. note: The result is subject to sampling error! Ensure the required accuracy corresponds to the input data size\n\n    '

    def test_aalenjohansen_simple_transitions(self):
        dataset_path = source_path + 'datasets/'
        data = pd.read_csv(dataset_path + 'synthetic_data8.csv')
        sorted_data = data.sort_values(['Time', 'ID'], ascending=[True, True])
        description = [('0', 'G'), ('1', 'B')]
        myState = tm.StateSpace(description)
        myEstimator = aj.AalenJohansenEstimator(states=myState)
        labels = {'Timestamp': 'Time',  'From_State': 'From',  'To_State': 'To',  'ID': 'ID'}
        result = myEstimator.fit(sorted_data, labels=labels)
        self.assertAlmostEqual(result[(0, 0, -1)], 0.5, places=ACCURATE_DIGITS, msg=None, delta=None)
        self.assertAlmostEqual(result[(0, 1, -1)], 0.5, places=ACCURATE_DIGITS, msg=None, delta=None)
        self.assertEqual(result[(1, 0, -1)], 0.0)
        self.assertEqual(result[(1, 1, -1)], 1.0)