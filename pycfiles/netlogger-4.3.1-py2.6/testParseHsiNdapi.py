# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/netlogger/tests/component/testParseHsiNdapi.py
# Compiled at: 2009-12-08 17:43:28
"""
Unittests for sge.py
"""
__author__ = 'Shreyas Cholia scholia@lbl.gov'
__rcsid__ = '$Id$'
import unittest, time, re
from netlogger.tests import shared
from netlogger.parsers.modules import hsi_ndapi

class TestCase(shared.BaseParserTestCase):
    basename = 'hsi_ndapi-'
    parser_class = hsi_ndapi.Parser

    def __init__(self, *args, **kw):
        shared.BaseParserTestCase.__init__(self, *args, **kw)

    def testBasic(self):
        """Test for correctly parsed lines
        """

        def _test(e, num):
            self.assert_(e.has_key('ts'))
            self.assert_(e.has_key('pid'))
            self.assertNotEquals(e['event'], '')

        filename = 'ndapilog'
        expected = 0
        pattern = re.compile('\\w{3} \\w{3} \\d{1,2} \\d{1,2}:\\d{1,2}:\\d{1,2} \\d{4}')
        for line in list(file(self.getFullPath(filename))):
            if pattern.match(line):
                expected += 1

        self.checkGood(filename=filename, test=_test, num_expected=expected)


def suite():
    return shared.suite(TestCase)


if __name__ == '__main__':
    shared.main()