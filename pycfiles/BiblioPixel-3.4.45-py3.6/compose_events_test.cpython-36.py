# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/test/bibliopixel/threads/compose_events_test.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 659 bytes
import threading, unittest
from bibliopixel.util.threads import compose_events

class ComposeEventTest(unittest.TestCase):

    def test_compose_events(self):
        a, b = threading.Event(), threading.Event()
        master = compose_events.compose_events([a, b])
        self.assertFalse(master.is_set())
        a.set()
        self.assertFalse(master.is_set())
        b.set()
        self.assertTrue(master.is_set())
        a.clear()
        self.assertFalse(master.is_set())
        b.clear()
        self.assertFalse(master.is_set())
        b.set()
        self.assertFalse(master.is_set())
        a.set()
        self.assertTrue(master.is_set())