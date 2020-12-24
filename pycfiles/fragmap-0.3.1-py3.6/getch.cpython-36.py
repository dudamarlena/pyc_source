# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\getch\getch.py
# Compiled at: 2019-08-04 05:05:23
# Size of source mod 2**32: 2038 bytes


class _Getch:
    __doc__ = '\n    Gets a single character from standard input.  Does not echo to\n    the screen.\n    '

    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            try:
                self.impl = _GetchMacCarbon()
            except (AttributeError, ImportError):
                self.impl = _GetchUnix()

    def __call__(self):
        return self.impl()


class _GetchUnix:

    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            return

        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _GetchWindows:

    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()


class _GetchMacCarbon:
    __doc__ = '\n    A function which returns the current ASCII key that is down;\n    if no ASCII key is down, the null string is returned.  The\n    page http://www.mactech.com/macintosh-c/chap02-1.html was\n    very helpful in figuring out how to do this.\n    '

    def __init__(self):
        import Carbon
        Carbon.Evt

    def __call__(self):
        import Carbon
        if Carbon.Evt.EventAvail(8)[0] == 0:
            return ''
        else:
            what, msg, when, where, mod = Carbon.Evt.GetNextEvent(8)[1]
            return chr(msg & 255)


getch = _Getch()