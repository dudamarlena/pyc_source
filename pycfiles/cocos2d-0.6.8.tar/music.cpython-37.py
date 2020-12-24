# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: d:\dev\cocos2020\cocos\audio\music.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 2726 bytes
"""This is a wrapper to the low level music API. You shouldn't use this in
your cocos applications; but instead use the music control functions in the
Scene class
"""
from cocos import audio
try:
    import cocos.audio.pygame.music
except ImportError:
    audio._working = False

class MusicControl(object):

    def load(self, filename):
        pygame.music.load(filename)

    def play(self):
        pygame.music.play()

    def stop(self):
        pygame.music.stop()


class DummyMusicControl(object):

    def load(self, filename):
        pass

    def play(self):
        pass

    def stop(self):
        pass


def set_control(name):
    global control
    assert name in ('dummy', 'pygame')
    control = globals()[('_' + name)]


_dummy = DummyMusicControl()
_pygame = MusicControl()
set_control('dummy')