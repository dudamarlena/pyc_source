# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/testoob/reporting/color_support.py
# Compiled at: 2009-10-07 18:08:46
import sys, os
DISABLE_COLOR_SUPPORT_ENV_VAR_NAME = 'TESTOOB_DISABLE_COLOR_SUPPORT'

def can_autodetect_color_support():
    if sys.platform.startswith('win'):
        try:
            import ctypes
            return True
        except ImportError:
            return False

    return True


def auto_color_support(stream):
    if sys.platform.startswith('win'):
        try:
            import ctypes
            return _win_ctypes_color_support()
        except ImportError:
            pass
        else:
            if DISABLE_COLOR_SUPPORT_ENV_VAR_NAME in os.environ:
                return False
            return True
    return _curses_color_support(stream)


def _win_ctypes_color_support():
    import ctypes
    STD_OUTPUT_HANDLE = -11
    out_handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
    csbi = ctypes.create_string_buffer(22)
    res = ctypes.windll.kernel32.GetConsoleScreenBufferInfo(out_handle, csbi)
    return res != 0


def _curses_color_support(stream):
    if not hasattr(stream, 'isatty'):
        return False
    if not stream.isatty():
        return False
    try:
        import curses
        curses.setupterm()
        return curses.tigetnum('colors') > 2
    except:
        return False