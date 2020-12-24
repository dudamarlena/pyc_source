# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\dev\cocos2020\samples\tetrico\colors.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 661 bytes
from __future__ import division, print_function, unicode_literals
import pyglet

class Colors(object):
    colors = [
     'black', 'orange', 'red', 'yellow', 'cyan', 'magenta', 'green', 'blue',
     'black',
     'rotate', 'scale', 'liquid', 'waves', 'twirl', 'lens',
     'black']
    BLACK, ORANGE, RED, YELLOW, CYAN, MAGENTA, GREEN, BLUE, LAST_COLOR, ROTATE, SCALE, LIQUID, WAVES, TWIRL, LENS, LAST_SPECIAL = range(len(colors))
    images = [pyglet.resource.image('block_%s.png' % color) for color in colors]
    specials = [k for k in range(LAST_COLOR + 1, LAST_SPECIAL)]