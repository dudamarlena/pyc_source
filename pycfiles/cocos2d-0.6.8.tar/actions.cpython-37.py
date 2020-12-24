# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\dev\cocos2020\cocos\audio\actions.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 2340 bytes
from cocos import actions
from cocos import audio

class PlayAction(actions.InstantAction):

    def init(self, sound):
        self.sound = sound

    def start(self):
        if audio._working:
            self.sound.play()

    def __deepcopy__(self, memo):
        return PlayAction(self.sound)