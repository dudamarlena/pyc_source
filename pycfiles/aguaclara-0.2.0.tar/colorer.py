# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/advancedcaching/colorer.py
# Compiled at: 2011-04-23 08:43:29
import logging

def add_coloring_to_emit_windows(fn):

    def _out_handle(self):
        import ctypes
        return ctypes.windll.kernel32.GetStdHandle(self.STD_OUTPUT_HANDLE)

    out_handle = property(_out_handle)

    def _set_color(self, code):
        import ctypes
        self.STD_OUTPUT_HANDLE = -11
        hdl = ctypes.windll.kernel32.GetStdHandle(self.STD_OUTPUT_HANDLE)
        ctypes.windll.kernel32.SetConsoleTextAttribute(hdl, code)

    setattr(logging.StreamHandler, '_set_color', _set_color)

    def new(*args):
        FOREGROUND_BLUE = 1
        FOREGROUND_GREEN = 2
        FOREGROUND_RED = 4
        FOREGROUND_INTENSITY = 8
        FOREGROUND_WHITE = FOREGROUND_BLUE | FOREGROUND_GREEN | FOREGROUND_RED
        STD_INPUT_HANDLE = -10
        STD_OUTPUT_HANDLE = -11
        STD_ERROR_HANDLE = -12
        FOREGROUND_BLACK = 0
        FOREGROUND_BLUE = 1
        FOREGROUND_GREEN = 2
        FOREGROUND_CYAN = 3
        FOREGROUND_RED = 4
        FOREGROUND_MAGENTA = 5
        FOREGROUND_YELLOW = 6
        FOREGROUND_GREY = 7
        FOREGROUND_INTENSITY = 8
        BACKGROUND_BLACK = 0
        BACKGROUND_BLUE = 16
        BACKGROUND_GREEN = 32
        BACKGROUND_CYAN = 48
        BACKGROUND_RED = 64
        BACKGROUND_MAGENTA = 80
        BACKGROUND_YELLOW = 96
        BACKGROUND_GREY = 112
        BACKGROUND_INTENSITY = 128
        levelno = args[1].levelno
        if levelno >= 50:
            color = BACKGROUND_YELLOW | FOREGROUND_RED | FOREGROUND_INTENSITY | BACKGROUND_INTENSITY
        elif levelno >= 40:
            color = FOREGROUND_RED | FOREGROUND_INTENSITY
        elif levelno >= 30:
            color = FOREGROUND_YELLOW | FOREGROUND_INTENSITY
        elif levelno >= 20:
            color = FOREGROUND_GREEN
        elif levelno >= 10:
            color = FOREGROUND_BLACK
        else:
            color = FOREGROUND_WHITE
        args[0]._set_color(color)
        ret = fn(*args)
        args[0]._set_color(FOREGROUND_WHITE)
        return ret

    return new


def add_coloring_to_emit_ansi(fn):

    def new(*args):
        levelno = args[1].levelno
        if levelno >= 50:
            color = '\x1b[31m'
        elif levelno >= 40:
            color = '\x1b[31m'
        elif levelno >= 30:
            color = '\x1b[33m'
        elif levelno >= 20:
            color = '\x1b[32m'
        elif levelno >= 10:
            color = '\x1b[39m'
        else:
            color = '\x1b[0m'
        args[1].msg = '%s%s%s' % (color, args[1].msg, '\x1b[0m')
        return fn(*args)

    return new


import platform
if platform.system() == 'Windows':
    logging.StreamHandler.emit = add_coloring_to_emit_windows(logging.StreamHandler.emit)
else:
    logging.StreamHandler.emit = add_coloring_to_emit_ansi(logging.StreamHandler.emit)