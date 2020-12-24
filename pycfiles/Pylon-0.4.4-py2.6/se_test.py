# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\pylon\test\se_test.py
# Compiled at: 2010-12-26 13:36:33
""" Test case for the state estimator.
"""
from os.path import join, dirname
import unittest
from scipy import array
from pylon.io import PickleReader
from pylon.estimator import StateEstimator, Measurement, PF, PT, PG, VM
DATA_FILE = join(dirname(__file__), 'data', 'case3bus_P6_6.pkl')

class StateEstimatorTest(unittest.TestCase):
    """ Tests the state estimator using data from Problem 6.7 in 'Computational
        Methods for Electric Power Systems' by Mariesa Crow.
    """

    def setUp(self):
        """ The test runner will execute this method prior to each test.
        """
        case = self.case = PickleReader().read(DATA_FILE)
        self.measurements = [
         Measurement(case.branches[0], PF, 0.12),
         Measurement(case.branches[1], PF, 0.1),
         Measurement(case.branches[2], PT, -0.04),
         Measurement(case.buses[0], PG, 0.58),
         Measurement(case.buses[1], PG, 0.3),
         Measurement(case.buses[2], PG, 0.14),
         Measurement(case.buses[1], VM, 1.04),
         Measurement(case.buses[2], VM, 0.98)]
        self.sigma = array([0.02, 0.02, 0, 0, 0.015, 0, 0.01, 0])

    def test_case(self):
        """ Test the Pylon case.
        """
        self.assertEqual(len(self.case.buses), 3)
        self.assertEqual(len(self.case.branches), 3)
        self.assertEqual(len(self.case.generators), 3)

    def test_estimation(self):
        """ Test state estimation.
        """
        se = StateEstimator(self.case, self.measurements, self.sigma)
        solution = se.run()
        V = solution['V']
        places = 4
        self.assertAlmostEqual(abs(V[0]), abs(1.0), places)
        self.assertAlmostEqual(abs(V[1]), abs(complex(1.0256, -0.0175)), places)
        self.assertAlmostEqual(abs(V[2]), abs(complex(0.979, 0.0007)), places)


if __name__ == '__main__':
    unittest.main()