# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./build/lib.linux-x86_64-2.7/serial/serialutil.py
# Compiled at: 2015-09-22 17:19:55
import io
try:
    memoryview
except (NameError, AttributeError):

    class memoryview(object):
        pass


try:
    unicode
except (NameError, AttributeError):
    unicode = str

def iterbytes(b):
    """Iterate over bytes, returning bytes instead of ints (python3)"""
    if isinstance(b, memoryview):
        b = b.tobytes()
    x = 0
    while True:
        a = b[x:x + 1]
        x += 1
        if a:
            yield a
        else:
            break


def to_bytes(seq):
    """convert a sequence to a bytes type"""
    if isinstance(seq, bytes):
        return seq
    if isinstance(seq, bytearray):
        return bytes(seq)
    if isinstance(seq, memoryview):
        return seq.tobytes()
    if isinstance(seq, unicode):
        raise TypeError('unicode strings are not supported, please encode to bytes: %r' % (seq,))
    else:
        b = bytearray()
        for item in seq:
            if isinstance(item, bytes):
                item = ord(item)
            b.append(item)

        return bytes(b)


XON = to_bytes([17])
XOFF = to_bytes([19])
CR = to_bytes([13])
LF = to_bytes([10])
PARITY_NONE, PARITY_EVEN, PARITY_ODD, PARITY_MARK, PARITY_SPACE = (
 'N', 'E', 'O', 'M', 'S')
STOPBITS_ONE, STOPBITS_ONE_POINT_FIVE, STOPBITS_TWO = (1, 1.5, 2)
FIVEBITS, SIXBITS, SEVENBITS, EIGHTBITS = (5, 6, 7, 8)
PARITY_NAMES = {PARITY_NONE: 'None', 
   PARITY_EVEN: 'Even', 
   PARITY_ODD: 'Odd', 
   PARITY_MARK: 'Mark', 
   PARITY_SPACE: 'Space'}

class SerialException(IOError):
    """Base class for serial port related exceptions."""
    pass


class SerialTimeoutException(SerialException):
    """Write timeouts give an exception"""
    pass


writeTimeoutError = SerialTimeoutException('Write timeout')
portNotOpenError = SerialException('Attempting to use a port that is not open')

class SerialBase(io.RawIOBase):
    """    Serial port base class. Provides __init__ function and properties to
    get/set port settings.
    """
    BAUDRATES = (50, 75, 110, 134, 150, 200, 300, 600, 1200, 1800, 2400, 4800, 9600,
                 19200, 38400, 57600, 115200, 230400, 460800, 500000, 576000, 921600,
                 1000000, 1152000, 1500000, 2000000, 2500000, 3000000, 3500000, 4000000)
    BYTESIZES = (FIVEBITS, SIXBITS, SEVENBITS, EIGHTBITS)
    PARITIES = (PARITY_NONE, PARITY_EVEN, PARITY_ODD, PARITY_MARK, PARITY_SPACE)
    STOPBITS = (STOPBITS_ONE, STOPBITS_ONE_POINT_FIVE, STOPBITS_TWO)

    def __init__(self, port=None, baudrate=9600, bytesize=EIGHTBITS, parity=PARITY_NONE, stopbits=STOPBITS_ONE, timeout=None, xonxoff=False, rtscts=False, write_timeout=None, dsrdtr=False, inter_byte_timeout=None):
        """        Initialize comm port object. If a port is given, then the port will be
        opened immediately. Otherwise a Serial port object in closed state
        is returned.
        """
        self.is_open = False
        self._port = None
        self._baudrate = None
        self._bytesize = None
        self._parity = None
        self._stopbits = None
        self._timeout = None
        self._write_timeout = None
        self._xonxoff = None
        self._rtscts = None
        self._dsrdtr = None
        self._inter_byte_timeout = None
        self._rs485_mode = None
        self._rts_state = True
        self._dtr_state = True
        self._break_state = False
        self.port = port
        self.baudrate = baudrate
        self.bytesize = bytesize
        self.parity = parity
        self.stopbits = stopbits
        self.timeout = timeout
        self.write_timeout = write_timeout
        self.xonxoff = xonxoff
        self.rtscts = rtscts
        self.dsrdtr = dsrdtr
        self.inter_character_timeout = inter_byte_timeout
        if port is not None:
            self.open()
        return

    @property
    def port(self):
        """        Get the current port setting. The value that was passed on init or using
        setPort() is passed back. See also the attribute portstr which contains
        the name of the port as a string.
        """
        return self._port

    @port.setter
    def port(self, port):
        """        Change the port. The attribute portstr is set to a string that
        contains the name of the port.
        """
        was_open = self.is_open
        if was_open:
            self.close()
        self.portstr = port
        self._port = port
        self.name = self.portstr
        if was_open:
            self.open()

    @property
    def baudrate(self):
        """Get the current baud rate setting."""
        return self._baudrate

    @baudrate.setter
    def baudrate(self, baudrate):
        """        Change baud rate. It raises a ValueError if the port is open and the
        baud rate is not possible. If the port is closed, then the value is
        accepted and the exception is raised when the port is opened.
        """
        try:
            b = int(baudrate)
        except TypeError:
            raise ValueError('Not a valid baudrate: %r' % (baudrate,))

        if b <= 0:
            raise ValueError('Not a valid baudrate: %r' % (baudrate,))
        self._baudrate = b
        if self.is_open:
            self._reconfigure_port()

    @property
    def bytesize(self):
        """Get the current byte size setting."""
        return self._bytesize

    @bytesize.setter
    def bytesize(self, bytesize):
        """Change byte size."""
        if bytesize not in self.BYTESIZES:
            raise ValueError('Not a valid byte size: %r' % (bytesize,))
        self._bytesize = bytesize
        if self.is_open:
            self._reconfigure_port()

    @property
    def parity(self):
        """Get the current parity setting."""
        return self._parity

    @parity.setter
    def parity(self, parity):
        """Change parity setting."""
        if parity not in self.PARITIES:
            raise ValueError('Not a valid parity: %r' % (parity,))
        self._parity = parity
        if self.is_open:
            self._reconfigure_port()

    @property
    def stopbits(self):
        """Get the current stop bits setting."""
        return self._stopbits

    @stopbits.setter
    def stopbits(self, stopbits):
        """Change stop bits size."""
        if stopbits not in self.STOPBITS:
            raise ValueError('Not a valid stop bit size: %r' % (stopbits,))
        self._stopbits = stopbits
        if self.is_open:
            self._reconfigure_port()

    @property
    def timeout(self):
        """Get the current timeout setting."""
        return self._timeout

    @timeout.setter
    def timeout(self, timeout):
        """Change timeout setting."""
        if timeout is not None:
            try:
                timeout + 1
            except TypeError:
                raise ValueError('Not a valid timeout: %r' % (timeout,))

            if timeout < 0:
                raise ValueError('Not a valid timeout: %r' % (timeout,))
        self._timeout = timeout
        if self.is_open:
            self._reconfigure_port()
        return

    @property
    def write_timeout(self):
        """Get the current timeout setting."""
        return self._write_timeout

    @write_timeout.setter
    def write_timeout(self, timeout):
        """Change timeout setting."""
        if timeout is not None:
            if timeout < 0:
                raise ValueError('Not a valid timeout: %r' % (timeout,))
            try:
                timeout + 1
            except TypeError:
                raise ValueError('Not a valid timeout: %r' % timeout)

        self._write_timeout = timeout
        if self.is_open:
            self._reconfigure_port()
        return

    @property
    def inter_byte_timeout(self):
        """Get the current inter-character timeout setting."""
        return self._inter_byte_timeout

    @inter_byte_timeout.setter
    def inter_byte_timeout(self, ic_timeout):
        """Change inter-byte timeout setting."""
        if ic_timeout is not None:
            if ic_timeout < 0:
                raise ValueError('Not a valid timeout: %r' % ic_timeout)
            try:
                ic_timeout + 1
            except TypeError:
                raise ValueError('Not a valid timeout: %r' % ic_timeout)

        self._inter_byte_timeout = ic_timeout
        if self.is_open:
            self._reconfigure_port()
        return

    @property
    def xonxoff(self):
        """Get the current XON/XOFF setting."""
        return self._xonxoff

    @xonxoff.setter
    def xonxoff(self, xonxoff):
        """Change XON/XOFF setting."""
        self._xonxoff = xonxoff
        if self.is_open:
            self._reconfigure_port()

    @property
    def rtscts(self):
        """Get the current RTS/CTS flow control setting."""
        return self._rtscts

    @rtscts.setter
    def rtscts(self, rtscts):
        """Change RTS/CTS flow control setting."""
        self._rtscts = rtscts
        if self.is_open:
            self._reconfigure_port()

    @property
    def dsrdtr(self):
        """Get the current DSR/DTR flow control setting."""
        return self._dsrdtr

    @dsrdtr.setter
    def dsrdtr(self, dsrdtr=None):
        """Change DsrDtr flow control setting."""
        if dsrdtr is None:
            self._dsrdtr = self._rtscts
        else:
            self._dsrdtr = dsrdtr
        if self.is_open:
            self._reconfigure_port()
        return

    @property
    def rts(self):
        return self._rts_state

    @rts.setter
    def rts(self, value):
        self._rts_state = value
        if self.is_open:
            self._update_rts_state()

    @property
    def dtr(self):
        return self._dtr_state

    @dtr.setter
    def dtr(self, value):
        self._dtr_state = value
        if self.is_open:
            self._update_dtr_state()

    @property
    def break_condition(self):
        return self._break_state

    @break_condition.setter
    def break_condition(self, value):
        self._break_state = value
        if self.is_open:
            self._update_break_state()

    @property
    def rs485_mode(self):
        """        Enable RS485 mode and apply new settings, set to None to disable.
        See serial.rs485.RS485Settings for more info about the value.
        """
        return self._rs485_mode

    @rs485_mode.setter
    def rs485_mode(self, rs485_settings):
        self._rs485_mode = rs485_settings
        if self.is_open:
            self._reconfigure_port()

    _SAVED_SETTINGS = ('baudrate', 'bytesize', 'parity', 'stopbits', 'xonxoff', 'dsrdtr',
                       'rtscts', 'timeout', 'write_timeout', 'inter_byte_timeout')

    def get_settings(self):
        """        Get current port settings as a dictionary. For use with
        apply_settings().
        """
        return dict([ (key, getattr(self, '_' + key)) for key in self._SAVED_SETTINGS ])

    def apply_settings(self, d):
        """        Apply stored settings from a dictionary returned from
        get_settings(). It's allowed to delete keys from the dictionary. These
        values will simply left unchanged.
        """
        for key in self._SAVED_SETTINGS:
            if key in d and d[key] != getattr(self, '_' + key):
                setattr(self, key, d[key])

    def __repr__(self):
        """String representation of the current port settings and its state."""
        return '%s<id=0x%x, open=%s>(port=%r, baudrate=%r, bytesize=%r, parity=%r, stopbits=%r, timeout=%r, xonxoff=%r, rtscts=%r, dsrdtr=%r)' % (
         self.__class__.__name__,
         id(self),
         self.is_open,
         self.portstr,
         self.baudrate,
         self.bytesize,
         self.parity,
         self.stopbits,
         self.timeout,
         self.xonxoff,
         self.rtscts,
         self.dsrdtr)

    def readable(self):
        return True

    def writable(self):
        return True

    def seekable(self):
        return False

    def readinto(self, b):
        data = self.read(len(b))
        n = len(data)
        try:
            b[:n] = data
        except TypeError as err:
            import array
            if not isinstance(b, array.array):
                raise err
            b[:n] = array.array('b', data)

        return n

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        self.close()

    def send_break(self, duration=0.25):
        """        Send break condition. Timed, returns to idle state after given
        duration.
        """
        if not self.is_open:
            raise portNotOpenError
        self.break_condition = True
        time.sleep(duration)
        self.break_condition = False

    def flushInput(self):
        self.reset_input_buffer()

    def flushOutput(self):
        self.reset_output_buffer()

    def inWaiting(self):
        return self.in_waiting

    def sendBreak(self, duration=0.25):
        self.send_break(duration)

    def setRTS(self, value=1):
        self.rts = value

    def setDTR(self, value=1):
        self.dtr = value

    def getCTS(self):
        return self.cts

    def getDSR(self):
        return self.dsr

    def getRI(self):
        return self.ri

    def getCD(self):
        return self.cd

    @property
    def writeTimeout(self):
        return self.write_timeout

    @writeTimeout.setter
    def writeTimeout(self, timeout):
        self.write_timeout = timeout

    @property
    def interCharTimeout(self):
        return self.inter_byte_timeout

    @interCharTimeout.setter
    def interCharTimeout(self, interCharTimeout):
        self.inter_byte_timeout = interCharTimeout

    def getSettingsDict(self):
        return self.get_settings()

    def applySettingsDict(self, d):
        self.apply_settings(d)

    def isOpen(self):
        return self.is_open

    def read_until(self, terminator=LF, size=None):
        """        Read until a termination sequence is found ('
' by default), the size
        is exceeded or until timeout occurs.
        """
        lenterm = len(terminator)
        line = bytearray()
        while True:
            c = self.read(1)
            if c:
                line += c
                if line[-lenterm:] == terminator:
                    break
                if size is not None and len(line) >= size:
                    break
            else:
                break

        return bytes(line)

    def iread_until(self, *args, **kwargs):
        """        Read lines, implemented as generator. It will raise StopIteration on
        timeout (empty read).
        """
        while True:
            line = self.read_until(*args, **kwargs)
            if not line:
                break
            yield line


if __name__ == '__main__':
    import sys
    s = SerialBase()
    sys.stdout.write('port name:  %s\n' % s.name)
    sys.stdout.write('baud rates: %s\n' % s.BAUDRATES)
    sys.stdout.write('byte sizes: %s\n' % s.BYTESIZES)
    sys.stdout.write('parities:   %s\n' % s.PARITIES)
    sys.stdout.write('stop bits:  %s\n' % s.STOPBITS)
    sys.stdout.write('%s\n' % s)