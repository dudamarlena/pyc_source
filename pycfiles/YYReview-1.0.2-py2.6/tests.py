# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\rbtools\utils\tests.py
# Compiled at: 2012-09-04 05:45:40
"""Tests for rbtools.api units.

Any new modules created under rbtools/api should be tested here."""
import os, re, sys
from rbtools.utils import checks, filesystem, process
from rbtools.utils.testbase import RBTestBase

class UtilitiesTest(RBTestBase):

    def test_check_install(self):
        """Test 'check_install' method."""
        self.assertTrue(checks.check_install(sys.executable + ' --version'))
        self.assertFalse(checks.check_install(self.gen_uuid()))

    def test_make_tempfile(self):
        """Test 'make_tempfile' method."""
        fname = filesystem.make_tempfile()
        self.assertTrue(os.path.isfile(fname))
        self.assertEqual(os.stat(fname).st_uid, os.geteuid())
        self.assertTrue(os.access(fname, os.R_OK | os.W_OK))

    def test_execute(self):
        """Test 'execute' method."""
        self.assertTrue(re.match('.*?%d.%d.%d' % sys.version_info[:3], process.execute([sys.executable, '-V'])))

    def test_die(self):
        """Test 'die' method."""
        self.assertRaises(SystemExit, process.die)