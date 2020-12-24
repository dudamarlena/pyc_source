# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/prompt_tool_kit/terminal/win32_input.py
# Compiled at: 2019-08-15 23:53:39
# Size of source mod 2**32: 13056 bytes
from __future__ import unicode_literals
from ctypes import windll, pointer
from ctypes.wintypes import DWORD
from six.moves import range
from prompt_tool_kit.key_binding.input_processor import KeyPress
from prompt_tool_kit.keys import Keys
from prompt_tool_kit.mouse_events import MouseEventType
from prompt_tool_kit.win32_types import EventTypes, KEY_EVENT_RECORD, MOUSE_EVENT_RECORD, INPUT_RECORD, STD_INPUT_HANDLE
import msvcrt, os, sys, six
__all__ = ('ConsoleInputReader', 'raw_mode', 'cooked_mode')

class ConsoleInputReader(object):
    """ConsoleInputReader"""
    mappings = {'\x1b':Keys.Escape, 
     '\x00':Keys.ControlSpace, 
     '\x01':Keys.ControlA, 
     '\x02':Keys.ControlB, 
     '\x03':Keys.ControlC, 
     '\x04':Keys.ControlD, 
     '\x05':Keys.ControlE, 
     '\x06':Keys.ControlF, 
     '\x07':Keys.ControlG, 
     '\x08':Keys.ControlH, 
     '\t':Keys.ControlI, 
     '\n':Keys.ControlJ, 
     '\x0b':Keys.ControlK, 
     '\x0c':Keys.ControlL, 
     '\r':Keys.ControlJ, 
     '\x0e':Keys.ControlN, 
     '\x0f':Keys.ControlO, 
     '\x10':Keys.ControlP, 
     '\x11':Keys.ControlQ, 
     '\x12':Keys.ControlR, 
     '\x13':Keys.ControlS, 
     '\x14':Keys.ControlT, 
     '\x15':Keys.ControlU, 
     '\x16':Keys.ControlV, 
     '\x17':Keys.ControlW, 
     '\x18':Keys.ControlX, 
     '\x19':Keys.ControlY, 
     '\x1a':Keys.ControlZ, 
     '\x1c':Keys.ControlBackslash, 
     '\x1d':Keys.ControlSquareClose, 
     '\x1e':Keys.ControlCircumflex, 
     '\x1f':Keys.ControlUnderscore, 
     '\x7f':Keys.Backspace}
    keycodes = {33:Keys.PageUp, 
     34:Keys.PageDown, 
     35:Keys.End, 
     36:Keys.Home, 
     37:Keys.Left, 
     38:Keys.Up, 
     39:Keys.Right, 
     40:Keys.Down, 
     45:Keys.Insert, 
     46:Keys.Delete, 
     112:Keys.F1, 
     113:Keys.F2, 
     114:Keys.F3, 
     115:Keys.F4, 
     116:Keys.F5, 
     117:Keys.F6, 
     118:Keys.F7, 
     119:Keys.F8, 
     120:Keys.F9, 
     121:Keys.F10, 
     122:Keys.F11, 
     123:Keys.F12}
    LEFT_ALT_PRESSED = 2
    RIGHT_ALT_PRESSED = 1
    SHIFT_PRESSED = 16
    LEFT_CTRL_PRESSED = 8
    RIGHT_CTRL_PRESSED = 4

    def __init__(self, recognize_paste=True):
        self._fdcon = None
        self.recognize_paste = recognize_paste
        if sys.stdin.isatty():
            self.handle = windll.kernel32.GetStdHandle(STD_INPUT_HANDLE)
        else:
            self._fdcon = os.open('CONIN$', os.O_RDWR | os.O_BINARY)
            self.handle = msvcrt.get_osfhandle(self._fdcon)

    def close(self):
        """ Close fdcon. """
        if self._fdcon is not None:
            os.close(self._fdcon)

    def read(self):
        """
        Return a list of `KeyPress` instances. It won't return anything when
        there was nothing to read.  (This function doesn't block.)

        http://msdn.microsoft.com/en-us/library/windows/desktop/ms684961(v=vs.85).aspx
        """
        max_count = 2048
        read = DWORD(0)
        arrtype = INPUT_RECORD * max_count
        input_records = arrtype()
        windll.kernel32.ReadConsoleInputW(self.handle, pointer(input_records), max_count, pointer(read))
        all_keys = list(self._get_keys(read, input_records))
        if self.recognize_paste:
            if self._is_paste(all_keys):
                gen = iter(all_keys)
                for k in gen:
                    data = []
                    while k and (isinstance(k.key, six.text_type) or k.key == Keys.ControlJ):
                        data.append(k.data)
                        try:
                            k = next(gen)
                        except StopIteration:
                            k = None

                    if data:
                        yield KeyPress(Keys.BracketedPaste, ''.join(data))
                    if k is not None:
                        yield k

        else:
            for k in all_keys:
                yield k

    def _get_keys(self, read, input_records):
        """
        Generator that yields `KeyPress` objects from the input records.
        """
        for i in range(read.value):
            ir = input_records[i]
            if ir.EventType in EventTypes:
                ev = getattr(ir.Event, EventTypes[ir.EventType])
                if type(ev) == KEY_EVENT_RECORD:
                    if ev.KeyDown:
                        for key_press in self._event_to_key_presses(ev):
                            yield key_press

                if type(ev) == MOUSE_EVENT_RECORD:
                    for key_press in self._handle_mouse(ev):
                        yield key_press

    @staticmethod
    def _is_paste(keys):
        """
        Return `True` when we should consider this list of keys as a paste
        event. Pasted text on windows will be turned into a
        `Keys.BracketedPaste` event. (It's not 100% correct, but it is probably
        the best possible way to detect pasting of text and handle that
        correctly.)
        """
        text_count = 0
        newline_count = 0
        for k in keys:
            if isinstance(k.key, six.text_type):
                text_count += 1
            if k.key == Keys.ControlJ:
                newline_count += 1

        return newline_count >= 1 and text_count > 1

    def _event_to_key_presses(self, ev):
        """
        For this `KEY_EVENT_RECORD`, return a list of `KeyPress` instances.
        """
        if not (type(ev) == KEY_EVENT_RECORD and ev.KeyDown):
            raise AssertionError
        else:
            result = None
            u_char = ev.uChar.UnicodeChar
            ascii_char = u_char.encode('utf-8')
            if u_char == '\x00':
                if ev.VirtualKeyCode in self.keycodes:
                    result = KeyPress(self.keycodes[ev.VirtualKeyCode], '')
            else:
                if ascii_char in self.mappings:
                    if self.mappings[ascii_char] == Keys.ControlJ:
                        u_char = '\n'
                    result = KeyPress(self.mappings[ascii_char], u_char)
                else:
                    result = KeyPress(u_char, u_char)
            if ev.ControlKeyState & self.LEFT_CTRL_PRESSED or ev.ControlKeyState & self.RIGHT_CTRL_PRESSED:
                if result:
                    if result.key == Keys.Left:
                        result.key = Keys.ControlLeft
                    else:
                        if result.key == Keys.Right:
                            result.key = Keys.ControlRight
                        if result.key == Keys.Up:
                            result.key = Keys.ControlUp
                    if result.key == Keys.Down:
                        result.key = Keys.ControlDown
            if ev.ControlKeyState & self.SHIFT_PRESSED:
                if result:
                    if result.key == Keys.Tab:
                        result.key = Keys.BackTab
            if ev.ControlKeyState & self.LEFT_CTRL_PRESSED or ev.ControlKeyState & self.RIGHT_CTRL_PRESSED:
                if result:
                    if result.data == ' ':
                        result = KeyPress(Keys.ControlSpace, ' ')
            if ev.ControlKeyState & self.LEFT_CTRL_PRESSED or ev.ControlKeyState & self.RIGHT_CTRL_PRESSED:
                if result:
                    if result.key == Keys.ControlJ:
                        return [KeyPress(Keys.Escape, ''), result]
            if result:
                meta_pressed = ev.ControlKeyState & self.LEFT_ALT_PRESSED
                if meta_pressed:
                    return [KeyPress(Keys.Escape, ''), result]
                else:
                    return [
                     result]
            else:
                return []

    def _handle_mouse(self, ev):
        """
        Handle mouse events. Return a list of KeyPress instances.
        """
        FROM_LEFT_1ST_BUTTON_PRESSED = 1
        result = []
        if ev.ButtonState == FROM_LEFT_1ST_BUTTON_PRESSED:
            for event_type in [MouseEventType.MOUSE_DOWN, MouseEventType.MOUSE_UP]:
                data = ';'.join([
                 event_type,
                 str(ev.MousePosition.X),
                 str(ev.MousePosition.Y)])
                result.append(KeyPress(Keys.WindowsMouseEvent, data))

        return result


class raw_mode(object):
    """raw_mode"""

    def __init__(self, fileno=None):
        self.handle = windll.kernel32.GetStdHandle(STD_INPUT_HANDLE)

    def __enter__(self):
        original_mode = DWORD()
        windll.kernel32.GetConsoleMode(self.handle, pointer(original_mode))
        self.original_mode = original_mode
        self._patch()

    def _patch(self):
        ENABLE_ECHO_INPUT = 4
        ENABLE_LINE_INPUT = 2
        ENABLE_PROCESSED_INPUT = 1
        windll.kernel32.SetConsoleMode(self.handle, self.original_mode.value & ~(ENABLE_ECHO_INPUT | ENABLE_LINE_INPUT | ENABLE_PROCESSED_INPUT))

    def __exit__(self, *a, **kw):
        windll.kernel32.SetConsoleMode(self.handle, self.original_mode)


class cooked_mode(raw_mode):
    """cooked_mode"""

    def _patch(self):
        ENABLE_ECHO_INPUT = 4
        ENABLE_LINE_INPUT = 2
        ENABLE_PROCESSED_INPUT = 1
        windll.kernel32.SetConsoleMode(self.handle, self.original_mode.value | (ENABLE_ECHO_INPUT | ENABLE_LINE_INPUT | ENABLE_PROCESSED_INPUT))