# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sbo/lib/python3.4/site-packages/vaitk/__init__.py
# Compiled at: 2015-05-02 14:14:14
# Size of source mod 2**32: 16309 bytes
import os, curses
__version__ = '1.7'

class FocusPolicy:
    NoFocus = 0
    StrongFocus = 11


class Orientation:
    Horizontal = 1
    Vertical = 2


class LineStyle:
    NoLine = 0
    Full = 1


class CornerCapStyle:
    NoCap = 0
    Plus = 1


class LineCapStyle:
    NoCap = 0
    Plus = 1


class Alignment:
    AlignLeft = 1
    AlignRight = 2
    AlignHCenter = 4
    AlignTop = 32
    AlignBottom = 64
    AlignVCenter = 128
    AlignCenter = AlignHCenter | AlignVCenter


class Key:
    Key_Escape = 16777216
    Key_Tab = 16777217
    Key_Backtab = 16777218
    Key_Backspace = 16777219
    Key_Return = 16777220
    Key_Enter = 16777221
    Key_Insert = 16777222
    Key_Delete = 16777223
    Key_Pause = 16777224
    Key_Print = 16777225
    Key_SysReq = 16777226
    Key_Clear = 16777227
    Key_Home = 16777232
    Key_End = 16777233
    Key_Left = 16777234
    Key_Up = 16777235
    Key_Right = 16777236
    Key_Down = 16777237
    Key_PageUp = 16777238
    Key_PageDown = 16777239
    Key_Shift = 16777248
    Key_Control = 16777249
    Key_Meta = 16777250
    Key_Alt = 16777251
    Key_AltGr = 16781571
    Key_CapsLock = 16777252
    Key_NumLock = 16777253
    Key_ScrollLock = 16777254
    Key_F1 = 16777264
    Key_F2 = 16777265
    Key_F3 = 16777266
    Key_F4 = 16777267
    Key_F5 = 16777268
    Key_F6 = 16777269
    Key_F7 = 16777270
    Key_F8 = 16777271
    Key_F9 = 16777272
    Key_F10 = 16777273
    Key_F11 = 16777274
    Key_F12 = 16777275
    Key_F13 = 16777276
    Key_F14 = 16777277
    Key_F15 = 16777278
    Key_F16 = 16777279
    Key_F17 = 16777280
    Key_F18 = 16777281
    Key_F19 = 16777282
    Key_F20 = 16777283
    Key_F21 = 16777284
    Key_F22 = 16777285
    Key_F23 = 16777286
    Key_F24 = 16777287
    Key_F25 = 16777288
    Key_F26 = 16777289
    Key_F27 = 16777290
    Key_F28 = 16777291
    Key_F29 = 16777292
    Key_F30 = 16777293
    Key_F31 = 16777294
    Key_F32 = 16777295
    Key_F33 = 16777296
    Key_F34 = 16777297
    Key_F35 = 16777298
    Key_Super_L = 16777299
    Key_Super_R = 16777300
    Key_Menu = 16777301
    Key_Hyper_L = 16777302
    Key_Hyper_R = 16777303
    Key_Help = 16777304
    Key_Direction_L = 16777305
    Key_Direction_R = 16777312
    Key_Space = 32
    Key_Any = Key_Space
    Key_Exclam = 33
    Key_QuoteDbl = 34
    Key_NumberSign = 35
    Key_Dollar = 36
    Key_Percent = 37
    Key_Ampersand = 38
    Key_Apostrophe = 39
    Key_ParenLeft = 40
    Key_ParenRight = 41
    Key_Asterisk = 42
    Key_Plus = 43
    Key_Comma = 44
    Key_Minus = 45
    Key_Period = 46
    Key_Slash = 47
    Key_0 = 48
    Key_1 = 49
    Key_2 = 50
    Key_3 = 51
    Key_4 = 52
    Key_5 = 53
    Key_6 = 54
    Key_7 = 55
    Key_8 = 56
    Key_9 = 57
    Key_Colon = 58
    Key_Semicolon = 59
    Key_Less = 60
    Key_Equal = 61
    Key_Greater = 62
    Key_Question = 63
    Key_At = 64
    Key_A = 65
    Key_B = 66
    Key_C = 67
    Key_D = 68
    Key_E = 69
    Key_F = 70
    Key_G = 71
    Key_H = 72
    Key_I = 73
    Key_J = 74
    Key_K = 75
    Key_L = 76
    Key_M = 77
    Key_N = 78
    Key_O = 79
    Key_P = 80
    Key_Q = 81
    Key_R = 82
    Key_S = 83
    Key_T = 84
    Key_U = 85
    Key_V = 86
    Key_W = 87
    Key_X = 88
    Key_Y = 89
    Key_Z = 90
    Key_BracketLeft = 91
    Key_Backslash = 92
    Key_BracketRight = 93
    Key_AsciiCircum = 94
    Key_Underscore = 95
    Key_QuoteLeft = 96
    Key_BraceLeft = 123
    Key_Bar = 124
    Key_BraceRight = 125
    Key_AsciiTilde = 126
    Key_unknown = 33554431
    NonPrintableMask = 16777216
    Mask = 33554431


class KeyModifier:
    NoModifier = 0
    ShiftModifier = 33554432
    ControlModifier = 67108864
    AltModifier = 134217728
    MetaModifier = 268435456
    KeypadModifier = 536870912
    Mask = 1056964608


def nativeToVaiKeyCode(native_key_code):
    """Transforms the keycode from native (ncurses) to vaitk representation"""
    key_mapper = {1: Key.Key_A | KeyModifier.ControlModifier, 
     2: Key.Key_B | KeyModifier.ControlModifier, 
     3: Key.Key_C | KeyModifier.ControlModifier, 
     4: Key.Key_D | KeyModifier.ControlModifier, 
     5: Key.Key_E | KeyModifier.ControlModifier, 
     6: Key.Key_F | KeyModifier.ControlModifier, 
     7: Key.Key_G | KeyModifier.ControlModifier, 
     8: Key.Key_Backspace, 
     9: Key.Key_Tab, 
     10: Key.Key_Return, 
     11: Key.Key_K | KeyModifier.ControlModifier, 
     12: Key.Key_L | KeyModifier.ControlModifier, 
     13: Key.Key_M | KeyModifier.ControlModifier, 
     14: Key.Key_N | KeyModifier.ControlModifier, 
     15: Key.Key_O | KeyModifier.ControlModifier, 
     16: Key.Key_P | KeyModifier.ControlModifier, 
     17: Key.Key_Q | KeyModifier.ControlModifier, 
     18: Key.Key_R | KeyModifier.ControlModifier, 
     19: Key.Key_S | KeyModifier.ControlModifier, 
     20: Key.Key_T | KeyModifier.ControlModifier, 
     21: Key.Key_U | KeyModifier.ControlModifier, 
     22: Key.Key_V | KeyModifier.ControlModifier, 
     23: Key.Key_W | KeyModifier.ControlModifier, 
     24: Key.Key_X | KeyModifier.ControlModifier, 
     25: Key.Key_Y | KeyModifier.ControlModifier, 
     26: Key.Key_Z | KeyModifier.ControlModifier, 
     27: Key.Key_Escape, 
     32: Key.Key_Space, 
     33: Key.Key_Exclam, 
     34: Key.Key_QuoteDbl, 
     35: Key.Key_NumberSign, 
     36: Key.Key_Dollar, 
     37: Key.Key_Percent, 
     38: Key.Key_Ampersand, 
     39: Key.Key_Apostrophe, 
     40: Key.Key_ParenLeft, 
     41: Key.Key_ParenRight, 
     42: Key.Key_Asterisk, 
     43: Key.Key_Plus, 
     44: Key.Key_Comma, 
     45: Key.Key_Minus, 
     46: Key.Key_Period, 
     47: Key.Key_Slash, 
     48: Key.Key_0, 
     49: Key.Key_1, 
     50: Key.Key_2, 
     51: Key.Key_3, 
     52: Key.Key_4, 
     53: Key.Key_5, 
     54: Key.Key_6, 
     55: Key.Key_7, 
     56: Key.Key_8, 
     57: Key.Key_9, 
     58: Key.Key_Colon, 
     59: Key.Key_Semicolon, 
     60: Key.Key_Less, 
     61: Key.Key_Equal, 
     62: Key.Key_Greater, 
     63: Key.Key_Question, 
     64: Key.Key_At, 
     65: Key.Key_A | KeyModifier.ShiftModifier, 
     66: Key.Key_B | KeyModifier.ShiftModifier, 
     67: Key.Key_C | KeyModifier.ShiftModifier, 
     68: Key.Key_D | KeyModifier.ShiftModifier, 
     69: Key.Key_E | KeyModifier.ShiftModifier, 
     70: Key.Key_F | KeyModifier.ShiftModifier, 
     71: Key.Key_G | KeyModifier.ShiftModifier, 
     72: Key.Key_H | KeyModifier.ShiftModifier, 
     73: Key.Key_I | KeyModifier.ShiftModifier, 
     74: Key.Key_J | KeyModifier.ShiftModifier, 
     75: Key.Key_K | KeyModifier.ShiftModifier, 
     76: Key.Key_L | KeyModifier.ShiftModifier, 
     77: Key.Key_M | KeyModifier.ShiftModifier, 
     78: Key.Key_N | KeyModifier.ShiftModifier, 
     79: Key.Key_O | KeyModifier.ShiftModifier, 
     80: Key.Key_P | KeyModifier.ShiftModifier, 
     81: Key.Key_Q | KeyModifier.ShiftModifier, 
     82: Key.Key_R | KeyModifier.ShiftModifier, 
     83: Key.Key_S | KeyModifier.ShiftModifier, 
     84: Key.Key_T | KeyModifier.ShiftModifier, 
     85: Key.Key_U | KeyModifier.ShiftModifier, 
     86: Key.Key_V | KeyModifier.ShiftModifier, 
     87: Key.Key_W | KeyModifier.ShiftModifier, 
     88: Key.Key_X | KeyModifier.ShiftModifier, 
     89: Key.Key_Y | KeyModifier.ShiftModifier, 
     90: Key.Key_Z | KeyModifier.ShiftModifier, 
     91: Key.Key_BracketLeft, 
     92: Key.Key_Backslash, 
     93: Key.Key_BracketRight, 
     94: Key.Key_AsciiCircum, 
     95: Key.Key_Underscore, 
     96: Key.Key_QuoteLeft, 
     97: Key.Key_A, 
     98: Key.Key_B, 
     99: Key.Key_C, 
     100: Key.Key_D, 
     101: Key.Key_E, 
     102: Key.Key_F, 
     103: Key.Key_G, 
     104: Key.Key_H, 
     105: Key.Key_I, 
     106: Key.Key_J, 
     107: Key.Key_K, 
     108: Key.Key_L, 
     109: Key.Key_M, 
     110: Key.Key_N, 
     111: Key.Key_O, 
     112: Key.Key_P, 
     113: Key.Key_Q, 
     114: Key.Key_R, 
     115: Key.Key_S, 
     116: Key.Key_T, 
     117: Key.Key_U, 
     118: Key.Key_V, 
     119: Key.Key_W, 
     120: Key.Key_X, 
     121: Key.Key_Y, 
     122: Key.Key_Z, 
     123: Key.Key_BraceLeft, 
     124: Key.Key_Bar, 
     125: Key.Key_BraceRight, 
     126: Key.Key_AsciiTilde, 
     127: Key.Key_Backspace, 
     curses.KEY_DOWN: Key.Key_Down, 
     curses.KEY_UP: Key.Key_Up, 
     curses.KEY_LEFT: Key.Key_Left, 
     curses.KEY_RIGHT: Key.Key_Right, 
     curses.KEY_BACKSPACE: Key.Key_Backspace, 
     curses.KEY_NPAGE: Key.Key_PageDown, 
     curses.KEY_PPAGE: Key.Key_PageUp, 
     curses.KEY_DC: Key.Key_Delete}
    return key_mapper.get(native_key_code)


def isKeyCodePrintable(key_code):
    return key_code & Key.NonPrintableMask == 0


def vaiKeyCodeToText(key_code):
    if not isKeyCodePrintable(key_code):
        return ''
    key_map = {Key.Key_Space: ' ', 
     Key.Key_Exclam: '!', 
     Key.Key_QuoteDbl: '"', 
     Key.Key_NumberSign: '#', 
     Key.Key_Dollar: '$', 
     Key.Key_Percent: '%', 
     Key.Key_Ampersand: '&', 
     Key.Key_Apostrophe: "'", 
     Key.Key_ParenLeft: '(', 
     Key.Key_ParenRight: ')', 
     Key.Key_Asterisk: '*', 
     Key.Key_Plus: '+', 
     Key.Key_Comma: ',', 
     Key.Key_Minus: '-', 
     Key.Key_Period: '.', 
     Key.Key_Slash: '/', 
     Key.Key_0: '0', 
     Key.Key_1: '1', 
     Key.Key_2: '2', 
     Key.Key_3: '3', 
     Key.Key_4: '4', 
     Key.Key_5: '5', 
     Key.Key_6: '6', 
     Key.Key_7: '7', 
     Key.Key_8: '8', 
     Key.Key_9: '9', 
     Key.Key_Colon: ':', 
     Key.Key_Semicolon: ';', 
     Key.Key_Less: '<', 
     Key.Key_Equal: '=', 
     Key.Key_Greater: '>', 
     Key.Key_Question: '?', 
     Key.Key_At: '@', 
     Key.Key_A: 'a', 
     Key.Key_B: 'b', 
     Key.Key_C: 'c', 
     Key.Key_D: 'd', 
     Key.Key_E: 'e', 
     Key.Key_F: 'f', 
     Key.Key_G: 'g', 
     Key.Key_H: 'h', 
     Key.Key_I: 'i', 
     Key.Key_J: 'j', 
     Key.Key_K: 'k', 
     Key.Key_L: 'l', 
     Key.Key_M: 'm', 
     Key.Key_N: 'n', 
     Key.Key_O: 'o', 
     Key.Key_P: 'p', 
     Key.Key_Q: 'q', 
     Key.Key_R: 'r', 
     Key.Key_S: 's', 
     Key.Key_T: 't', 
     Key.Key_U: 'u', 
     Key.Key_V: 'v', 
     Key.Key_W: 'w', 
     Key.Key_X: 'x', 
     Key.Key_Y: 'y', 
     Key.Key_Z: 'z', 
     Key.Key_BracketLeft: '[', 
     Key.Key_Backslash: '\\', 
     Key.Key_BracketRight: ']', 
     Key.Key_AsciiCircum: '^', 
     Key.Key_Underscore: '_', 
     Key.Key_QuoteLeft: '`', 
     Key.Key_BraceLeft: '{', 
     Key.Key_Bar: '|', 
     Key.Key_BraceRight: '}', 
     Key.Key_AsciiTilde: '~', 
     Key.Key_A | KeyModifier.ShiftModifier: 'A', 
     Key.Key_B | KeyModifier.ShiftModifier: 'B', 
     Key.Key_C | KeyModifier.ShiftModifier: 'C', 
     Key.Key_D | KeyModifier.ShiftModifier: 'D', 
     Key.Key_E | KeyModifier.ShiftModifier: 'E', 
     Key.Key_F | KeyModifier.ShiftModifier: 'F', 
     Key.Key_G | KeyModifier.ShiftModifier: 'G', 
     Key.Key_H | KeyModifier.ShiftModifier: 'H', 
     Key.Key_I | KeyModifier.ShiftModifier: 'I', 
     Key.Key_J | KeyModifier.ShiftModifier: 'J', 
     Key.Key_K | KeyModifier.ShiftModifier: 'K', 
     Key.Key_L | KeyModifier.ShiftModifier: 'L', 
     Key.Key_M | KeyModifier.ShiftModifier: 'M', 
     Key.Key_N | KeyModifier.ShiftModifier: 'N', 
     Key.Key_O | KeyModifier.ShiftModifier: 'O', 
     Key.Key_P | KeyModifier.ShiftModifier: 'P', 
     Key.Key_Q | KeyModifier.ShiftModifier: 'Q', 
     Key.Key_R | KeyModifier.ShiftModifier: 'R', 
     Key.Key_S | KeyModifier.ShiftModifier: 'S', 
     Key.Key_T | KeyModifier.ShiftModifier: 'T', 
     Key.Key_U | KeyModifier.ShiftModifier: 'U', 
     Key.Key_V | KeyModifier.ShiftModifier: 'V', 
     Key.Key_W | KeyModifier.ShiftModifier: 'W', 
     Key.Key_X | KeyModifier.ShiftModifier: 'X', 
     Key.Key_Y | KeyModifier.ShiftModifier: 'Y', 
     Key.Key_Z | KeyModifier.ShiftModifier: 'Z'}
    return key_map.get(key_code, '')