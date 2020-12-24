# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ajdiaz/env/drove/lib/python3.4/site-packages/drove/tests/test_reloader.py
# Compiled at: 2015-01-20 05:42:58
# Size of source mod 2**32: 671 bytes
import unittest, drove.reloader

class TestReloader(unittest.TestCase):

    class MockObject(object):

        def reload(self):
            pass

    def setUp(self):
        self._Timer = drove.reloader.Timer

    def tearDown(self):
        drove.reloader.Timer = self._Timer

    def test_reloader(self):
        """Testing Reloader: basic behaviour"""
        x = drove.reloader.Reloader([TestReloader.MockObject()])
        x.reload()

    def test_reloader_start(self):
        """Testing Reloader: start()"""
        x = drove.reloader.Reloader([TestReloader.MockObject()])
        x.start()