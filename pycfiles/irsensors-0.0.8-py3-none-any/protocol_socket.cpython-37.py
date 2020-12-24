# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\ISEN\AppData\Local\Temp\pip-install-57ghrzot\pyserial\serial\urlhandler\protocol_socket.py
# Compiled at: 2019-09-23 21:15:07
# Size of source mod 2**32: 14130 bytes
import errno, logging, select, socket, time
try:
    import urlparse
except ImportError:
    import urllib.parse as urlparse

from serial.serialutil import SerialBase, SerialException, to_bytes, portNotOpenError, writeTimeoutError, Timeout
LOGGER_LEVELS = {'debug':logging.DEBUG, 
 'info':logging.INFO, 
 'warning':logging.WARNING, 
 'error':logging.ERROR}
POLL_TIMEOUT = 5

class Serial(SerialBase):
    __doc__ = 'Serial port implementation for plain sockets.'
    BAUDRATES = (50, 75, 110, 134, 150, 200, 300, 600, 1200, 1800, 2400, 4800, 9600,
                 19200, 38400, 57600, 115200)

    def open(self):
        """        Open port with current settings. This may throw a SerialException
        if the port cannot be opened.
        """
        self.logger = None
        if self._port is None:
            raise SerialException('Port must be configured before it can be used.')
        if self.is_open:
            raise SerialException('Port is already open.')
        try:
            self._socket = socket.create_connection((self.from_url(self.portstr)), timeout=POLL_TIMEOUT)
        except Exception as msg:
            try:
                self._socket = None
                raise SerialException('Could not open port {}: {}'.format(self.portstr, msg))
            finally:
                msg = None
                del msg

        self._socket.setblocking(False)
        self._reconfigure_port()
        self.is_open = True
        if not self._dsrdtr:
            self._update_dtr_state()
        if not self._rtscts:
            self._update_rts_state()
        self.reset_input_buffer()
        self.reset_output_buffer()

    def _reconfigure_port(self):
        """        Set communication parameters on opened port. For the socket://
        protocol all settings are ignored!
        """
        if self._socket is None:
            raise SerialException('Can only operate on open ports')
        if self.logger:
            self.logger.info('ignored port configuration change')

    def close(self):
        """Close port"""
        if self.is_open:
            if self._socket:
                try:
                    self._socket.shutdown(socket.SHUT_RDWR)
                    self._socket.close()
                except:
                    pass

                self._socket = None
            self.is_open = False
            time.sleep(0.3)

    def from_url(self, url):
        """extract host and port from an URL string"""
        parts = urlparse.urlsplit(url)
        if parts.scheme != 'socket':
            raise SerialException('expected a string in the form "socket://<host>:<port>[?logging={debug|info|warning|error}]": not starting with socket:// ({!r})'.format(parts.scheme))
        try:
            for option, values in urlparse.parse_qs(parts.query, True).items():
                if option == 'logging':
                    logging.basicConfig()
                    self.logger = logging.getLogger('pySerial.socket')
                    self.logger.setLevel(LOGGER_LEVELS[values[0]])
                    self.logger.debug('enabled logging')
                else:
                    raise ValueError('unknown option: {!r}'.format(option))

            if not 0 <= parts.port < 65536:
                raise ValueError('port not in range 0...65535')
        except ValueError as e:
            try:
                raise SerialException('expected a string in the form "socket://<host>:<port>[?logging={debug|info|warning|error}]": {}'.format(e))
            finally:
                e = None
                del e

        return (
         parts.hostname, parts.port)

    @property
    def in_waiting(self):
        """Return the number of bytes currently in the input buffer."""
        if not self.is_open:
            raise portNotOpenError
        lr, lw, lx = select.select([self._socket], [], [], 0)
        return len(lr)

    def read(self, size=1):
        """        Read size bytes from the serial port. If a timeout is set it may
        return less characters as requested. With no timeout it will block
        until the requested number of bytes is read.
        """
        if not self.is_open:
            raise portNotOpenError
        read = bytearray()
        timeout = Timeout(self._timeout)
        while len(read) < size:
            try:
                ready, _, _ = select.select([self._socket], [], [], timeout.time_left())
                if not ready:
                    break
                buf = self._socket.recv(size - len(read))
                if not buf:
                    raise SerialException('socket disconnected')
                read.extend(buf)
            except OSError as e:
                try:
                    if e.errno not in (errno.EAGAIN, errno.EALREADY, errno.EWOULDBLOCK, errno.EINPROGRESS, errno.EINTR):
                        raise SerialException('read failed: {}'.format(e))
                finally:
                    e = None
                    del e

            except (select.error, socket.error) as e:
                try:
                    if e[0] not in (errno.EAGAIN, errno.EALREADY, errno.EWOULDBLOCK, errno.EINPROGRESS, errno.EINTR):
                        raise SerialException('read failed: {}'.format(e))
                finally:
                    e = None
                    del e

            if timeout.expired():
                break

        return bytes(read)

    def write(self, data):
        """        Output the given byte string over the serial port. Can block if the
        connection is blocked. May raise SerialException if the connection is
        closed.
        """
        if not self.is_open:
            raise portNotOpenError
        d = to_bytes(data)
        tx_len = length = len(d)
        timeout = Timeout(self._write_timeout)
        while tx_len > 0:
            try:
                n = self._socket.send(d)
                if timeout.is_non_blocking:
                    return n
                if not timeout.is_infinite:
                    if timeout.expired():
                        raise writeTimeoutError
                    _, ready, _ = select.select([], [self._socket], [], timeout.time_left())
                    assert ready
                else:
                    assert timeout.time_left() is None
                    _, ready, _ = select.select([], [self._socket], [], None)
                    if not ready:
                        raise SerialException('write failed (select)')
                d = d[n:]
                tx_len -= n
            except SerialException:
                raise
            except OSError as e:
                try:
                    if e.errno not in (errno.EAGAIN, errno.EALREADY, errno.EWOULDBLOCK, errno.EINPROGRESS, errno.EINTR):
                        raise SerialException('write failed: {}'.format(e))
                finally:
                    e = None
                    del e

            except select.error as e:
                try:
                    if e[0] not in (errno.EAGAIN, errno.EALREADY, errno.EWOULDBLOCK, errno.EINPROGRESS, errno.EINTR):
                        raise SerialException('write failed: {}'.format(e))
                finally:
                    e = None
                    del e

            if timeout.is_non_blocking or timeout.expired():
                raise writeTimeoutError

        return length - len(d)

    def reset_input_buffer(self):
        """Clear input buffer, discarding all that is in the buffer."""
        if not self.is_open:
            raise portNotOpenError
        ready = True
        while ready:
            ready, _, _ = select.select([self._socket], [], [], 0)
            try:
                self._socket.recv(4096)
            except OSError as e:
                try:
                    if e.errno not in (errno.EAGAIN, errno.EALREADY, errno.EWOULDBLOCK, errno.EINPROGRESS, errno.EINTR):
                        raise SerialException('read failed: {}'.format(e))
                finally:
                    e = None
                    del e

            except (select.error, socket.error) as e:
                try:
                    if e[0] not in (errno.EAGAIN, errno.EALREADY, errno.EWOULDBLOCK, errno.EINPROGRESS, errno.EINTR):
                        raise SerialException('read failed: {}'.format(e))
                finally:
                    e = None
                    del e

    def reset_output_buffer(self):
        """        Clear output buffer, aborting the current output and
        discarding all that is in the buffer.
        """
        if not self.is_open:
            raise portNotOpenError
        if self.logger:
            self.logger.info('ignored reset_output_buffer')

    def send_break(self, duration=0.25):
        """        Send break condition. Timed, returns to idle state after given
        duration.
        """
        if not self.is_open:
            raise portNotOpenError
        if self.logger:
            self.logger.info('ignored send_break({!r})'.format(duration))

    def _update_break_state(self):
        """Set break: Controls TXD. When active, to transmitting is
        possible."""
        if self.logger:
            self.logger.info('ignored _update_break_state({!r})'.format(self._break_state))

    def _update_rts_state(self):
        """Set terminal status line: Request To Send"""
        if self.logger:
            self.logger.info('ignored _update_rts_state({!r})'.format(self._rts_state))

    def _update_dtr_state(self):
        """Set terminal status line: Data Terminal Ready"""
        if self.logger:
            self.logger.info('ignored _update_dtr_state({!r})'.format(self._dtr_state))

    @property
    def cts(self):
        """Read terminal status line: Clear To Send"""
        if not self.is_open:
            raise portNotOpenError
        if self.logger:
            self.logger.info('returning dummy for cts')
        return True

    @property
    def dsr(self):
        """Read terminal status line: Data Set Ready"""
        if not self.is_open:
            raise portNotOpenError
        if self.logger:
            self.logger.info('returning dummy for dsr')
        return True

    @property
    def ri(self):
        """Read terminal status line: Ring Indicator"""
        if not self.is_open:
            raise portNotOpenError
        if self.logger:
            self.logger.info('returning dummy for ri')
        return False

    @property
    def cd(self):
        """Read terminal status line: Carrier Detect"""
        if not self.is_open:
            raise portNotOpenError
        if self.logger:
            self.logger.info('returning dummy for cd)')
        return True

    def fileno(self):
        """Get the file handle of the underlying socket for use with select"""
        return self._socket.fileno()


if __name__ == '__main__':
    import sys
    s = Serial('socket://localhost:7000')
    sys.stdout.write('{}\n'.format(s))
    sys.stdout.write('write...\n')
    s.write(b'hello\n')
    s.flush()
    sys.stdout.write('read: {}\n'.format(s.read(5)))
    s.close()