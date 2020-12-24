# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: d:\dev\cocos2020\cocos\audio\music.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 2726 bytes
__doc__ = "This is a wrapper to the low level music API. You shouldn't use this in\nyour cocos applications; but instead use the music control functions in the\nScene class\n"
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