# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/netlogger/tests/unit/testStartend.py
# Compiled at: 2009-12-08 17:43:28
"""
Unittests for analysis/startend.py
"""
__author__ = 'Dan Gunter dkgunter@lbl.gov'
__rcsid__ = '$Id: testStartend.py 23596 2009-03-18 03:58:50Z dang $'
from netlogger.tests import shared
import unittest
from netlogger.analysis import startend

class TestCase(unittest.TestCase):
    event_source_1 = [
     {'ts': '2007-12-18T19:00:17.880754Z', 'event': 'something.else', 
        'value': 1},
     {'ts': '2007-12-18T19:00:18.880754Z', 'event': 'a.start', 
        'guid': '792d15d6-ad9b-11dc-a674-001b63926e0d'},
     {'ts': '2007-12-18T20:00:19.880754Z', 'event': 'b.start', 
        'guid': '792d15d6-ad9b-11dc-a674-001b63926e0d'},
     {'ts': '2007-12-18T20:00:20.880754Z', 'event': 'a.end', 
        'guid': '792d15d6-ad9b-11dc-a674-001b63926e0d'},
     {'ts': '2007-12-18T20:00:20.980754Z', 'event': 'b.end', 
        'guid': '792d15d6-ad9b-11dc-a674-001b63926e0d'}]

    def _testOne(self, events, non_se, scanned_a):
        m = startend.StartEndMatcher(idlist=('event', 'guid'), max_time=3600, scan=2)
        for (i, e) in enumerate(events):
            added = m.add(e)
            self.assert_(i == non_se or added, 'add(event) at %d' % i)
            if len(m) > 0:
                if i == scanned_a:
                    r = m.getResults()[0]
                    self.assertEquals(r[1], None, 'non-empty end')
                else:
                    r = m.getResults()[0]
                    self.assertEquals(r[0]['event'], 'b.start', '%d: b.start not returned' % i)
                    self.assertEquals(r[1]['event'], 'b.end', '%d: b.end not returned' % i)

        return

    def testOneOrdered(self):
        """Test correctness with one StartEnd class and ordered events.
        """
        self._testOne(self.event_source_1, 0, 3)

    def testOneUnordered(self):
        """Test correctness with one StartEnd class and out-of-order events.
        """
        esrc = self.event_source_1[:]
        first = esrc[0]
        esrc = esrc[1:] + [first]
        self._testOne(esrc, len(esrc) - 1, 2)


def suite():
    return shared.suite(TestCase)


if __name__ == '__main__':
    shared.main()