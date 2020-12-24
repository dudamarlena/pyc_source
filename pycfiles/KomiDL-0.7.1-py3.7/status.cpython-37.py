# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\komidl\status.py
# Compiled at: 2019-10-12 01:12:13
# Size of source mod 2**32: 5628 bytes
"""This module contains the StatusBar class

When importing the module, a single instance of StatusBar is created.

Only singletons and public static methods are exported as module-level
functions.
"""
import sys
from contextlib import contextmanager

class StatusBar:
    __doc__ = 'A class to draw progress bars and handle user input.'
    BAR = '='
    MSG_SIZE = 13

    def __init__(self, length: int=0, total: int=0):
        self.length = length
        self.total = total
        self.current = 0

    @classmethod
    @contextmanager
    def progress(cls, msg: str, length: int, total: int, **kwargs: int) -> 'StatusBar':
        """Create an instance of StatusBar for drawing progress bars

        Parameters
        ----------
        kwargs['bar']: char         The character to display for progress bars
        kwargs['msg_size']: int     The length of space for msg in progress bar
        """
        sys.stdout.write(f"{msg}\n")
        status_bar = StatusBar(length=length, total=total)
        status_bar.BAR = kwargs.get('bar', status_bar.BAR)
        status_bar.MSG_SIZE = kwargs.get('msg_size', status_bar.MSG_SIZE)
        try:
            try:
                yield status_bar
            except Exception as e:
                try:
                    status_bar.update((status_bar.current), msg='Failed')
                    raise e
                finally:
                    e = None
                    del e

            else:
                status_bar.update((status_bar.current), msg='Success')
        finally:
            sys.stdout.write('\n')

    @staticmethod
    def _bar_size(length: int, current: int, total: int) -> int:
        """Return the number of bars to draw"""
        return int(current * length / float(total))

    @staticmethod
    def _percent(current: int, total: int) -> int:
        """Return the percentage progress"""
        return int(current * 100 / float(total))

    @staticmethod
    def _carriage_print(line: str) -> None:
        """Print to the current line using a carriage return"""
        sys.stdout.write('\r')
        sys.stdout.write(line)
        sys.stdout.flush()

    def _progress_print(self, msg: str) -> None:
        """Print the progress bar"""
        bars = self._bar_size(self.length, self.current, self.total)
        percent = self._percent(self.current, self.total)
        bar_str = self.BAR * bars
        msg += ':'
        line = f"{msg:<{self.MSG_SIZE}}[{bar_str:<{self.length}}]{percent:>4}%"
        self._carriage_print(line)

    def update(self, current: int, msg: str='Progress') -> None:
        """Update the progress bar with the new current value"""
        if current > self.total:
            raise ValueError(f"Current value ({current}) exceeds total " + f"({self.total})")
        if current < self.current:
            raise ValueError(f"Current value ({current}) lower than " + f"historical ({self.current})")
        self.current = current
        self._progress_print(msg)

    @staticmethod
    def prompt(msg: str, skip: bool=False) -> bool:
        """Print a yes/no prompt message, returns True if user answered yes"""
        if skip:
            return skip
        response = input(f"{msg} [y/N] ")
        return response.lower() == 'y'


_statusbar = StatusBar()
progress = _statusbar.progress
prompt = _statusbar.prompt
_percent = StatusBar._percent
_bar_size = StatusBar._bar_size