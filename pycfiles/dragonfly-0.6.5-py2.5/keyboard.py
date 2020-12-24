# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\dragonfly\actions\keyboard.py
# Compiled at: 2009-02-02 02:43:30
"""
This file implements a Win32 keyboard interface using sendinput.

"""
import time, win32con
from ctypes import windll, c_char, c_wchar
from dragonfly.actions.sendinput import KeyboardInput, make_input_array, send_input_array

class Typeable(object):
    __slots__ = ('_code', '_modifiers', '_name')

    def __init__(self, code, modifiers=(), name=None):
        self._code = code
        self._modifiers = modifiers
        self._name = name

    def __str__(self):
        return '%s(%s)' % (self.__class__.__name__, self._name) + repr(self.events())

    def on_events(self, timeout=0):
        events = [ (m, True, 0) for m in self._modifiers ]
        events.append((self._code, True, timeout))
        return events

    def off_events(self, timeout=0):
        events = [ (m, False, 0) for m in self._modifiers ]
        events.append((self._code, False, timeout))
        events.reverse()
        return events

    def events(self, timeout=0):
        events = [(self._code, True, 0), (self._code, False, timeout)]
        for m in self._modifiers[-1::-1]:
            events.insert(0, (m, True, 0))
            events.append((m, False, 0))

        return events


class Keyboard(object):
    shift_code = win32con.VK_SHIFT
    ctrl_code = win32con.VK_CONTROL
    alt_code = win32con.VK_MENU

    @classmethod
    def send_keyboard_events(cls, events):
        """
            Send a sequence of keyboard events.

            Positional arguments:
            events -- a sequence of 3-tuples of the form
                (keycode, down, timeout), where
                keycode (int): virtual key code.
                down (boolean): True means the key will be pressed down,
                    False means the key will be released.
                timeout (int): number of seconds to sleep after
                    the keyboard event.

        """
        items = []
        for (keycode, down, timeout) in events:
            input = KeyboardInput(keycode, down)
            items.append(input)
            if timeout:
                array = make_input_array(items)
                items = []
                send_input_array(array)
                time.sleep(timeout)

        if items:
            array = make_input_array(items)
            send_input_array(array)
            if timeout:
                time.sleep(timeout)

    @classmethod
    def xget_virtual_keycode(cls, char):
        if isinstance(char, str):
            code = windll.user32.VkKeyScanA(c_char(char))
        else:
            code = windll.user32.VkKeyScanW(c_wchar(char))
        if code == -1:
            raise ValueError('Unknown char: %r' % char)
        codes = [
         code & 255]
        if code & 256:
            codes.append(cls.shift_code)
        elif code & 512:
            codes.append(cls.ctrl_code)
        elif code & 1024:
            codes.append(cls.alt_code)
        return codes

    @classmethod
    def get_keycode_and_modifiers(cls, char):
        if isinstance(char, str):
            code = windll.user32.VkKeyScanA(c_char(char))
        else:
            code = windll.user32.VkKeyScanW(c_wchar(char))
        if code == -1:
            raise ValueError('Unknown char: %r' % char)
        modifiers = []
        if code & 256:
            modifiers.append(cls.shift_code)
        elif code & 512:
            modifiers.append(cls.ctrl_code)
        elif code & 1024:
            modifiers.append(cls.alt_code)
        code &= 255
        return (code, modifiers)

    @classmethod
    def get_typeable(cls, char):
        (code, modifiers) = cls.get_keycode_and_modifiers(char)
        return Typeable(code, modifiers)


keyboard = Keyboard()