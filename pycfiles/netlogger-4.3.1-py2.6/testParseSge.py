# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/netlogger/tests/component/testParseSge.py
# Compiled at: 2009-12-08 17:43:28
"""
Unittests for sge.py
"""
__author__ = 'Dan Gunter dkgunter@lbl.gov'
__rcsid__ = '$Id$'
from netlogger.tests import shared
import unittest
from netlogger.parsers.modules import sge
from netlogger.parsers.base import NLFastParser

class TestCase(shared.BaseParserTestCase):
    basename = 'sge-'
    parser_class = sge.Parser

    def __init__(self, *args, **kw):
        shared.BaseParserTestCase.__init__(self, *args, **kw)
        self._p = NLFastParser()

    def testStartEnd(self):
        """Test for correctly parsed values in start and end event
        """
        e0 = {}

        def _test(e, num):
            if num == 0:
                self.assertEquals(int(e['job.id']), 2779793)
                e0.update(e)
            else:
                self.assertEquals(int(e['job.id']), 2779793)
                self.assertEquals(float(e['maxvmem']), 219533312.0)
                self.failUnless(e['ts'] > e0['ts'], 'Time is backwards')

        self.checkGood(filename='basic.log', test=_test, num_expected=2)

    def testOneEvent(self):
        """Test for correctly parsed values in single event"""

        def _test(e, num):
            self.assert_(float(e['dur']) >= 0, 'Time is backwards')
            self.assertEquals(float(e['maxvmem']), 219533312.0)
            self.assertEquals(int(e['job.id']), 2779793)

        self.checkGood('basic.log', test=_test, num_expected=1, parser_kw={'one_event': True})


def suite():
    return shared.suite(TestCase)


if __name__ == '__main__':
    shared.main()