# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/netlogger/tests/component/testParseGramAcct.py
# Compiled at: 2009-12-08 17:43:28
"""
Unittests for gram_acct.py
"""
__author__ = 'Dan Gunter dkgunter@lbl.gov'
__rcsid__ = '$Id: testParseGramAcct.py 23798 2009-07-14 17:18:22Z dang $'
import unittest
from netlogger.tests import shared
from netlogger.parsers.modules import gram_acct

class TestCase(shared.BaseParserTestCase):
    """Unit test cases.
    """
    basename = 'gram_acct-'
    parser_class = gram_acct.Parser

    def testBasic(self):
        """Parse the sample log
        """
        filename = 'basic.log'
        expected = 0
        f = file(self.getFullPath(filename))
        for line in f:
            if 'GRAM_SCRIPT_JOB_ID' in line:
                expected += 1

        self.checkGood(filename=filename, num_expected=expected)


def suite():
    return shared.suite(TestCase)


if __name__ == '__main__':
    shared.main()