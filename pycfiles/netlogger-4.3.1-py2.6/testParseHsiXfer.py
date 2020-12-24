# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/netlogger/tests/component/testParseHsiXfer.py
# Compiled at: 2009-12-08 17:43:28
"""
Unittests for sge.py
"""
__author__ = 'Shreyas Cholia scholia@lbl.gov'
__rcsid__ = '$Id$'
import unittest
from netlogger import nlapi
from netlogger.tests import shared
from netlogger.parsers.modules import hsi_xfer
from netlogger.parsers.base import NLFastParser

class TestCase(shared.BaseParserTestCase):
    basename = 'hsi_xfer-'
    parser_class = hsi_xfer.Parser

    def __init__(self, *args, **kw):
        shared.BaseParserTestCase.__init__(self, *args, **kw)
        self._p = NLFastParser()
        nlapi.clearGuid()

    def testBasic(self):
        """Test for correctly parsed lines
        """

        def _test(e, num):
            self.assertEquals(len(e), 14, "Expected 14 items, got %d in '%s'" % (
             len(e), e))
            self.failIf(int(e['uid']) < 0, 'Invalid UID')
            self.failIf(int(e['pid']) < 0, 'Invalid PID')
            self.assertNotEquals(e['hostname'], '')

        filename = 'xferlog'
        expected = len(list(file(self.getFullPath(filename))))
        self.checkGood(filename=filename, test=_test, num_expected=expected)


def suite():
    return shared.suite(TestCase)


if __name__ == '__main__':
    shared.main()