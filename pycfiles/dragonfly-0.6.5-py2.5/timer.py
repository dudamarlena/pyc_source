# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\dragonfly\timer.py
# Compiled at: 2008-11-19 12:15:17
"""
        This file implements a basic multiplexing interface to the natlink timer.
"""
import time, natlink

class _Timer(object):

    class Callback(object):

        def __init__(self, function, interval):
            self.function = function
            self.interval = interval
            self.next_time = time.clock() + self.interval

        def call(self):
            self.next_time += self.interval
            self.function()

    def __init__(self, interval):
        self.interval = interval
        self.callbacks = []

    def add_callback(self, function, interval):
        self.callbacks.append(self.Callback(function, interval))
        if len(self.callbacks) == 1:
            natlink.setTimerCallback(self.callback, int(self.interval * 1000))

    def remove_callback(self, function):
        for c in self.callbacks:
            if c.function == function:
                self.callbacks.remove(c)

        if len(self.callbacks) == 0:
            natlink.setTimerCallback(None, 0)
        return

    def callback(self):
        now = time.clock()
        for c in self.callbacks:
            if c.next_time < now:
                c.call()


timer = _Timer(0.025)