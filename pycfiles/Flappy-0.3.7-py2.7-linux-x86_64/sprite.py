# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/flappy/display/sprite.py
# Compiled at: 2014-03-13 10:09:15
from flappy.geom import Rectangle
from flappy.display import DisplayObjectContainer

class Sprite(DisplayObjectContainer):

    def __init__(self, name=None):
        DisplayObjectContainer.__init__(self, name)

    def startDrag(self, lock_center=False, bounds=None):
        if self.stage:
            self.stage._start_drag(self, lock_center, bounds)

    def stopDrag(self):
        if self.stage:
            self.stage._stop_drag(self)