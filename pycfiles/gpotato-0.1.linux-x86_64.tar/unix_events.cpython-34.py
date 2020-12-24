# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.4/dist-packages/gpotato/unix_events.py
# Compiled at: 2015-05-03 15:01:52
# Size of source mod 2**32: 25120 bytes
"""Selector eventloop for Unix with signal handling."""
import errno, fcntl, os, signal, socket, stat, subprocess, sys, threading
from asyncio import base_subprocess
from asyncio import constants
from asyncio import events
from asyncio import protocols
from . import selector_events
from asyncio import tasks
from asyncio import transports
from asyncio.log import logger
from asyncio.unix_events import AbstractChildWatcher, DefaultEventLoopPolicy
__all__ = [
 'SelectorEventLoop',
 'AbstractChildWatcher', 'SafeChildWatcher',
 'FastChildWatcher', 'DefaultEventLoopPolicy']
STDIN = 0
STDOUT = 1
STDERR = 2

class _UnixSelectorEventLoop(selector_events.BaseSelectorEventLoop):
    __doc__ = 'Unix event loop\n\n    Adds signal handling to SelectorEventLoop\n    '

    def _socketpair(self):
        return socket.socketpair()

    def _check_signal(self, sig):
        """Internal helper to validate a signal.

        Raise ValueError if the signal number is invalid or uncatchable.
        Raise RuntimeError if there is a problem setting up the handler.
        """
        if not isinstance(sig, int):
            raise TypeError('sig must be an int, not {!r}'.format(sig))
        if not 1 <= sig < signal.NSIG:
            raise ValueError('sig {} out of range(1, {})'.format(sig, signal.NSIG))

    def _make_read_pipe_transport(self, pipe, protocol, waiter=None, extra=None):
        return _UnixReadPipeTransport(self, pipe, protocol, waiter, extra)

    def _make_write_pipe_transport(self, pipe, protocol, waiter=None, extra=None):
        return _UnixWritePipeTransport(self, pipe, protocol, waiter, extra)

    @tasks.coroutine
    def _make_subprocess_transport(self, protocol, args, shell, stdin, stdout, stderr, bufsize, extra=None, **kwargs):
        with events.get_child_watcher() as (watcher):
            transp = _UnixSubprocessTransport(self, protocol, args, shell, stdin, stdout, stderr, bufsize, extra=extra, **kwargs)
            yield from transp._post_init()
            watcher.add_child_handler(transp.get_pid(), self._child_watcher_callback, transp)
        return transp

    def _child_watcher_callback(self, pid, returncode, transp):
        self.call_soon_threadsafe(transp._process_exited, returncode)


def _set_nonblocking(fd):
    flags = fcntl.fcntl(fd, fcntl.F_GETFL)
    flags = flags | os.O_NONBLOCK
    fcntl.fcntl(fd, fcntl.F_SETFL, flags)


class _UnixReadPipeTransport(transports.ReadTransport):
    max_size = 262144

    def __init__(self, loop, pipe, protocol, waiter=None, extra=None):
        super().__init__(extra)
        self._extra['pipe'] = pipe
        self._loop = loop
        self._pipe = pipe
        self._fileno = pipe.fileno()
        mode = os.fstat(self._fileno).st_mode
        if not (stat.S_ISFIFO(mode) or stat.S_ISSOCK(mode) or stat.S_ISCHR(mode)):
            raise ValueError('Pipe transport is for pipes/sockets only.')
        _set_nonblocking(self._fileno)
        self._protocol = protocol
        self._closing = False
        self._loop.add_reader(self._fileno, self._read_ready)
        self._loop.call_soon(self._protocol.connection_made, self)
        if waiter is not None:
            self._loop.call_soon(waiter.set_result, None)

    def _read_ready(self):
        try:
            data = os.read(self._fileno, self.max_size)
        except (BlockingIOError, InterruptedError):
            pass
        except OSError as exc:
            self._fatal_error(exc)
        else:
            if data:
                self._protocol.data_received(data)
            else:
                self._closing = True
                self._loop.remove_reader(self._fileno)
                self._loop.call_soon(self._protocol.eof_received)
                self._loop.call_soon(self._call_connection_lost, None)

    def pause_reading(self):
        self._loop.remove_reader(self._fileno)

    def resume_reading(self):
        self._loop.add_reader(self._fileno, self._read_ready)

    def close(self):
        if not self._closing:
            self._close(None)

    def _fatal_error(self, exc):
        if not (isinstance(exc, OSError) and exc.errno == errno.EIO):
            logger.exception('Fatal error for %s', self)
        self._close(exc)

    def _close(self, exc):
        self._closing = True
        self._loop.remove_reader(self._fileno)
        self._loop.call_soon(self._call_connection_lost, exc)

    def _call_connection_lost(self, exc):
        try:
            self._protocol.connection_lost(exc)
        finally:
            self._pipe.close()
            self._pipe = None
            self._protocol = None
            self._loop = None


class _UnixWritePipeTransport(selector_events._FlowControlMixin, transports.WriteTransport):

    def __init__(self, loop, pipe, protocol, waiter=None, extra=None):
        super().__init__(extra)
        self._extra['pipe'] = pipe
        self._loop = loop
        self._pipe = pipe
        self._fileno = pipe.fileno()
        mode = os.fstat(self._fileno).st_mode
        is_socket = stat.S_ISSOCK(mode)
        if not (is_socket or stat.S_ISFIFO(mode) or stat.S_ISCHR(mode)):
            raise ValueError('Pipe transport is only for pipes, sockets and character devices')
        _set_nonblocking(self._fileno)
        self._protocol = protocol
        self._buffer = []
        self._conn_lost = 0
        self._closing = False
        if is_socket or not sys.platform.startswith('aix'):
            self._loop.add_reader(self._fileno, self._read_ready)
        self._loop.call_soon(self._protocol.connection_made, self)
        if waiter is not None:
            self._loop.call_soon(waiter.set_result, None)

    def get_write_buffer_size(self):
        return sum(len(data) for data in self._buffer)

    def _read_ready(self):
        if self._buffer:
            self._close(BrokenPipeError())
        else:
            self._close()

    def write(self, data):
        assert isinstance(data, (bytes, bytearray, memoryview)), repr(data)
        if isinstance(data, bytearray):
            data = memoryview(data)
        if not data:
            return
        if self._conn_lost or self._closing:
            if self._conn_lost >= constants.LOG_THRESHOLD_FOR_CONNLOST_WRITES:
                logger.warning('pipe closed by peer or os.write(pipe, data) raised exception.')
            self._conn_lost += 1
            return
        if not self._buffer:
            try:
                n = os.write(self._fileno, data)
            except (BlockingIOError, InterruptedError):
                n = 0
            except Exception as exc:
                self._conn_lost += 1
                self._fatal_error(exc)
                return

            if n == len(data):
                return
            if n > 0:
                data = data[n:]
            self._loop.add_writer(self._fileno, self._write_ready)
        self._buffer.append(data)
        self._maybe_pause_protocol()

    def _write_ready(self):
        data = (b'').join(self._buffer)
        assert data, 'Data should not be empty'
        self._buffer.clear()
        try:
            n = os.write(self._fileno, data)
        except (BlockingIOError, InterruptedError):
            self._buffer.append(data)
        except Exception as exc:
            self._conn_lost += 1
            self._loop.remove_writer(self._fileno)
            self._fatal_error(exc)
        else:
            if n == len(data):
                self._loop.remove_writer(self._fileno)
                self._maybe_resume_protocol()
                if not self._buffer:
                    if self._closing:
                        self._loop.remove_reader(self._fileno)
                        self._call_connection_lost(None)
                return
            if n > 0:
                data = data[n:]
            self._buffer.append(data)

    def can_write_eof(self):
        return True

    def write_eof(self):
        if self._closing:
            return
        assert self._pipe
        self._closing = True
        if not self._buffer:
            self._loop.remove_reader(self._fileno)
            self._loop.call_soon(self._call_connection_lost, None)

    def close(self):
        if not self._closing:
            self.write_eof()

    def abort(self):
        self._close(None)

    def _fatal_error(self, exc):
        if not isinstance(exc, (BrokenPipeError, ConnectionResetError)):
            logger.exception('Fatal error for %s', self)
        self._close(exc)

    def _close(self, exc=None):
        self._closing = True
        if self._buffer:
            self._loop.remove_writer(self._fileno)
        self._buffer.clear()
        self._loop.remove_reader(self._fileno)
        self._loop.call_soon(self._call_connection_lost, exc)

    def _call_connection_lost(self, exc):
        try:
            self._protocol.connection_lost(exc)
        finally:
            self._pipe.close()
            self._pipe = None
            self._protocol = None
            self._loop = None


class _UnixSubprocessTransport(base_subprocess.BaseSubprocessTransport):

    def _start(self, args, shell, stdin, stdout, stderr, bufsize, **kwargs):
        stdin_w = None
        if stdin == subprocess.PIPE:
            stdin, stdin_w = self._loop._socketpair()
        self._proc = subprocess.Popen(args, shell=shell, stdin=stdin, stdout=stdout, stderr=stderr, universal_newlines=False, bufsize=bufsize, **kwargs)
        if stdin_w is not None:
            stdin.close()
            self._proc.stdin = open(stdin_w.detach(), 'rb', buffering=bufsize)


SelectorEventLoop = _UnixSelectorEventLoop