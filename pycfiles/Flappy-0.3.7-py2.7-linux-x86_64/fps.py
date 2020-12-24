# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/flappy/display/fps.py
# Compiled at: 2014-03-13 10:09:15
from flappy.text import TextField, TextFormat, TextFieldAutoSize
from flappy.events import Event
import time

class FPS(TextField):

    def __init__(self, x=0.0, y=0.0, color=16776960):
        super(FPS, self).__init__()
        self.x = x
        self.y = y
        self.text = 'starting...'
        self.second = 0.0
        self.frames = 0
        self.prevtime = time.time()
        self.addEventListener(Event.ENTER_FRAME, self._on_frame, use_weak_reference=True)

    def _on_frame(self, e):
        now = time.time()
        dt = now - self.prevtime
        self.second += dt
        if self.second >= 1.0:
            self.text = 'FPS: ' + str(self.frames)
            self.frames = 0
            self.second = 0.0
        else:
            self.frames += 1
        self.prevtime = now