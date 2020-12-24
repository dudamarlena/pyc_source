# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\pylon\test\udopf_test.py
# Compiled at: 2010-12-26 13:36:33
__doc__ = ' Defines a test case for the combined unit decommitment / OPF routine.\n'
import sys, logging, unittest
from os.path import dirname, join
from pylon.case import Case
from pylon.opf import UDOPF
DATA_FILE = join(dirname(__file__), 'data', 'case6ww.pkl')
PWL_FILE = join(dirname(__file__), '..', '..', 'pyreto', 'test', 'data', 't_auction_case.pkl')

class UOPFTestCase(unittest.TestCase):
    """ Defines a test case for the UOPF routine.
    """

    def setUp(self):
        """ The test runner will execute this method prior to each test.
        """
        case = self.case = Case.load(DATA_FILE)
        self.solver = UDOPF(case, dc=True)

    def test_dc(self):
        """ Test solver using DC formulation.
        """
        solution = self.solver.solve()
        generators = self.case.generators
        self.assertTrue(solution['converged'] == True)
        self.assertFalse(generators[0].online)
        self.assertAlmostEqual(generators[1].p, 110.8, places=2)
        self.assertAlmostEqual(generators[2].p, 99.2, places=2)
        self.assertAlmostEqual(solution['f'], 2841.59, places=2)

    def test_pwl(self):
        """ Test UDOPF solver with pwl auction case.
        """
        case = Case.load(PWL_FILE)
        solver = UDOPF(case, dc=True)
        solution = solver.solve()
        generators = self.case.generators
        self.assertTrue(solution['converged'] == True)
        self.assertTrue(False not in [ g.online for g in generators ])


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format='%(levelname)s: %(message)s')
    unittest.main()