# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ajdiaz/env/drove/lib/python3.4/site-packages/drove/tests/util/test_daemon.py
# Compiled at: 2015-01-20 05:42:58
# Size of source mod 2**32: 591 bytes
import os, unittest
from drove.util.daemon import Daemon

class TestDaemon(unittest.TestCase):

    def setUp(self):
        self._os = os.name

    def tearDown(self):
        os.name = self._os

    def test_daemon(self):
        """Testing Daemon: invalid platform"""
        os.name = 'foo'
        with self.assertRaises(NotImplementedError):
            Daemon.create(lambda : None)

    def test_daemon_posix(self):
        """Testing Daemon: posix"""
        os.name = 'posix'
        Daemon.create(lambda : None)