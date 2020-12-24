# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \Ft\Lib\Terminal.py
# Compiled at: 2006-09-22 13:17:00
"""
Provides some of the information from the terminfo database.

Copyright 2005 Fourthought, Inc. (USA).
Detailed license and copyright information: http://4suite.org/COPYRIGHT
Project home, documentation, distributions: http://4suite.org/
"""
import os, re, sys
from Ft.Lib.Terminfo import TERMTYPES as _ANSITERMS
from Ft.Lib.Terminfo import DEFAULT_LINES as _LINES
from Ft.Lib.Terminfo import DEFAULT_COLUMNS as _COLUMNS
if sys.platform == 'win32':
    import msvcrt
    from Ft.Lib import _win32con
elif os.name == 'posix':
    _HAVE_TIOCGWINSZ = False
    try:
        import fcntl, termios, struct
    except ImportError:
        pass
    else:
        _HAVE_TIOCGWINSZ = hasattr(termios, 'TIOCGWINSZ')

class AnsiEscapes:
    __module__ = __name__

    class Colors:
        __module__ = __name__
        DEFAULT = '\x1b[0m'
        BOLD = '\x1b[1m'
        FOREGROUND_BLACK = '\x1b[30m'
        FOREGROUND_MAROON = '\x1b[31m'
        FOREGROUND_GREEN = '\x1b[32m'
        FOREGROUND_BROWN = FOREGROUND_OLIVE = '\x1b[33m'
        FOREGROUND_NAVY = '\x1b[34m'
        FOREGROUND_PURPLE = '\x1b[35m'
        FOREGROUND_TEAL = '\x1b[36m'
        FOREGROUND_SILVER = '\x1b[37m'
        FOREGROUND_GRAY = '\x1b[1;30m'
        FOREGROUND_RED = '\x1b[1;31m'
        FOREGROUND_LIME = '\x1b[1;32m'
        FOREGROUND_YELLOW = '\x1b[1;33m'
        FOREGROUND_BLUE = '\x1b[1;34m'
        FOREGROUND_MAGENTA = FOREGROUND_FUCHSIA = '\x1b[1;35m'
        FOREGROUND_CYAN = FOREGROUND_AQUA = '\x1b[1;36m'
        FOREGROUND_WHITE = '\x1b[1;37m'
        BACKGROUND_BLACK = '\x1b[40m'
        BACKGROUND_MAROON = '\x1b[41m'
        BACKGROUND_GREEN = '\x1b[42m'
        BACKGROUND_BROWN = BACKGROUND_OLIVE = '\x1b[43m'
        BACKGROUND_NAVY = '\x1b[44m'
        BACKGROUND_PURPLE = '\x1b[45m'
        BACKGROUND_TEAL = '\x1b[46m'
        BACKGROUND_SILVER = '\x1b[47m'


_file_methods = (
 'flush', 'write', 'read', 'isatty', 'encoding')

class Terminal:
    __module__ = __name__

    def __init__(self, stream, keepAnsiEscapes=True):
        self._stream = stream
        for name in _file_methods:
            method = getattr(stream, name, None)
            if method is not None:
                setattr(self, name, method)

        if self.isatty():
            if sys.platform == 'win32':
                self._init_win32(stream, keepAnsiEscapes)
            elif os.name == 'posix' and os.environ.get('TERM') in _ANSITERMS:
                self._init_posix(stream, keepAnsiEscapes)
        return
        return

    def _init_win32(self, stream, keepAnsiEscapes):
        try:
            fileno = stream.fileno()
        except AttributeError:
            return

        try:
            self._handle = msvcrt.get_osfhandle(fileno)
        except IOError:
            return

        if keepAnsiEscapes:
            self._write_escape = self._escape_win32
            self._default_attribute = _win32con.GetConsoleScreenBufferInfo(self._handle)[2]
        self.size = self._size_win32
        return

    def _init_posix(self, stream, keepAnsiEscapes):
        if keepAnsiEscapes:
            self.writetty = stream.write
        if _HAVE_TIOCGWINSZ:
            self.size = self._size_termios
        return

    def lines(self):
        return self.size()[0]

    def columns(self):
        return self.size()[1]

    def size(self):
        return (
         _LINES, _COLUMNS)

    def flush(self):
        return

    def write(self, str):
        return

    def read(self, size=-1):
        return ''

    def isatty(self):
        return False

    def close(self):
        if self.isatty():
            return
        try:
            self._stream.close()
        except:
            pass

        return

    _ansi_sdm = re.compile('\x1b\\[([0-9]+)(?:;([0-9]+))*m')

    def writetty(self, bytes):
        start = 0
        match = self._ansi_sdm.search(bytes)
        while match is not None:
            self._stream.write(bytes[start:match.start()])
            self._write_escape(match.groups())
            start = match.end()
            match = self._ansi_sdm.search(bytes, start)

        self._stream.write(bytes[start:])
        return
        return

    def _write_escape(self, codes):
        """
        Escape function for handling ANSI Set Display Mode.

        Default behavior is to simply ignore the call (e.g. nothing is added
        to the output).
        """
        return

    def _size_termios(self):
        ws = struct.pack('HHHH', 0, 0, 0, 0)
        ws = fcntl.ioctl(self._stream.fileno(), termios.TIOCGWINSZ, ws)
        (lines, columns, x, y) = struct.unpack('HHHH', ws)
        return (lines, columns)

    def _escape_win32(self, codes):
        """Translates the ANSI color codes into the Win32 API equivalents."""
        (size, cursor, attributes, window) = _win32con.GetConsoleScreenBufferInfo(self._handle)
        for code in map(int, filter(None, codes)):
            if code == 0:
                attributes = self._default_attribute
            elif code == 1:
                attributes |= _win32con.FOREGROUND_INTENSITY
            elif code == 30:
                attributes &= _win32con.BACKGROUND
            elif code == 31:
                attributes &= _win32con.FOREGROUND_INTENSITY | _win32con.BACKGROUND
                attributes |= _win32con.FOREGROUND_RED
            elif code == 32:
                attributes &= _win32con.FOREGROUND_INTENSITY | _win32con.BACKGROUND
                attributes |= _win32con.FOREGROUND_GREEN
            elif code == 33:
                attributes &= _win32con.FOREGROUND_INTENSITY | _win32con.BACKGROUND
                attributes |= _win32con.FOREGROUND_RED | _win32con.FOREGROUND_GREEN
            elif code == 34:
                attributes &= _win32con.FOREGROUND_INTENSITY | _win32con.BACKGROUND
                attributes |= _win32con.FOREGROUND_BLUE
            elif code == 35:
                attributes &= _win32con.FOREGROUND_INTENSITY | _win32con.BACKGROUND
                attributes |= _win32con.FOREGROUND_RED | _win32con.FOREGROUND_BLUE
            elif code == 36:
                attributes &= _win32con.FOREGROUND_INTENSITY | _win32con.BACKGROUND
                attributes |= _win32con.FOREGROUND_BLUE | _win32con.FOREGROUND_GREEN
            elif code == 37:
                attributes &= _win32con.FOREGROUND_INTENSITY | _win32con.BACKGROUND
                attributes |= _win32con.FOREGROUND_RED | _win32con.FOREGROUND_GREEN | _win32con.FOREGROUND_BLUE
            elif code == 40:
                attributes &= _win32con.FOREGROUND
            elif code == 41:
                attributes &= _win32con.FOREGROUND
                attributes |= _win32con.BACKGROUND_RED
            elif code == 42:
                attributes &= _win32con.FOREGROUND
                attributes |= _win32con.BACKGROUND_GREEN
            elif code == 43:
                attributes &= _win32con.FOREGROUND
                attributes |= _win32con.BACKGROUND_RED | _win32con.BACKGROUND_GREEN
            elif code == 44:
                attributes &= _win32con.FOREGROUND
                attributes |= _win32con.BACKGROUND_BLUE
            elif code == 45:
                attributes &= _win32con.FOREGROUND
                attributes |= _win32con.BACKGROUND_RED | _win32con.BACKGROUND_BLUE
            elif code == 46:
                attributes &= _win32con.FOREGROUND
                attributes |= _win32con.BACKGROUND_BLUE | _win32con.BACKGROUND_GREEN
            elif code == 47:
                attributes &= _win32con.FOREGROUND
                attributes |= _win32con.BACKGROUND_RED | _win32con.BACKGROUND_GREEN | _win32con.BACKGROUND_BLUE

        _win32con.SetConsoleTextAttribute(self._handle, attributes)
        return
        return

    def _size_win32(self):
        (size, cursor, attributes, window) = _win32con.GetConsoleScreenBufferInfo(self._handle)
        (left, top, right, bottom) = window
        (columns, lines) = size
        return (bottom - top, columns - 1)