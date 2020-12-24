# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/netlogger/tests/component/testParseJobstate.py
# Compiled at: 2009-12-08 17:43:28
"""
Unittests for Pegasus jobstate parser.
"""
__author__ = 'Dan Gunter <dkgunter@lbl.gov>'
__rcsid__ = '$Id: testParseJobstate.py 23798 2009-07-14 17:18:22Z dang $'
import unittest
from netlogger import nlapi
from netlogger.tests import shared
from netlogger.parsers.modules import jobstate

class TestCase(shared.BaseParserTestCase):
    basename = 'jobstate-'
    parser_class = jobstate.Parser
    NUM = 6

    def testWithoutHeader(self):
        """Test for lines without a header
        """

        def _test(event, num):
            self.must_have(event, {'event': 'pegasus\\.jobstate\\.\\S+', 'comp.id': 'CyberShake_USC_.*'}, regex=True)

        self.checkGood(filename='nohdr.log', test=_test, num_expected=self.NUM)

    def testWithHeader(self):
        """Test for lines with a header
        """

        def _test(event, num):
            self.must_have(event, {'event': 'pegasus\\.jobstate\\.\\S+', jobstate.Parser.WORKFLOW_LABEL: '\\S+'}, regex=True)

        self.checkGood(filename='hdr.log', test=_test, num_expected=self.NUM)


def suite():
    return shared.suite(TestCase)


if __name__ == '__main__':
    shared.main()