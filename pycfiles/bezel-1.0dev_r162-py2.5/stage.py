# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/bezel/graphics/stage.py
# Compiled at: 2009-02-25 04:20:27
from bezel.graphics.containers import Bin

class Stage(Bin):

    def __init__(self):
        super(Stage, self).__init__()
        self.scene_stack = []

    def update_child(self):
        if self.child is not None:
            self.child.deactivate()
            self.child.stage = None
        child = self.scene_stack[(-1)]
        child.stage = self
        self.child = child
        self.child.activate()
        self.invalidate()
        return

    def push(self, child):
        self.scene_stack.append(child)
        self.update_child()

    add = push

    def pop(self):
        assert len(self.scene_stack) > 0
        self.scene_stack.pop()
        self.update_child()

    def replace(self, child):
        self.scene_stack.pop()
        self.push(child)