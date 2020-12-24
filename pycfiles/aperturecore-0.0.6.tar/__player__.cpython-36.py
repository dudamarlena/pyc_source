# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\Neko\Desktop\aperturec\aperture\__player__.py
# Compiled at: 2020-01-09 14:43:57
# Size of source mod 2**32: 88 bytes


class sounds:
    current = None


def queue(sound: str):
    sounds.current = sound