# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\Sascha\Documents\PycharmProjects\maverig\maverig\tests\test_event.py
# Compiled at: 2014-07-14 12:57:26
# Size of source mod 2**32: 1042 bytes
from unittest import TestCase
from maverig.utils.event import Event

class TestEvent(TestCase):

    def test_handle(self):
        data_changed = Event()
        data_changed += self.on_data_changed
        data_changed += self.on_data_changed
        assert len(data_changed) == 1

    def test_unhandle(self):
        data_changed = Event()
        data_changed += self.on_data_changed
        assert len(data_changed) == 1
        data_changed -= self.on_data_changed
        assert len(data_changed) == 0
        self.assertRaises(ValueError, data_changed.unhandle, self.on_data_changed)
        assert len(data_changed) == 0

    def test_fire(self):
        data_changed = Event()
        data_changed += self.on_data_changed
        param1 = 2
        data_changed(param1, param2=3)

    def on_data_changed(self, param1, param2):
        assert param1 == 2 and param2 == 3