# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/data/christian/Documents/workspace/Yeti/yeti/modules/gameclock.py
# Compiled at: 2016-03-04 11:22:04
# Size of source mod 2**32: 838 bytes
from yeti import Module

class GameClock(Module):
    __doc__ = '\n    A built-in module for keeping track of current game mode.\n    '
    _teleop = False
    _autonomous = False
    _disabled = False

    def module_init(self):
        pass

    def teleop_init(self):
        self._teleop = True
        self._autonomous = False
        self._disabled = False

    def autonomous_init(self):
        self._teleop = False
        self._autonomous = True
        self._disabled = False

    def disabled_init(self):
        self._teleop = False
        self._autonomous = False
        self._disabled = True

    def is_teleop(self):
        return self._teleop

    def is_autonomous(self):
        return self._autonomous

    def is_enabled(self):
        return not self._disabled

    def is_disabled(self):
        return self._disabled