# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sparked/test/test_launcher.py
# Compiled at: 2010-12-21 15:42:19
"""
Tests for sparked.launcher.*

Maintainer: Arjan Scherpenisse
"""
from twisted.python import usage, filepath
from twisted.trial import unittest
from sparked import launcher

class TestLauncher(unittest.TestCase):
    """
    Test the L{sparked.launcher}
    """

    def testLaunchMissingApplicationName(self):
        self.assertRaises(usage.UsageError, launcher.launchApplication, [])

    def testLaunchApplicationNotFound(self):
        self.assertRaises(usage.UsageError, launcher.launchApplication, ['somethingthatdoesnotexist'])

    def testSplitOptions(self):
        self.assertEquals(([], None, []), launcher.splitOptions([]))
        self.assertEquals((['-f'], None, []), launcher.splitOptions(['-f']))
        self.assertEquals(([], 'bla', ['-f']), launcher.splitOptions(['bla', '-f']))
        self.assertEquals((['-a'], 'bla', ['-f']), launcher.splitOptions(['-a', 'bla', '-f']))
        self.assertEquals((['-a', '--b=bleh'], 'bla', ['-f']), launcher.splitOptions(['-a', '--b=bleh', 'bla', '-f']))
        return


class TestQuitFlag(unittest.TestCase):

    def setUp(self):
        import tempfile
        self.flag = launcher.QuitFlag(filepath.FilePath(tempfile.mkstemp()[1]))

    def tearDown(self):
        self.flag.reset()

    def testSimple(self):
        self.assertEquals(False, self.flag.isSet())

    def testSet(self):
        self.flag.set()
        self.assertEquals(True, self.flag.isSet())

    def testSetReset(self):
        self.flag.set()
        self.assertEquals(True, self.flag.isSet())
        self.flag.reset()
        self.assertEquals(False, self.flag.isSet())