# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/netlogger/tests/component/testParseCondorDag.py
# Compiled at: 2009-12-08 17:43:28
"""
Unittests for condor_dag.py
"""
__author__ = 'Dan Gunter dkgunter@lbl.gov'
__rcsid__ = '$Id: testParseCondorDag.py 23923 2009-09-18 22:42:26Z ksb $'
import unittest
from netlogger.tests import shared
from netlogger.parsers.modules import condor_dag

class TestCase(shared.BaseParserTestCase):
    """Unit test cases.
    """
    basename = 'condor_dag_parser-'
    parser_class = condor_dag.Parser

    def setUp(self):
        shared.BaseParserTestCase.setUp(self)
        self.set_up_nl_logger()

    def testBasic(self):
        """Basic test of the parser
        """
        filename = 'sample.log'
        expected = 0
        for line in file(self.getFullPath(filename)):
            if 'PARENT' in line:
                expected += 1

        self.checkGood(filename=filename, num_expected=expected)

    def testCrazy(self):
        """Test parser against cuh-RAY-zeee inputs
        """
        filename = 'crazy.log'
        self.checkGood(filename=filename, num_expected=0)


def suite():
    return shared.suite(TestCase)


if __name__ == '__main__':
    shared.main()