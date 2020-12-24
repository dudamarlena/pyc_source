# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/netlogger/tests/unit/testParseDynamic.py
# Compiled at: 2009-12-08 17:43:28
"""
Unittests for parsers/modules/dynamic.py
"""
__author__ = 'Dan Gunter dkgunter@lbl.gov'
__rcsid__ = '$Id: testParseDynamic.py 23614 2009-03-26 16:27:48Z dang $'
import re
from StringIO import StringIO
import unittest
from netlogger.parsers.modules import dynamic
from netlogger.parsers.modules import globus_condor
from netlogger.tests import shared
import testParseGlobusCondor
HEADER = 'MyApp '
EVENT1 = HEADER + 'This-is-my-data  '

class Parser:
    """Dummy parser class
    """

    def process(self, line):
        return line

    def setHeaderValues(self, data):
        pass


class TestCase(shared.BaseTestCase):
    """Unit test cases.
    """

    def setUp(self):
        """Create a parser instance.
        """
        self.parser = dynamic.Parser(StringIO('FAKE'), pattern='(?P<app>\\S+)')

    def tearDown(self):
        """Any cleanup actions
        """
        pass

    def testStripWhitespace(self):
        """Make sure leading/trailing whitespace is stripped.
        """
        self.parser.add('me', {'app': re.compile('MyApp')}, Parser())
        value = self.parser.process(EVENT1)
        self.failUnless(value.strip() == value, "Whitespace in '%s'" % value)

    def testStripWhitespaceGC(self):
        """Check globus_condor parser with whitespace stripping
        """
        self.parser.add('gc', {'app': re.compile('MyApp')}, globus_condor.Parser(StringIO('FAKE')))
        result = ()
        for line in testParseGlobusCondor.SUBMIT_EVENT.split('\n'):
            self.failIf(result, 'Event parsed prematurely')
            event = HEADER + line
            result = self.parser.process(event)

        self.failUnless(len(result) == 1, 'Event not parsed')


def suite():
    return shared.suite(TestCase)


if __name__ == '__main__':
    shared.main()