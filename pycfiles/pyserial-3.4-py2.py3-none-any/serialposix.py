# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./build/lib.linux-x86_64-2.7/serial/serialposix.py
# Compiled at: 2015-09-18 20:07:12
import errno, fcntl, os, select, struct, sys, termios, time, serial
from serial.serialutil import SerialBase, SerialException, to_bytes, portNotOpenError, writeTimeoutError

class PlatformSpecificBase(object):
    BAUDRATE_CONSTANTS = {}

    def number_to_device(self, port_number):
        sys.stderr.write("don't know how to number ttys on this system.\n! Use an explicit path (eg /dev/ttyS1) or send this information to\n! the author of this module:\n\nsys.platform = %r\nos.name = %r\nserialposix.py version = %s\n\nalso add the device name of the serial port and where the\ncounting starts for the first serial port.\ne.g. 'first serial port: /dev/ttyS0'\nand with a bit luck you can get this module running...\n" % (sys.platform, os.name, serial.VERSION))
        raise NotImplementedError('no number-to-device mapping defined on this platform')

    def _set_special_baudrate(self, baudrate):
        raise NotImplementedError('non-standard baudrates are not supported on this platform')

    def _set_rs485_mode(self, rs485_settings):
        raise NotImplementedError('RS485 not supported on this platform')


plat = sys.platform.lower()
if plat[:5] == 'linux':
    import array
    TCGETS2 = 2150388778
    TCSETS2 = 1076646955
    BOTHER = 4096
    TIOCGRS485 = 21550
    TIOCSRS485 = 21551
    SER_RS485_ENABLED = 1
    SER_RS485_RTS_ON_SEND = 2
    SER_RS485_RTS_AFTER_SEND = 4
    SER_RS485_RX_DURING_TX = 16

    class PlatformSpecific(PlatformSpecificBase):
        BAUDRATE_CONSTANTS = {0: 0, 
           50: 1, 
           75: 2, 
           110: 3, 
           134: 4, 
           150: 5, 
           200: 6, 
           300: 7, 
           600: 8, 
           1200: 9, 
           1800: 10, 
           2400: 11, 
           4800: 12, 
           9600: 13, 
           19200: 14, 
           38400: 15, 
           57600: 4097, 
           115200: 4098, 
           230400: 4099, 
           460800: 4100, 
           500000: 4101, 
           576000: 4102, 
           921600: 4103, 
           1000000: 4104, 
           1152000: 4105, 
           1500000: 4106, 
           2000000: 4107, 
           2500000: 4108, 
           3000000: 4109, 
           3500000: 4110, 
           4000000: 4111}

        def number_to_device(self, port_number):
            return '/dev/ttyS%d' % (port_number,)

        def _set_special_baudrate(self, baudrate):
            buf = array.array('i', [0] * 64)
            try:
                fcntl.ioctl(self.fd, TCGETS2, buf)
                buf[2] &= ~termios.CBAUD
                buf[2] |= BOTHER
                buf[9] = buf[10] = baudrate
                fcntl.ioctl(self.fd, TCSETS2, buf)
            except IOError as e:
                raise ValueError('Failed to set custom baud rate (%s): %s' % (baudrate, e))

        def _set_rs485_mode(self, rs485_settings):
            buf = array.array('i', [0] * 8)
            try:
                fcntl.ioctl(self.fd, TIOCGRS485, buf)
                if rs485_settings is not None:
                    if rs485_settings.loopback:
                        buf[0] |= SER_RS485_RX_DURING_TX
                    else:
                        buf[0] &= ~SER_RS485_RX_DURING_TX
                    if rs485_settings.rts_level_for_tx:
                        buf[0] |= SER_RS485_RTS_ON_SEND
                    else:
                        buf[0] &= ~SER_RS485_RTS_ON_SEND
                    if rs485_settings.rts_level_for_rx:
                        buf[0] |= SER_RS485_RTS_AFTER_SEND
                    else:
                        buf[0] &= ~SER_RS485_RTS_AFTER_SEND
                    buf[1] = int(rs485_settings.delay_rts_before_send * 1000)
                    buf[2] = int(rs485_settings.delay_rts_after_send * 1000)
                else:
                    buf[0] = 0
                fcntl.ioctl(self.fd, TIOCSRS485, buf)
            except IOError as e:
                raise ValueError('Failed to set RS485 mode: %s' % (e,))

            return


elif plat == 'cygwin':

    class PlatformSpecific(PlatformSpecificBase):
        BAUDRATE_CONSTANTS = {128000: 4099, 
           256000: 4101, 
           500000: 4103, 
           576000: 4104, 
           921600: 4105, 
           1000000: 4106, 
           1152000: 4107, 
           1500000: 4108, 
           2000000: 4109, 
           2500000: 4110, 
           3000000: 4111}

        def number_to_device(self, port_number):
            return '/dev/com%d' % (port_number + 1,)


elif plat[:7] == 'openbsd':

    class PlatformSpecific(PlatformSpecificBase):

        def number_to_device(self, port_number):
            return '/dev/cua%02d' % (port_number,)


elif plat[:3] == 'bsd' or plat[:7] == 'freebsd':

    class PlatformSpecific(PlatformSpecificBase):

        def number_to_device(self, port_number):
            return '/dev/cuad%d' % (port_number,)


elif plat[:6] == 'darwin':
    import array
    IOSSIOSPEED = 2147767298

    class PlatformSpecific(PlatformSpecificBase):

        def number_to_device(self, port_number):
            return '/dev/cuad%d' % (port_number,)

        osx_version = os.uname()[2].split('.')
        if int(osx_version[0]) >= 8:

            def _set_special_baudrate(self, baudrate):
                buf = array.array('i', [baudrate])
                fcntl.ioctl(self.fd, IOSSIOSPEED, buf, 1)


elif plat[:6] == 'netbsd':

    class PlatformSpecific(PlatformSpecificBase):

        def number_to_device(self, port_number):
            return '/dev/dty%02d' % (port_number,)


elif plat[:4] == 'irix':

    class PlatformSpecific(PlatformSpecificBase):

        def number_to_device(self, port_number):
            return '/dev/ttyf%d' % (port_number + 1,)


elif plat[:2] == 'hp':

    class PlatformSpecific(PlatformSpecificBase):

        def number_to_device(self, port_number):
            return '/dev/tty%dp0' % (port_number + 1,)


elif plat[:5] == 'sunos':

    class PlatformSpecific(PlatformSpecificBase):

        def number_to_device(self, port_number):
            return '/dev/tty%c' % (ord('a') + port_number,)


elif plat[:3] == 'aix':

    class PlatformSpecific(PlatformSpecificBase):

        def number_to_device(self, port_number):
            return '/dev/tty%d' % (port_number,)


else:

    class PlatformSpecific(PlatformSpecificBase):
        pass


TIOCMGET = getattr(termios, 'TIOCMGET', 21525)
TIOCMBIS = getattr(termios, 'TIOCMBIS', 21526)
TIOCMBIC = getattr(termios, 'TIOCMBIC', 21527)
TIOCMSET = getattr(termios, 'TIOCMSET', 21528)
TIOCM_DTR = getattr(termios, 'TIOCM_DTR', 2)
TIOCM_RTS = getattr(termios, 'TIOCM_RTS', 4)
TIOCM_CTS = getattr(termios, 'TIOCM_CTS', 32)
TIOCM_CAR = getattr(termios, 'TIOCM_CAR', 64)
TIOCM_RNG = getattr(termios, 'TIOCM_RNG', 128)
TIOCM_DSR = getattr(termios, 'TIOCM_DSR', 256)
TIOCM_CD = getattr(termios, 'TIOCM_CD', TIOCM_CAR)
TIOCM_RI = getattr(termios, 'TIOCM_RI', TIOCM_RNG)
if hasattr(termios, 'TIOCINQ'):
    TIOCINQ = termios.TIOCINQ
else:
    TIOCINQ = getattr(termios, 'FIONREAD', 21531)
TIOCOUTQ = getattr(termios, 'TIOCOUTQ', 21521)
TIOCM_zero_str = struct.pack('I', 0)
TIOCM_RTS_str = struct.pack('I', TIOCM_RTS)
TIOCM_DTR_str = struct.pack('I', TIOCM_DTR)
TIOCSBRK = getattr(termios, 'TIOCSBRK', 21543)
TIOCCBRK = getattr(termios, 'TIOCCBRK', 21544)
CMSPAR = 1073741824

class Serial(SerialBase, PlatformSpecific):
    """    Serial port class POSIX implementation. Serial port configuration is
    done with termios and fcntl. Runs on Linux and many other Un*x like
    systems.
    """

    def open(self):
        """        Open port with current settings. This may throw a SerialException
        if the port cannot be opened."""
        if self._port is None:
            raise SerialException('Port must be configured before it can be used.')
        if self.is_open:
            raise SerialException('Port is already open.')
        self.fd = None
        try:
            self.fd = os.open(self.portstr, os.O_RDWR | os.O_NOCTTY | os.O_NONBLOCK)
        except OSError as msg:
            self.fd = None
            raise SerialException(msg.errno, 'could not open port %s: %s' % (self._port, msg))

        try:
            self._reconfigure_port()
        except:
            try:
                os.close(self.fd)
            except:
                pass

            self.fd = None
            raise
        else:
            self.is_open = True

        if not self._dsrdtr:
            self._update_dtr_state()
        if not self._rtscts:
            self._update_rts_state()
        self.reset_input_buffer()
        return

    def _reconfigure_port(self):
        """Set communication parameters on opened port."""
        if self.fd is None:
            raise SerialException('Can only operate on a valid file descriptor')
        custom_baud = None
        vmin = vtime = 0
        if self._inter_byte_timeout is not None:
            vmin = 1
            vtime = int(self._inter_byte_timeout * 10)
        try:
            orig_attr = termios.tcgetattr(self.fd)
            iflag, oflag, cflag, lflag, ispeed, ospeed, cc = orig_attr
        except termios.error as msg:
            raise SerialException('Could not configure port: %s' % msg)

        cflag |= termios.CLOCAL | termios.CREAD
        lflag &= ~(termios.ICANON | termios.ECHO | termios.ECHOE | termios.ECHOK | termios.ECHONL | termios.ISIG | termios.IEXTEN)
        for flag in ('ECHOCTL', 'ECHOKE'):
            if hasattr(termios, flag):
                lflag &= ~getattr(termios, flag)

        oflag &= ~(termios.OPOST | termios.ONLCR | termios.OCRNL)
        iflag &= ~(termios.INLCR | termios.IGNCR | termios.ICRNL | termios.IGNBRK)
        if hasattr(termios, 'IUCLC'):
            iflag &= ~termios.IUCLC
        if hasattr(termios, 'PARMRK'):
            iflag &= ~termios.PARMRK
        try:
            ispeed = ospeed = getattr(termios, 'B%s' % self._baudrate)
        except AttributeError:
            try:
                ispeed = ospeed = self.BAUDRATE_CONSTANTS[self._baudrate]
            except KeyError:
                ispeed = ospeed = getattr(termios, 'B38400')
                try:
                    custom_baud = int(self._baudrate)
                except ValueError:
                    raise ValueError('Invalid baud rate: %r' % self._baudrate)
                else:
                    if custom_baud < 0:
                        raise ValueError('Invalid baud rate: %r' % self._baudrate)

        cflag &= ~termios.CSIZE
        if self._bytesize == 8:
            cflag |= termios.CS8
        elif self._bytesize == 7:
            cflag |= termios.CS7
        elif self._bytesize == 6:
            cflag |= termios.CS6
        elif self._bytesize == 5:
            cflag |= termios.CS5
        else:
            raise ValueError('Invalid char len: %r' % self._bytesize)
        if self._stopbits == serial.STOPBITS_ONE:
            cflag &= ~termios.CSTOPB
        elif self._stopbits == serial.STOPBITS_ONE_POINT_FIVE:
            cflag |= termios.CSTOPB
        elif self._stopbits == serial.STOPBITS_TWO:
            cflag |= termios.CSTOPB
        else:
            raise ValueError('Invalid stop bit specification: %r' % self._stopbits)
        iflag &= ~(termios.INPCK | termios.ISTRIP)
        if self._parity == serial.PARITY_NONE:
            cflag &= ~(termios.PARENB | termios.PARODD)
        elif self._parity == serial.PARITY_EVEN:
            cflag &= ~termios.PARODD
            cflag |= termios.PARENB
        elif self._parity == serial.PARITY_ODD:
            cflag |= termios.PARENB | termios.PARODD
        elif self._parity == serial.PARITY_MARK and plat[:5] == 'linux':
            cflag |= termios.PARENB | CMSPAR | termios.PARODD
        elif self._parity == serial.PARITY_SPACE and plat[:5] == 'linux':
            cflag |= termios.PARENB | CMSPAR
            cflag &= ~termios.PARODD
        else:
            raise ValueError('Invalid parity: %r' % self._parity)
        if hasattr(termios, 'IXANY'):
            if self._xonxoff:
                iflag |= termios.IXON | termios.IXOFF
            else:
                iflag &= ~(termios.IXON | termios.IXOFF | termios.IXANY)
        elif self._xonxoff:
            iflag |= termios.IXON | termios.IXOFF
        else:
            iflag &= ~(termios.IXON | termios.IXOFF)
        if hasattr(termios, 'CRTSCTS'):
            if self._rtscts:
                cflag |= termios.CRTSCTS
            else:
                cflag &= ~termios.CRTSCTS
        elif hasattr(termios, 'CNEW_RTSCTS'):
            if self._rtscts:
                cflag |= termios.CNEW_RTSCTS
            else:
                cflag &= ~termios.CNEW_RTSCTS
        if vmin < 0 or vmin > 255:
            raise ValueError('Invalid vmin: %r ' % vmin)
        cc[termios.VMIN] = vmin
        if vtime < 0 or vtime > 255:
            raise ValueError('Invalid vtime: %r' % vtime)
        cc[termios.VTIME] = vtime
        if [
         iflag, oflag, cflag, lflag, ispeed, ospeed, cc] != orig_attr:
            termios.tcsetattr(self.fd, termios.TCSANOW, [
             iflag, oflag, cflag, lflag, ispeed, ospeed, cc])
        if custom_baud is not None:
            self._set_special_baudrate(custom_baud)
        if self._rs485_mode is not None:
            self._set_rs485_mode(self._rs485_mode)
        return

    def close(self):
        """Close port"""
        if self.is_open:
            if self.fd is not None:
                os.close(self.fd)
                self.fd = None
            self.is_open = False
        return

    @property
    def in_waiting(self):
        """Return the number of bytes currently in the input buffer."""
        s = fcntl.ioctl(self.fd, TIOCINQ, TIOCM_zero_str)
        return struct.unpack('I', s)[0]

    def read(self, size=1):
        """        Read size bytes from the serial port. If a timeout is set it may
        return less characters as requested. With no timeout it will block
        until the requested number of bytes is read.
        """
        if not self.is_open:
            raise portNotOpenError
        read = bytearray()
        while len(read) < size:
            try:
                ready, _, _ = select.select([self.fd], [], [], self._timeout)
                if not ready:
                    break
                buf = os.read(self.fd, size - len(read))
                if not buf:
                    raise SerialException('device reports readiness to read but returned no data (device disconnected or multiple access on port?)')
                read.extend(buf)
            except OSError as e:
                if e.errno != errno.EAGAIN:
                    raise SerialException('read failed: %s' % (e,))
            except select.error as e:
                if e[0] != errno.EAGAIN:
                    raise SerialException('read failed: %s' % (e,))

        return bytes(read)

    def write(self, data):
        """Output the given byte string over the serial port."""
        if not self.is_open:
            raise portNotOpenError
        d = to_bytes(data)
        tx_len = len(d)
        if self._write_timeout is not None and self._write_timeout > 0:
            timeout = time.time() + self._write_timeout
        else:
            timeout = None
        while tx_len > 0:
            try:
                n = os.write(self.fd, d)
                if timeout:
                    timeleft = timeout - time.time()
                    if timeleft < 0:
                        raise writeTimeoutError
                    _, ready, _ = select.select([], [self.fd], [], timeleft)
                    if not ready:
                        raise writeTimeoutError
                else:
                    _, ready, _ = select.select([], [self.fd], [], None)
                    if not ready:
                        raise SerialException('write failed (select)')
                d = d[n:]
                tx_len -= n
            except SerialException:
                raise
            except OSError as v:
                if v.errno != errno.EAGAIN:
                    raise SerialException('write failed: %s' % (v,))

        return len(data)

    def flush(self):
        """        Flush of file like objects. In this case, wait until all data
        is written.
        """
        if not self.is_open:
            raise portNotOpenError
        termios.tcdrain(self.fd)

    def reset_input_buffer(self):
        """Clear input buffer, discarding all that is in the buffer."""
        if not self.is_open:
            raise portNotOpenError
        termios.tcflush(self.fd, termios.TCIFLUSH)

    def reset_output_buffer(self):
        """        Clear output buffer, aborting the current output and discarding all
        that is in the buffer.
        """
        if not self.is_open:
            raise portNotOpenError
        termios.tcflush(self.fd, termios.TCOFLUSH)

    def send_break(self, duration=0.25):
        """        Send break condition. Timed, returns to idle state after given
        duration.
        """
        if not self.is_open:
            raise portNotOpenError
        termios.tcsendbreak(self.fd, int(duration / 0.25))

    def _update_break_state(self):
        """        Set break: Controls TXD. When active, no transmitting is possible.
        """
        if self._break_state:
            fcntl.ioctl(self.fd, TIOCSBRK)
        else:
            fcntl.ioctl(self.fd, TIOCCBRK)

    def _update_rts_state(self):
        """Set terminal status line: Request To Send"""
        if self._rts_state:
            fcntl.ioctl(self.fd, TIOCMBIS, TIOCM_RTS_str)
        else:
            fcntl.ioctl(self.fd, TIOCMBIC, TIOCM_RTS_str)

    def _update_dtr_state(self):
        """Set terminal status line: Data Terminal Ready"""
        if self._dtr_state:
            fcntl.ioctl(self.fd, TIOCMBIS, TIOCM_DTR_str)
        else:
            fcntl.ioctl(self.fd, TIOCMBIC, TIOCM_DTR_str)

    @property
    def cts(self):
        """Read terminal status line: Clear To Send"""
        if not self.is_open:
            raise portNotOpenError
        s = fcntl.ioctl(self.fd, TIOCMGET, TIOCM_zero_str)
        return struct.unpack('I', s)[0] & TIOCM_CTS != 0

    @property
    def dsr(self):
        """Read terminal status line: Data Set Ready"""
        if not self.is_open:
            raise portNotOpenError
        s = fcntl.ioctl(self.fd, TIOCMGET, TIOCM_zero_str)
        return struct.unpack('I', s)[0] & TIOCM_DSR != 0

    @property
    def ri(self):
        """Read terminal status line: Ring Indicator"""
        if not self.is_open:
            raise portNotOpenError
        s = fcntl.ioctl(self.fd, TIOCMGET, TIOCM_zero_str)
        return struct.unpack('I', s)[0] & TIOCM_RI != 0

    @property
    def cd(self):
        """Read terminal status line: Carrier Detect"""
        if not self.is_open:
            raise portNotOpenError
        s = fcntl.ioctl(self.fd, TIOCMGET, TIOCM_zero_str)
        return struct.unpack('I', s)[0] & TIOCM_CD != 0

    @property
    def out_waiting(self):
        """Return the number of bytes currently in the output buffer."""
        s = fcntl.ioctl(self.fd, TIOCOUTQ, TIOCM_zero_str)
        return struct.unpack('I', s)[0]

    def nonblocking(self):
        """internal - not portable!"""
        if not self.is_open:
            raise portNotOpenError
        fcntl.fcntl(self.fd, fcntl.F_SETFL, os.O_NONBLOCK)

    def fileno(self):
        """        For easier use of the serial port instance with select.
        WARNING: this function is not portable to different platforms!
        """
        if not self.is_open:
            raise portNotOpenError
        return self.fd

    def set_input_flow_control(self, enable=True):
        """        Manually control flow - when software flow control is enabled.
        This will send XON (true) or XOFF (false) to the other device.
        WARNING: this function is not portable to different platforms!
        """
        if not self.is_open:
            raise portNotOpenError
        if enable:
            termios.tcflow(self.fd, termios.TCION)
        else:
            termios.tcflow(self.fd, termios.TCIOFF)

    def set_output_flow_control(self, enable=True):
        """        Manually control flow of outgoing data - when hardware or software flow
        control is enabled.
        WARNING: this function is not portable to different platforms!
        """
        if not self.is_open:
            raise portNotOpenError
        if enable:
            termios.tcflow(self.fd, termios.TCOON)
        else:
            termios.tcflow(self.fd, termios.TCOOFF)


class PosixPollSerial(Serial):
    """    Poll based read implementation. Not all systems support poll properly.
    However this one has better handling of errors, such as a device
    disconnecting while it's in use (e.g. USB-serial unplugged).
    """

    def read(self, size=1):
        """        Read size bytes from the serial port. If a timeout is set it may
        return less characters as requested. With no timeout it will block
        until the requested number of bytes is read.
        """
        if self.fd is None:
            raise portNotOpenError
        read = bytearray()
        poll = select.poll()
        poll.register(self.fd, select.POLLIN | select.POLLERR | select.POLLHUP | select.POLLNVAL)
        if size > 0:
            while len(read) < size:
                for fd, event in poll.poll(self._timeout * 1000):
                    if event & (select.POLLERR | select.POLLHUP | select.POLLNVAL):
                        raise SerialException('device reports error (poll)')

                buf = os.read(self.fd, size - len(read))
                read.extend(buf)
                if (self._timeout is not None and self._timeout >= 0 or self._inter_byte_timeout is not None and self._inter_byte_timeout > 0) and not buf:
                    break

        return bytes(read)


if __name__ == '__main__':
    s = Serial(0, baudrate=19200, bytesize=serial.EIGHTBITS, parity=serial.PARITY_EVEN, stopbits=serial.STOPBITS_ONE, timeout=3, xonxoff=0, rtscts=0)
    s.rts = True
    s.dtr = True
    s.reset_input_buffer()
    s.reset_output_buffer()
    s.write('hello')
    sys.stdout.write('%r\n' % s.read(5))
    sys.stdout.write('%s\n' % s.inWaiting())
    del s