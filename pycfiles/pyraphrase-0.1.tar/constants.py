# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/mareike/work/app/pyrap-dev/python3/pyrap/constants.py
# Compiled at: 2017-11-23 08:40:56
__doc__ = '\nCreated on Oct 10, 2015\n\n@author: nyga\n'
from pyrap.utils import BitMask
inf = float('inf')
APPSTATE = BitMask('UNINITIALIZED', 'INITIALIZED', 'RUNNING')
RWT = BitMask('NONE', 'VISIBLE', 'ENABLED', 'ACTIVE', 'MAXIMIZED', 'MINIMIZED', 'BORDER', 'MINIMIZE', 'MAXIMIZE', 'RESTORE', 'CLOSE', 'RESIZE', 'TITLE', 'MODAL', 'CENTER', 'LEFT', 'RIGHT', 'TOP', 'BOTTOM', 'FILL', 'MULTI', 'WRAP', 'HSCROLL', 'VSCROLL', 'VERTICAL', 'HORIZONTAL', 'BAR', 'CASCADE', 'DROP_DOWN', 'PUSH', 'SEPARATOR', 'MULTI', 'MARKUP', 'NOSCROLL', 'SINGLE', 'POPUP', 'DRAW_MNEMONIC', 'DRAW_DELIMITER', 'DRAW_TAB', 'CHECK', 'RADIO', 'INFINITE', 'PASSWORD')
GCBITS = BitMask('DRAW_MNEMONIC', 'DRAW_DELIMITER', 'DRAW_TAB', 'ALIGN_CENTERX', 'ALIGN_CENTERY', 'BOLD', 'ITALIC', 'NORMAL')
DLG = BitMask('INFORMATION', 'QUESTION', 'WARNING', 'ERROR')

class CURSOR:
    DEFAULT = 1
    POINTER = 2

    @staticmethod
    def str(i):
        return {CURSOR.DEFAULT: 'default', 
           CURSOR.POINTER: 'pointer'}[i]


class FONT:
    NONE = 0
    IT = 1
    BF = 2
    str = {NONE: '', IT: 'italic', 
       BF: 'bold'}


class SHADOW:
    NONE = 0
    IN = 1
    OUT = 2
    str = {IN: 'inset', 
       OUT: 'out'}


class ANIMATION(object):
    EASE_IN = 2
    EASE_OUT = 4
    LINEAR = 8

    @staticmethod
    def str(i):
        return {ANIMATION.EASE_IN: 'easeIn', 
           ANIMATION.EASE_OUT: 'easeOut', 
           ANIMATION.LINEAR: 'linear'}[i]


class BORDER(object):
    NONE = 1
    SOLID = 2
    DOTTED = 4

    @staticmethod
    def str(i):
        return {BORDER.NONE: 'none', 
           BORDER.SOLID: 'solid', 
           BORDER.DOTTED: 'dotted'}[i]


class GRADIENT:
    VERTICAL = 2
    HORIZONTAL = 4