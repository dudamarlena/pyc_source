# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/flappy/display/interactiveobject.py
# Compiled at: 2014-03-13 10:09:15
from flappy.display import DisplayObject

class InteractiveObject(DisplayObject):

    def __init__(self, name=None):
        DisplayObject.__init__(self, name)
        self.doubleClickEnabled = False

    def requestSoftKeyboard(self):
        raise NotImplementedError

    @property
    def mouseEnabled(self):
        return self.getMouseEnabled()

    @mouseEnabled.setter
    def mouseEnabled(self, value):
        self.setMouseEnabled(value)

    @property
    def moveForSoftKeyboard(self):
        raise NotImplementedError

    @moveForSoftKeyboard.setter
    def moveForSoftKeyboard(self, value):
        raise NotImplementedError

    @property
    def needsSoftKeyboard(self):
        raise NotImplementedError

    @needsSoftKeyboard.setter
    def needsSoftKeyboard(self, value):
        raise NotImplementedError