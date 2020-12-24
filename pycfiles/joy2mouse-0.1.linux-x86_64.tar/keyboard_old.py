# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/joy2mouselib/keyboard_old.py
# Compiled at: 2011-06-02 03:00:57
import Xlib.display, Xlib.X, Xlib.XK, Xlib.protocol.event
special_X_keysyms = {' ': 'space', 
   '\t': 'Tab', 
   '\n': 'Return', 
   '\r': 'Return', 
   '\\e': 'Escape', 
   '!': 'exclam', 
   '#': 'numbersign', 
   '%': 'percent', 
   '$': 'dollar', 
   '&': 'ampersand', 
   '"': 'quotedbl', 
   "'": 'apostrophe', 
   '(': 'parenleft', 
   ')': 'parenright', 
   '*': 'asterisk', 
   '=': 'equal', 
   '+': 'plus', 
   ',': 'comma', 
   '-': 'minus', 
   '.': 'period', 
   '/': 'slash', 
   ':': 'colon', 
   ';': 'semicolon', 
   '<': 'less', 
   '>': 'greater', 
   '?': 'question', 
   '@': 'at', 
   '[': 'bracketleft', 
   ']': 'bracketright', 
   '\\': 'backslash', 
   '^': 'asciicircum', 
   '_': 'underscore', 
   '`': 'grave', 
   '{': 'braceleft', 
   '|': 'bar', 
   '}': 'braceright', 
   '~': 'asciitilde'}

def get_keysym(ch):
    keysym = Xlib.XK.string_to_keysym(ch)
    if keysym == 0:
        keysym = Xlib.XK.string_to_keysym(special_X_keysyms[ch])
    return keysym


def is_shifted(ch):
    if ch.isupper():
        return True
    if ('~!@#$%^&*()_+{}|:"<>?').find(ch) >= 0:
        return True
    return False


def char_to_keycode(ch, display):
    keysym = get_keysym(ch)
    keycode = display.keysym_to_keycode(keysym)
    if keycode == 0:
        print "Sorry, can't map", ch
    if is_shifted(ch):
        shift_mask = Xlib.X.ShiftMask
    else:
        shift_mask = 0
    return (keycode, shift_mask)


class Keyboard(object):

    def __init__(self):
        self.display = Xlib.display.Display()

    def press_key(self, key):
        keycode, shift_mask = char_to_keycode(key, self.display)
        if shift_mask != 0:
            Xlib.ext.xtest.fake_input(self.display, Xlib.X.KeyPress, 50)
        Xlib.ext.xtest.fake_input(self.display, Xlib.X.KeyPress, keycode)

    def release_key(self, key):
        keycode, shift_mask = char_to_keycode(key, self.display)
        Xlib.ext.xtest.fake_input(self.display, Xlib.X.KeyRelease, keycode)
        if shift_mask != 0:
            Xlib.ext.xtest.fake_input(self.display, Xlib.X.KeyRelease, 50)