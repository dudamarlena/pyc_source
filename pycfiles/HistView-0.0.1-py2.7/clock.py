# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-x86_64/egg/HistView/clock.py
# Compiled at: 2015-11-09 15:14:37
from kivy.app import App
from kivy.uix.label import Label
from kivy.clock import Clock
import time

class SampleClock(Label):

    def update(self, *args):
        self.text = time.asctime()


class TimeApp(App):

    def build(self):
        clock = SampleClock()
        Clock.schedule_interval(clock.update, 1)
        return clock


if __name__ == '__main__':
    TimeApp().run()