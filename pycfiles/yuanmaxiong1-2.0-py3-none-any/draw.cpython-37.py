# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\Users\asus\Desktop\PythonGameEngine\Walimaker\draw.py
# Compiled at: 2019-08-08 06:55:20
# Size of source mod 2**32: 174 bytes
from .config import *

def draw_line(p1, p2, color, width):
    p1 = Cartesian2pygame(p1)
    p2 = Cartesian2pygame(p2)
    global_var.LINES.append((p1, p2, color, width))