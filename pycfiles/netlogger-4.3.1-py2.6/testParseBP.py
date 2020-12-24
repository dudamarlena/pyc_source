# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/netlogger/tests/unit/testParseBP.py
# Compiled at: 2011-08-17 23:42:54
"""
Unittests for BP parsing in netlogger.parsers.base
"""
__author__ = 'Dan Gunter dkgunter@lbl.gov'
__rcsid__ = '$Id: testParseBP.py 28287 2011-08-18 03:42:53Z dang $'
import unittest
from netlogger.tests import shared
from netlogger.parsers import base
BASIC_OK = [
 'ts=2011-08-17T07:49:22.000Z event=test',
 'ts=2011-08-17T07:49:22.000Z event=test name=val',
 '   ts=2011-08-17T07:49:22.000Z    event=test    name=val   ',
 'ts=2011-08-17T07:49:22.000Z event=test name="value with spaces"',
 '  ts=2011-08-17T07:49:22.000Z   event=test name="value with spaces"  ',
 'ts=2011-08-17T07:49:22.000Z event=test name="value with \\"quote\\" and spaces"',
 ' ts=2011-08-17T07:49:22.000Z event=test \tname="value with \\"quote\\" and spaces"  ']
BASIC_FAIL = [
 '',
 '=',
 "'",
 'name=',
 'ts=2011-08-17T07:49:22.000Z']
BASIC_FAIL_VERIFY = [
 'ts=2011-08-17T07:49:22.000Z event=foo solo',
 'ts=2011-08-17T07:49:22.000Z event=foo solo mio',
 'ts=2011-08-17T07:49:22.000Z event=foo solo="mio "and" foo"']
MATCH = [
 (
  'ts=2011-08-17T07:49:22.000Z event=test', {'ts': '2011-08-17T07:49:22.000Z', 'event': 'test'}),
 (
  'ts=2011-08-17T07:49:22.000Z event=test name="value with \\"quote\\" and spaces"', {'ts': '2011-08-17T07:49:22.000Z', 'event': 'test', 'name': 'value with "quote" and spaces'}),
 (
  ' ts=2011-08-17T07:49:22.000Z event=test \tname="value with \\"quote\\" and spaces"  ', {'ts': '2011-08-17T07:49:22.000Z', 'event': 'test', 'name': 'value with "quote" and spaces'})]

class SimpleParserTestCase(shared.BaseTestCase):
    """Unit test cases.
    """

    def test_basic_noverify(self):
        """parsing succeeds or fails on a basic set of tests, without verification
        """
        self._test_basic(False)

    def test_basic_verify(self):
        """parsing succeeds or fails on a basic set of tests, with verification
        """
        self._test_basic(True)

    def _test_basic(self, verify):
        p = base.NLSimpleParser(verify=verify)
        for line in BASIC_OK:
            p.parseLine(line)
            p.parseLine(line + '\n')

        for line in BASIC_FAIL:
            try:
                p.parseLine(line)
                self.assert_(False, ("Unexpected success for '{0}'").format(line))
            except base.BPError:
                pass

        if verify:
            for line in BASIC_FAIL_VERIFY:
                try:
                    p.parseLine(line)
                    self.assert_(False, ("Unexpected success for '{0}'").format(line))
                except base.BPError:
                    pass

    def test_match_verify(self):
        """parsing matches expected result, with verification
        """
        self._test_match(True)

    def test_match_noverify(self):
        """parsing matches expected result, without verification
        """
        self._test_match(False)

    def _test_match(self, verify):
        p = base.NLSimpleParser(verify=verify, parse_date=False)
        for (line, expected) in MATCH:
            result = p.parseLine(line)
            self.assertEquals(result, expected)


def suite():
    return shared.suite(SimpleParserTestCase)


if __name__ == '__main__':
    shared.main()