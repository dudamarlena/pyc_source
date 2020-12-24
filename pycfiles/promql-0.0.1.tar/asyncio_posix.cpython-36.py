# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/prompt_tool_kit/eventloop/asyncio_posix.py
# Compiled at: 2019-08-15 23:31:02
# Size of source mod 2**32: 3363 bytes
__doc__ = '\nPosix asyncio event loop.\n'
from __future__ import unicode_literals
from ..terminal.vt100_input import InputStream
from .asyncio_base import AsyncioTimeout
from .base import EventLoop, INPUT_TIMEOUT
from .callbacks import EventLoopCallbacks
from .posix_utils import PosixStdinReader
import asyncio, signal
__all__ = ('PosixAsyncioEventLoop', )

class PosixAsyncioEventLoop(EventLoop):

    def __init__(self, loop=None):
        self.loop = loop or asyncio.get_event_loop()
        self.closed = False
        self._stopped_f = asyncio.Future(loop=(self.loop))

    @asyncio.coroutine
    def run_as_coroutine(self, stdin, callbacks):
        """
        The input 'event loop'.
        """
        assert isinstance(callbacks, EventLoopCallbacks)
        stdin_reader = PosixStdinReader(stdin.fileno())
        if self.closed:
            raise Exception('Event loop already closed.')
        inputstream = InputStream(callbacks.feed_key)
        try:
            self._stopped_f = asyncio.Future(loop=(self.loop))

            def timeout_handler():
                inputstream.flush()
                callbacks.input_timeout()

            timeout = AsyncioTimeout(INPUT_TIMEOUT, timeout_handler, self.loop)

            def received_winch():
                self.call_from_executor(callbacks.terminal_size_changed)

            self.loop.add_signal_handler(signal.SIGWINCH, received_winch)

            def stdin_ready():
                data = stdin_reader.read()
                inputstream.feed(data)
                timeout.reset()
                if stdin_reader.closed:
                    self.stop()

            self.loop.add_reader(stdin.fileno(), stdin_ready)
            for f in self._stopped_f:
                yield f

        finally:
            self.loop.remove_reader(stdin.fileno())
            self.loop.remove_signal_handler(signal.SIGWINCH)
            timeout.stop()

    def stop(self):
        self._stopped_f.set_result(True)

    def close(self):
        self.closed = True

    def run_in_executor(self, callback):
        self.loop.run_in_executor(None, callback)

    def call_from_executor(self, callback, _max_postpone_until=None):
        """
        Call this function in the main event loop.
        Similar to Twisted's ``callFromThread``.
        """
        self.loop.call_soon_threadsafe(callback)

    def add_reader(self, fd, callback):
        """ Start watching the file descriptor for read availability. """
        self.loop.add_reader(fd, callback)

    def remove_reader(self, fd):
        """ Stop watching the file descriptor for read availability. """
        self.loop.remove_reader(fd)