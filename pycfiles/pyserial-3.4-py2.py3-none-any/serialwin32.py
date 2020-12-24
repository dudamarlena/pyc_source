# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./build/lib.linux-x86_64-2.7/serial/serialwin32.py
# Compiled at: 2015-09-09 21:21:35
import ctypes, time
from serial import win32
import serial
from serial.serialutil import SerialBase, SerialException, to_bytes, portNotOpenError, writeTimeoutError

class Serial(SerialBase):
    """Serial port implementation for Win32 based on ctypes."""
    BAUDRATES = (50, 75, 110, 134, 150, 200, 300, 600, 1200, 1800, 2400, 4800, 9600,
                 19200, 38400, 57600, 115200)

    def __init__(self, *args, **kwargs):
        super(SerialBase, self).__init__()
        self._port_handle = None
        self._overlapped_read = None
        self._overlapped_write = None
        SerialBase.__init__(self, *args, **kwargs)
        return

    def open(self):
        """        Open port with current settings. This may throw a SerialException
        if the port cannot be opened.
        """
        if self._port is None:
            raise SerialException('Port must be configured before it can be used.')
        if self.is_open:
            raise SerialException('Port is already open.')
        port = self.name
        try:
            if port.upper().startswith('COM') and int(port[3:]) > 8:
                port = '\\\\.\\' + port
        except ValueError:
            pass

        self._port_handle = win32.CreateFile(port, win32.GENERIC_READ | win32.GENERIC_WRITE, 0, None, win32.OPEN_EXISTING, win32.FILE_ATTRIBUTE_NORMAL | win32.FILE_FLAG_OVERLAPPED, 0)
        if self._port_handle == win32.INVALID_HANDLE_VALUE:
            self._port_handle = None
            raise SerialException('could not open port %r: %r' % (self.portstr, ctypes.WinError()))
        try:
            self._overlapped_read = win32.OVERLAPPED()
            self._overlapped_read.hEvent = win32.CreateEvent(None, 1, 0, None)
            self._overlapped_write = win32.OVERLAPPED()
            self._overlapped_write.hEvent = win32.CreateEvent(None, 0, 0, None)
            win32.SetupComm(self._port_handle, 4096, 4096)
            self._orgTimeouts = win32.COMMTIMEOUTS()
            win32.GetCommTimeouts(self._port_handle, ctypes.byref(self._orgTimeouts))
            self._reconfigure_port()
            win32.PurgeComm(self._port_handle, win32.PURGE_TXCLEAR | win32.PURGE_TXABORT | win32.PURGE_RXCLEAR | win32.PURGE_RXABORT)
        except:
            try:
                self._close()
            except:
                pass

            self._port_handle = None
            raise
        else:
            self.is_open = True

        return

    def _reconfigure_port(self):
        """Set communication parameters on opened port."""
        if not self._port_handle:
            raise SerialException('Can only operate on a valid port handle')
        if self._timeout is None:
            timeouts = (0, 0, 0, 0, 0)
        elif self._timeout == 0:
            timeouts = (
             win32.MAXDWORD, 0, 0, 0, 0)
        else:
            timeouts = (
             0, 0, int(self._timeout * 1000), 0, 0)
        if self._timeout != 0 and self._inter_byte_timeout is not None:
            timeouts = (
             int(self._inter_byte_timeout * 1000),) + timeouts[1:]
        if self._write_timeout is None:
            pass
        elif self._write_timeout == 0:
            timeouts = timeouts[:-2] + (0, win32.MAXDWORD)
        else:
            timeouts = timeouts[:-2] + (0, int(self._write_timeout * 1000))
        win32.SetCommTimeouts(self._port_handle, ctypes.byref(win32.COMMTIMEOUTS(*timeouts)))
        win32.SetCommMask(self._port_handle, win32.EV_ERR)
        comDCB = win32.DCB()
        win32.GetCommState(self._port_handle, ctypes.byref(comDCB))
        comDCB.BaudRate = self._baudrate
        if self._bytesize == serial.FIVEBITS:
            comDCB.ByteSize = 5
        elif self._bytesize == serial.SIXBITS:
            comDCB.ByteSize = 6
        elif self._bytesize == serial.SEVENBITS:
            comDCB.ByteSize = 7
        elif self._bytesize == serial.EIGHTBITS:
            comDCB.ByteSize = 8
        else:
            raise ValueError('Unsupported number of data bits: %r' % self._bytesize)
        if self._parity == serial.PARITY_NONE:
            comDCB.Parity = win32.NOPARITY
            comDCB.fParity = 0
        elif self._parity == serial.PARITY_EVEN:
            comDCB.Parity = win32.EVENPARITY
            comDCB.fParity = 1
        elif self._parity == serial.PARITY_ODD:
            comDCB.Parity = win32.ODDPARITY
            comDCB.fParity = 1
        elif self._parity == serial.PARITY_MARK:
            comDCB.Parity = win32.MARKPARITY
            comDCB.fParity = 1
        elif self._parity == serial.PARITY_SPACE:
            comDCB.Parity = win32.SPACEPARITY
            comDCB.fParity = 1
        else:
            raise ValueError('Unsupported parity mode: %r' % self._parity)
        if self._stopbits == serial.STOPBITS_ONE:
            comDCB.StopBits = win32.ONESTOPBIT
        elif self._stopbits == serial.STOPBITS_ONE_POINT_FIVE:
            comDCB.StopBits = win32.ONE5STOPBITS
        elif self._stopbits == serial.STOPBITS_TWO:
            comDCB.StopBits = win32.TWOSTOPBITS
        else:
            raise ValueError('Unsupported number of stop bits: %r' % self._stopbits)
        comDCB.fBinary = 1
        if self._rs485_mode is None:
            if self._rtscts:
                comDCB.fRtsControl = win32.RTS_CONTROL_HANDSHAKE
            else:
                comDCB.fRtsControl = win32.RTS_CONTROL_ENABLE if self._rts_state else win32.RTS_CONTROL_DISABLE
            comDCB.fOutxCtsFlow = self._rtscts
        else:
            if not self._rs485_mode.rts_level_for_tx:
                raise ValueError('Unsupported value for RS485Settings.rts_level_for_tx: %r' % (
                 self._rs485_mode.rts_level_for_tx,))
            if self._rs485_mode.rts_level_for_rx:
                raise ValueError('Unsupported value for RS485Settings.rts_level_for_rx: %r' % (
                 self._rs485_mode.rts_level_for_rx,))
            if self._rs485_mode.delay_before_tx is not None:
                raise ValueError('Unsupported value for RS485Settings.delay_before_tx: %r' % (
                 self._rs485_mode.delay_before_tx,))
            if self._rs485_mode.delay_before_rx is not None:
                raise ValueError('Unsupported value for RS485Settings.delay_before_rx: %r' % (
                 self._rs485_mode.delay_before_rx,))
            if self._rs485_mode.loopback:
                raise ValueError('Unsupported value for RS485Settings.loopback: %r' % (
                 self._rs485_mode.loopback,))
            comDCB.fRtsControl = win32.RTS_CONTROL_TOGGLE
            comDCB.fOutxCtsFlow = 0
        if self._dsrdtr:
            comDCB.fDtrControl = win32.DTR_CONTROL_HANDSHAKE
        else:
            comDCB.fDtrControl = win32.DTR_CONTROL_ENABLE if self._dtr_state else win32.DTR_CONTROL_DISABLE
        comDCB.fOutxDsrFlow = self._dsrdtr
        comDCB.fOutX = self._xonxoff
        comDCB.fInX = self._xonxoff
        comDCB.fNull = 0
        comDCB.fErrorChar = 0
        comDCB.fAbortOnError = 0
        comDCB.XonChar = serial.XON
        comDCB.XoffChar = serial.XOFF
        if not win32.SetCommState(self._port_handle, ctypes.byref(comDCB)):
            raise ValueError('Cannot configure port, some setting was wrong. Original message: %r' % ctypes.WinError())
        return

    def _close(self):
        """internal close port helper"""
        if self._port_handle:
            win32.SetCommTimeouts(self._port_handle, self._orgTimeouts)
            win32.CloseHandle(self._port_handle)
            if self._overlapped_read is not None:
                win32.CloseHandle(self._overlapped_read.hEvent)
                self._overlapped_read = None
            if self._overlapped_write is not None:
                win32.CloseHandle(self._overlapped_write.hEvent)
                self._overlapped_write = None
            self._port_handle = None
        return

    def close(self):
        """Close port"""
        if self.is_open:
            self._close()
            self.is_open = False

    @property
    def in_waiting(self):
        """Return the number of bytes currently in the input buffer."""
        flags = win32.DWORD()
        comstat = win32.COMSTAT()
        if not win32.ClearCommError(self._port_handle, ctypes.byref(flags), ctypes.byref(comstat)):
            raise SerialException('call to ClearCommError failed')
        return comstat.cbInQue

    def read(self, size=1):
        """        Read size bytes from the serial port. If a timeout is set it may
        return less characters as requested. With no timeout it will block
        until the requested number of bytes is read."""
        if not self._port_handle:
            raise portNotOpenError
        if size > 0:
            win32.ResetEvent(self._overlapped_read.hEvent)
            flags = win32.DWORD()
            comstat = win32.COMSTAT()
            if not win32.ClearCommError(self._port_handle, ctypes.byref(flags), ctypes.byref(comstat)):
                raise SerialException('call to ClearCommError failed')
            if self.timeout == 0:
                n = min(comstat.cbInQue, size)
                if n > 0:
                    buf = ctypes.create_string_buffer(n)
                    rc = win32.DWORD()
                    err = win32.ReadFile(self._port_handle, buf, n, ctypes.byref(rc), ctypes.byref(self._overlapped_read))
                    if not err and win32.GetLastError() != win32.ERROR_IO_PENDING:
                        raise SerialException('ReadFile failed (%r)' % ctypes.WinError())
                    err = win32.WaitForSingleObject(self._overlapped_read.hEvent, win32.INFINITE)
                    read = buf.raw[:rc.value]
                else:
                    read = bytes()
            else:
                buf = ctypes.create_string_buffer(size)
                rc = win32.DWORD()
                err = win32.ReadFile(self._port_handle, buf, size, ctypes.byref(rc), ctypes.byref(self._overlapped_read))
                if not err and win32.GetLastError() != win32.ERROR_IO_PENDING:
                    raise SerialException('ReadFile failed (%r)' % ctypes.WinError())
                err = win32.GetOverlappedResult(self._port_handle, ctypes.byref(self._overlapped_read), ctypes.byref(rc), True)
                read = buf.raw[:rc.value]
        else:
            read = bytes()
        return bytes(read)

    def write(self, data):
        """Output the given byte string over the serial port."""
        if not self._port_handle:
            raise portNotOpenError
        data = to_bytes(data)
        if data:
            n = win32.DWORD()
            err = win32.WriteFile(self._port_handle, data, len(data), ctypes.byref(n), self._overlapped_write)
            if not err and win32.GetLastError() != win32.ERROR_IO_PENDING:
                raise SerialException('WriteFile failed (%r)' % ctypes.WinError())
            if self._write_timeout != 0:
                err = win32.GetOverlappedResult(self._port_handle, self._overlapped_write, ctypes.byref(n), True)
                if n.value != len(data):
                    raise writeTimeoutError
            return n.value
        else:
            return 0

    def flush(self):
        """        Flush of file like objects. In this case, wait until all data
        is written.
        """
        while self.out_waiting:
            time.sleep(0.05)

    def reset_input_buffer(self):
        """Clear input buffer, discarding all that is in the buffer."""
        if not self._port_handle:
            raise portNotOpenError
        win32.PurgeComm(self._port_handle, win32.PURGE_RXCLEAR | win32.PURGE_RXABORT)

    def reset_output_buffer(self):
        """        Clear output buffer, aborting the current output and discarding all
        that is in the buffer.
        """
        if not self._port_handle:
            raise portNotOpenError
        win32.PurgeComm(self._port_handle, win32.PURGE_TXCLEAR | win32.PURGE_TXABORT)

    def _update_break_state(self):
        """Set break: Controls TXD. When active, to transmitting is possible."""
        if not self._port_handle:
            raise portNotOpenError
        if self._break_state:
            win32.SetCommBreak(self._port_handle)
        else:
            win32.ClearCommBreak(self._port_handle)

    def _update_rts_state(self):
        """Set terminal status line: Request To Send"""
        if self._rts_state:
            win32.EscapeCommFunction(self._port_handle, win32.SETRTS)
        else:
            win32.EscapeCommFunction(self._port_handle, win32.CLRRTS)

    def _update_dtr_state(self):
        """Set terminal status line: Data Terminal Ready"""
        if self._dtr_state:
            win32.EscapeCommFunction(self._port_handle, win32.SETDTR)
        else:
            win32.EscapeCommFunction(self._port_handle, win32.CLRDTR)

    def _GetCommModemStatus(self):
        if not self._port_handle:
            raise portNotOpenError
        stat = win32.DWORD()
        win32.GetCommModemStatus(self._port_handle, ctypes.byref(stat))
        return stat.value

    @property
    def cts(self):
        """Read terminal status line: Clear To Send"""
        return win32.MS_CTS_ON & self._GetCommModemStatus() != 0

    @property
    def dsr(self):
        """Read terminal status line: Data Set Ready"""
        return win32.MS_DSR_ON & self._GetCommModemStatus() != 0

    @property
    def ri(self):
        """Read terminal status line: Ring Indicator"""
        return win32.MS_RING_ON & self._GetCommModemStatus() != 0

    @property
    def cd(self):
        """Read terminal status line: Carrier Detect"""
        return win32.MS_RLSD_ON & self._GetCommModemStatus() != 0

    def set_buffer_size(self, rx_size=4096, tx_size=None):
        """        Recommend a buffer size to the driver (device driver can ignore this
        value). Must be called before the port is opended.
        """
        if tx_size is None:
            tx_size = rx_size
        win32.SetupComm(self._port_handle, rx_size, tx_size)
        return

    def set_output_flow_control(self, enable=True):
        """        Manually control flow - when software flow control is enabled.
        This will do the same as if XON (true) or XOFF (false) are received
        from the other device and control the transmission accordingly.
        WARNING: this function is not portable to different platforms!
        """
        if not self._port_handle:
            raise portNotOpenError
        if enable:
            win32.EscapeCommFunction(self._port_handle, win32.SETXON)
        else:
            win32.EscapeCommFunction(self._port_handle, win32.SETXOFF)

    @property
    def out_waiting(self):
        """Return how many bytes the in the outgoing buffer"""
        flags = win32.DWORD()
        comstat = win32.COMSTAT()
        if not win32.ClearCommError(self._port_handle, ctypes.byref(flags), ctypes.byref(comstat)):
            raise SerialException('call to ClearCommError failed')
        return comstat.cbOutQue


if __name__ == '__main__':
    import sys
    s = Serial(0)
    sys.stdout.write('%s\n' % s)
    s = Serial()
    sys.stdout.write('%s\n' % s)
    s.baudrate = 19200
    s.databits = 7
    s.close()
    s.port = 0
    s.open()
    sys.stdout.write('%s\n' % s)