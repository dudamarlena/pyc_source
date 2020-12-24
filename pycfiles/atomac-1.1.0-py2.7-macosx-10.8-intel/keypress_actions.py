# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-intel/egg/atomac/ldtpd/keypress_actions.py
# Compiled at: 2013-02-13 13:37:18
"""KeyboardOp class."""
import time
from atomac.AXKeyCodeConstants import *
from server_exception import LdtpServerException

class KeyCombo:

    def __init__(self):
        self.modifiers = False
        self.value = ''
        self.modVal = None
        return


class KeyboardOp:

    def __init__(self):
        self._undefined_key = None
        self._max_tokens = 256
        self._max_tok_size = 15
        return

    def _get_key_value(self, keyval):
        return_val = KeyCombo()
        if keyval == 'command':
            keyval = 'command_l'
        else:
            if keyval == 'option':
                keyval = 'option_l'
            else:
                if keyval == 'control':
                    keyval = 'control_l'
                else:
                    if keyval == 'shift':
                        keyval = 'shift_l'
                    elif keyval == 'left':
                        keyval = 'cursor_left'
                    elif keyval == 'right':
                        keyval = 'cursor_right'
                    elif keyval == 'up':
                        keyval = 'cursor_up'
                    elif keyval == 'down':
                        keyval = 'cursor_down'
                    elif keyval == 'bksp':
                        keyval = 'backspace'
                    elif keyval == 'enter':
                        keyval = 'return'
                    elif keyval == 'pgdown':
                        keyval = 'page_down'
                    elif keyval == 'pagedown':
                        keyval = 'page_down'
                    elif keyval == 'pgup':
                        keyval = 'page_up'
                    elif keyval == 'pageup':
                        keyval = 'page_up'
                    key = '<%s>' % keyval
                    if key in ('<command_l>', '<command_r>', '<shift_l>', '<shift_r>',
                               '<control_l>', '<control_r>', '<option_l>', '<option_r>'):
                        return_val.modifiers = True
                        return_val.modVal = [key]
                        return return_val
                if keyval.lower() in US_keyboard:
                    return_val.value = keyval
                    return return_val
            if key in specialKeys:
                return_val.value = key
                return return_val
        return return_val

    def get_keyval_id(self, input_str):
        index = 0
        key_vals = []
        lastModifiers = None
        while index < len(input_str):
            token = ''
            if input_str[index] == '<':
                index += 1
                i = 0
                while input_str[index] != '>' and i < self._max_tok_size:
                    token += input_str[index]
                    index += 1
                    i += 1

                if input_str[index] != '>':
                    return
                index += 1
            else:
                token = input_str[index]
                index += 1
            key_val = self._get_key_value(token)
            if lastModifiers and key_val.value != self._undefined_key:
                last_item = key_vals.pop()
                last_item.value = key_val.value
                key_val = last_item
                lastModifiers = None
            elif key_val.modifiers:
                if not lastModifiers:
                    lastModifiers = key_val
                else:
                    last_item = key_vals.pop()
                    last_item.modVal.extend(key_val.modVal)
                    key_val = last_item
            elif key_val.value == self._undefined_key:
                return
            key_vals.append(key_val)

        return key_vals


class KeyComboAction:

    def __init__(self, window, data):
        self._data = data
        self._window = window
        _keyOp = KeyboardOp()
        self._keyvalId = _keyOp.get_keyval_id(data)
        if not self._keyvalId:
            raise LdtpServerException('Unsupported keys passed')
        self._doCombo()

    def _doCombo(self):
        for key_val in self._keyvalId:
            if key_val.modifiers:
                self._window.sendKeyWithModifiers(key_val.value, key_val.modVal)
            else:
                self._window.sendKey(key_val.value)
            time.sleep(0.01)


class KeyPressAction:

    def __init__(self, window, data):
        self._data = data
        self._window = window
        _keyOp = KeyboardOp()
        self._keyvalId = _keyOp.get_keyval_id(data)
        if not self._keyvalId:
            raise LdtpServerException('Unsupported keys passed')
        self._doPress()

    def _doPress(self):
        for key_val in self._keyvalId:
            if key_val.modifiers:
                self._window.sendKeyWithModifiers(key_val.value, key_val.modVal)
            else:
                raise LdtpServerException('Unsupported modifiers')
            time.sleep(0.01)


class KeyReleaseAction:

    def __init__(self, window, data):
        self._data = data
        self._window = window
        _keyOp = KeyboardOp()
        self._keyvalId = _keyOp.get_keyval_id(data)
        if not self._keyvalId:
            raise LdtpServerException('Unsupported keys passed')
        self._doRelease()

    def _doRelease(self):
        for key_val in self._keyvalId:
            if key_val.modifiers:
                self._window.sendKeyWithModifiers(key_val.value, key_val.modVal)
            else:
                raise LdtpServerException('Unsupported modifiers')
            time.sleep(0.01)