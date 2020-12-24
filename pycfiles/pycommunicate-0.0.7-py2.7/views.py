# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\pycommunicate\server\bases\views.py
# Compiled at: 2016-06-11 08:16:50
import eventlet

class View:

    def __init__(self, controller):
        self.controller = controller
        self.html_wrapper = controller.html_wrapper
        self.timers = []

    def add_timer(self, time, function):

        def timer():
            while True:
                eventlet.greenthread.sleep(time)
                function()

        green_thread = eventlet.greenthread.spawn(timer)
        self.timers.append(green_thread)
        return self.timers.index(green_thread)

    def cancel_timer(self, timer):
        self.timers[timer].kill()

    def teardown(self):
        for timer in self.timers:
            timer.kill()

    def load(self):
        pass

    def render(self):
        pass