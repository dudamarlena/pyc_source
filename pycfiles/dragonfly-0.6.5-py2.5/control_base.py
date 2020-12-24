# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\dragonfly\windows\control_base.py
# Compiled at: 2009-01-19 04:06:55
"""
This file implements a Win32 control base class.
"""
import sys, ctypes, struct, winxpgui as win32gui, win32api, win32con, os

class ControlBase(object):
    _next_id = 1024

    @classmethod
    def _get_next_id(cls):
        ControlBase._next_id += 1
        return ControlBase._next_id - 1

    _message_names = {'on_command': win32con.WM_COMMAND}

    def __init__(self, parent, flavor, text, size, style, **kwargs):
        self._parent = parent
        self._flavor = flavor
        self._text = text
        self._size = size
        self._style = style
        self._message_callbacks = {}
        for (name, callback) in kwargs.items():
            message = self._message_names[name]
            self._message_callbacks[message] = callback

        self._id = self._get_next_id()
        self._handle = None
        self._parent.add_control(self)
        return

    def _get_handle(self):
        if self._handle is not None:
            return self._handle
        self._handle = win32gui.GetDlgItem(self._parent.hwnd, self.id)
        return self._handle

    handle = property(lambda self: self._get_handle())

    def _get_text(self):
        return win32gui.GetWindowText(self.handle)

    def _set_text(self, text):
        return win32gui.SetWindowText(self.handle, text)

    text = property(fget=lambda self: self._get_text(), fset=lambda self, text: self._set_text(text))
    id = property(lambda self: self._id)
    message_callbacks = property(lambda self: self._message_callbacks)

    def calculate_size(self, width, height):
        return self._size(width, height)

    def template_entry(self, width, height):
        entry = [
         self._flavor, self._text, self._id,
         self.calculate_size(width, height), self._style]
        return entry

    def enable(self):
        style = win32gui.GetWindowLong(self.handle, win32con.GWL_STYLE)
        style &= ~win32con.WS_DISABLED
        win32gui.SetWindowLong(self.handle, win32con.GWL_STYLE, style)
        win32gui.SendMessage(self.handle, win32con.WM_ENABLE, 1, 0)

    def disable(self):
        style = win32gui.GetWindowLong(self.handle, win32con.GWL_STYLE)
        style |= win32con.WS_DISABLED
        win32gui.SetWindowLong(self.handle, win32con.GWL_STYLE, style)
        win32gui.SendMessage(self.handle, win32con.WM_ENABLE, 0, 0)