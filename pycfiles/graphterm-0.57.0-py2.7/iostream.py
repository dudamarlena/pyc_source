# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-x86_64/egg/graphterm/bin/tornado/iostream.py
# Compiled at: 2012-01-25 00:22:49
"""A utility class to write to and read from a non-blocking socket."""
from __future__ import with_statement
import collections, errno, logging, socket, sys, re
from tornado import ioloop
from tornado import stack_context
from tornado.util import b, bytes_type
try:
    import ssl
except ImportError:
    ssl = None

class IOStream(object):
    r"""A utility class to write to and read from a non-blocking socket.

    We support a non-blocking ``write()`` and a family of ``read_*()`` methods.
    All of the methods take callbacks (since writing and reading are
    non-blocking and asynchronous). 

    The socket parameter may either be connected or unconnected.  For
    server operations the socket is the result of calling socket.accept().
    For client operations the socket is created with socket.socket(),
    and may either be connected before passing it to the IOStream or
    connected with IOStream.connect.

    A very simple (and broken) HTTP client using this class::

        from tornado import ioloop
        from tornado import iostream
        import socket

        def send_request():
            stream.write("GET / HTTP/1.0\r\nHost: friendfeed.com\r\n\r\n")
            stream.read_until("\r\n\r\n", on_headers)

        def on_headers(data):
            headers = {}
            for line in data.split("\r\n"):
               parts = line.split(":")
               if len(parts) == 2:
                   headers[parts[0].strip()] = parts[1].strip()
            stream.read_bytes(int(headers["Content-Length"]), on_body)

        def on_body(data):
            print data
            stream.close()
            ioloop.IOLoop.instance().stop()

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        stream = iostream.IOStream(s)
        stream.connect(("friendfeed.com", 80), send_request)
        ioloop.IOLoop.instance().start()

    """

    def __init__(self, socket, io_loop=None, max_buffer_size=104857600, read_chunk_size=4096):
        self.socket = socket
        self.socket.setblocking(False)
        self.io_loop = io_loop or ioloop.IOLoop.instance()
        self.max_buffer_size = max_buffer_size
        self.read_chunk_size = read_chunk_size
        self._read_buffer = collections.deque()
        self._write_buffer = collections.deque()
        self._read_buffer_size = 0
        self._write_buffer_frozen = False
        self._read_delimiter = None
        self._read_regex = None
        self._read_bytes = None
        self._read_until_close = False
        self._read_callback = None
        self._streaming_callback = None
        self._write_callback = None
        self._close_callback = None
        self._connect_callback = None
        self._connecting = False
        self._state = None
        self._pending_callbacks = 0
        return

    def connect(self, address, callback=None):
        """Connects the socket to a remote address without blocking.

        May only be called if the socket passed to the constructor was
        not previously connected.  The address parameter is in the
        same format as for socket.connect, i.e. a (host, port) tuple.
        If callback is specified, it will be called when the
        connection is completed.

        Note that it is safe to call IOStream.write while the
        connection is pending, in which case the data will be written
        as soon as the connection is ready.  Calling IOStream read
        methods before the socket is connected works on some platforms
        but is non-portable.
        """
        self._connecting = True
        try:
            self.socket.connect(address)
        except socket.error as e:
            if e.args[0] not in (errno.EINPROGRESS, errno.EWOULDBLOCK):
                logging.warning('Connect error on fd %d: %s', self.socket.fileno(), e)
                self.close()
                return

        self._connect_callback = stack_context.wrap(callback)
        self._add_io_state(self.io_loop.WRITE)

    def read_until_regex(self, regex, callback):
        """Call callback when we read the given regex pattern."""
        assert not self._read_callback, 'Already reading'
        self._read_regex = re.compile(regex)
        self._read_callback = stack_context.wrap(callback)
        while True:
            if self._read_from_buffer():
                return
            self._check_closed()
            if self._read_to_buffer() == 0:
                break

        self._add_io_state(self.io_loop.READ)

    def read_until(self, delimiter, callback):
        """Call callback when we read the given delimiter."""
        assert not self._read_callback, 'Already reading'
        self._read_delimiter = delimiter
        self._read_callback = stack_context.wrap(callback)
        while True:
            if self._read_from_buffer():
                return
            self._check_closed()
            if self._read_to_buffer() == 0:
                break

        self._add_io_state(self.io_loop.READ)

    def read_bytes(self, num_bytes, callback, streaming_callback=None):
        """Call callback when we read the given number of bytes.

        If a ``streaming_callback`` is given, it will be called with chunks
        of data as they become available, and the argument to the final
        ``callback`` will be empty.
        """
        assert not self._read_callback, 'Already reading'
        assert isinstance(num_bytes, (int, long))
        self._read_bytes = num_bytes
        self._read_callback = stack_context.wrap(callback)
        self._streaming_callback = stack_context.wrap(streaming_callback)
        while True:
            if self._read_from_buffer():
                return
            self._check_closed()
            if self._read_to_buffer() == 0:
                break

        self._add_io_state(self.io_loop.READ)

    def read_until_close(self, callback, streaming_callback=None):
        """Reads all data from the socket until it is closed.

        If a ``streaming_callback`` is given, it will be called with chunks
        of data as they become available, and the argument to the final
        ``callback`` will be empty.

        Subject to ``max_buffer_size`` limit from `IOStream` constructor if
        a ``streaming_callback`` is not used.
        """
        assert not self._read_callback, 'Already reading'
        if self.closed():
            self._run_callback(callback, self._consume(self._read_buffer_size))
            return
        self._read_until_close = True
        self._read_callback = stack_context.wrap(callback)
        self._streaming_callback = stack_context.wrap(streaming_callback)
        self._add_io_state(self.io_loop.READ)

    def write(self, data, callback=None):
        """Write the given data to this stream.

        If callback is given, we call it when all of the buffered write
        data has been successfully written to the stream. If there was
        previously buffered write data and an old write callback, that
        callback is simply overwritten with this new callback.
        """
        assert isinstance(data, bytes_type)
        self._check_closed()
        if data:
            self._write_buffer.append(data)
        self._write_callback = stack_context.wrap(callback)
        self._handle_write()
        if self._write_buffer:
            self._add_io_state(self.io_loop.WRITE)
        self._maybe_add_error_listener()

    def set_close_callback(self, callback):
        """Call the given callback when the stream is closed."""
        self._close_callback = stack_context.wrap(callback)

    def close(self):
        """Close this stream."""
        if self.socket is not None:
            if self._read_until_close:
                callback = self._read_callback
                self._read_callback = None
                self._read_until_close = False
                self._run_callback(callback, self._consume(self._read_buffer_size))
            if self._state is not None:
                self.io_loop.remove_handler(self.socket.fileno())
                self._state = None
            self.socket.close()
            self.socket = None
            if self._close_callback and self._pending_callbacks == 0:
                cb = self._close_callback
                self._close_callback = None
                self._run_callback(cb)
        return

    def reading(self):
        """Returns true if we are currently reading from the stream."""
        return self._read_callback is not None

    def writing(self):
        """Returns true if we are currently writing to the stream."""
        return bool(self._write_buffer)

    def closed(self):
        """Returns true if the stream has been closed."""
        return self.socket is None

    def _handle_events(self, fd, events):
        if not self.socket:
            logging.warning('Got events for closed stream %d', fd)
            return
        else:
            try:
                if events & self.io_loop.READ:
                    self._handle_read()
                if not self.socket:
                    return
                if events & self.io_loop.WRITE:
                    if self._connecting:
                        self._handle_connect()
                    self._handle_write()
                if not self.socket:
                    return
                if events & self.io_loop.ERROR:
                    self.io_loop.add_callback(self.close)
                    return
                state = self.io_loop.ERROR
                if self.reading():
                    state |= self.io_loop.READ
                if self.writing():
                    state |= self.io_loop.WRITE
                if state == self.io_loop.ERROR:
                    state |= self.io_loop.READ
                if state != self._state:
                    assert self._state is not None, "shouldn't happen: _handle_events without self._state"
                    self._state = state
                    self.io_loop.update_handler(self.socket.fileno(), self._state)
            except Exception:
                logging.error('Uncaught exception, closing connection.', exc_info=True)
                self.close()
                raise

            return

    def _run_callback(self, callback, *args):

        def wrapper():
            self._pending_callbacks -= 1
            try:
                callback(*args)
            except Exception:
                logging.error('Uncaught exception, closing connection.', exc_info=True)
                self.close()
                raise

            self._maybe_add_error_listener()

        with stack_context.NullContext():
            self._pending_callbacks += 1
            self.io_loop.add_callback(wrapper)

    def _handle_read(self):
        while True:
            try:
                result = self._read_to_buffer()
            except Exception:
                self.close()
                return

            if result == 0:
                break
            elif self._read_from_buffer():
                return

    def _read_from_socket(self):
        """Attempts to read from the socket.

        Returns the data read or None if there is nothing to read.
        May be overridden in subclasses.
        """
        try:
            chunk = self.socket.recv(self.read_chunk_size)
        except socket.error as e:
            if e.args[0] in (errno.EWOULDBLOCK, errno.EAGAIN):
                return None
            raise

        if not chunk:
            self.close()
            return None
        else:
            return chunk

    def _read_to_buffer(self):
        """Reads from the socket and appends the result to the read buffer.

        Returns the number of bytes read.  Returns 0 if there is nothing
        to read (i.e. the read returns EWOULDBLOCK or equivalent).  On
        error closes the socket and raises an exception.
        """
        try:
            chunk = self._read_from_socket()
        except socket.error as e:
            logging.warning('Read error on %d: %s', self.socket.fileno(), e)
            self.close()
            raise

        if chunk is None:
            return 0
        else:
            self._read_buffer.append(chunk)
            self._read_buffer_size += len(chunk)
            if self._read_buffer_size >= self.max_buffer_size:
                logging.error('Reached maximum read buffer size')
                self.close()
                raise IOError('Reached maximum read buffer size')
            return len(chunk)

    def _read_from_buffer(self):
        """Attempts to complete the currently-pending read from the buffer.

        Returns True if the read was completed.
        """
        if self._read_bytes is not None:
            if self._streaming_callback is not None and self._read_buffer_size:
                bytes_to_consume = min(self._read_bytes, self._read_buffer_size)
                self._read_bytes -= bytes_to_consume
                self._run_callback(self._streaming_callback, self._consume(bytes_to_consume))
            if self._read_buffer_size >= self._read_bytes:
                num_bytes = self._read_bytes
                callback = self._read_callback
                self._read_callback = None
                self._streaming_callback = None
                self._read_bytes = None
                self._run_callback(callback, self._consume(num_bytes))
                return True
        elif self._read_delimiter is not None:
            loc = -1
            if self._read_buffer:
                loc = self._read_buffer[0].find(self._read_delimiter)
            while loc == -1 and len(self._read_buffer) > 1:
                new_len = max(len(self._read_buffer[0]) * 2, len(self._read_buffer[0]) + len(self._read_buffer[1]))
                _merge_prefix(self._read_buffer, new_len)
                loc = self._read_buffer[0].find(self._read_delimiter)

            if loc != -1:
                callback = self._read_callback
                delimiter_len = len(self._read_delimiter)
                self._read_callback = None
                self._streaming_callback = None
                self._read_delimiter = None
                self._run_callback(callback, self._consume(loc + delimiter_len))
                return True
        elif self._read_regex is not None:
            m = None
            if self._read_buffer:
                m = self._read_regex.search(self._read_buffer[0])
            while m is None and len(self._read_buffer) > 1:
                new_len = max(len(self._read_buffer[0]) * 2, len(self._read_buffer[0]) + len(self._read_buffer[1]))
                _merge_prefix(self._read_buffer, new_len)
                m = self._read_regex.search(self._read_buffer[0])

            _merge_prefix(self._read_buffer, sys.maxint)
            m = self._read_regex.search(self._read_buffer[0])
            if m:
                callback = self._read_callback
                self._read_callback = None
                self._streaming_callback = None
                self._read_regex = None
                self._run_callback(callback, self._consume(m.end()))
                return True
        elif self._read_until_close:
            if self._streaming_callback is not None and self._read_buffer_size:
                self._run_callback(self._streaming_callback, self._consume(self._read_buffer_size))
        return False

    def _handle_connect(self):
        err = self.socket.getsockopt(socket.SOL_SOCKET, socket.SO_ERROR)
        if err != 0:
            logging.warning('Connect error on fd %d: %s', self.socket.fileno(), errno.errorcode[err])
            self.close()
            return
        else:
            if self._connect_callback is not None:
                callback = self._connect_callback
                self._connect_callback = None
                self._run_callback(callback)
            self._connecting = False
            return

    def _handle_write(self):
        while self._write_buffer:
            try:
                if not self._write_buffer_frozen:
                    _merge_prefix(self._write_buffer, 131072)
                num_bytes = self.socket.send(self._write_buffer[0])
                if num_bytes == 0:
                    self._write_buffer_frozen = True
                    break
                self._write_buffer_frozen = False
                _merge_prefix(self._write_buffer, num_bytes)
                self._write_buffer.popleft()
            except socket.error as e:
                if e.args[0] in (errno.EWOULDBLOCK, errno.EAGAIN):
                    self._write_buffer_frozen = True
                    break
                else:
                    logging.warning('Write error on %d: %s', self.socket.fileno(), e)
                    self.close()
                    return

        if not self._write_buffer and self._write_callback:
            callback = self._write_callback
            self._write_callback = None
            self._run_callback(callback)
        return

    def _consume(self, loc):
        if loc == 0:
            return b('')
        _merge_prefix(self._read_buffer, loc)
        self._read_buffer_size -= loc
        return self._read_buffer.popleft()

    def _check_closed(self):
        if not self.socket:
            raise IOError('Stream is closed')

    def _maybe_add_error_listener(self):
        if self._state is None and self._pending_callbacks == 0:
            if self.socket is None:
                cb = self._close_callback
                if cb is not None:
                    self._close_callback = None
                    self._run_callback(cb)
            else:
                self._add_io_state(ioloop.IOLoop.READ)
        return

    def _add_io_state(self, state):
        """Adds `state` (IOLoop.{READ,WRITE} flags) to our event handler.

        Implementation notes: Reads and writes have a fast path and a
        slow path.  The fast path reads synchronously from socket
        buffers, while the slow path uses `_add_io_state` to schedule
        an IOLoop callback.  Note that in both cases, the callback is
        run asynchronously with `_run_callback`.

        To detect closed connections, we must have called
        `_add_io_state` at some point, but we want to delay this as
        much as possible so we don't have to set an `IOLoop.ERROR`
        listener that will be overwritten by the next slow-path
        operation.  As long as there are callbacks scheduled for
        fast-path ops, those callbacks may do more reads.
        If a sequence of fast-path ops do not end in a slow-path op,
        (e.g. for an @asynchronous long-poll request), we must add
        the error handler.  This is done in `_run_callback` and `write`
        (since the write callback is optional so we can have a
        fast-path write with no `_run_callback`)
        """
        if self.socket is None:
            return
        else:
            if self._state is None:
                self._state = ioloop.IOLoop.ERROR | state
                with stack_context.NullContext():
                    self.io_loop.add_handler(self.socket.fileno(), self._handle_events, self._state)
            elif not self._state & state:
                self._state = self._state | state
                self.io_loop.update_handler(self.socket.fileno(), self._state)
            return


class SSLIOStream(IOStream):
    """A utility class to write to and read from a non-blocking SSL socket.

    If the socket passed to the constructor is already connected,
    it should be wrapped with::

        ssl.wrap_socket(sock, do_handshake_on_connect=False, **kwargs)

    before constructing the SSLIOStream.  Unconnected sockets will be
    wrapped when IOStream.connect is finished.
    """

    def __init__(self, *args, **kwargs):
        """Creates an SSLIOStream.

        If a dictionary is provided as keyword argument ssl_options,
        it will be used as additional keyword arguments to ssl.wrap_socket.
        """
        self._ssl_options = kwargs.pop('ssl_options', {})
        super(SSLIOStream, self).__init__(*args, **kwargs)
        self._ssl_accepting = True
        self._handshake_reading = False
        self._handshake_writing = False

    def reading(self):
        return self._handshake_reading or super(SSLIOStream, self).reading()

    def writing(self):
        return self._handshake_writing or super(SSLIOStream, self).writing()

    def _do_ssl_handshake(self):
        try:
            self._handshake_reading = False
            self._handshake_writing = False
            self.socket.do_handshake()
        except ssl.SSLError as err:
            if err.args[0] == ssl.SSL_ERROR_WANT_READ:
                self._handshake_reading = True
                return
            if err.args[0] == ssl.SSL_ERROR_WANT_WRITE:
                self._handshake_writing = True
                return
            if err.args[0] in (ssl.SSL_ERROR_EOF,
             ssl.SSL_ERROR_ZERO_RETURN):
                return self.close()
            if err.args[0] == ssl.SSL_ERROR_SSL:
                logging.warning('SSL Error on %d: %s', self.socket.fileno(), err)
                return self.close()
            raise
        except socket.error as err:
            if err.args[0] == errno.ECONNABORTED:
                return self.close()
        else:
            self._ssl_accepting = False
            super(SSLIOStream, self)._handle_connect()

    def _handle_read(self):
        if self._ssl_accepting:
            self._do_ssl_handshake()
            return
        super(SSLIOStream, self)._handle_read()

    def _handle_write(self):
        if self._ssl_accepting:
            self._do_ssl_handshake()
            return
        super(SSLIOStream, self)._handle_write()

    def _handle_connect(self):
        self.socket = ssl.wrap_socket(self.socket, do_handshake_on_connect=False, **self._ssl_options)

    def _read_from_socket(self):
        if self._ssl_accepting:
            return None
        else:
            try:
                chunk = self.socket.read(self.read_chunk_size)
            except ssl.SSLError as e:
                if e.args[0] == ssl.SSL_ERROR_WANT_READ:
                    return None
                raise
            except socket.error as e:
                if e.args[0] in (errno.EWOULDBLOCK, errno.EAGAIN):
                    return None
                raise

            if not chunk:
                self.close()
                return None
            return chunk


def _merge_prefix(deque, size):
    """Replace the first entries in a deque of strings with a single
    string of up to size bytes.

    >>> d = collections.deque(['abc', 'de', 'fghi', 'j'])
    >>> _merge_prefix(d, 5); print d
    deque(['abcde', 'fghi', 'j'])

    Strings will be split as necessary to reach the desired size.
    >>> _merge_prefix(d, 7); print d
    deque(['abcdefg', 'hi', 'j'])

    >>> _merge_prefix(d, 3); print d
    deque(['abc', 'defg', 'hi', 'j'])

    >>> _merge_prefix(d, 100); print d
    deque(['abcdefghij'])
    """
    if len(deque) == 1 and len(deque[0]) <= size:
        return
    prefix = []
    remaining = size
    while deque and remaining > 0:
        chunk = deque.popleft()
        if len(chunk) > remaining:
            deque.appendleft(chunk[remaining:])
            chunk = chunk[:remaining]
        prefix.append(chunk)
        remaining -= len(chunk)

    if prefix:
        deque.appendleft(type(prefix[0])().join(prefix))
    if not deque:
        deque.appendleft(b(''))


def doctests():
    import doctest
    return doctest.DocTestSuite()