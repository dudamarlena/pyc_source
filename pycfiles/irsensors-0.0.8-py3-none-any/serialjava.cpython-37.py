# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\ISEN\AppData\Local\Temp\pip-install-57ghrzot\pyserial\serial\serialjava.py
# Compiled at: 2019-09-23 21:15:07
# Size of source mod 2**32: 8414 bytes
from serial.serialutil import *

def my_import(name):
    mod = __import__(name)
    components = name.split('.')
    for comp in components[1:]:
        mod = getattr(mod, comp)

    return mod


def detect_java_comm(names):
    """try given list of modules and return that imports"""
    for name in names:
        try:
            mod = my_import(name)
            mod.SerialPort
            return mod
        except (ImportError, AttributeError):
            pass

    raise ImportError('No Java Communications API implementation found')


comm = detect_java_comm([
 'javax.comm',
 'gnu.io'])

def device(portnumber):
    """Turn a port number into a device name"""
    enum = comm.CommPortIdentifier.getPortIdentifiers()
    ports = []
    while enum.hasMoreElements():
        el = enum.nextElement()
        if el.getPortType() == comm.CommPortIdentifier.PORT_SERIAL:
            ports.append(el)

    return ports[portnumber].getName()


class Serial(SerialBase):
    __doc__ = '    Serial port class, implemented with Java Communications API and\n    thus usable with jython and the appropriate java extension.\n    '

    def open(self):
        """        Open port with current settings. This may throw a SerialException
        if the port cannot be opened.
        """
        if self._port is None:
            raise SerialException('Port must be configured before it can be used.')
        else:
            if self.is_open:
                raise SerialException('Port is already open.')
            elif type(self._port) == type(''):
                portId = comm.CommPortIdentifier.getPortIdentifier(self._port)
            else:
                portId = comm.CommPortIdentifier.getPortIdentifier(device(self._port))
            try:
                self.sPort = portId.open('python serial module', 10)
            except Exception as msg:
                try:
                    self.sPort = None
                    raise SerialException('Could not open port: %s' % msg)
                finally:
                    msg = None
                    del msg

        self._reconfigurePort()
        self._instream = self.sPort.getInputStream()
        self._outstream = self.sPort.getOutputStream()
        self.is_open = True

    def _reconfigurePort(self):
        """Set communication parameters on opened port."""
        if not self.sPort:
            raise SerialException('Can only operate on a valid port handle')
        else:
            self.sPort.enableReceiveTimeout(30)
            if self._bytesize == FIVEBITS:
                jdatabits = comm.SerialPort.DATABITS_5
            else:
                if self._bytesize == SIXBITS:
                    jdatabits = comm.SerialPort.DATABITS_6
                else:
                    if self._bytesize == SEVENBITS:
                        jdatabits = comm.SerialPort.DATABITS_7
                    else:
                        if self._bytesize == EIGHTBITS:
                            jdatabits = comm.SerialPort.DATABITS_8
                        else:
                            raise ValueError('unsupported bytesize: %r' % self._bytesize)
            if self._stopbits == STOPBITS_ONE:
                jstopbits = comm.SerialPort.STOPBITS_1
            else:
                if self._stopbits == STOPBITS_ONE_POINT_FIVE:
                    jstopbits = comm.SerialPort.STOPBITS_1_5
                else:
                    if self._stopbits == STOPBITS_TWO:
                        jstopbits = comm.SerialPort.STOPBITS_2
                    else:
                        raise ValueError('unsupported number of stopbits: %r' % self._stopbits)
            if self._parity == PARITY_NONE:
                jparity = comm.SerialPort.PARITY_NONE
            else:
                if self._parity == PARITY_EVEN:
                    jparity = comm.SerialPort.PARITY_EVEN
                else:
                    if self._parity == PARITY_ODD:
                        jparity = comm.SerialPort.PARITY_ODD
                    else:
                        if self._parity == PARITY_MARK:
                            jparity = comm.SerialPort.PARITY_MARK
                        else:
                            if self._parity == PARITY_SPACE:
                                jparity = comm.SerialPort.PARITY_SPACE
                            else:
                                raise ValueError('unsupported parity type: %r' % self._parity)
            jflowin = jflowout = 0
            if self._rtscts:
                jflowin |= comm.SerialPort.FLOWCONTROL_RTSCTS_IN
                jflowout |= comm.SerialPort.FLOWCONTROL_RTSCTS_OUT
            if self._xonxoff:
                jflowin |= comm.SerialPort.FLOWCONTROL_XONXOFF_IN
                jflowout |= comm.SerialPort.FLOWCONTROL_XONXOFF_OUT
            self.sPort.setSerialPortParams(self._baudrate, jdatabits, jstopbits, jparity)
            self.sPort.setFlowControlMode(jflowin | jflowout)
            if self._timeout >= 0:
                self.sPort.enableReceiveTimeout(int(self._timeout * 1000))
            else:
                self.sPort.disableReceiveTimeout()

    def close(self):
        """Close port"""
        if self.is_open:
            if self.sPort:
                self._instream.close()
                self._outstream.close()
                self.sPort.close()
                self.sPort = None
            self.is_open = False

    @property
    def in_waiting(self):
        """Return the number of characters currently in the input buffer."""
        if not self.sPort:
            raise portNotOpenError
        return self._instream.available()

    def read(self, size=1):
        """        Read size bytes from the serial port. If a timeout is set it may
        return less characters as requested. With no timeout it will block
        until the requested number of bytes is read.
        """
        if not self.sPort:
            raise portNotOpenError
        read = bytearray()
        if size > 0:
            while len(read) < size:
                x = self._instream.read()
                if x == -1:
                    if self.timeout >= 0:
                        break
                else:
                    read.append(x)

        return bytes(read)

    def write(self, data):
        """Output the given string over the serial port."""
        if not self.sPort:
            raise portNotOpenError
        if not isinstance(data, (bytes, bytearray)):
            raise TypeError('expected %s or bytearray, got %s' % (bytes, type(data)))
        self._outstream.write(data)
        return len(data)

    def reset_input_buffer(self):
        """Clear input buffer, discarding all that is in the buffer."""
        if not self.sPort:
            raise portNotOpenError
        self._instream.skip(self._instream.available())

    def reset_output_buffer(self):
        """        Clear output buffer, aborting the current output and
        discarding all that is in the buffer.
        """
        if not self.sPort:
            raise portNotOpenError
        self._outstream.flush()

    def send_break(self, duration=0.25):
        """Send break condition. Timed, returns to idle state after given duration."""
        if not self.sPort:
            raise portNotOpenError
        self.sPort.sendBreak(duration * 1000.0)

    def _update_break_state(self):
        """Set break: Controls TXD. When active, to transmitting is possible."""
        if self.fd is None:
            raise portNotOpenError
        raise SerialException('The _update_break_state function is not implemented in java.')

    def _update_rts_state(self):
        """Set terminal status line: Request To Send"""
        if not self.sPort:
            raise portNotOpenError
        self.sPort.setRTS(self._rts_state)

    def _update_dtr_state(self):
        """Set terminal status line: Data Terminal Ready"""
        if not self.sPort:
            raise portNotOpenError
        self.sPort.setDTR(self._dtr_state)

    @property
    def cts(self):
        """Read terminal status line: Clear To Send"""
        if not self.sPort:
            raise portNotOpenError
        self.sPort.isCTS()

    @property
    def dsr(self):
        """Read terminal status line: Data Set Ready"""
        if not self.sPort:
            raise portNotOpenError
        self.sPort.isDSR()

    @property
    def ri(self):
        """Read terminal status line: Ring Indicator"""
        if not self.sPort:
            raise portNotOpenError
        self.sPort.isRI()

    @property
    def cd(self):
        """Read terminal status line: Carrier Detect"""
        if not self.sPort:
            raise portNotOpenError
        self.sPort.isCD()