# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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