# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: C:\Users\Neko\Desktop\aperturec\aperture\__init__.py
# Compiled at: 2020-01-09 14:43:57
# Size of source mod 2**32: 1275 bytes
from . import __s_lib__ as soundlib
from . import __player__ as player

def current_sound():
    return player.sounds.current


class sounds:
    pitch = 1
    volume = 100
    speed = 1

    class imports:

        def __init__(self):
            self.a = None

        def csp(name: str, value: str):
            v = soundlib._import.csp(name, value)
            player.queue(v)
            return v

        def ctp(name: str):
            v = soundlib._import.ctp(name=name)
            sounds.volume = v['volume']
            sounds.pitch = v['pitch']
            sounds.speed = v['speed']
            return v

    class modifiers:

        def __init__(self):
            self.pitch = sounds.pitch
            self.volume = sounds.volume
            self.speed = sounds.speed

        def set_speed(self, speed):
            sounds.speed, self.speed = speed, speed
            soundlib.modifiers.speed = self.speed

        def set_volume(self, volume):
            sounds.volume, self.volume = volume, volume
            soundlib.modifiers.volume = self.volume

        def set_pitch(self, pitch):
            sounds.pitch, self.pitch = pitch, pitch
            soundlib.modifiers.pitch = self.pitch