# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/doubanfm/getch.py
# Compiled at: 2016-06-22 17:23:26
"""
Copyright (c) 2006-2015 sqlmap developers (http://sqlmap.org/)
See the file 'doc/COPYING' for copying permission
"""

class _Getch(object):
    """
    Gets a single character from standard input.  Does not echo to
    the screen (reference: http://code.activestate.com/recipes/134892/)
    """

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


class _GetchUnix(object):

    def __init__(self):
        import tty

    def __call__(self):
        import sys, termios, tty
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

        return ch


class _GetchWindows(object):

    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()


class _GetchMacCarbon(object):
    """
    A function which returns the current ASCII key that is down;
    if no ASCII key is down, the null string is returned.  The
    page http://www.mactech.com/macintosh-c/chap02-1.html was
    very helpful in figuring out how to do this.
    """

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