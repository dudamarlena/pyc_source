# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/daniel/Programming/python/joy2mouse/joy2mouselib/keyboard.py
# Compiled at: 2011-06-07 03:10:53
import virtkey, gtk

def keystroke_to_x11(keystroke):
    """ convert "CTRL+Shift+T" to (1<<2 | 1<<0, 28)
        :param keystroke: The keystroke string.
                         - can handle at least one 'real' key
                         - only ctrl, shift and alt supported yet (case-insensitive)
        :returns: tuple: (modifiers, keysym)
    """
    modifiers = 0
    key = ''
    splitted = keystroke.split('+')
    for stroke in splitted:
        lstroke = stroke.lower()
        if lstroke == 'ctrl' or lstroke == 'control':
            modifiers |= 4
        elif lstroke == 'shift':
            modifiers |= 1
        elif lstroke == 'alt':
            modifiers |= 8
        elif len(stroke) == 1:
            key = ord(stroke)
        else:
            key = gtk.gdk.keyval_from_name(stroke)

    return (
     modifiers, key)


class Keyboard(object):

    def __init__(self):
        self.keyboard = virtkey.virtkey()

    def press_key(self, keys):
        modifiers, key = keystroke_to_x11(keys)
        if modifiers:
            self.keyboard.lock_mod(modifiers)
        try:
            self.keyboard.press_keysym(key)
        finally:
            pass

    def release_key(self, keys):
        modifiers, key = keystroke_to_x11(keys)
        try:
            self.keyboard.release_keysym(key)
        finally:
            self.keyboard.unlock_mod(modifiers)