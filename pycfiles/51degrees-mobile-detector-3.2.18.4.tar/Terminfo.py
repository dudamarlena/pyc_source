# uncompyle6 version 3.6.7
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: \Ft\Lib\Terminfo.py
# Compiled at: 2005-11-15 02:36:24
__doc__ = '\nProvides some of the information from the terminfo database.\n\nCopyright 2005 Fourthought, Inc. (USA).\nDetailed license and copyright information: http://4suite.org/COPYRIGHT\nProject home, documentation, distributions: http://4suite.org/\n'
import sys, os
TERMTYPES = [
 'linux', 'console', 'con132x25', 'con132x30', 'con132x43', 'con132x60', 'con80x25', 'con80x28', 'con80x30', 'con80x43', 'con80x50', 'con80x60', 'xterm', 'xterm-color', 'color-xterm', 'vt100', 'vt100-color', 'rxvt', 'ansi', 'Eterm', 'putty', 'vt220-color', 'cygwin']
DEFAULT_LINES = 24
DEFAULT_COLUMNS = 80

def GetLines(stream=sys.stdout):
    lines = DEFAULT_LINES
    if hasattr(stream, 'isatty') and stream.isatty() and os.environ.get('TERM') in TERMTYPES:
        try:
            import fcntl, termios, struct
        except ImportError:
            pass
        else:
            if hasattr(termios, 'TIOCGWINSZ'):
                ws = struct.pack('HHHH', 0, 0, 0, 0)
                ws = fcntl.ioctl(stream.fileno(), termios.TIOCGWINSZ, ws)
                (lines, columns, x, y) = struct.unpack('HHHH', ws)
    return lines


def GetColumns(stream=sys.stdout):
    columns = DEFAULT_COLUMNS
    if stream.isatty() and os.environ.get('TERM') in TERMTYPES:
        try:
            import fcntl, termios, struct
        except ImportError:
            pass
        else:
            if hasattr(termios, 'TIOCGWINSZ'):
                ws = struct.pack('HHHH', 0, 0, 0, 0)
                ws = fcntl.ioctl(stream.fileno(), termios.TIOCGWINSZ, ws)
                (lines, columns, x, y) = struct.unpack('HHHH', ws)
    return columns