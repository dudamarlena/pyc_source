# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tools/tmp/cmd2/thgcmd/rl_utils.py
# Compiled at: 2019-07-17 15:07:37
# Size of source mod 2**32: 7439 bytes
"""
Imports the proper readline for the platform and provides utility functions for it
"""
from enum import Enum
import sys
try:
    import gnureadline as readline
except ImportError:
    try:
        import readline
    except ImportError:
        pass

class RlType(Enum):
    __doc__ = 'Readline library types we recognize'
    GNU = 1
    PYREADLINE = 2
    NONE = 3


rl_type = RlType.NONE
vt100_support = False
if 'pyreadline' in sys.modules:
    rl_type = RlType.PYREADLINE
    from ctypes import byref
    from ctypes.wintypes import DWORD, HANDLE
    import atexit
    if sys.stdout.isatty():

        def enable_win_vt100(handle: HANDLE) -> bool:
            """
            Enables VT100 character sequences in a Windows console
            This only works on Windows 10 and up
            :param handle: the handle on which to enable vt100
            :return: True if vt100 characters are enabled for the handle
            """
            ENABLE_VIRTUAL_TERMINAL_PROCESSING = 4
            cur_mode = DWORD(0)
            readline.rl.console.GetConsoleMode(handle, byref(cur_mode))
            retVal = False
            if cur_mode.value & ENABLE_VIRTUAL_TERMINAL_PROCESSING != 0:
                retVal = True
            else:
                if readline.rl.console.SetConsoleMode(handle, cur_mode.value | ENABLE_VIRTUAL_TERMINAL_PROCESSING):
                    atexit.register(readline.rl.console.SetConsoleMode, handle, cur_mode)
                    retVal = True
            return retVal


        STD_OUT_HANDLE = -11
        STD_ERROR_HANDLE = -12
        vt100_stdout_support = enable_win_vt100(readline.rl.console.GetStdHandle(STD_OUT_HANDLE))
        vt100_stderr_support = enable_win_vt100(readline.rl.console.GetStdHandle(STD_ERROR_HANDLE))
        vt100_support = vt100_stdout_support and vt100_stderr_support
    try:
        getattr(readline, 'redisplay')
    except AttributeError:
        readline.redisplay = readline.rl.mode._update_line

    try:
        getattr(readline, 'remove_history_item')
    except AttributeError:

        def pyreadline_remove_history_item(pos: int) -> None:
            """
            An implementation of remove_history_item() for pyreadline
            :param pos: The 0-based position in history to remove
            """
            saved_cursor = readline.rl.mode._history.history_cursor
            del readline.rl.mode._history.history[pos]
            if saved_cursor > pos:
                readline.rl.mode._history.history_cursor -= 1


        readline.remove_history_item = pyreadline_remove_history_item

else:
    if 'gnureadline' in sys.modules or 'readline' in sys.modules:
        if 'libedit' not in readline.__doc__:
            rl_type = RlType.GNU
            import ctypes
            readline_lib = ctypes.CDLL(readline.__file__)
            if sys.stdout.isatty():
                vt100_support = True

    def rl_force_redisplay() -> None:
        """
    Causes readline to display the prompt and input text wherever the cursor is and start
    reading input from this location. This is the proper way to restore the input line after
    printing to the screen
    """
        if not sys.stdout.isatty():
            return
        elif rl_type == RlType.GNU:
            readline_lib.rl_forced_update_display()
            display_fixed = ctypes.c_int.in_dll(readline_lib, 'rl_display_fixed')
            display_fixed.value = 1
        else:
            if rl_type == RlType.PYREADLINE:
                readline.rl.mode._print_prompt()
                readline.rl.mode._update_line()


    def rl_get_point() -> int:
        """
    Returns the offset of the current cursor position in rl_line_buffer
    """
        if rl_type == RlType.GNU:
            return ctypes.c_int.in_dll(readline_lib, 'rl_point').value
        if rl_type == RlType.PYREADLINE:
            return readline.rl.mode.l_buffer.point
        return 0


    def rl_set_prompt(prompt: str) -> None:
        """
    Sets readline's prompt
    :param prompt: the new prompt value
    """
        safe_prompt = rl_make_safe_prompt(prompt)
        if rl_type == RlType.GNU:
            encoded_prompt = bytes(safe_prompt, encoding='utf-8')
            readline_lib.rl_set_prompt(encoded_prompt)
        else:
            if rl_type == RlType.PYREADLINE:
                readline.rl._set_prompt(safe_prompt)


    def rl_make_safe_prompt(prompt: str) -> str:
        """Overcome bug in GNU Readline in relation to calculation of prompt length in presence of ANSI escape codes.

    :param prompt: original prompt
    :return: prompt safe to pass to GNU Readline
    """
        if rl_type == RlType.GNU:
            start = '\x01'
            end = '\x02'
            escaped = False
            result = ''
            for c in prompt:
                if c == '\x1b':
                    escaped or result += start + c
                    escaped = True
                elif c.isalpha() and escaped:
                    result += c + end
                    escaped = False
                else:
                    result += c

            return result
        return prompt