# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ditz/term.py
# Compiled at: 2014-12-05 09:06:10
"""
Terminal utilities.

http://stackoverflow.com/questions/566746/how-to-get-console-window-width-in-python
"""
import os, shlex, struct, platform, subprocess

def get_terminal_size(default=(80, 25)):
    """
    Return width and height of console window.
    """
    current_os = platform.system()
    size = None
    if current_os == 'Windows':
        size = _get_terminal_size_windows()
        if size is None:
            size = _get_terminal_size_tput()
    if current_os in ('Linux', 'Darwin') or current_os.startswith('CYGWIN'):
        size = _get_terminal_size_linux()
    return size or default


def _get_terminal_size_windows():
    try:
        from ctypes import windll, create_string_buffer
        h = windll.kernel32.GetStdHandle(-12)
        csbi = create_string_buffer(22)
        res = windll.kernel32.GetConsoleScreenBufferInfo(h, csbi)
        if res:
            bufx, bufy, curx, cury, wattr, left, top, right, bottom, maxx, maxy = struct.unpack('hhhhHhhhhhh', csbi.raw)
            cols = right - left + 1
            rows = bottom - top + 1
            return (
             cols, rows)
    except Exception:
        pass


def _get_terminal_size_tput():
    try:
        cols = int(subprocess.check_call(shlex.split('tput cols')))
        rows = int(subprocess.check_call(shlex.split('tput lines')))
        return (cols, rows)
    except Exception:
        pass


def _get_terminal_size_linux():

    def ioctl_GWINSZ(fd):
        try:
            import fcntl, termios
            data = fcntl.ioctl(fd, termios.TIOCGWINSZ, '1234')
            return struct.unpack('hh', data)
        except Exception:
            pass

    size = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
    if not size:
        try:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            size = ioctl_GWINSZ(fd)
            os.close(fd)
        except Exception:
            pass

    if not size:
        try:
            size = (
             os.environ['LINES'], os.environ['COLUMNS'])
        except Exception:
            return

    return (
     int(size[1]), int(size[0]))


if __name__ == '__main__':
    sizex, sizey = get_terminal_size()
    print ('width =', sizex, 'height =', sizey)