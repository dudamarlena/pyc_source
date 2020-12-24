# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/leon/tests/test_file_change_watcher.py
# Compiled at: 2013-05-06 08:51:38
import os
from unittest import TestCase
from leon.file_change_watcher import FileChangeWatcher

class TestFileChangeWatcher(TestCase):

    def test_start_stop(self):
        watcher = FileChangeWatcher(os.path.abspath(os.path.join(os.path.dirname(__file__), 'files', 'watcher')), None)
        watcher.start()
        self.assertTrue(watcher.is_alive())
        watcher.stop()
        watcher.join(1)
        self.assertFalse(watcher.is_alive())
        return