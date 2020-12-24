# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/paul/src/scspell-0.1/scspell_lib/_portable.py
# Compiled at: 2009-06-06 00:05:46
"""
portable -- contains functions for hiding differences between platforms.
"""
import os, sys
try:
    import msvcrt

    def getch():
        return msvcrt.getch()


except ImportError:
    import tty, termios

    def getch():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

        return ch


def get_data_dir(progname):
    """Retrieves a platform-appropriate data directory for the specified program."""
    if sys.platform == 'win32':
        parent_dir = os.getenv('APPDATA')
        prog_dir = progname
    else:
        parent_dir = os.getenv('HOME')
        prog_dir = '.' + progname
    return os.path.normpath(os.path.join(parent_dir, prog_dir))