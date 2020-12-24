# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/karas/training/utils.py
# Compiled at: 2019-01-07 03:45:02
# Size of source mod 2**32: 2663 bytes
import contextlib, os, shutil, tempfile
if os.name == 'nt':
    import ctypes
    _STD_OUTPUT_HANDLE = -11

    class _COORD(ctypes.Structure):
        _fields_ = [
         (
          'X', ctypes.c_short), ('Y', ctypes.c_short)]


    class _SMALL_RECT(ctypes.Structure):
        _fields_ = [
         (
          'Left', ctypes.c_short), ('Top', ctypes.c_short),
         (
          'Right', ctypes.c_short), ('Bottom', ctypes.c_short)]


    class _CONSOLE_SCREEN_BUFFER_INFO(ctypes.Structure):
        _fields_ = [
         (
          'dwSize', _COORD), ('dwCursorPosition', _COORD),
         (
          'wAttributes', ctypes.c_ushort),
         (
          'srWindow', _SMALL_RECT),
         (
          'dwMaximumWindowSize', _COORD)]


    def set_console_cursor_position(x, y):
        """Set relative cursor position from current position to (x,y)"""
        whnd = ctypes.windll.kernel32.GetStdHandle(_STD_OUTPUT_HANDLE)
        csbi = _CONSOLE_SCREEN_BUFFER_INFO()
        ctypes.windll.kernel32.GetConsoleScreenBufferInfo(whnd, ctypes.byref(csbi))
        cur_pos = csbi.dwCursorPosition
        pos = _COORD(cur_pos.X + x, cur_pos.Y + y)
        ctypes.windll.kernel32.SetConsoleCursorPosition(whnd, pos)


    def erase_console(x, y, mode=0):
        """Erase screen.

        Mode=0: From (x,y) position down to the bottom of the screen.
        Mode=1: From (x,y) position down to the begining of line.
        Mode=2: Hole screen
        """
        whnd = ctypes.windll.kernel32.GetStdHandle(_STD_OUTPUT_HANDLE)
        csbi = _CONSOLE_SCREEN_BUFFER_INFO()
        ctypes.windll.kernel32.GetConsoleScreenBufferInfo(whnd, ctypes.byref(csbi))
        cur_pos = csbi.dwCursorPosition
        wr = ctypes.c_ulong()
        if mode == 0:
            num = csbi.srWindow.Right * (csbi.srWindow.Bottom - cur_pos.Y) - cur_pos.X
            ctypes.windll.kernel32.FillConsoleOutputCharacterA(whnd, ord(' '), num, cur_pos, ctypes.byref(wr))
        else:
            if mode == 1:
                num = cur_pos.X
                ctypes.windll.kernel32.FillConsoleOutputCharacterA(whnd, ord(' '), num, _COORD(0, cur_pos.Y), ctypes.byref(wr))
            elif mode == 2:
                os.system('cls')


@contextlib.contextmanager
def tempdir(**kwargs):
    ignore_errors = kwargs.pop('ignore_errors', False)
    temp_dir = (tempfile.mkdtemp)(**kwargs)
    try:
        yield temp_dir
    finally:
        shutil.rmtree(temp_dir, ignore_errors=ignore_errors)