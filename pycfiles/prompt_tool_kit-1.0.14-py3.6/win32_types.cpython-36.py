# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/prompt_tool_kit/win32_types.py
# Compiled at: 2019-08-15 23:29:33
# Size of source mod 2**32: 4046 bytes
from ctypes import Union, Structure, c_char, c_short, c_long, c_ulong
from ctypes.wintypes import DWORD, BOOL, LPVOID, WORD, WCHAR
STD_INPUT_HANDLE = c_ulong(-10)
STD_OUTPUT_HANDLE = c_ulong(-11)
STD_ERROR_HANDLE = c_ulong(-12)

class COORD(Structure):
    __doc__ = '\n    Struct in wincon.h\n    http://msdn.microsoft.com/en-us/library/windows/desktop/ms682119(v=vs.85).aspx\n    '
    _fields_ = [
     (
      'X', c_short),
     (
      'Y', c_short)]

    def __repr__(self):
        return '%s(X=%r, Y=%r, type_x=%r, type_y=%r)' % (
         self.__class__.__name__, self.X, self.Y, type(self.X), type(self.Y))


class UNICODE_OR_ASCII(Union):
    _fields_ = [
     (
      'AsciiChar', c_char),
     (
      'UnicodeChar', WCHAR)]


class KEY_EVENT_RECORD(Structure):
    __doc__ = '\n    http://msdn.microsoft.com/en-us/library/windows/desktop/ms684166(v=vs.85).aspx\n    '
    _fields_ = [
     (
      'KeyDown', c_long),
     (
      'RepeatCount', c_short),
     (
      'VirtualKeyCode', c_short),
     (
      'VirtualScanCode', c_short),
     (
      'uChar', UNICODE_OR_ASCII),
     (
      'ControlKeyState', c_long)]


class MOUSE_EVENT_RECORD(Structure):
    __doc__ = '\n    http://msdn.microsoft.com/en-us/library/windows/desktop/ms684239(v=vs.85).aspx\n    '
    _fields_ = [
     (
      'MousePosition', COORD),
     (
      'ButtonState', c_long),
     (
      'ControlKeyState', c_long),
     (
      'EventFlags', c_long)]


class WINDOW_BUFFER_SIZE_RECORD(Structure):
    __doc__ = '\n    http://msdn.microsoft.com/en-us/library/windows/desktop/ms687093(v=vs.85).aspx\n    '
    _fields_ = [
     (
      'Size', COORD)]


class MENU_EVENT_RECORD(Structure):
    __doc__ = '\n    http://msdn.microsoft.com/en-us/library/windows/desktop/ms684213(v=vs.85).aspx\n    '
    _fields_ = [
     (
      'CommandId', c_long)]


class FOCUS_EVENT_RECORD(Structure):
    __doc__ = '\n    http://msdn.microsoft.com/en-us/library/windows/desktop/ms683149(v=vs.85).aspx\n    '
    _fields_ = [
     (
      'SetFocus', c_long)]


class EVENT_RECORD(Union):
    _fields_ = [
     (
      'KeyEvent', KEY_EVENT_RECORD),
     (
      'MouseEvent', MOUSE_EVENT_RECORD),
     (
      'WindowBufferSizeEvent', WINDOW_BUFFER_SIZE_RECORD),
     (
      'MenuEvent', MENU_EVENT_RECORD),
     (
      'FocusEvent', FOCUS_EVENT_RECORD)]


class INPUT_RECORD(Structure):
    __doc__ = '\n    http://msdn.microsoft.com/en-us/library/windows/desktop/ms683499(v=vs.85).aspx\n    '
    _fields_ = [
     (
      'EventType', c_short),
     (
      'Event', EVENT_RECORD)]


EventTypes = {1:'KeyEvent', 
 2:'MouseEvent', 
 4:'WindowBufferSizeEvent', 
 8:'MenuEvent', 
 16:'FocusEvent'}

class SMALL_RECT(Structure):
    __doc__ = 'struct in wincon.h.'
    _fields_ = [
     (
      'Left', c_short),
     (
      'Top', c_short),
     (
      'Right', c_short),
     (
      'Bottom', c_short)]


class CONSOLE_SCREEN_BUFFER_INFO(Structure):
    __doc__ = 'struct in wincon.h.'
    _fields_ = [
     (
      'dwSize', COORD),
     (
      'dwCursorPosition', COORD),
     (
      'wAttributes', WORD),
     (
      'srWindow', SMALL_RECT),
     (
      'dwMaximumWindowSize', COORD)]

    def __str__(self):
        return '(%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d)' % (
         self.dwSize.Y, self.dwSize.X,
         self.dwCursorPosition.Y, self.dwCursorPosition.X,
         self.wAttributes,
         self.srWindow.Top, self.srWindow.Left, self.srWindow.Bottom, self.srWindow.Right,
         self.dwMaximumWindowSize.Y, self.dwMaximumWindowSize.X)


class SECURITY_ATTRIBUTES(Structure):
    __doc__ = '\n    http://msdn.microsoft.com/en-us/library/windows/desktop/aa379560(v=vs.85).aspx\n    '
    _fields_ = [
     (
      'nLength', DWORD),
     (
      'lpSecurityDescriptor', LPVOID),
     (
      'bInheritHandle', BOOL)]