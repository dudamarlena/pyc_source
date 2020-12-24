# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/netlogger/tests/component/testParsePBS.py
# Compiled at: 2009-12-08 17:43:28
"""
Unittests for pbs_parser.py
"""
__author__ = 'Shreyas Cholia scholia@lbl.gov'
__rcsid__ = '$Id: testParsePBS.py 23798 2009-07-14 17:18:22Z dang $'
import unittest
from netlogger.tests import shared
from netlogger.parsers.modules import pbs

class TestCase(shared.BaseParserTestCase):
    """Unit test cases.
    """
    basename = 'pbs_parser-'
    parser_class = pbs.Parser

    def testBasic(self):
        """Basic test of pbs_parser
        """
        filename = 'sample.log'
        expected = len(list(file(self.getFullPath(filename))))
        self.checkGood(filename=filename, num_expected=expected)


def suite():
    return shared.suite(TestCase)


if __name__ == '__main__':
    shared.main()