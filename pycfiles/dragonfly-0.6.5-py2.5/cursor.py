# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\dragonfly\windows\cursor.py
# Compiled at: 2009-03-12 12:12:34
"""
    This file offers an interface to the Win32 cursor control.

"""
import win32gui, ctypes
from ..log import get_log

class _point_t(ctypes.Structure):
    _fields_ = [
     (
      'x', ctypes.c_long),
     (
      'y', ctypes.c_long)]


def get_cursor_position():
    point = _point_t()
    result = ctypes.windll.user32.GetCursorPos(ctypes.pointer(point))
    if result:
        return (point.x, point.y)
    else:
        return
    return