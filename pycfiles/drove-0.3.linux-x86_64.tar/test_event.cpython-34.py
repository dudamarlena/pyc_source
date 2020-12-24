# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ajdiaz/env/drove/lib/python3.4/site-packages/drove/tests/data/test_event.py
# Compiled at: 2015-01-20 05:42:58
# Size of source mod 2**32: 1043 bytes
import time, unittest
from drove.data.event import Event
from drove.data.event import Severity

class TestEvent(unittest.TestCase):

    def test_event(self):
        """Testing Event: dump()"""
        event = Event('example', Severity.CRITICAL, 'message', nodename='test', timestamp=0)
        assert event.is_event()
        assert event.dump() == 'E|0|test|example|2|message'
        event = Event('example', Severity.CRITICAL, 'message', nodename='test')
        assert event.dump() == 'E|%d|test|example|2|message' % (
         int(time.time()),)

    def test_event_dump(self):
        """Testing Event: from_dump()"""
        event = Event.from_dump('E|0|test|example|2|message')
        assert event.dump() == 'E|0|test|example|2|message' == repr(event)

    def test_event_malformed(self):
        """Testing Event: malformed event"""
        with self.assertRaises(ValueError):
            Event.from_dump('E|0')