# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/beantop/charreader.py
# Compiled at: 2013-05-21 03:52:38


class CharReader:

    def __init__(self, operative_system, sys, termios, fcntl):
        self._operative_system = operative_system
        self._sys = sys
        self._termios = termios
        self._fcntl = fcntl
        self._stdin_file_descriptor = None
        self._oldterm = None
        self._oldflags = None
        return

    def get_char(self):
        try:
            char_read = self._sys.stdin.read(1)
        except IOError:
            char_read = None

        return char_read

    def setup_terminal_for_char_read(self):
        self._stdin_file_descriptor = self._sys.stdin.fileno()
        self._oldterm = self._termios.tcgetattr(self._stdin_file_descriptor)
        newattr = self._termios.tcgetattr(self._stdin_file_descriptor)
        newattr[3] = newattr[3] & ~self._termios.ICANON & ~self._termios.ECHO
        self._termios.tcsetattr(self._stdin_file_descriptor, self._termios.TCSANOW, newattr)
        self._oldflags = self._fcntl.fcntl(self._stdin_file_descriptor, self._fcntl.F_GETFL)
        newflags = self._oldflags | self._operative_system.O_NONBLOCK
        self._fcntl.fcntl(self._stdin_file_descriptor, self._fcntl.F_SETFL, newflags)

    def reset_terminal_options(self):
        self._termios.tcsetattr(self._stdin_file_descriptor, self._termios.TCSAFLUSH, self._oldterm)
        self._fcntl.fcntl(self._stdin_file_descriptor, self._fcntl.F_SETFL, self._oldflags)