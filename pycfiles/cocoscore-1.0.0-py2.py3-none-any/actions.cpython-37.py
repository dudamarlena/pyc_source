# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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