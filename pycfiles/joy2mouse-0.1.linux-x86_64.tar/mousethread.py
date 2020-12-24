# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/daniel/Programming/python/joy2mouse/joy2mouselib/mousethread.py
# Compiled at: 2011-06-08 12:43:57
import threading, time, mouse

class MouseThread(threading.Thread):

    def __init__(self, pointermode):
        threading.Thread.__init__(self)
        self.pointermode = pointermode
        self.mouse = mouse.Mouse()
        self.x = 0
        self.y = 0
        self.running = True

    def run(self):
        while self.running:
            if self.x != 0 or self.y != 0:
                self.mouse.move_relative(self.x, self.y)
                if not self.pointermode:
                    self.x, self.y = (0, 0)
            time.sleep(1 / 500.0)