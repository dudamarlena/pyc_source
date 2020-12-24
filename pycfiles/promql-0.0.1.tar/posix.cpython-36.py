# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/prompt_tool_kit/eventloop/posix.py
# Compiled at: 2019-08-15 23:53:38
# Size of source mod 2**32: 12136 bytes
from __future__ import unicode_literals
import fcntl, os, random, signal, threading, time
from prompt_tool_kit.terminal.vt100_input import InputStream
from prompt_tool_kit.utils import DummyContext, in_main_thread
from prompt_tool_kit.input import Input
from .base import EventLoop, INPUT_TIMEOUT
from .callbacks import EventLoopCallbacks
from .inputhook import InputHookContext
from .posix_utils import PosixStdinReader
from .utils import TimeIt
from .select import AutoSelector, Selector, fd_to_int
__all__ = ('PosixEventLoop', )
_now = time.time

class PosixEventLoop(EventLoop):
    """PosixEventLoop"""

    def __init__(self, inputhook=None, selector=AutoSelector):
        if not inputhook is None:
            if not callable(inputhook):
                raise AssertionError
        elif not issubclass(selector, Selector):
            raise AssertionError
        self.running = False
        self.closed = False
        self._running = False
        self._callbacks = None
        self._calls_from_executor = []
        self._read_fds = {}
        self.selector = selector()
        self._schedule_pipe = os.pipe()
        fcntl.fcntl(self._schedule_pipe[0], fcntl.F_SETFL, os.O_NONBLOCK)
        self._inputhook_context = InputHookContext(inputhook) if inputhook else None

    def run(self, stdin, callbacks):
        """
        The input 'event loop'.
        """
        if not isinstance(stdin, Input):
            raise AssertionError
        else:
            if not isinstance(callbacks, EventLoopCallbacks):
                raise AssertionError
            else:
                assert not self._running
                if self.closed:
                    raise Exception('Event loop already closed.')
            self._running = True
            self._callbacks = callbacks
            inputstream = InputStream(callbacks.feed_key)
            current_timeout = [INPUT_TIMEOUT]
            stdin_reader = PosixStdinReader(stdin.fileno())
            if in_main_thread():
                ctx = call_on_sigwinch(self.received_winch)
            else:
                ctx = DummyContext()

        def read_from_stdin():
            data = stdin_reader.read()
            inputstream.feed(data)
            current_timeout[0] = INPUT_TIMEOUT
            if stdin_reader.closed:
                self.stop()

        self.add_reader(stdin, read_from_stdin)
        self.add_reader(self._schedule_pipe[0], None)
        with ctx:
            while self._running:
                if self._inputhook_context:
                    with TimeIt() as (inputhook_timer):

                        def ready(wait):
                            return self._ready_for_reading(current_timeout[0] if wait else 0) != []

                        self._inputhook_context.call_inputhook(ready)
                    inputhook_duration = inputhook_timer.duration
                else:
                    inputhook_duration = 0
                if current_timeout[0] is None:
                    remaining_timeout = None
                else:
                    remaining_timeout = max(0, current_timeout[0] - inputhook_duration)
                fds = self._ready_for_reading(remaining_timeout)
                if fds:
                    tasks = []
                    low_priority_tasks = []
                    now = None
                    for fd in fds:
                        if fd == self._schedule_pipe[0]:
                            for c, max_postpone_until in self._calls_from_executor:
                                if max_postpone_until is None:
                                    tasks.append(c)
                                else:
                                    now = now or _now()
                                    if max_postpone_until < now:
                                        tasks.append(c)
                                    else:
                                        low_priority_tasks.append((c, max_postpone_until))

                            self._calls_from_executor = []
                            os.read(self._schedule_pipe[0], 1024)
                        else:
                            handler = self._read_fds.get(fd)
                            if handler:
                                tasks.append(handler)

                    random.shuffle(tasks)
                    random.shuffle(low_priority_tasks)
                    if tasks:
                        for t in tasks:
                            t()

                        for t, max_postpone_until in low_priority_tasks:
                            self.call_from_executor(t, _max_postpone_until=max_postpone_until)

                    else:
                        for t, _ in low_priority_tasks:
                            t()

                else:
                    inputstream.flush()
                    callbacks.input_timeout()
                    current_timeout[0] = None

        self.remove_reader(stdin)
        self.remove_reader(self._schedule_pipe[0])
        self._callbacks = None

    def _ready_for_reading(self, timeout=None):
        """
        Return the file descriptors that are ready for reading.
        """
        fds = self.selector.select(timeout)
        return fds

    def received_winch(self):
        """
        Notify the event loop that SIGWINCH has been received
        """

        def process_winch():
            if self._callbacks:
                self._callbacks.terminal_size_changed()

        self.call_from_executor(process_winch)

    def run_in_executor(self, callback):
        """
        Run a long running function in a background thread.
        (This is recommended for code that could block the event loop.)
        Similar to Twisted's ``deferToThread``.
        """

        def start_executor():
            threading.Thread(target=callback).start()

        self.call_from_executor(start_executor)

    def call_from_executor(self, callback, _max_postpone_until=None):
        """
        Call this function in the main event loop.
        Similar to Twisted's ``callFromThread``.

        :param _max_postpone_until: `None` or `time.time` value. For interal
            use. If the eventloop is saturated, consider this task to be low
            priority and postpone maximum until this timestamp. (For instance,
            repaint is done using low priority.)
        """
        if not _max_postpone_until is None:
            if not isinstance(_max_postpone_until, float):
                raise AssertionError
        self._calls_from_executor.append((callback, _max_postpone_until))
        if self._schedule_pipe:
            try:
                os.write(self._schedule_pipe[1], 'x')
            except (AttributeError, IndexError, OSError):
                pass

    def stop(self):
        """
        Stop the event loop.
        """
        self._running = False

    def close(self):
        self.closed = True
        schedule_pipe = self._schedule_pipe
        self._schedule_pipe = None
        if schedule_pipe:
            os.close(schedule_pipe[0])
            os.close(schedule_pipe[1])
        if self._inputhook_context:
            self._inputhook_context.close()

    def add_reader(self, fd, callback):
        """ Add read file descriptor to the event loop. """
        fd = fd_to_int(fd)
        self._read_fds[fd] = callback
        self.selector.register(fd)

    def remove_reader(self, fd):
        """ Remove read file descriptor from the event loop. """
        fd = fd_to_int(fd)
        if fd in self._read_fds:
            del self._read_fds[fd]
        self.selector.unregister(fd)


class call_on_sigwinch(object):
    """call_on_sigwinch"""

    def __init__(self, callback):
        self.callback = callback
        self.previous_callback = None

    def __enter__(self):
        self.previous_callback = signal.signal(signal.SIGWINCH, lambda *a: self.callback())

    def __exit__(self, *a, **kw):
        if self.previous_callback is None:
            signal.signal(signal.SIGWINCH, 0)
        else:
            signal.signal(signal.SIGWINCH, self.previous_callback)