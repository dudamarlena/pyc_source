# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\研发资料\瓦力课程\试听课\代码\dianyi\music.py
# Compiled at: 2019-08-07 06:36:56
# Size of source mod 2**32: 181 bytes
from .config import *

def bgmusic(bgm):
    pygame.mixer.music.load(bgm)
    pygame.mixer.music.play(loops=(-1))


def set_volume(vol):
    pygame.mixer.music.set_volume(vol)