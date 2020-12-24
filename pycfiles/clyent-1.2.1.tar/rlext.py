# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/cly/rlext.py
# Compiled at: 2007-12-09 10:28:16
from ctypes import *
from ctypes.util import find_library
readline = cdll.LoadLibrary(find_library('readline'))
rl_command_func_t = CFUNCTYPE(c_int, c_int, c_int)
rl_point = c_int.in_dll(readline, 'rl_point')
rl_end = c_int.in_dll(readline, 'rl_end')
rl_forced_update_display = readline.rl_forced_update_display
rl_bind_key = readline.rl_bind_key
rl_bind_key.argtypes = [c_int, rl_command_func_t]
rl_bind_key.restype = c_int

def force_redisplay():
    """Force the line to be updated and redisplayed, whether or not Readline
    thinks the screen display is correct."""
    rl_forced_update_display()


def bind_key(key, callback):
    """Bind key to function. Function must be a callable with one argument
    representing the count for that key."""
    c_callback = rl_command_func_t(callback)
    rl_bind_key(key, c_callback)


def cursor(pos=None):
    """Set or get the cursor location."""
    if pos is None:
        return rl_point.value
    elif rl_point.value > rl_end.value:
        rl_point.value = rl_end.value
    elif rl_point.value < 0:
        rl_point.value = 0
    else:
        rl_point.value = pos
    return 0