# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/netlogger/tests/unit/testParseVmstat.py
# Compiled at: 2010-01-09 10:32:25
"""
Unittests for vmstat parser
"""
__author__ = 'Dan Gunter dkgunter@lbl.gov'
__rcsid__ = '$Id: testParseVmstat.py 24045 2010-01-09 15:32:24Z dang $'
import logging, StringIO, unittest
from netlogger.parsers.modules import vmstat
from netlogger.tests import shared
SAMPLE1 = 'procs -----------memory---------- ---swap-- -----io---- --system-- -----cpu------\nr  b   swpd   free   buff  cache   si   so    bi    bo   in   cs us sy id wa st\n0  0      0 5414724 245476 481588    0    0  4425  1225    4   10  2  8 90  0  0\n'
SAMPLE1_PARSED = dict(r=0, b=0, swpd=0, free=5414724, buff=245476, cache=481588, si=0, so=0, bi=4425, bo=1225, cs=10, us=2, sy=8, id=90, wa=0, st=0)
SAMPLE1_PARSED['in'] = 4

class TestCase(shared.BaseTestCase, shared.ParserTestCase):

    def setUp(self):
        self.setParser(vmstat.Parser)

    def test1(self):
        """Validate on correct input
        """
        result = self.feedRecord(SAMPLE1)
        self.failUnless(result, 'Could not parse: %s' % SAMPLE1)
        data = result[0]
        for (key, value) in SAMPLE1_PARSED.items():
            self.failUnless(data.has_key(key), "Missing key '%s'" % key)
            self.failUnless(data[key] == value, "Wrong value (%d, not %d) for key '%s'" % (
             data[key], value, key))


def suite():
    return shared.suite(TestCase)


if __name__ == '__main__':
    shared.main()