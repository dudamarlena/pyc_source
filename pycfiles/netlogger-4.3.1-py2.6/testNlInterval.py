# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/netlogger/tests/component/testNlInterval.py
# Compiled at: 2010-10-15 14:38:49
"""
Tests for nl_interval
"""
__author__ = 'Dan Gunter dkgunter@lbl.gov'
__rcsid__ = '$Id: testNlInterval.py 26609 2010-10-15 18:38:47Z dang $'
import unittest
from netlogger.tests import shared

class TestCase(shared.BaseTestCase):
    """Unit test cases.
    """

    def setUp(self):
        self.setProgram('nl_interval')
        self._base_args = ['-t', 'csv', '-i', 'x.id']

    def test_basic(self):
        """Basic happy-path functionality.
        """
        args = self._base_args
        self.cmd(args + [self.data_dir + '/startend.1'], action='communicate')
        expected = ('ts,event,key,interval_sec', '1287099406.44,a,1,5.963682', '1287099430.46,a,3,7.215700')
        self.check_result(expected)

    def test_badarg(self):
        """Handling of bad command-line args
        """
        args = self._base_args
        kw = dict(action='wait', should_fail=True)
        self.cmd((args + ['-i', 'x.id']), **kw)
        self.cmd((args + ['-i', 'foo:x.id', '-i', 'foo:bar']), **kw)
        self.cmd(['-t', 'bad'], **kw)

    def test_multifile(self):
        """Test with start/end spread across input files.
        """
        args = self._base_args
        self.cmd(args + [self.data_dir + '/startend.1',
         self.data_dir + '/startend.2'], action='communicate')
        expected = ('ts,event,key,interval_sec', '1287099406.44,a,1,5.963682', '1287099430.46,a,3,7.215700',
                    '1287099420.28,a,2,1153.624779')
        self.check_result(expected)

    def check_result(self, expected):
        for (i, received) in enumerate(self.cmd_stdout.split('\n')):
            received = received.strip()
            if not received:
                continue
            self.failUnless(expected[i] == received, "bad output: expected '%s' != received '%s'" % (
             expected[i], received))


def suite():
    return shared.suite(TestCase)


if __name__ == '__main__':
    shared.main()