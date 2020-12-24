# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/bezel/graphics/scene.py
# Compiled at: 2009-02-25 04:20:27
from bezel.graphics.containers import Bin

class Scene(Bin):

    def __init__(self, *args, **kwargs):
        super(Scene, self).__init__(*args, **kwargs)
        self.stage = None
        return

    def activate(self):
        pass

    def deactivate(self):
        pass

    def finish(self):
        self.stage.pop()

    def replace(self, next):
        self.stage.replace(next)