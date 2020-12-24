# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/prompt_tool_kit/input.py
# Compiled at: 2019-08-15 23:53:38
# Size of source mod 2**32: 3216 bytes
"""
Abstraction of CLI Input.
"""
from __future__ import unicode_literals
from .utils import DummyContext, is_windows
from abc import ABCMeta, abstractmethod
from six import with_metaclass
import io, os, sys
if is_windows():
    from .terminal.win32_input import raw_mode, cooked_mode
else:
    from .terminal.vt100_input import raw_mode, cooked_mode
__all__ = ('Input', 'StdinInput', 'PipeInput')

class Input(with_metaclass(ABCMeta, object)):
    __doc__ = '\n    Abstraction for any input.\n\n    An instance of this class can be given to the constructor of a\n    :class:`~prompt_tool_kit.interface.CommandLineInterface` and will also be\n    passed to the :class:`~prompt_tool_kit.eventloop.base.EventLoop`.\n    '

    @abstractmethod
    def fileno(self):
        """
        Fileno for putting this in an event loop.
        """
        pass

    @abstractmethod
    def read(self):
        """
        Return text from the input.
        """
        pass

    @abstractmethod
    def raw_mode(self):
        """
        Context manager that turns the input into raw mode.
        """
        pass

    @abstractmethod
    def cooked_mode(self):
        """
        Context manager that turns the input into cooked mode.
        """
        pass


class StdinInput(Input):
    __doc__ = '\n    Simple wrapper around stdin.\n    '

    def __init__(self, stdin=None):
        self.stdin = stdin or sys.stdin
        assert self.stdin.isatty()
        try:
            self.stdin.fileno()
        except io.UnsupportedOperation:
            if 'idlelib.run' in sys.modules:
                raise io.UnsupportedOperation('Stdin is not a terminal. Running from Idle is not supported.')
            else:
                raise io.UnsupportedOperation('Stdin is not a terminal.')

    def __repr__(self):
        return 'StdinInput(stdin=%r)' % (self.stdin,)

    def raw_mode(self):
        return raw_mode(self.stdin.fileno())

    def cooked_mode(self):
        return cooked_mode(self.stdin.fileno())

    def fileno(self):
        return self.stdin.fileno()

    def read(self):
        return self.stdin.read()


class PipeInput(Input):
    __doc__ = "\n    Input that is send through a pipe.\n    This is useful if we want to send the input programatically into the\n    interface, but still use the eventloop.\n\n    Usage::\n\n        input = PipeInput()\n        input.send('inputdata')\n    "

    def __init__(self):
        self._r, self._w = os.pipe()

    def fileno(self):
        return self._r

    def read(self):
        return os.read(self._r)

    def send_text(self, data):
        """ Send text to the input. """
        os.write(self._w, data.encode('utf-8'))

    send = send_text

    def raw_mode(self):
        return DummyContext()

    def cooked_mode(self):
        return DummyContext()

    def close(self):
        """ Close pipe fds. """
        os.close(self._r)
        os.close(self._w)
        self._r = None
        self._w = None