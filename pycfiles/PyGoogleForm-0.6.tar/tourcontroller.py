# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\pygoogleearth\tourcontroller.py
# Compiled at: 2009-09-26 22:10:50


class TourController(object):

    def __init__(self, comobject):
        self.ge_tc = comobject

    def __getattr__(self, name):
        if name == 'speed':
            return self.ge_tc.Speed
        if name == 'pause_delay':
            return self.ge_tc.PauseDelay
        if name == 'cycles':
            return self.ge_tc.Cycles
        raise AttributeError

    def __setattr__(self, name, value):
        if name == 'speed':
            self.ge_tc.Speed = value
        elif name == 'pause_delay':
            self.ge_tc.PauseDelay = value
        elif name == 'cycles':
            self.ge_tc.Cycles = value
        else:
            raise AttributeError

    def play_or_pause(self):
        self.ge_tc.PlayOrPause()

    def stop(self):
        self.ge_tc.Stop()