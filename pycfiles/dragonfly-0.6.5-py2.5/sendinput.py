# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\dragonfly\actions\sendinput.py
# Compiled at: 2009-03-17 08:27:56
"""
    This file implements an interface to the Win32 SendInput function
    for simulating keyboard and mouse events.
"""
from ctypes import *
import win32con, win32api

class KeyboardInput(Structure):
    _fields_ = [
     (
      'wVk', c_ushort),
     (
      'wScan', c_ushort),
     (
      'dwFlags', c_ulong),
     (
      'time', c_ulong),
     (
      'dwExtraInfo', POINTER(c_ulong))]
    extended_keys = (
     win32con.VK_UP,
     win32con.VK_DOWN,
     win32con.VK_LEFT,
     win32con.VK_RIGHT,
     win32con.VK_HOME,
     win32con.VK_END,
     win32con.VK_PRIOR,
     win32con.VK_NEXT,
     win32con.VK_INSERT,
     win32con.VK_LWIN)

    def __init__(self, virtual_keycode, down):
        scancode = windll.user32.MapVirtualKeyA(virtual_keycode, 0)
        flags = 0
        if not down:
            flags |= win32con.KEYEVENTF_KEYUP
        if virtual_keycode in self.extended_keys:
            flags |= win32con.KEYEVENTF_EXTENDEDKEY
        extra = pointer(c_ulong(0))
        Structure.__init__(self, virtual_keycode, scancode, flags, 0, extra)


class HardwareInput(Structure):
    _fields_ = [
     (
      'uMsg', c_ulong),
     (
      'wParamL', c_short),
     (
      'wParamH', c_ushort)]


class MouseInput(Structure):
    _fields_ = [
     (
      'dx', c_long),
     (
      'dy', c_long),
     (
      'mouseData', c_ulong),
     (
      'dwFlags', c_ulong),
     (
      'time', c_ulong),
     (
      'dwExtraInfo', POINTER(c_ulong))]


class _InputUnion(Union):
    _fields_ = [
     (
      'ki', KeyboardInput),
     (
      'mi', MouseInput),
     (
      'hi', HardwareInput)]


class _Input(Structure):
    _fields_ = [
     (
      'type', c_ulong),
     (
      'ii', _InputUnion)]

    def __init__(self, element):
        if isinstance(element, KeyboardInput):
            element_type = win32con.INPUT_KEYBOARD
            union = _InputUnion(ki=element)
        elif isinstance(element, MouseInput):
            element_type = win32con.INPUT_MOUSE
            union = _InputUnion(mi=element)
        elif isinstance(element, HardwareInput):
            element_type = win32con.INPUT_HARDWARE
            union = _InputUnion(hi=element)
        else:
            raise TypeError('Unknown input type: %r' % element)
        Structure.__init__(self, type=element_type, ii=union)


def make_input_array(inputs):
    arguments = [ (i,) for i in inputs ]
    InputArray = _Input * len(inputs)
    return InputArray(*arguments)


def send_input_array(input_array):
    length = len(input_array)
    assert length >= 0
    size = sizeof(input_array[0])
    ptr = pointer(input_array)
    count_inserted = windll.user32.SendInput(length, ptr, size)
    if count_inserted != length:
        last_error = win32api.GetLastError()
        message = win32api.FormatMessage(last_error)
        raise ValueError('windll.user32.SendInput(): %s' % message)