# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ../..\cocos\actions\instant_actions.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 4698 bytes
"""Instant Actions

Instant Actions
===============

Instant actions are immediate actions. They don't have a duration like
the Interval Actions.

"""
from __future__ import division, print_function, unicode_literals
__docformat__ = 'restructuredtext'
import copy
from .base_actions import *
__all__ = [
 'Place',
 'CallFunc', 'CallFuncS',
 'Hide', 'Show', 'ToggleVisibility']

class Place(InstantAction):
    __doc__ = 'Place the `CocosNode` object in the position x,y.\n\n    Example::\n\n        action = Place((320,240))\n        sprite.do(action)\n    '

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
    __doc__ = 'Hides the `CocosNode` object. To show it again call the `Show` () action\n\n    Example::\n\n        action = Hide()\n        sprite.do(action)\n    '

    def start(self):
        self.target.visible = False

    def __reversed__(self):
        return Show()


class Show(InstantAction):
    __doc__ = 'Shows the `CocosNode` object. To hide it call the `Hide` () action\n\n    Example::\n\n        action = Show()\n        sprite.do(action)\n    '

    def start(self):
        self.target.visible = True

    def __reversed__(self):
        return Hide()


class ToggleVisibility(InstantAction):
    __doc__ = 'Toggles the visible attribute of a `CocosNode` object\n\n    Example::\n\n        action = ToggleVisibility()\n        sprite.do(action)\n    '

    def start(self):
        self.target.visible = not self.target.visible

    def __reversed__(self):
        return self


class CallFunc(InstantAction):
    __doc__ = 'An action that will call a function.\n\n    Example::\n\n        def my_func():\n            print "hello baby"\n\n        action = CallFunc(my_func)\n        sprite.do(action)\n    '

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
    __doc__ = 'An action that will call a funtion with the target as the first argument\n\n    Example::\n\n        def my_func(sprite):\n            print "hello baby"\n\n        action = CallFuncS(my_func)\n        sprite.do(action)\n        '

    def start(self):
        (self.func)(self.target, *(self.args), **self.kwargs)