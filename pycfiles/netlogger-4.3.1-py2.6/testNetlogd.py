# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/netlogger/tests/unit/testNetlogd.py
# Compiled at: 2009-12-08 17:43:28
"""
Unittests for netlogd.py
"""
__author__ = 'Dan Gunter dkgunter@lbl.gov'
__rcsid__ = '$Id: testNetlogd.py 23960 2009-10-12 18:23:32Z dang $'
import os, unittest
from tempfile import mkstemp
from netlogger.tests import shared

class TestCase(shared.BaseTestCase):
    program = shared.script_path('netlogd')
    long_args = [
     '--flush', '--kill', '10m', '--port', '33553', '--rollover',
     '100kb', '--udp', '--quiet']
    short_args = [
     '-f', '-k', '10m', '-p', '33553', '-r', '100MB', '-U', '-v']

    def testArgsBasic(self):
        """Test different combinations of command line arguments.
        """
        self.cmd(['-h'], 'wait')
        self.cmd([''])
        self.cmd(['--foobar'], 'wait', should_fail=True)

    def testArgsAllExceptFile(self):
        """Test the whole batch of short args / long args
        """
        self.cmd(self.short_args)
        self.cmd(self.long_args)

    def testArgsFile(self):
        """Test args including output files
        """
        tempfiles = (
         mkstemp()[1], mkstemp()[1])
        self.cmd(self.short_args + ['-o', tempfiles[0], '-o', tempfiles[1]])
        self.cmd(self.long_args + ['--output', tempfiles[0],
         '--output', tempfiles[1]])
        for f in tempfiles:
            os.unlink(f)


def suite():
    return shared.suite(TestCase)


if __name__ == '__main__':
    shared.main()