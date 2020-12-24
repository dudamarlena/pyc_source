# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\pylon\test\suite.py
# Compiled at: 2010-12-26 13:36:33
__doc__ = ' Pylon test suite.\n'
import unittest
from pylon.test.case_test import CaseTest, BusTest, BranchTest, CaseMatrixTest, CaseMatrix24RTSTest, CaseMatrixIEEE30Test
from pylon.test.generator_test import GeneratorTest, OfferBidToPWLTest
from dcpf_test import DCPFTest, DCPFCase24RTSTest, DCPFCaseIEEE30Test
from acpf_test import ACPFTest, ACPFCase24RTSTest, ACPFCaseIEEE30Test
from opf_test import DCOPFTest, DCOPFCase24RTSTest, DCOPFCaseIEEE30Test
from opf_test import DCOPFSolverTest, DCOPFSolverCase24RTSTest, DCOPFSolverCaseIEEE30Test
from opf_test import PIPSSolverTest, PIPSSolverCase24RTSTest, PIPSSolvercaseIEEE30Test
from opf_model_test import OPFModelTest
from reader_test import MatpowerReaderTest, PSSEReaderTest
from se_test import StateEstimatorTest

def suite():
    """ Returns the Pylon test suite.
    """
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(CaseTest))
    suite.addTest(unittest.makeSuite(CaseMatrixTest))
    suite.addTest(unittest.makeSuite(CaseMatrix24RTSTest))
    suite.addTest(unittest.makeSuite(CaseMatrixIEEE30Test))
    suite.addTest(unittest.makeSuite(BusTest))
    suite.addTest(unittest.makeSuite(BranchTest))
    suite.addTest(unittest.makeSuite(GeneratorTest))
    suite.addTest(unittest.makeSuite(OfferBidToPWLTest))
    suite.addTest(unittest.makeSuite(DCPFTest))
    suite.addTest(unittest.makeSuite(DCPFCase24RTSTest))
    suite.addTest(unittest.makeSuite(DCPFCaseIEEE30Test))
    suite.addTest(unittest.makeSuite(ACPFTest))
    suite.addTest(unittest.makeSuite(ACPFCase24RTSTest))
    suite.addTest(unittest.makeSuite(ACPFCaseIEEE30Test))
    suite.addTest(unittest.makeSuite(DCOPFTest))
    suite.addTest(unittest.makeSuite(DCOPFCase24RTSTest))
    suite.addTest(unittest.makeSuite(DCOPFCaseIEEE30Test))
    suite.addTest(unittest.makeSuite(DCOPFSolverTest))
    suite.addTest(unittest.makeSuite(DCOPFSolverCase24RTSTest))
    suite.addTest(unittest.makeSuite(DCOPFSolverCaseIEEE30Test))
    suite.addTest(unittest.makeSuite(PIPSSolverTest))
    suite.addTest(unittest.makeSuite(PIPSSolverCase24RTSTest))
    suite.addTest(unittest.makeSuite(PIPSSolvercaseIEEE30Test))
    suite.addTest(unittest.makeSuite(OPFModelTest))
    suite.addTest(unittest.makeSuite(MatpowerReaderTest))
    suite.addTest(unittest.makeSuite(PSSEReaderTest))
    suite.addTest(unittest.makeSuite(StateEstimatorTest))
    return suite


if __name__ == '__main__':
    import logging, sys
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    unittest.TextTestRunner(verbosity=2).run(suite())