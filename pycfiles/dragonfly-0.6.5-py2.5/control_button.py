# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\dragonfly\windows\control_button.py
# Compiled at: 2009-01-27 11:15:43
"""
This file implements a standard Win32 button control.

"""
import win32con
from dragonfly.windows.control_base import ControlBase

class Button(ControlBase):

    def __init__(self, parent, text, size, default=False, **kwargs):
        flavor = 128
        style = win32con.BS_PUSHBUTTON | win32con.BS_TEXT | win32con.WS_CHILD | win32con.WS_TABSTOP | win32con.WS_OVERLAPPED | win32con.WS_VISIBLE
        if default:
            style |= win32con.BS_DEFPUSHBUTTON
        else:
            style |= win32con.BS_PUSHBUTTON
        ControlBase.__init__(self, parent, flavor, text, size, style, **kwargs)