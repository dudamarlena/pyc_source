# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\ISEN\AppData\Local\Temp\pip-install-57ghrzot\pyserial\serial\urlhandler\protocol_loop.py
# Compiled at: 2019-09-23 21:15:07
# Size of source mod 2**32: 10119 bytes
import logging, numbers, time
try:
    import urlparse
except ImportError:
    import urllib.parse as urlparse

try:
    import queue
except ImportError:
    import Queue as queue

from serial.serialutil import SerialBase, SerialException, to_bytes, iterbytes, writeTimeoutError, portNotOpenError
LOGGER_LEVELS = {'debug':logging.DEBUG, 
 'info':logging.INFO, 
 'warning':logging.WARNING, 
 'error':logging.ERROR}

class Serial(SerialBase):
    __doc__ = 'Serial port implementation that simulates a loop back connection in plain software.'
    BAUDRATES = (50, 75, 110, 134, 150, 200, 300, 600, 1200, 1800, 2400, 4800, 9600,
                 19200, 38400, 57600, 115200)

    def __init__(self, *args, **kwargs):
        self.buffer_size = 4096
        self.queue = None
        self.logger = None
        self._cancel_write = False
        (super(Serial, self).__init__)(*args, **kwargs)

    def open(self):
        """        Open port with current settings. This may throw a SerialException
        if the port cannot be opened.
        """
        if self.is_open:
            raise SerialException('Port is already open.')
        else:
            self.logger = None
            self.queue = queue.Queue(self.buffer_size)
            if self._port is None:
                raise SerialException('Port must be configured before it can be used.')
            self.from_url(self.port)
            self._reconfigure_port()
            self.is_open = True
            if not self._dsrdtr:
                self._update_dtr_state()
            self._rtscts or self._update_rts_state()
        self.reset_input_buffer()
        self.reset_output_buffer()

    def close(self):
        if self.is_open:
            self.is_open = False
            try:
                self.queue.put_nowait(None)
            except queue.Full:
                pass

        super(Serial, self).close()

    def _reconfigure_port--- This code section failed: ---

 L.  94         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                _baudrate
                6  LOAD_GLOBAL              numbers
                8  LOAD_ATTR                Integral
               10  CALL_FUNCTION_2       2  '2 positional arguments'
               12  POP_JUMP_IF_FALSE    38  'to 38'
               14  LOAD_CONST               0
               16  LOAD_FAST                'self'
               18  LOAD_ATTR                _baudrate
               20  DUP_TOP          
               22  ROT_THREE        
               24  COMPARE_OP               <
               26  POP_JUMP_IF_FALSE    36  'to 36'
               28  LOAD_CONST               4294967296
               30  COMPARE_OP               <
               32  POP_JUMP_IF_TRUE     54  'to 54'
               34  JUMP_FORWARD         38  'to 38'
             36_0  COME_FROM            26  '26'
               36  POP_TOP          
             38_0  COME_FROM            34  '34'
             38_1  COME_FROM            12  '12'

 L.  95        38  LOAD_GLOBAL              ValueError
               40  LOAD_STR                 'invalid baudrate: {!r}'
               42  LOAD_METHOD              format
               44  LOAD_FAST                'self'
               46  LOAD_ATTR                _baudrate
               48  CALL_METHOD_1         1  '1 positional argument'
               50  CALL_FUNCTION_1       1  '1 positional argument'
               52  RAISE_VARARGS_1       1  'exception instance'
             54_0  COME_FROM            32  '32'

 L.  96        54  LOAD_FAST                'self'
               56  LOAD_ATTR                logger
               58  POP_JUMP_IF_FALSE    72  'to 72'

 L.  97        60  LOAD_FAST                'self'
               62  LOAD_ATTR                logger
               64  LOAD_METHOD              info
               66  LOAD_STR                 '_reconfigure_port()'
               68  CALL_METHOD_1         1  '1 positional argument'
               70  POP_TOP          
             72_0  COME_FROM            58  '58'

Parse error at or near `POP_TOP' instruction at offset 70

    def from_url(self, url):
        """extract host and port from an URL string"""
        parts = urlparse.urlsplit(url)
        if parts.scheme != 'loop':
            raise SerialException('expected a string in the form "loop://[?logging={debug|info|warning|error}]": not starting with loop:// ({!r})'.format(parts.scheme))
        try:
            for option, values in urlparse.parse_qs(parts.query, True).items():
                if option == 'logging':
                    logging.basicConfig()
                    self.logger = logging.getLogger('pySerial.loop')
                    self.logger.setLevel(LOGGER_LEVELS[values[0]])
                    self.logger.debug('enabled logging')
                else:
                    raise ValueError('unknown option: {!r}'.format(option))

        except ValueError as e:
            try:
                raise SerialException('expected a string in the form "loop://[?logging={debug|info|warning|error}]": {}'.format(e))
            finally:
                e = None
                del e

    @property
    def in_waiting(self):
        """Return the number of bytes currently in the input buffer."""
        if not self.is_open:
            raise portNotOpenError
        if self.logger:
            self.logger.debug('in_waiting -> {:d}'.format(self.queue.qsize()))
        return self.queue.qsize()

    def read(self, size=1):
        """        Read size bytes from the serial port. If a timeout is set it may
        return less characters as requested. With no timeout it will block
        until the requested number of bytes is read.
        """
        if not self.is_open:
            raise portNotOpenError
        if self._timeout is not None and self._timeout != 0:
            timeout = time.time() + self._timeout
        else:
            timeout = None
        data = bytearray()
        while size > 0 and self.is_open:
            try:
                b = self.queue.get(timeout=(self._timeout))
            except queue.Empty:
                if self._timeout == 0:
                    break
            else:
                if b is not None:
                    data += b
                    size -= 1
                else:
                    break
                break

        return bytes(data)

    def cancel_read(self):
        self.queue.put_nowait(None)

    def cancel_write(self):
        self._cancel_write = True

    def write(self, data):
        """        Output the given byte string over the serial port. Can block if the
        connection is blocked. May raise SerialException if the connection is
        closed.
        """
        self._cancel_write = False
        if not self.is_open:
            raise portNotOpenError
        else:
            data = to_bytes(data)
            time_used_to_send = 10.0 * len(data) / self._baudrate
            if self._write_timeout is not None and time_used_to_send > self._write_timeout:
                time_left = self._write_timeout
                while time_left > 0:
                    self._cancel_write or time.sleep(min(time_left, 0.5))
                    time_left -= 0.5

                if self._cancel_write:
                    return 0
                raise writeTimeoutError
        for byte in iterbytes(data):
            self.queue.put(byte, timeout=(self._write_timeout))

        return len(data)

    def reset_input_buffer(self):
        """Clear input buffer, discarding all that is in the buffer."""
        if not self.is_open:
            raise portNotOpenError
        else:
            if self.logger:
                self.logger.info('reset_input_buffer()')
            try:
                while self.queue.qsize():
                    self.queue.get_nowait()

            except queue.Empty:
                pass

    def reset_output_buffer(self):
        """        Clear output buffer, aborting the current output and
        discarding all that is in the buffer.
        """
        if not self.is_open:
            raise portNotOpenError
        else:
            if self.logger:
                self.logger.info('reset_output_buffer()')
            try:
                while self.queue.qsize():
                    self.queue.get_nowait()

            except queue.Empty:
                pass

    def _update_break_state(self):
        """        Set break: Controls TXD. When active, to transmitting is
        possible.
        """
        if self.logger:
            self.logger.info('_update_break_state({!r})'.format(self._break_state))

    def _update_rts_state(self):
        """Set terminal status line: Request To Send"""
        if self.logger:
            self.logger.info('_update_rts_state({!r}) -> state of CTS'.format(self._rts_state))

    def _update_dtr_state(self):
        """Set terminal status line: Data Terminal Ready"""
        if self.logger:
            self.logger.info('_update_dtr_state({!r}) -> state of DSR'.format(self._dtr_state))

    @property
    def cts(self):
        """Read terminal status line: Clear To Send"""
        if not self.is_open:
            raise portNotOpenError
        if self.logger:
            self.logger.info('CTS -> state of RTS ({!r})'.format(self._rts_state))
        return self._rts_state

    @property
    def dsr(self):
        """Read terminal status line: Data Set Ready"""
        if self.logger:
            self.logger.info('DSR -> state of DTR ({!r})'.format(self._dtr_state))
        return self._dtr_state

    @property
    def ri(self):
        """Read terminal status line: Ring Indicator"""
        if not self.is_open:
            raise portNotOpenError
        if self.logger:
            self.logger.info('returning dummy for RI')
        return False

    @property
    def cd(self):
        """Read terminal status line: Carrier Detect"""
        if not self.is_open:
            raise portNotOpenError
        if self.logger:
            self.logger.info('returning dummy for CD')
        return True


if __name__ == '__main__':
    import sys
    s = Serial('loop://')
    sys.stdout.write('{}\n'.format(s))
    sys.stdout.write('write...\n')
    s.write('hello\n')
    s.flush()
    sys.stdout.write('read: {!r}\n'.format(s.read(5)))
    s.close()