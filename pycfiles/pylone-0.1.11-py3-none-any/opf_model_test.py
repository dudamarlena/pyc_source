# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\pylon\test\opf_model_test.py
# Compiled at: 2010-12-26 13:36:33
__doc__ = ' Test case for the optimal power flow solver.\n'
from os.path import join, dirname
import unittest
from numpy import Inf
from pylon import OPF, Case
POLY_FILE = join(dirname(__file__), 'data', 'case6ww.pkl')

class OPFModelTest(unittest.TestCase):
    """ Test case for the OPF model.
    """

    def setUp(self):
        """ The test runner will execute this method prior to each test.
        """
        self.case = Case.load(POLY_FILE)
        self.opf = OPF(self.case)

    def test_dc_linear_constraints(self):
        """ Test linear OPF constraints.
        """
        self.opf.dc = True
        om = self.opf._construct_opf_model(self.case)
        (A, l, u) = om.linear_constraints()
        self.assertEqual(A.shape, (28, 9))
        self.assertEqual(l.shape, (28, ))
        self.assertEqual(u.shape, (28, ))
        pl = 4
        self.assertAlmostEqual(A[(0, 0)], 13.3333, pl)
        self.assertAlmostEqual(A[(4, 2)], -3.8462, pl)
        self.assertAlmostEqual(A[(2, 8)], -1.0, pl)
        self.assertAlmostEqual(A[(9, 1)], 4.0, pl)
        self.assertAlmostEqual(A[(27, 5)], 3.3333, pl)
        self.assertAlmostEqual(l[0], 0.0, pl)
        self.assertAlmostEqual(l[3], -0.7, pl)
        self.assertEqual(l[6], -Inf)
        self.assertEqual(l[27], -Inf)
        self.assertAlmostEqual(u[0], 0.0, pl)
        self.assertAlmostEqual(u[3], -0.7, pl)
        self.assertAlmostEqual(u[6], 0.4, pl)
        self.assertAlmostEqual(u[7], 0.6, pl)
        self.assertAlmostEqual(u[23], 0.9, pl)

    def test_ac_linear_constraints(self):
        """ Test linear OPF constraints.
        """
        self.opf.dc = False
        om = self.opf._construct_opf_model(self.case)
        (A, l, u) = om.linear_constraints()
        self.assertEqual(A, None)
        self.assertEqual(l.shape, (0, ))
        self.assertEqual(u.shape, (0, ))
        return


if __name__ == '__main__':
    import logging, sys
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format='%(levelname)s: %(message)s')
    logger = logging.getLogger('pylon')
    unittest.main()