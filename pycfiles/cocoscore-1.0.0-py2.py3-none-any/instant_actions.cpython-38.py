# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ../..\cocos\actions\instant_actions.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 4698 bytes
__doc__ = "Instant Actions\n\nInstant Actions\n===============\n\nInstant actions are immediate actions. They don't have a duration like\nthe Interval Actions.\n\n\n"
from __future__ import division, print_function, unicode_literals
__docformat__ = 'restructuredtext'
import copy
from .base_actions import *
__all__ = [
 'Place',
 'CallFunc', 'CallFuncS',
 'Hide', 'Show', 'ToggleVisibility']

class Place(InstantAction):
    """Place"""

    def init(self, position):
        """Init method.

        :Parameters:
            `position` : (x,y)
                Coordinates where the sprite will be placed
        """
        self.position = position

    def start(self):
        self.target.position = self.position


class Hide(InstantAction):
    """Hide"""

    def start(self):
        self.target.visible = False

    def __reversed__(self):
        return Show()


class Show(InstantAction):
    """Show"""

    def start(self):
        self.target.visible = True

    def __reversed__(self):
        return Hide()


class ToggleVisibility(InstantAction):
    """ToggleVisibility"""

    def start(self):
        self.target.visible = not self.target.visible

    def __reversed__(self):
        return self


class CallFunc(InstantAction):
    """CallFunc"""

    def init(self, func, *args, **kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def start(self):
        (self.func)(*self.args, **self.kwargs)

    def __deepcopy__(self, memo):
        return copy.copy(self)

    def __reversed__(self):
        return self


class CallFuncS(CallFunc):
    """CallFuncS"""

    def start(self):
        (self.func)(self.target, *(self.args), **self.kwargs)