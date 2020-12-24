# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/hugo/.virtualenvs/gitinspector/lib/python2.7/site-packages/gitinspector/terminal.py
# Compiled at: 2015-08-05 12:31:15
from __future__ import print_function
import codecs, os, platform, sys, unicodedata
__bold__ = '\x1b[1m'
__normal__ = '\x1b[0;0m'
DEFAULT_TERMINAL_SIZE = (80, 25)

def __get_size_windows__():
    res = None
    try:
        from ctypes import windll, create_string_buffer
        handler = windll.kernel32.GetStdHandle(-12)
        csbi = create_string_buffer(22)
        res = windll.kernel32.GetConsoleScreenBufferInfo(handler, csbi)
    except:
        return DEFAULT_TERMINAL_SIZE

    if res:
        import struct
        _, _, _, _, _, left, top, right, bottom, _, _ = struct.unpack('hhhhHhhhhhh', csbi.raw)
        sizex = right - left + 1
        sizey = bottom - top + 1
        return (
         sizex, sizey)
    else:
        return DEFAULT_TERMINAL_SIZE
        return


def __get_size_linux__():

    def ioctl_get_window_size(file_descriptor):
        try:
            import fcntl, termios, struct
            size = struct.unpack('hh', fcntl.ioctl(file_descriptor, termios.TIOCGWINSZ, '1234'))
        except:
            return DEFAULT_TERMINAL_SIZE

        return size

    size = ioctl_get_window_size(0) or ioctl_get_window_size(1) or ioctl_get_window_size(2)
    if not size:
        try:
            file_descriptor = os.open(os.ctermid(), os.O_RDONLY)
            size = ioctl_get_window_size(file_descriptor)
            os.close(file_descriptor)
        except:
            pass

    if not size:
        try:
            size = (
             os.environ['LINES'], os.environ['COLUMNS'])
        except:
            return DEFAULT_TERMINAL_SIZE

    return (
     int(size[1]), int(size[0]))


def clear_row():
    print('\x08' * 200, end='')


def skip_escapes(skip):
    global __bold__
    global __normal__
    if skip:
        __bold__ = ''
        __normal__ = ''


def printb(string):
    print(__bold__ + string + __normal__)


def get_size():
    width = 0
    height = 0
    if sys.stdout.isatty():
        current_os = platform.system()
        if current_os == 'Windows':
            width, height = __get_size_windows__()
        elif current_os == 'Linux' or current_os == 'Darwin' or current_os.startswith('CYGWIN'):
            width, height = __get_size_linux__()
    if width > 0:
        return (width, height)
    return DEFAULT_TERMINAL_SIZE


def set_stdout_encoding():
    if not sys.stdout.isatty() and sys.version_info < (3, ):
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout)


def set_stdin_encoding():
    if not sys.stdin.isatty() and sys.version_info < (3, ):
        sys.stdin = codecs.getreader('utf-8')(sys.stdin)


def convert_command_line_to_utf8():
    try:
        argv = []
        for arg in sys.argv:
            argv.append(arg.decode(sys.stdin.encoding, 'replace'))

        return argv
    except AttributeError:
        return sys.argv


def check_terminal_encoding():
    if sys.stdout.isatty() and (sys.stdout.encoding == None or sys.stdin.encoding == None):
        print(_("WARNING: The terminal encoding is not correctly configured. gitinspector might malfunction. The encoding can be configured with the environment variable 'PYTHONIOENCODING'."), file=sys.stderr)
    return


def get_excess_column_count(string):
    width_mapping = {'F': 2, 'H': 1, 'W': 2, 'Na': 1, 'N': 1, 'A': 1}
    result = 0
    for c in string:
        w = unicodedata.east_asian_width(c)
        result += width_mapping[w]

    return result - len(string)


def ljust(string, pad):
    return string.ljust(pad - get_excess_column_count(string))


def rjust(string, pad):
    return string.rjust(pad - get_excess_column_count(string))