# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/event/shortcut_action.py
# Compiled at: 2013-04-04 15:36:37
"""A special type of C{Action}s used to create keyboard shortcuts."""
import re
from muntjac.event.action import Action

class ShortcutAction(Action):
    """Shortcuts are a special type of L{Action}s used to create keyboard
    shortcuts.

    The ShortcutAction is triggered when the user presses a given key in
    combination with the (optional) given modifier keys.

    ShortcutActions can be global (by attaching to the L{Window}), or attached
    to different parts of the UI so that a specific shortcut is only valid in
    part of the UI. For instance, one can attach shortcuts to a specific
    L{Panel} - look for L{ComponentContainer}s implementing L{IHandler} or
    L{INotifier}.

    ShortcutActions have a caption that may be used to display the shortcut
    visually. This allows the ShortcutAction to be used as a plain Action while
    still reacting to a keyboard shortcut. Note that this functionality is not
    very well supported yet, but it might still be a good idea to give a caption
    to the shortcut.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    """
    SHORTHAND_CHAR_ALT = '&'
    SHORTHAND_CHAR_SHIFT = '_'
    SHORTHAND_CHAR_CTRL = '^'
    _SHORTHAND_ALT = re.escape(SHORTHAND_CHAR_ALT)
    _SHORTHAND_SHIFT = re.escape(SHORTHAND_CHAR_SHIFT)
    _SHORTHAND_CTRL = re.escape(SHORTHAND_CHAR_CTRL)
    _SHORTHAND_ESCAPE = re.compile('(' + _SHORTHAND_ALT + '?)' + _SHORTHAND_ALT + '|(' + _SHORTHAND_SHIFT + '?)' + _SHORTHAND_SHIFT + '|(' + _SHORTHAND_CTRL + '?)' + _SHORTHAND_CTRL)
    _SHORTHAND_REMOVE = re.compile('([' + _SHORTHAND_ALT + '|' + _SHORTHAND_SHIFT + '|' + _SHORTHAND_CTRL + '])\\1')
    _SHORTHANDS = re.compile('(' + _SHORTHAND_ALT + '|' + _SHORTHAND_SHIFT + '|' + _SHORTHAND_CTRL + ')(?!\\1)(?:(' + _SHORTHAND_ALT + '|' + _SHORTHAND_SHIFT + '|' + _SHORTHAND_CTRL + ')(?!\\1|\\2))?(?:(' + _SHORTHAND_ALT + '|' + _SHORTHAND_SHIFT + '|' + _SHORTHAND_CTRL + ')(?!\\1|\\2|\\3))?.')

    def __init__(self, *args):
        """Creates a shortcut either using a shorthand notation to encode the
        keycode a in the caption or one that reacts to the given L{KeyCode} and
        (optionally) L{ModifierKey}s.

        The shortcut might be shown in the UI (e.g context menu), in which case
        the caption will be used.

        Insert one or more modifier characters before the character to use as
        keycode. E.g C{"&Save"} will make a shortcut responding to
        ALT-S, C{"E^xit"} will respond to CTRL-X.<br/>
        Multiple modifiers can be used, e.g C{"&^Delete"} will respond
        to CTRL-ALT-D (the order of the modifier characters is not important).

        The modifier characters will be removed from the caption. The modifier
        character is be escaped by itself: two consecutive characters are turned
        into the original character w/o the special meaning. E.g
        C{"Save&&&close"} will respond to ALT-C, and the caption will
        say "Save&close".

        @param args: tuple of the form
            - (caption, kc, m)
              1. used when displaying the shortcut visually
              2. KeyCode that the shortcut reacts to
              3. optional modifier keys
            - (caption, icon, kc, m)
              1. used when displaying the shortcut visually
              2. used when displaying the shortcut visually
              3. KeyCode that the shortcut reacts to
              4. optional modifier keys
            - (shorthandCaption)
              1. the caption in modifier shorthand
            - (shorthandCaption, modifierKeys)
              1. the caption in modifier shorthand
              2. modifier keys
        """
        self._keyCode = None
        self._modifiers = tuple()
        args = args
        nargs = len(args)
        if nargs == 1:
            shorthandCaption, = args
            ShortcutAction.__init__(self, shorthandCaption, None)
        elif nargs == 2:
            shorthandCaption, modifierKeys = args
            super(ShortcutAction, self).__init__(self._SHORTHAND_ESCAPE.sub(shorthandCaption, '$1$2$3'))
            shorthandCaption = self._SHORTHAND_REMOVE.sub(shorthandCaption, '\\u001A')
            m = self._SHORTHANDS.search(shorthandCaption)
            if m is not None:
                match = m.group()
                self._keyCode = m.group()[(len(match) - 1)].upper()
                if modifierKeys is not None:
                    self._modifiers = modifierKeys
                else:
                    mod = [
                     None] * (len(match) - 1)
                    for i in range(len(mod)):
                        kc = match[i]
                        if kc == self.SHORTHAND_CHAR_ALT:
                            mod[i] = self.ModifierKey.ALT
                        elif kc == self.SHORTHAND_CHAR_CTRL:
                            mod[i] = self.ModifierKey.CTRL
                        elif kc == self.SHORTHAND_CHAR_SHIFT:
                            mod[i] = self.ModifierKey.SHIFT

                    self._modifiers = mod
            else:
                self._keyCode = -1
                self._modifiers = modifierKeys
        elif nargs == 3:
            caption, kc, m = args
            super(ShortcutAction, self).__init__(caption)
            self._keyCode = kc
            self._modifiers = m
        elif nargs == 4:
            caption, icon, kc, m = args
            super(ShortcutAction, self).__init__(caption, icon)
            self._keyCode = kc
            self._modifiers = m
        else:
            raise ValueError, 'invalid number of arguments'
        return

    def getKeyCode(self):
        """Get the L{KeyCode} that this shortcut reacts to (in
        combination with the L{ModifierKey}s).

        @return: keycode for this shortcut
        """
        return self._keyCode

    def getModifiers(self):
        """Get the L{ModifierKey}s required for the shortcut to react.

        @return: modifier keys for this shortcut
        """
        return self._modifiers


class KeyCode(object):
    """Key codes that can be used for shortcuts"""
    ENTER = 13
    ESCAPE = 27
    PAGE_UP = 33
    PAGE_DOWN = 34
    TAB = 9
    ARROW_LEFT = 37
    ARROW_UP = 38
    ARROW_RIGHT = 39
    ARROW_DOWN = 40
    BACKSPACE = 8
    DELETE = 46
    INSERT = 45
    END = 35
    HOME = 36
    F1 = 112
    F2 = 113
    F3 = 114
    F4 = 115
    F5 = 116
    F6 = 117
    F7 = 118
    F8 = 119
    F9 = 120
    F10 = 121
    F11 = 122
    F12 = 123
    A = 65
    B = 66
    C = 67
    D = 68
    E = 69
    F = 70
    G = 71
    H = 72
    I = 73
    J = 74
    K = 75
    L = 76
    M = 77
    N = 78
    O = 79
    P = 80
    Q = 81
    R = 82
    S = 83
    T = 84
    U = 85
    V = 86
    W = 87
    X = 88
    Y = 89
    Z = 90
    NUM0 = 48
    NUM1 = 49
    NUM2 = 50
    NUM3 = 51
    NUM4 = 52
    NUM5 = 53
    NUM6 = 54
    NUM7 = 55
    NUM8 = 56
    NUM9 = 57
    SPACEBAR = 32


class ModifierKey(object):
    """Modifier key constants"""
    SHIFT = 16
    CTRL = 17
    ALT = 18
    META = 91