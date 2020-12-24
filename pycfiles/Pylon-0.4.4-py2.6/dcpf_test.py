# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\pylon\test\dcpf_test.py
# Compiled at: 2010-12-26 13:36:33
""" Defines a test case for DC power flow.
"""
import unittest
from os.path import join, dirname
from scipy import array, alltrue
from scipy.io.mmio import mmread
from pylon import Case, DCPF
DATA_DIR = join(dirname(__file__), 'data')

class DCPFTest(unittest.TestCase):

    def __init__(self, methodName='runTest'):
        super(DCPFTest, self).__init__(methodName)
        self.case_name = 'case6ww'
        self.case = None
        return

    def setUp(self):
        """ The test runner will execute this method prior to each test.
        """
        self.case = Case.load(join(DATA_DIR, self.case_name, self.case_name + '.pkl'))

    def testVa(self):
        """ Test voltage angle solution vector from DC power flow.
        """
        solver = DCPF(self.case)
        solver.solve()
        mpVa = mmread(join(DATA_DIR, self.case_name, 'Va.mtx')).flatten()
        self.assertTrue(abs(max(solver.v_angle - mpVa)) < 1e-14, self.case_name)


class DCPFCase24RTSTest(DCPFTest):

    def __init__(self, methodName='runTest'):
        super(DCPFCase24RTSTest, self).__init__(methodName)
        self.case_name = 'case24_ieee_rts'


class DCPFCaseIEEE30Test(DCPFTest):

    def __init__(self, methodName='runTest'):
        super(DCPFCaseIEEE30Test, self).__init__(methodName)
        self.case_name = 'case_ieee30'


if __name__ == '__main__':
    import logging, sys
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format='%(levelname)s: %(message)s')
    unittest.main()