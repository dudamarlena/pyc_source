# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/christian/PycharmProjects/Yeti/yeti/modules/gameclock.py
# Compiled at: 2015-09-22 08:32:28
# Size of source mod 2**32: 818 bytes
from yeti import Module

class GameClock(Module):
    __doc__ = '\n    A built-in module for keeping track of current game mode.\n    '
    _teleop = False
    _autonomous = False
    _disabled = False

    def module_init(self):
        pass

    def teleop(self):
        self._teleop = True
        self._autonomous = False
        self._disabled = False

    def autonomous(self):
        self._teleop = False
        self._autonomous = True
        self._disabled = False

    def disabled(self):
        self._teleop = False
        self._autonomous = False
        self._disabled = True

    def is_teleop(self):
        return self.teleop

    def is_autonomous(self):
        return self.autonomous

    def is_enabled(self):
        return not self.disabled

    def is_disabled(self):
        return self.disabled