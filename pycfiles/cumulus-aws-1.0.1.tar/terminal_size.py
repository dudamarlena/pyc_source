# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/sebastian/git/skymill/cumulus/cumulus/cumulus_ds/terminal_size.py
# Compiled at: 2014-03-03 09:28:20
__doc__ = ' Functions for calculating the teminal size '
import os, shlex, struct, platform, subprocess

def get_terminal_size():
    """ Get the current terminal size """
    current_os = platform.system()
    tuple_xy = None
    if current_os == 'Windows':
        tuple_xy = _get_terminal_size_windows()
        if tuple_xy is None:
            tuple_xy = _get_terminal_size_tput()
    if current_os in ('Linux', 'Darwin') or current_os.startswith('CYGWIN'):
        tuple_xy = _get_terminal_size_linux()
    if tuple_xy is None:
        print 'default'
        tuple_xy = (80, 25)
    return tuple_xy


def _get_terminal_size_windows():
    """ Get the terminal size on Windows """
    try:
        from ctypes import windll, create_string_buffer
        handle = windll.kernel32.GetStdHandle(-12)
        csbi = create_string_buffer(22)
        res = windll.kernel32.GetConsoleScreenBufferInfo(handle, csbi)
        if res:
            _, _, _, _, _, left, top, right, bottom, _, _ = struct.unpack('hhhhHhhhhhh', csbi.raw)
            sizex = right - left + 1
            sizey = bottom - top + 1
            return (
             sizex, sizey)
    except:
        pass


def _get_terminal_size_tput():
    """ Fallback function for Windows """
    try:
        cols = int(subprocess.check_call(shlex.split('tput cols')))
        rows = int(subprocess.check_call(shlex.split('tput lines')))
        return (
         cols, rows)
    except:
        pass


def _get_terminal_size_linux():
    """ Get the terminal size in Linux / Darwin """

    def ioctl_GWINSZ(fdd):
        """ Undocumented """
        try:
            import fcntl, termios
            crd = struct.unpack('hh', fcntl.ioctl(fdd, termios.TIOCGWINSZ, '1234'))
            return crd
        except:
            pass

    crd = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
    if not crd:
        try:
            fdd = os.open(os.ctermid(), os.O_RDONLY)
            crd = ioctl_GWINSZ(fdd)
            os.close(fdd)
        except:
            pass

    if not crd:
        try:
            crd = (
             os.environ['LINES'], os.environ['COLUMNS'])
        except:
            return

    return (
     int(crd[1]), int(crd[0]))