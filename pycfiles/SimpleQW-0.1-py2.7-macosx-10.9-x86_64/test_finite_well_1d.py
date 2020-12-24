# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/simpleqw/tests/test_finite_well_1d.py
# Compiled at: 2014-12-31 17:12:30
import unittest
from simpleqw import finite_well_1d

class TestFiniteWell1D(unittest.TestCase):

    def testNumStatesScaled(self):
        self.assertEqual(finite_well_1d.num_states_scaled(1.0), 1)
        self.assertEqual(finite_well_1d.num_states_scaled(4.5), 3)
        self.assertEqual(finite_well_1d.num_states_scaled(6.0), 4)

    def testEnergyScaled(self):
        self.assertAlmostEqual(finite_well_1d.energy_scaled(1.0, n=1), 1.0925, places=4)
        self.assertAlmostEqual(finite_well_1d.energy_scaled(4.5, n=1), 3.2867, places=4)
        self.assertAlmostEqual(finite_well_1d.energy_scaled(4.5, n=2), 12.9179, places=4)
        self.assertAlmostEqual(finite_well_1d.energy_scaled(4.5, n=3), 27.8821, places=4)
        self.assertAlmostEqual(finite_well_1d.energy_scaled(6.0, n=1), 3.6167, places=4)
        self.assertAlmostEqual(finite_well_1d.energy_scaled(6.0, n=2), 14.3518, places=4)
        self.assertAlmostEqual(finite_well_1d.energy_scaled(6.0, n=3), 31.7736, places=4)
        self.assertAlmostEqual(finite_well_1d.energy_scaled(6.0, n=4), 54.6214, places=4)

    def testEnergy(self):
        self.assertAlmostEqual(finite_well_1d.energy(L=1.0 / 2.56158355342, m=1, U=1, n=1), 0.546246834314, places=4)
        self.assertAlmostEqual(finite_well_1d.energy(L=100000.0 / 2.56158355342, m=1, U=1, n=1), 0.0, places=4)
        self.assertAlmostEqual(finite_well_1d.energy(L=1e-05 / 2.56158355342, m=1, U=1, n=1), 1.0, places=4)


if __name__ == '__main__':
    unittest.main()