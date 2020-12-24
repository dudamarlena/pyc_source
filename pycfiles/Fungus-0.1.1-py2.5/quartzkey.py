# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyglet/window/carbon/quartzkey.py
# Compiled at: 2009-02-07 06:48:50
"""
"""
__docformat__ = 'restructuredtext'
__version__ = ''
from pyglet.window import key
QZ_ESCAPE = 53
QZ_F1 = 122
QZ_F2 = 120
QZ_F3 = 99
QZ_F4 = 118
QZ_F5 = 96
QZ_F6 = 97
QZ_F7 = 98
QZ_F8 = 100
QZ_F9 = 101
QZ_F10 = 109
QZ_F11 = 103
QZ_F12 = 111
QZ_PRINT = 105
QZ_SCROLLOCK = 107
QZ_PAUSE = 113
QZ_POWER = 127
QZ_BACKQUOTE = 50
QZ_1 = 18
QZ_2 = 19
QZ_3 = 20
QZ_4 = 21
QZ_5 = 23
QZ_6 = 22
QZ_7 = 26
QZ_8 = 28
QZ_9 = 25
QZ_0 = 29
QZ_MINUS = 27
QZ_EQUALS = 24
QZ_BACKSPACE = 51
QZ_INSERT = 114
QZ_HOME = 115
QZ_PAGEUP = 116
QZ_NUMLOCK = 71
QZ_KP_EQUALS = 81
QZ_KP_DIVIDE = 75
QZ_KP_MULTIPLY = 67
QZ_TAB = 48
QZ_q = 12
QZ_w = 13
QZ_e = 14
QZ_r = 15
QZ_t = 17
QZ_y = 16
QZ_u = 32
QZ_i = 34
QZ_o = 31
QZ_p = 35
QZ_LEFTBRACKET = 33
QZ_RIGHTBRACKET = 30
QZ_BACKSLASH = 42
QZ_DELETE = 117
QZ_END = 119
QZ_PAGEDOWN = 121
QZ_KP7 = 89
QZ_KP8 = 91
QZ_KP9 = 92
QZ_KP_MINUS = 78
QZ_CAPSLOCK = 57
QZ_a = 0
QZ_s = 1
QZ_d = 2
QZ_f = 3
QZ_g = 5
QZ_h = 4
QZ_j = 38
QZ_k = 40
QZ_l = 37
QZ_SEMICOLON = 41
QZ_QUOTE = 39
QZ_RETURN = 36
QZ_KP4 = 86
QZ_KP5 = 87
QZ_KP6 = 88
QZ_KP_PLUS = 69
QZ_LSHIFT = 56
QZ_z = 6
QZ_x = 7
QZ_c = 8
QZ_v = 9
QZ_b = 11
QZ_n = 45
QZ_m = 46
QZ_COMMA = 43
QZ_PERIOD = 47
QZ_SLASH = 44
QZ_RSHIFT = 60
QZ_UP = 126
QZ_KP1 = 83
QZ_KP2 = 84
QZ_KP3 = 85
QZ_KP_ENTER = 76
QZ_LCTRL = 59
QZ_LALT = 58
QZ_LMETA = 55
QZ_SPACE = 49
QZ_RMETA = 54
QZ_RALT = 61
QZ_RCTRL = 62
QZ_LEFT = 123
QZ_DOWN = 125
QZ_RIGHT = 124
QZ_KP0 = 82
QZ_KP_PERIOD = 65
QZ_IBOOK_ENTER = 52
QZ_IBOOK_LEFT = 59
QZ_IBOOK_RIGHT = 60
QZ_IBOOK_DOWN = 61
QZ_IBOOK_UP = 62
keymap = {QZ_ESCAPE: key.ESCAPE, 
   QZ_F1: key.F1, 
   QZ_F2: key.F2, 
   QZ_F3: key.F3, 
   QZ_F4: key.F4, 
   QZ_F5: key.F5, 
   QZ_F6: key.F6, 
   QZ_F7: key.F7, 
   QZ_F8: key.F8, 
   QZ_F9: key.F9, 
   QZ_F10: key.F10, 
   QZ_F11: key.F11, 
   QZ_F12: key.F12, 
   QZ_PRINT: key.PRINT, 
   QZ_SCROLLOCK: key.SCROLLLOCK, 
   QZ_PAUSE: key.PAUSE, 
   QZ_BACKQUOTE: key.QUOTELEFT, 
   QZ_1: key._1, 
   QZ_2: key._2, 
   QZ_3: key._3, 
   QZ_4: key._4, 
   QZ_5: key._5, 
   QZ_6: key._6, 
   QZ_7: key._7, 
   QZ_8: key._8, 
   QZ_9: key._9, 
   QZ_0: key._0, 
   QZ_MINUS: key.MINUS, 
   QZ_EQUALS: key.EQUAL, 
   QZ_BACKSPACE: key.BACKSPACE, 
   QZ_INSERT: key.INSERT, 
   QZ_HOME: key.HOME, 
   QZ_PAGEUP: key.PAGEUP, 
   QZ_NUMLOCK: key.NUMLOCK, 
   QZ_KP_EQUALS: key.NUM_EQUAL, 
   QZ_KP_DIVIDE: key.NUM_DIVIDE, 
   QZ_KP_MULTIPLY: key.NUM_MULTIPLY, 
   QZ_TAB: key.TAB, 
   QZ_q: key.Q, 
   QZ_w: key.W, 
   QZ_e: key.E, 
   QZ_r: key.R, 
   QZ_t: key.T, 
   QZ_y: key.Y, 
   QZ_u: key.U, 
   QZ_i: key.I, 
   QZ_o: key.O, 
   QZ_p: key.P, 
   QZ_LEFTBRACKET: key.BRACKETLEFT, 
   QZ_RIGHTBRACKET: key.BRACKETRIGHT, 
   QZ_BACKSLASH: key.BACKSLASH, 
   QZ_DELETE: key.DELETE, 
   QZ_END: key.END, 
   QZ_PAGEDOWN: key.PAGEDOWN, 
   QZ_KP7: key.NUM_7, 
   QZ_KP8: key.NUM_8, 
   QZ_KP9: key.NUM_9, 
   QZ_KP_MINUS: key.NUM_SUBTRACT, 
   QZ_CAPSLOCK: key.CAPSLOCK, 
   QZ_a: key.A, 
   QZ_s: key.S, 
   QZ_d: key.D, 
   QZ_f: key.F, 
   QZ_g: key.G, 
   QZ_h: key.H, 
   QZ_j: key.J, 
   QZ_k: key.K, 
   QZ_l: key.L, 
   QZ_SEMICOLON: key.SEMICOLON, 
   QZ_QUOTE: key.APOSTROPHE, 
   QZ_RETURN: key.RETURN, 
   QZ_KP4: key.NUM_4, 
   QZ_KP5: key.NUM_5, 
   QZ_KP6: key.NUM_6, 
   QZ_KP_PLUS: key.NUM_ADD, 
   QZ_LSHIFT: key.LSHIFT, 
   QZ_z: key.Z, 
   QZ_x: key.X, 
   QZ_c: key.C, 
   QZ_v: key.V, 
   QZ_b: key.B, 
   QZ_n: key.N, 
   QZ_m: key.M, 
   QZ_COMMA: key.COMMA, 
   QZ_PERIOD: key.PERIOD, 
   QZ_SLASH: key.SLASH, 
   QZ_RSHIFT: key.RSHIFT, 
   QZ_UP: key.UP, 
   QZ_KP1: key.NUM_1, 
   QZ_KP2: key.NUM_2, 
   QZ_KP3: key.NUM_3, 
   QZ_KP_ENTER: key.NUM_ENTER, 
   QZ_LCTRL: key.LCTRL, 
   QZ_LALT: key.LALT, 
   QZ_LMETA: key.LMETA, 
   QZ_SPACE: key.SPACE, 
   QZ_RMETA: key.RMETA, 
   QZ_RALT: key.RALT, 
   QZ_RCTRL: key.RCTRL, 
   QZ_LEFT: key.LEFT, 
   QZ_DOWN: key.DOWN, 
   QZ_RIGHT: key.RIGHT, 
   QZ_KP0: key.NUM_0, 
   QZ_KP_PERIOD: key.NUM_DECIMAL, 
   QZ_IBOOK_ENTER: key.ENTER, 
   QZ_IBOOK_LEFT: key.LEFT, 
   QZ_IBOOK_RIGHT: key.RIGHT, 
   QZ_IBOOK_DOWN: key.DOWN, 
   QZ_IBOOK_UP: key.UP}