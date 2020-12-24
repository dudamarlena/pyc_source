# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/quantecon/tests/test_arma.py
# Compiled at: 2019-07-07 21:19:40
# Size of source mod 2**32: 1226 bytes
"""
Tests for arma.py file.  Most of this testing can be considered
covered by the numpy tests since we rely on much of their code.

"""
import sys, unittest, numpy as np
from numpy.testing import assert_array_equal
from quantecon.arma import ARMA

class TestARMA(unittest.TestCase):

    def setUp(self):
        phi = np.array([0.95, -0.4, -0.4])
        theta = np.zeros(3)
        sigma = 0.15
        self.lp = ARMA(phi, theta, sigma)

    def tearDown(self):
        del self.lp

    def test_simulate(self):
        lp = self.lp
        sim = lp.simulation(ts_length=250)
        self.assertTrue(sim.size == 250)

    def test_simulate_with_seed(self):
        lp = self.lp
        seed = 5
        sim0 = lp.simulation(ts_length=10, random_state=seed)
        sim1 = lp.simulation(ts_length=10, random_state=seed)
        assert_array_equal(sim0, sim1)

    def test_impulse_response(self):
        lp = self.lp
        imp_resp = lp.impulse_response(impulse_length=75)
        self.assertTrue(imp_resp.size == 75)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestARMA)
    unittest.TextTestRunner(verbosity=2, stream=(sys.stderr)).run(suite)