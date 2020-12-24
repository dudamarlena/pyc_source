# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\dev\cocos2020\cocos\audio\effect.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 2789 bytes
from __future__ import division, print_function, unicode_literals
__docformat__ = 'restructuredtext'
from cocos import audio
try:
    from cocos.audio.pygame.mixer import Sound
except ImportError:
    audio._working = False

from . import actions

class Effect(object):
    __doc__ = "Effects are sounds effect loaded in memory\n\n    Example ::\n\n        shot = Effect('bullet.wav')\n        shot.play() # Play right now\n        sprite.do(shot.action)\n    "

    def __init__(self, filename):
        """Initialize the effect

        :Parameters:
            `filename` : fullpath
                path of a WAV or Ogg audio file
        """
        if audio._working:
            self.sound = Sound(filename)
        else:
            self.sound = None
        self.action = actions.PlayAction(self.sound)

    def play(self):
        if audio._working:
            self.sound.play()