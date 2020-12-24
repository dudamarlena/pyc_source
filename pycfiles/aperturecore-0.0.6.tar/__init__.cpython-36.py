# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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