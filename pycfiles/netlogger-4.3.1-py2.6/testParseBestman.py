# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/netlogger/tests/component/testParseBestman.py
# Compiled at: 2009-12-08 17:43:28
"""
Unittests for <module>.py
"""
__author__ = 'Dan Gunter dkgunter@lbl.gov'
__rcsid__ = '$Id: testParseBestman.py 23798 2009-07-14 17:18:22Z dang $'
import unittest
from netlogger.tests import shared
from netlogger.parsers.modules import bestman

class TestCase(shared.BaseParserTestCase):
    """Unit test cases.
    """
    basename = 'srm-'
    parser_class = bestman.Parser

    def testVersion1(self):
        """Bestman version-1 style logs copied off PDSF
        """
        self.checkGood(filename='transfer.log', num_expected=4, parser_kw={'version': '1'})

    def testVersion2(self):
        """Bestman version-2 style logs copied off PDSF"""
        self.checkGood(filename='transfer2.log', num_expected=200, parser_kw={'version': '2'})


def suite():
    return shared.suite(TestCase)


if __name__ == '__main__':
    shared.main()