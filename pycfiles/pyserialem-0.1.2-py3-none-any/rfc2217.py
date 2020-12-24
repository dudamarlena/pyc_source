# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ./build/lib.linux-x86_64-2.7/serial/rfc2217.py
# Compiled at: 2015-08-30 00:13:51
import logging, socket, struct, threading, time
try:
    import urlparse
except ImportError:
    import urllib.parse as urlparse

try:
    import Queue
except ImportError:
    import queue as Queue

import serial
from serial.serialutil import SerialBase, SerialException, to_bytes, iterbytes, portNotOpenError
LOGGER_LEVELS = {'debug': logging.DEBUG, 
   'info': logging.INFO, 
   'warning': logging.WARNING, 
   'error': logging.ERROR}
SE = b'\xf0'
NOP = b'\xf1'
DM = b'\xf2'
BRK = b'\xf3'
IP = b'\xf4'
AO = b'\xf5'
AYT = b'\xf6'
EC = b'\xf7'
EL = b'\xf8'
GA = b'\xf9'
SB = b'\xfa'
WILL = b'\xfb'
WONT = b'\xfc'
DO = b'\xfd'
DONT = b'\xfe'
IAC = b'\xff'
IAC_DOUBLED = b'\xff\xff'
BINARY = '\x00'
ECHO = '\x01'
SGA = '\x03'
COM_PORT_OPTION = ','
SET_BAUDRATE = '\x01'
SET_DATASIZE = '\x02'
SET_PARITY = '\x03'
SET_STOPSIZE = '\x04'
SET_CONTROL = '\x05'
NOTIFY_LINESTATE = '\x06'
NOTIFY_MODEMSTATE = '\x07'
FLOWCONTROL_SUSPEND = '\x08'
FLOWCONTROL_RESUME = '\t'
SET_LINESTATE_MASK = '\n'
SET_MODEMSTATE_MASK = '\x0b'
PURGE_DATA = '\x0c'
SERVER_SET_BAUDRATE = 'e'
SERVER_SET_DATASIZE = 'f'
SERVER_SET_PARITY = 'g'
SERVER_SET_STOPSIZE = 'h'
SERVER_SET_CONTROL = 'i'
SERVER_NOTIFY_LINESTATE = 'j'
SERVER_NOTIFY_MODEMSTATE = 'k'
SERVER_FLOWCONTROL_SUSPEND = 'l'
SERVER_FLOWCONTROL_RESUME = 'm'
SERVER_SET_LINESTATE_MASK = 'n'
SERVER_SET_MODEMSTATE_MASK = 'o'
SERVER_PURGE_DATA = 'p'
RFC2217_ANSWER_MAP = {SET_BAUDRATE: SERVER_SET_BAUDRATE, 
   SET_DATASIZE: SERVER_SET_DATASIZE, 
   SET_PARITY: SERVER_SET_PARITY, 
   SET_STOPSIZE: SERVER_SET_STOPSIZE, 
   SET_CONTROL: SERVER_SET_CONTROL, 
   NOTIFY_LINESTATE: SERVER_NOTIFY_LINESTATE, 
   NOTIFY_MODEMSTATE: SERVER_NOTIFY_MODEMSTATE, 
   FLOWCONTROL_SUSPEND: SERVER_FLOWCONTROL_SUSPEND, 
   FLOWCONTROL_RESUME: SERVER_FLOWCONTROL_RESUME, 
   SET_LINESTATE_MASK: SERVER_SET_LINESTATE_MASK, 
   SET_MODEMSTATE_MASK: SERVER_SET_MODEMSTATE_MASK, 
   PURGE_DATA: SERVER_PURGE_DATA}
SET_CONTROL_REQ_FLOW_SETTING = '\x00'
SET_CONTROL_USE_NO_FLOW_CONTROL = '\x01'
SET_CONTROL_USE_SW_FLOW_CONTROL = '\x02'
SET_CONTROL_USE_HW_FLOW_CONTROL = '\x03'
SET_CONTROL_REQ_BREAK_STATE = '\x04'
SET_CONTROL_BREAK_ON = '\x05'
SET_CONTROL_BREAK_OFF = '\x06'
SET_CONTROL_REQ_DTR = '\x07'
SET_CONTROL_DTR_ON = '\x08'
SET_CONTROL_DTR_OFF = '\t'
SET_CONTROL_REQ_RTS = '\n'
SET_CONTROL_RTS_ON = '\x0b'
SET_CONTROL_RTS_OFF = '\x0c'
SET_CONTROL_REQ_FLOW_SETTING_IN = '\r'
SET_CONTROL_USE_NO_FLOW_CONTROL_IN = '\x0e'
SET_CONTROL_USE_SW_FLOW_CONTOL_IN = '\x0f'
SET_CONTROL_USE_HW_FLOW_CONTOL_IN = '\x10'
SET_CONTROL_USE_DCD_FLOW_CONTROL = '\x11'
SET_CONTROL_USE_DTR_FLOW_CONTROL = '\x12'
SET_CONTROL_USE_DSR_FLOW_CONTROL = '\x13'
LINESTATE_MASK_TIMEOUT = 128
LINESTATE_MASK_SHIFTREG_EMPTY = 64
LINESTATE_MASK_TRANSREG_EMPTY = 32
LINESTATE_MASK_BREAK_DETECT = 16
LINESTATE_MASK_FRAMING_ERROR = 8
LINESTATE_MASK_PARTIY_ERROR = 4
LINESTATE_MASK_OVERRUN_ERROR = 2
LINESTATE_MASK_DATA_READY = 1
MODEMSTATE_MASK_CD = 128
MODEMSTATE_MASK_RI = 64
MODEMSTATE_MASK_DSR = 32
MODEMSTATE_MASK_CTS = 16
MODEMSTATE_MASK_CD_CHANGE = 8
MODEMSTATE_MASK_RI_CHANGE = 4
MODEMSTATE_MASK_DSR_CHANGE = 2
MODEMSTATE_MASK_CTS_CHANGE = 1
PURGE_RECEIVE_BUFFER = '\x01'
PURGE_TRANSMIT_BUFFER = '\x02'
PURGE_BOTH_BUFFERS = '\x03'
RFC2217_PARITY_MAP = {serial.PARITY_NONE: 1, 
   serial.PARITY_ODD: 2, 
   serial.PARITY_EVEN: 3, 
   serial.PARITY_MARK: 4, 
   serial.PARITY_SPACE: 5}
RFC2217_REVERSE_PARITY_MAP = dict((v, k) for k, v in RFC2217_PARITY_MAP.items())
RFC2217_STOPBIT_MAP = {serial.STOPBITS_ONE: 1, 
   serial.STOPBITS_ONE_POINT_FIVE: 3, 
   serial.STOPBITS_TWO: 2}
RFC2217_REVERSE_STOPBIT_MAP = dict((v, k) for k, v in RFC2217_STOPBIT_MAP.items())
M_NORMAL = 0
M_IAC_SEEN = 1
M_NEGOTIATE = 2
REQUESTED = 'REQUESTED'
ACTIVE = 'ACTIVE'
INACTIVE = 'INACTIVE'
REALLY_INACTIVE = 'REALLY_INACTIVE'

class TelnetOption(object):
    """Manage a single telnet option, keeps track of DO/DONT WILL/WONT."""

    def __init__(self, connection, name, option, send_yes, send_no, ack_yes, ack_no, initial_state, activation_callback=None):
        """        Initialize option.
        :param connection: connection used to transmit answers
        :param name: a readable name for debug outputs
        :param send_yes: what to send when option is to be enabled.
        :param send_no: what to send when option is to be disabled.
        :param ack_yes: what to expect when remote agrees on option.
        :param ack_no: what to expect when remote disagrees on option.
        :param initial_state: options initialized with REQUESTED are tried to
            be enabled on startup. use INACTIVE for all others.
        """
        self.connection = connection
        self.name = name
        self.option = option
        self.send_yes = send_yes
        self.send_no = send_no
        self.ack_yes = ack_yes
        self.ack_no = ack_no
        self.state = initial_state
        self.active = False
        self.activation_callback = activation_callback

    def __repr__(self):
        """String for debug outputs"""
        return '%s:%s(%s)' % (self.name, self.active, self.state)

    def process_incoming(self, command):
        """        A DO/DONT/WILL/WONT was received for this option, update state and
        answer when needed.
        """
        if command == self.ack_yes:
            if self.state is REQUESTED:
                self.state = ACTIVE
                self.active = True
                if self.activation_callback is not None:
                    self.activation_callback()
            elif self.state is ACTIVE:
                pass
            elif self.state is INACTIVE:
                self.state = ACTIVE
                self.connection.telnetSendOption(self.send_yes, self.option)
                self.active = True
                if self.activation_callback is not None:
                    self.activation_callback()
            elif self.state is REALLY_INACTIVE:
                self.connection.telnetSendOption(self.send_no, self.option)
            else:
                raise ValueError('option in illegal state %r' % self)
        elif command == self.ack_no:
            if self.state is REQUESTED:
                self.state = INACTIVE
                self.active = False
            elif self.state is ACTIVE:
                self.state = INACTIVE
                self.connection.telnetSendOption(self.send_no, self.option)
                self.active = False
            elif self.state is INACTIVE:
                pass
            elif self.state is REALLY_INACTIVE:
                pass
            else:
                raise ValueError('option in illegal state %r' % self)
        return


class TelnetSubnegotiation(object):
    """    A object to handle subnegotiation of options. In this case actually
    sub-sub options for RFC 2217. It is used to track com port options.
    """

    def __init__(self, connection, name, option, ack_option=None):
        if ack_option is None:
            ack_option = option
        self.connection = connection
        self.name = name
        self.option = option
        self.value = None
        self.ack_option = ack_option
        self.state = INACTIVE
        return

    def __repr__(self):
        """String for debug outputs."""
        return '%s:%s' % (self.name, self.state)

    def set(self, value):
        """        Request a change of the value. a request is sent to the server. if
        the client needs to know if the change is performed he has to check the
        state of this object.
        """
        self.value = value
        self.state = REQUESTED
        self.connection.rfc2217SendSubnegotiation(self.option, self.value)
        if self.connection.logger:
            self.connection.logger.debug('SB Requesting %s -> %r' % (self.name, self.value))

    def isReady(self):
        """        Check if answer from server has been received. when server rejects
        the change, raise a ValueError.
        """
        if self.state == REALLY_INACTIVE:
            raise ValueError('remote rejected value for option %r' % self.name)
        return self.state == ACTIVE

    active = property(isReady)

    def wait(self, timeout=3):
        """        Wait until the subnegotiation has been acknowledged or timeout. It
        can also throw a value error when the answer from the server does not
        match the value sent.
        """
        timeout_time = time.time() + timeout
        while time.time() < timeout_time:
            time.sleep(0.05)
            if self.isReady():
                break
        else:
            raise SerialException('timeout while waiting for option %r' % self.name)

    def checkAnswer(self, suboption):
        """        Check an incoming subnegotiation block. The parameter already has
        cut off the header like sub option number and com port option value.
        """
        if self.value == suboption[:len(self.value)]:
            self.state = ACTIVE
        else:
            self.state = REALLY_INACTIVE
        if self.connection.logger:
            self.connection.logger.debug('SB Answer %s -> %r -> %s' % (self.name, suboption, self.state))


class Serial(SerialBase):
    """Serial port implementation for RFC 2217 remote serial ports."""
    BAUDRATES = (50, 75, 110, 134, 150, 200, 300, 600, 1200, 1800, 2400, 4800, 9600,
                 19200, 38400, 57600, 115200)

    def open(self):
        """        Open port with current settings. This may throw a SerialException
        if the port cannot be opened.
        """
        self.logger = None
        self._ignore_set_control_answer = False
        self._poll_modem_state = False
        self._network_timeout = 3
        if self._port is None:
            raise SerialException('Port must be configured before it can be used.')
        if self.is_open:
            raise SerialException('Port is already open.')
        try:
            self._socket = socket.create_connection(self.from_url(self.portstr))
            self._socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        except Exception as msg:
            self._socket = None
            raise SerialException('Could not open port %s: %s' % (self.portstr, msg))

        self._socket.settimeout(5)
        self._read_buffer = Queue.Queue()
        self._write_lock = threading.Lock()
        mandadory_options = [
         TelnetOption(self, 'we-BINARY', BINARY, WILL, WONT, DO, DONT, INACTIVE),
         TelnetOption(self, 'we-RFC2217', COM_PORT_OPTION, WILL, WONT, DO, DONT, REQUESTED)]
        self._telnet_options = [
         TelnetOption(self, 'ECHO', ECHO, DO, DONT, WILL, WONT, REQUESTED),
         TelnetOption(self, 'we-SGA', SGA, WILL, WONT, DO, DONT, REQUESTED),
         TelnetOption(self, 'they-SGA', SGA, DO, DONT, WILL, WONT, REQUESTED),
         TelnetOption(self, 'they-BINARY', BINARY, DO, DONT, WILL, WONT, INACTIVE),
         TelnetOption(self, 'they-RFC2217', COM_PORT_OPTION, DO, DONT, WILL, WONT, REQUESTED)] + mandadory_options
        self._rfc2217_port_settings = {'baudrate': TelnetSubnegotiation(self, 'baudrate', SET_BAUDRATE, SERVER_SET_BAUDRATE), 
           'datasize': TelnetSubnegotiation(self, 'datasize', SET_DATASIZE, SERVER_SET_DATASIZE), 
           'parity': TelnetSubnegotiation(self, 'parity', SET_PARITY, SERVER_SET_PARITY), 
           'stopsize': TelnetSubnegotiation(self, 'stopsize', SET_STOPSIZE, SERVER_SET_STOPSIZE)}
        self._rfc2217_options = {'purge': TelnetSubnegotiation(self, 'purge', PURGE_DATA, SERVER_PURGE_DATA), 
           'control': TelnetSubnegotiation(self, 'control', SET_CONTROL, SERVER_SET_CONTROL)}
        self._rfc2217_options.update(self._rfc2217_port_settings)
        self._linestate = 0
        self._modemstate = None
        self._modemstate_expires = 0
        self._remote_suspend_flow = False
        self._thread = threading.Thread(target=self._telnetReadLoop)
        self._thread.setDaemon(True)
        self._thread.setName('pySerial RFC 2217 reader thread for %s' % (self._port,))
        self._thread.start()
        for option in self._telnet_options:
            if option.state is REQUESTED:
                self.telnetSendOption(option.send_yes, option.option)

        timeout_time = time.time() + self._network_timeout
        while time.time() < timeout_time:
            time.sleep(0.05)
            if sum(o.active for o in mandadory_options) == sum(o.state != INACTIVE for o in mandadory_options):
                break
        else:
            raise SerialException('Remote does not seem to support RFC2217 or BINARY mode %r' % mandadory_options)

        if self.logger:
            self.logger.info('Negotiated options: %s' % self._telnet_options)
        self._reconfigure_port()
        self.is_open = True
        if not self._dsrdtr:
            self._update_dtr_state()
        if not self._rtscts:
            self._update_rts_state()
        self.reset_input_buffer()
        self.reset_output_buffer()
        return

    def _reconfigure_port(self):
        """Set communication parameters on opened port."""
        if self._socket is None:
            raise SerialException('Can only operate on open ports')
        if self._write_timeout is not None:
            raise NotImplementedError('write_timeout is currently not supported')
        if not 0 < self._baudrate < 4294967296:
            raise ValueError('invalid baudrate: %r' % self._baudrate)
        self._rfc2217_port_settings['baudrate'].set(struct.pack('!I', self._baudrate))
        self._rfc2217_port_settings['datasize'].set(struct.pack('!B', self._bytesize))
        self._rfc2217_port_settings['parity'].set(struct.pack('!B', RFC2217_PARITY_MAP[self._parity]))
        self._rfc2217_port_settings['stopsize'].set(struct.pack('!B', RFC2217_STOPBIT_MAP[self._stopbits]))
        items = self._rfc2217_port_settings.values()
        if self.logger:
            self.logger.debug('Negotiating settings: %s' % (items,))
        timeout_time = time.time() + self._network_timeout
        while time.time() < timeout_time:
            time.sleep(0.05)
            if sum(o.active for o in items) == len(items):
                break
        else:
            raise SerialException('Remote does not accept parameter change (RFC2217): %r' % items)

        if self.logger:
            self.logger.info('Negotiated settings: %s' % (items,))
        if self._rtscts and self._xonxoff:
            raise ValueError('xonxoff and rtscts together are not supported')
        elif self._rtscts:
            self.rfc2217SetControl(SET_CONTROL_USE_HW_FLOW_CONTROL)
        elif self._xonxoff:
            self.rfc2217SetControl(SET_CONTROL_USE_SW_FLOW_CONTROL)
        else:
            self.rfc2217SetControl(SET_CONTROL_USE_NO_FLOW_CONTROL)
        return

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
            if self._thread:
                self._thread.join()
            self.is_open = False
            time.sleep(0.3)
        return

    def from_url(self, url):
        """extract host and port from an URL string"""
        parts = urlparse.urlsplit(url)
        if parts.scheme != 'rfc2217':
            raise SerialException('expected a string in the form "rfc2217://<host>:<port>[?option[&option...]]": not starting with rfc2217:// (%r)' % (parts.scheme,))
        try:
            for option, values in urlparse.parse_qs(parts.query, True).items():
                if option == 'logging':
                    logging.basicConfig()
                    self.logger = logging.getLogger('pySerial.rfc2217')
                    self.logger.setLevel(LOGGER_LEVELS[values[0]])
                    self.logger.debug('enabled logging')
                elif option == 'ign_set_control':
                    self._ignore_set_control_answer = True
                elif option == 'poll_modem':
                    self._poll_modem_state = True
                elif option == 'timeout':
                    self._network_timeout = float(values[0])
                else:
                    raise ValueError('unknown option: %r' % (option,))

            host, port = parts.hostname, parts.port
            if not 0 <= port < 65536:
                raise ValueError('port not in range 0...65535')
        except ValueError as e:
            raise SerialException('expected a string in the form "rfc2217://<host>:<port>[?option[&option...]]": %s' % e)

        return (host, port)

    @property
    def in_waiting(self):
        """Return the number of bytes currently in the input buffer."""
        if not self.is_open:
            raise portNotOpenError
        return self._read_buffer.qsize()

    def read(self, size=1):
        """        Read size bytes from the serial port. If a timeout is set it may
        return less characters as requested. With no timeout it will block
        until the requested number of bytes is read.
        """
        if not self.is_open:
            raise portNotOpenError
        data = bytearray()
        try:
            while len(data) < size:
                if self._thread is None:
                    raise SerialException('connection failed (reader thread died)')
                data += self._read_buffer.get(True, self._timeout)

        except Queue.Empty:
            pass

        return bytes(data)

    def write(self, data):
        """        Output the given byte string over the serial port. Can block if the
        connection is blocked. May raise SerialException if the connection is
        closed.
        """
        if not self.is_open:
            raise portNotOpenError
        with self._write_lock:
            try:
                self._socket.sendall(to_bytes(data).replace(IAC, IAC_DOUBLED))
            except socket.error as e:
                raise SerialException('connection failed (socket error): %s' % (e,))

        return len(data)

    def reset_input_buffer(self):
        """Clear input buffer, discarding all that is in the buffer."""
        if not self.is_open:
            raise portNotOpenError
        self.rfc2217SendPurge(PURGE_RECEIVE_BUFFER)
        while self._read_buffer.qsize():
            self._read_buffer.get(False)

    def reset_output_buffer(self):
        """        Clear output buffer, aborting the current output and
        discarding all that is in the buffer.
        """
        if not self.is_open:
            raise portNotOpenError
        self.rfc2217SendPurge(PURGE_TRANSMIT_BUFFER)

    def _update_break_state(self):
        """        Set break: Controls TXD. When active, to transmitting is
        possible.
        """
        if not self.is_open:
            raise portNotOpenError
        if self.logger:
            self.logger.info('set BREAK to %s' % ('active' if self._break_state else 'inactive'))
        if self._break_state:
            self.rfc2217SetControl(SET_CONTROL_BREAK_ON)
        else:
            self.rfc2217SetControl(SET_CONTROL_BREAK_OFF)

    def _update_rts_state(self):
        """Set terminal status line: Request To Send."""
        if not self.is_open:
            raise portNotOpenError
        if self.logger:
            self.logger.info('set RTS to %s' % ('active' if self._rts_state else 'inactive'))
        if self._rts_state:
            self.rfc2217SetControl(SET_CONTROL_RTS_ON)
        else:
            self.rfc2217SetControl(SET_CONTROL_RTS_OFF)

    def _update_dtr_state(self, level=True):
        """Set terminal status line: Data Terminal Ready."""
        if not self.is_open:
            raise portNotOpenError
        if self.logger:
            self.logger.info('set DTR to %s' % ('active' if self._dtr_state else 'inactive'))
        if self._dtr_state:
            self.rfc2217SetControl(SET_CONTROL_DTR_ON)
        else:
            self.rfc2217SetControl(SET_CONTROL_DTR_OFF)

    @property
    def cts(self):
        """Read terminal status line: Clear To Send."""
        if not self.is_open:
            raise portNotOpenError
        return bool(self.getModemState() & MODEMSTATE_MASK_CTS)

    @property
    def dsr(self):
        """Read terminal status line: Data Set Ready."""
        if not self.is_open:
            raise portNotOpenError
        return bool(self.getModemState() & MODEMSTATE_MASK_DSR)

    @property
    def ri(self):
        """Read terminal status line: Ring Indicator."""
        if not self.is_open:
            raise portNotOpenError
        return bool(self.getModemState() & MODEMSTATE_MASK_RI)

    @property
    def cd(self):
        """Read terminal status line: Carrier Detect."""
        if not self.is_open:
            raise portNotOpenError
        return bool(self.getModemState() & MODEMSTATE_MASK_CD)

    def _telnetReadLoop(self):
        """Read loop for the socket."""
        mode = M_NORMAL
        suboption = None
        try:
            while self._socket is not None:
                try:
                    data = self._socket.recv(1024)
                except socket.timeout:
                    continue
                except socket.error as e:
                    if self.logger:
                        self.logger.debug('socket error in reader thread: %s' % (e,))
                    break

                if not data:
                    break
                for byte in iterbytes(data):
                    if mode == M_NORMAL:
                        if byte == IAC:
                            mode = M_IAC_SEEN
                        elif suboption is not None:
                            suboption += byte
                        else:
                            self._read_buffer.put(byte)
                    elif mode == M_IAC_SEEN:
                        if byte == IAC:
                            if suboption is not None:
                                suboption += IAC
                            else:
                                self._read_buffer.put(IAC)
                            mode = M_NORMAL
                        elif byte == SB:
                            suboption = bytearray()
                            mode = M_NORMAL
                        elif byte == SE:
                            self._telnetProcessSubnegotiation(bytes(suboption))
                            suboption = None
                            mode = M_NORMAL
                        elif byte in (DO, DONT, WILL, WONT):
                            telnet_command = byte
                            mode = M_NEGOTIATE
                        else:
                            self._telnetProcessCommand(byte)
                            mode = M_NORMAL
                    elif mode == M_NEGOTIATE:
                        self._telnetNegotiateOption(telnet_command, byte)
                        mode = M_NORMAL

        finally:
            self._thread = None
            if self.logger:
                self.logger.debug('read thread terminated')

        return

    def _telnetProcessCommand(self, command):
        """Process commands other than DO, DONT, WILL, WONT."""
        if self.logger:
            self.logger.warning('ignoring Telnet command: %r' % (command,))

    def _telnetNegotiateOption(self, command, option):
        """Process incoming DO, DONT, WILL, WONT."""
        known = False
        for item in self._telnet_options:
            if item.option == option:
                item.process_incoming(command)
                known = True

        if not known:
            if command == WILL or command == DO:
                self.telnetSendOption(DONT if command == WILL else WONT, option)
                if self.logger:
                    self.logger.warning('rejected Telnet option: %r' % (option,))

    def _telnetProcessSubnegotiation(self, suboption):
        """Process subnegotiation, the data between IAC SB and IAC SE."""
        if suboption[0:1] == COM_PORT_OPTION:
            if suboption[1:2] == SERVER_NOTIFY_LINESTATE and len(suboption) >= 3:
                self._linestate = ord(suboption[2:3])
                if self.logger:
                    self.logger.info('NOTIFY_LINESTATE: %s' % self._linestate)
            elif suboption[1:2] == SERVER_NOTIFY_MODEMSTATE and len(suboption) >= 3:
                self._modemstate = ord(suboption[2:3])
                if self.logger:
                    self.logger.info('NOTIFY_MODEMSTATE: %s' % self._modemstate)
                self._modemstate_expires = time.time() + 0.3
            elif suboption[1:2] == FLOWCONTROL_SUSPEND:
                self._remote_suspend_flow = True
            elif suboption[1:2] == FLOWCONTROL_RESUME:
                self._remote_suspend_flow = False
            else:
                for item in self._rfc2217_options.values():
                    if item.ack_option == suboption[1:2]:
                        item.checkAnswer(bytes(suboption[2:]))
                        break
                else:
                    if self.logger:
                        self.logger.warning('ignoring COM_PORT_OPTION: %r' % (suboption,))
        elif self.logger:
            self.logger.warning('ignoring subnegotiation: %r' % (suboption,))

    def _internal_raw_write(self, data):
        """internal socket write with no data escaping. used to send telnet stuff."""
        with self._write_lock:
            self._socket.sendall(data)

    def telnetSendOption(self, action, option):
        """Send DO, DONT, WILL, WONT."""
        self._internal_raw_write(to_bytes([IAC, action, option]))

    def rfc2217SendSubnegotiation(self, option, value=''):
        """Subnegotiation of RFC2217 parameters."""
        value = value.replace(IAC, IAC_DOUBLED)
        self._internal_raw_write(to_bytes([IAC, SB, COM_PORT_OPTION, option] + list(value) + [IAC, SE]))

    def rfc2217SendPurge(self, value):
        item = self._rfc2217_options['purge']
        item.set(value)
        item.wait(self._network_timeout)

    def rfc2217SetControl(self, value):
        item = self._rfc2217_options['control']
        item.set(value)
        if self._ignore_set_control_answer:
            time.sleep(0.1)
        else:
            item.wait(self._network_timeout)

    def rfc2217FlowServerReady(self):
        """        check if server is ready to receive data. block for some time when
        not.
        """
        pass

    def getModemState--- This code section failed: ---

 L. 864         0  LOAD_FAST             0  'self'
                3  LOAD_ATTR             0  '_poll_modem_state'
                6  POP_JUMP_IF_FALSE   184  'to 184'
                9  LOAD_FAST             0  'self'
               12  LOAD_ATTR             1  '_modemstate_expires'
               15  LOAD_GLOBAL           2  'time'
               18  LOAD_ATTR             2  'time'
               21  CALL_FUNCTION_0       0  None
               24  COMPARE_OP            0  <
             27_0  COME_FROM             6  '6'
               27  POP_JUMP_IF_FALSE   184  'to 184'

 L. 865        30  LOAD_FAST             0  'self'
               33  LOAD_ATTR             3  'logger'
               36  POP_JUMP_IF_FALSE    58  'to 58'

 L. 866        39  LOAD_FAST             0  'self'
               42  LOAD_ATTR             3  'logger'
               45  LOAD_ATTR             4  'debug'
               48  LOAD_CONST               'polling modem state'
               51  CALL_FUNCTION_1       1  None
               54  POP_TOP          
               55  JUMP_FORWARD          0  'to 58'
             58_0  COME_FROM            55  '55'

 L. 868        58  LOAD_FAST             0  'self'
               61  LOAD_ATTR             5  'rfc2217SendSubnegotiation'
               64  LOAD_GLOBAL           6  'NOTIFY_MODEMSTATE'
               67  CALL_FUNCTION_1       1  None
               70  POP_TOP          

 L. 869        71  LOAD_GLOBAL           2  'time'
               74  LOAD_ATTR             2  'time'
               77  CALL_FUNCTION_0       0  None
               80  LOAD_FAST             0  'self'
               83  LOAD_ATTR             7  '_network_timeout'
               86  BINARY_ADD       
               87  STORE_FAST            1  'timeout_time'

 L. 870        90  SETUP_LOOP           91  'to 184'
               93  LOAD_GLOBAL           2  'time'
               96  LOAD_ATTR             2  'time'
               99  CALL_FUNCTION_0       0  None
              102  LOAD_FAST             1  'timeout_time'
              105  COMPARE_OP            0  <
              108  POP_JUMP_IF_FALSE   152  'to 152'

 L. 871       111  LOAD_GLOBAL           2  'time'
              114  LOAD_ATTR             8  'sleep'
              117  LOAD_CONST               0.05
              120  CALL_FUNCTION_1       1  None
              123  POP_TOP          

 L. 874       124  LOAD_FAST             0  'self'
              127  LOAD_ATTR             1  '_modemstate_expires'
              130  LOAD_GLOBAL           2  'time'
              133  LOAD_ATTR             2  'time'
              136  CALL_FUNCTION_0       0  None
              139  COMPARE_OP            4  >
              142  POP_JUMP_IF_FALSE    93  'to 93'

 L. 875       145  BREAK_LOOP       
              146  JUMP_BACK            93  'to 93'
              149  JUMP_BACK            93  'to 93'
              152  POP_BLOCK        

 L. 877       153  LOAD_FAST             0  'self'
              156  LOAD_ATTR             3  'logger'
              159  POP_JUMP_IF_FALSE   184  'to 184'

 L. 878       162  LOAD_FAST             0  'self'
              165  LOAD_ATTR             3  'logger'
              168  LOAD_ATTR             9  'warning'
              171  LOAD_CONST               'poll for modem state failed'
              174  CALL_FUNCTION_1       1  None
              177  POP_TOP          
              178  JUMP_ABSOLUTE       184  'to 184'
            181_0  COME_FROM            90  '90'
              181  JUMP_FORWARD          0  'to 184'
            184_0  COME_FROM            90  '90'

 L. 883       184  LOAD_FAST             0  'self'
              187  LOAD_ATTR            10  '_modemstate'
              190  LOAD_CONST               None
              193  COMPARE_OP            9  is-not
              196  POP_JUMP_IF_FALSE   234  'to 234'

 L. 884       199  LOAD_FAST             0  'self'
              202  LOAD_ATTR             3  'logger'
              205  POP_JUMP_IF_FALSE   227  'to 227'

 L. 885       208  LOAD_FAST             0  'self'
              211  LOAD_ATTR             3  'logger'
              214  LOAD_ATTR             4  'debug'
              217  LOAD_CONST               'using cached modem state'
              220  CALL_FUNCTION_1       1  None
              223  POP_TOP          
              224  JUMP_FORWARD          0  'to 227'
            227_0  COME_FROM           224  '224'

 L. 886       227  LOAD_FAST             0  'self'
              230  LOAD_ATTR            10  '_modemstate'
              233  RETURN_END_IF    
            234_0  COME_FROM           196  '196'

 L. 889       234  LOAD_GLOBAL          12  'SerialException'
              237  LOAD_CONST               'remote sends no NOTIFY_MODEMSTATE'
              240  CALL_FUNCTION_1       1  None
              243  RAISE_VARARGS_1       1  None
              246  LOAD_CONST               None
              249  RETURN_VALUE     

Parse error at or near `COME_FROM' instruction at offset 181_0


class PortManager(object):
    """    This class manages the state of Telnet and RFC 2217. It needs a serial
    instance and a connection to work with. Connection is expected to implement
    a (thread safe) write function, that writes the string to the network.
    """

    def __init__(self, serial_port, connection, logger=None):
        self.serial = serial_port
        self.connection = connection
        self.logger = logger
        self._client_is_rfc2217 = False
        self.mode = M_NORMAL
        self.suboption = None
        self.telnet_command = None
        self.modemstate_mask = 255
        self.last_modemstate = None
        self.linstate_mask = 0
        self._telnet_options = [
         TelnetOption(self, 'ECHO', ECHO, WILL, WONT, DO, DONT, REQUESTED),
         TelnetOption(self, 'we-SGA', SGA, WILL, WONT, DO, DONT, REQUESTED),
         TelnetOption(self, 'they-SGA', SGA, DO, DONT, WILL, WONT, INACTIVE),
         TelnetOption(self, 'we-BINARY', BINARY, WILL, WONT, DO, DONT, INACTIVE),
         TelnetOption(self, 'they-BINARY', BINARY, DO, DONT, WILL, WONT, REQUESTED),
         TelnetOption(self, 'we-RFC2217', COM_PORT_OPTION, WILL, WONT, DO, DONT, REQUESTED, self._client_ok),
         TelnetOption(self, 'they-RFC2217', COM_PORT_OPTION, DO, DONT, WILL, WONT, INACTIVE, self._client_ok)]
        if self.logger:
            self.logger.debug('requesting initial Telnet/RFC 2217 options')
        for option in self._telnet_options:
            if option.state is REQUESTED:
                self.telnetSendOption(option.send_yes, option.option)

        return

    def _client_ok(self):
        """        callback of telnet option. It gets called when option is activated.
        This one here is used to detect when the client agrees on RFC 2217. A
        flag is set so that other functions like check_modem_lines know if the
        client is OK.
        """
        self._client_is_rfc2217 = True
        if self.logger:
            self.logger.info('client accepts RFC 2217')
        self.check_modem_lines(force_notification=True)

    def telnetSendOption(self, action, option):
        """Send DO, DONT, WILL, WONT."""
        self.connection.write(to_bytes([IAC, action, option]))

    def rfc2217SendSubnegotiation(self, option, value=''):
        """Subnegotiation of RFC 2217 parameters."""
        value = value.replace(IAC, IAC_DOUBLED)
        self.connection.write(to_bytes([IAC, SB, COM_PORT_OPTION, option] + list(value) + [IAC, SE]))

    def check_modem_lines(self, force_notification=False):
        modemstate = (self.serial.getCTS() and MODEMSTATE_MASK_CTS) | (self.serial.getDSR() and MODEMSTATE_MASK_DSR) | (self.serial.getRI() and MODEMSTATE_MASK_RI) | (self.serial.getCD() and MODEMSTATE_MASK_CD)
        deltas = modemstate ^ (self.last_modemstate or 0)
        if deltas & MODEMSTATE_MASK_CTS:
            modemstate |= MODEMSTATE_MASK_CTS_CHANGE
        if deltas & MODEMSTATE_MASK_DSR:
            modemstate |= MODEMSTATE_MASK_DSR_CHANGE
        if deltas & MODEMSTATE_MASK_RI:
            modemstate |= MODEMSTATE_MASK_RI_CHANGE
        if deltas & MODEMSTATE_MASK_CD:
            modemstate |= MODEMSTATE_MASK_CD_CHANGE
        if modemstate != self.last_modemstate or force_notification:
            if self._client_is_rfc2217 and modemstate & self.modemstate_mask or force_notification:
                self.rfc2217SendSubnegotiation(SERVER_NOTIFY_MODEMSTATE, to_bytes([modemstate & self.modemstate_mask]))
                if self.logger:
                    self.logger.info('NOTIFY_MODEMSTATE: %s' % (modemstate,))
            self.last_modemstate = modemstate & 240

    def escape(self, data):
        """        This generator function is for the user. All outgoing data has to be
        properly escaped, so that no IAC character in the data stream messes up
        the Telnet state machine in the server.

        socket.sendall(escape(data))
        """
        for byte in data:
            if byte == IAC:
                yield IAC
                yield IAC
            else:
                yield byte

    def filter(self, data):
        """        Handle a bunch of incoming bytes. This is a generator. It will yield
        all characters not of interest for Telnet/RFC 2217.

        The idea is that the reader thread pushes data from the socket through
        this filter:

        for byte in filter(socket.recv(1024)):
            # do things like CR/LF conversion/whatever
            # and write data to the serial port
            serial.write(byte)

        (socket error handling code left as exercise for the reader)
        """
        for byte in iterbytes(data):
            if self.mode == M_NORMAL:
                if byte == IAC:
                    self.mode = M_IAC_SEEN
                elif self.suboption is not None:
                    self.suboption += byte
                else:
                    yield byte
            elif self.mode == M_IAC_SEEN:
                if byte == IAC:
                    if self.suboption is not None:
                        self.suboption += byte
                    else:
                        yield byte
                    self.mode = M_NORMAL
                elif byte == SB:
                    self.suboption = bytearray()
                    self.mode = M_NORMAL
                elif byte == SE:
                    self._telnetProcessSubnegotiation(bytes(self.suboption))
                    self.suboption = None
                    self.mode = M_NORMAL
                elif byte in (DO, DONT, WILL, WONT):
                    self.telnet_command = byte
                    self.mode = M_NEGOTIATE
                else:
                    self._telnetProcessCommand(byte)
                    self.mode = M_NORMAL
            elif self.mode == M_NEGOTIATE:
                self._telnetNegotiateOption(self.telnet_command, byte)
                self.mode = M_NORMAL

        return

    def _telnetProcessCommand(self, command):
        """Process commands other than DO, DONT, WILL, WONT."""
        if self.logger:
            self.logger.warning('ignoring Telnet command: %r' % (command,))

    def _telnetNegotiateOption(self, command, option):
        """Process incoming DO, DONT, WILL, WONT."""
        known = False
        for item in self._telnet_options:
            if item.option == option:
                item.process_incoming(command)
                known = True

        if not known:
            if command == WILL or command == DO:
                self.telnetSendOption(DONT if command == WILL else WONT, option)
                if self.logger:
                    self.logger.warning('rejected Telnet option: %r' % (option,))

    def _telnetProcessSubnegotiation(self, suboption):
        """Process subnegotiation, the data between IAC SB and IAC SE."""
        if suboption[0:1] == COM_PORT_OPTION:
            if self.logger:
                self.logger.debug('received COM_PORT_OPTION: %r' % (suboption,))
            if suboption[1:2] == SET_BAUDRATE:
                backup = self.serial.baudrate
                try:
                    baudrate, = struct.unpack('!I', suboption[2:6])
                    if baudrate != 0:
                        self.serial.baudrate = baudrate
                except ValueError as e:
                    if self.logger:
                        self.logger.error('failed to set baud rate: %s' % (e,))
                    self.serial.baudrate = backup

                if self.logger:
                    self.logger.info('%s baud rate: %s' % ('set' if baudrate else 'get', self.serial.baudrate))
                self.rfc2217SendSubnegotiation(SERVER_SET_BAUDRATE, struct.pack('!I', self.serial.baudrate))
            elif suboption[1:2] == SET_DATASIZE:
                backup = self.serial.bytesize
                try:
                    datasize, = struct.unpack('!B', suboption[2:3])
                    if datasize != 0:
                        self.serial.bytesize = datasize
                except ValueError as e:
                    if self.logger:
                        self.logger.error('failed to set data size: %s' % (e,))
                    self.serial.bytesize = backup

                if self.logger:
                    self.logger.info('%s data size: %s' % ('set' if datasize else 'get', self.serial.bytesize))
                self.rfc2217SendSubnegotiation(SERVER_SET_DATASIZE, struct.pack('!B', self.serial.bytesize))
            elif suboption[1:2] == SET_PARITY:
                backup = self.serial.parity
                try:
                    parity = struct.unpack('!B', suboption[2:3])[0]
                    if parity != 0:
                        self.serial.parity = RFC2217_REVERSE_PARITY_MAP[parity]
                except ValueError as e:
                    if self.logger:
                        self.logger.error('failed to set parity: %s' % (e,))
                    self.serial.parity = backup

                if self.logger:
                    self.logger.info('%s parity: %s' % ('set' if parity else 'get', self.serial.parity))
                self.rfc2217SendSubnegotiation(SERVER_SET_PARITY, struct.pack('!B', RFC2217_PARITY_MAP[self.serial.parity]))
            elif suboption[1:2] == SET_STOPSIZE:
                backup = self.serial.stopbits
                try:
                    stopbits = struct.unpack('!B', suboption[2:3])[0]
                    if stopbits != 0:
                        self.serial.stopbits = RFC2217_REVERSE_STOPBIT_MAP[stopbits]
                except ValueError as e:
                    if self.logger:
                        self.logger.error('failed to set stop bits: %s' % (e,))
                    self.serial.stopbits = backup

                if self.logger:
                    self.logger.info('%s stop bits: %s' % ('set' if stopbits else 'get', self.serial.stopbits))
                self.rfc2217SendSubnegotiation(SERVER_SET_STOPSIZE, struct.pack('!B', RFC2217_STOPBIT_MAP[self.serial.stopbits]))
            elif suboption[1:2] == SET_CONTROL:
                if suboption[2:3] == SET_CONTROL_REQ_FLOW_SETTING:
                    if self.serial.xonxoff:
                        self.rfc2217SendSubnegotiation(SERVER_SET_CONTROL, SET_CONTROL_USE_SW_FLOW_CONTROL)
                    elif self.serial.rtscts:
                        self.rfc2217SendSubnegotiation(SERVER_SET_CONTROL, SET_CONTROL_USE_HW_FLOW_CONTROL)
                    else:
                        self.rfc2217SendSubnegotiation(SERVER_SET_CONTROL, SET_CONTROL_USE_NO_FLOW_CONTROL)
                elif suboption[2:3] == SET_CONTROL_USE_NO_FLOW_CONTROL:
                    self.serial.xonxoff = False
                    self.serial.rtscts = False
                    if self.logger:
                        self.logger.info('changed flow control to None')
                    self.rfc2217SendSubnegotiation(SERVER_SET_CONTROL, SET_CONTROL_USE_NO_FLOW_CONTROL)
                elif suboption[2:3] == SET_CONTROL_USE_SW_FLOW_CONTROL:
                    self.serial.xonxoff = True
                    if self.logger:
                        self.logger.info('changed flow control to XON/XOFF')
                    self.rfc2217SendSubnegotiation(SERVER_SET_CONTROL, SET_CONTROL_USE_SW_FLOW_CONTROL)
                elif suboption[2:3] == SET_CONTROL_USE_HW_FLOW_CONTROL:
                    self.serial.rtscts = True
                    if self.logger:
                        self.logger.info('changed flow control to RTS/CTS')
                    self.rfc2217SendSubnegotiation(SERVER_SET_CONTROL, SET_CONTROL_USE_HW_FLOW_CONTROL)
                elif suboption[2:3] == SET_CONTROL_REQ_BREAK_STATE:
                    if self.logger:
                        self.logger.warning('requested break state - not implemented')
                elif suboption[2:3] == SET_CONTROL_BREAK_ON:
                    self.serial.setBreak(True)
                    if self.logger:
                        self.logger.info('changed BREAK to active')
                    self.rfc2217SendSubnegotiation(SERVER_SET_CONTROL, SET_CONTROL_BREAK_ON)
                elif suboption[2:3] == SET_CONTROL_BREAK_OFF:
                    self.serial.setBreak(False)
                    if self.logger:
                        self.logger.info('changed BREAK to inactive')
                    self.rfc2217SendSubnegotiation(SERVER_SET_CONTROL, SET_CONTROL_BREAK_OFF)
                elif suboption[2:3] == SET_CONTROL_REQ_DTR:
                    if self.logger:
                        self.logger.warning('requested DTR state - not implemented')
                elif suboption[2:3] == SET_CONTROL_DTR_ON:
                    self.serial.setDTR(True)
                    if self.logger:
                        self.logger.info('changed DTR to active')
                    self.rfc2217SendSubnegotiation(SERVER_SET_CONTROL, SET_CONTROL_DTR_ON)
                elif suboption[2:3] == SET_CONTROL_DTR_OFF:
                    self.serial.setDTR(False)
                    if self.logger:
                        self.logger.info('changed DTR to inactive')
                    self.rfc2217SendSubnegotiation(SERVER_SET_CONTROL, SET_CONTROL_DTR_OFF)
                elif suboption[2:3] == SET_CONTROL_REQ_RTS:
                    if self.logger:
                        self.logger.warning('requested RTS state - not implemented')
                elif suboption[2:3] == SET_CONTROL_RTS_ON:
                    self.serial.setRTS(True)
                    if self.logger:
                        self.logger.info('changed RTS to active')
                    self.rfc2217SendSubnegotiation(SERVER_SET_CONTROL, SET_CONTROL_RTS_ON)
                elif suboption[2:3] == SET_CONTROL_RTS_OFF:
                    self.serial.setRTS(False)
                    if self.logger:
                        self.logger.info('changed RTS to inactive')
                    self.rfc2217SendSubnegotiation(SERVER_SET_CONTROL, SET_CONTROL_RTS_OFF)
            elif suboption[1:2] == NOTIFY_LINESTATE:
                self.rfc2217SendSubnegotiation(SERVER_NOTIFY_LINESTATE, to_bytes([0]))
            elif suboption[1:2] == NOTIFY_MODEMSTATE:
                if self.logger:
                    self.logger.info('request for modem state')
                self.check_modem_lines(force_notification=True)
            elif suboption[1:2] == FLOWCONTROL_SUSPEND:
                if self.logger:
                    self.logger.info('suspend')
                self._remote_suspend_flow = True
            elif suboption[1:2] == FLOWCONTROL_RESUME:
                if self.logger:
                    self.logger.info('resume')
                self._remote_suspend_flow = False
            elif suboption[1:2] == SET_LINESTATE_MASK:
                self.linstate_mask = ord(suboption[2:3])
                if self.logger:
                    self.logger.info('line state mask: 0x%02x' % (self.linstate_mask,))
            elif suboption[1:2] == SET_MODEMSTATE_MASK:
                self.modemstate_mask = ord(suboption[2:3])
                if self.logger:
                    self.logger.info('modem state mask: 0x%02x' % (self.modemstate_mask,))
            elif suboption[1:2] == PURGE_DATA:
                if suboption[2:3] == PURGE_RECEIVE_BUFFER:
                    self.serial.reset_input_buffer()
                    if self.logger:
                        self.logger.info('purge in')
                    self.rfc2217SendSubnegotiation(SERVER_PURGE_DATA, PURGE_RECEIVE_BUFFER)
                elif suboption[2:3] == PURGE_TRANSMIT_BUFFER:
                    self.serial.reset_output_buffer()
                    if self.logger:
                        self.logger.info('purge out')
                    self.rfc2217SendSubnegotiation(SERVER_PURGE_DATA, PURGE_TRANSMIT_BUFFER)
                elif suboption[2:3] == PURGE_BOTH_BUFFERS:
                    self.serial.reset_input_buffer()
                    self.serial.reset_output_buffer()
                    if self.logger:
                        self.logger.info('purge both')
                    self.rfc2217SendSubnegotiation(SERVER_PURGE_DATA, PURGE_BOTH_BUFFERS)
                elif self.logger:
                    self.logger.error('undefined PURGE_DATA: %r' % list(suboption[2:]))
            elif self.logger:
                self.logger.error('undefined COM_PORT_OPTION: %r' % list(suboption[1:]))
        elif self.logger:
            self.logger.warning('unknown subnegotiation: %r' % (suboption,))


if __name__ == '__main__':
    import sys
    s = Serial('rfc2217://localhost:7000', 115200)
    sys.stdout.write('%s\n' % s)
    sys.stdout.write('write...\n')
    s.write('hello\n')
    s.flush()
    sys.stdout.write('read: %s\n' % s.read(5))
    s.close()