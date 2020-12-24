# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/philip_pal/serial_driver.py
# Compiled at: 2020-03-03 05:45:43
# Size of source mod 2**32: 3939 bytes
"""Serial Driver for philip_pal
This module handles generic connection and IO to the serial driver.
"""
import logging, time
from serial import Serial, serial_for_url, SerialException
from serial.tools import list_ports

class SerialDriver:
    __doc__ = 'Serial Port Driver\n\n    Contains all reusable functions for connecting, sending and receiving\n    data.  Arguments are passed through to the standard pyserial driver.  The\n    defaults are changed.  Also if env variables are defined they get used as\n    defaults.  Automatically opens the serial port on initialize.  If nothing\n    is specified the port is set to the first available port.\n\n    Args:\n        (*args, **kwargs) -> See pyserial for documentation of args\n    '
    DEFAULT_TIMEOUT = 0.5
    DEFAULT_BAUDRATE = 115200

    def __init__(self, *args, **kwargs):
        (self._connect)(*args, **kwargs)
        time.sleep(0.05)
        self.writeline('')
        try:
            self.readline(0.3)
        except TimeoutError:
            pass

    def _connect(self, *args, **kwargs):
        if 'timeout' not in kwargs:
            kwargs['timeout'] = self.DEFAULT_TIMEOUT
        elif len(args) < 2:
            if 'baudrate' not in kwargs:
                kwargs['baudrate'] = self.DEFAULT_BAUDRATE
        else:
            if len(args) == 0:
                if 'port' not in kwargs:
                    kwargs['port'] = list_ports.comports()[0][0]
            logging.debug('Serial connection args %r -- %r', args, kwargs)
            try:
                self._dev = Serial(*args, **kwargs)
            except SerialException:
                self._dev = serial_for_url(*args, **kwargs)

        self._args = args
        self._kwargs = kwargs

    def open(self, *args, **kwargs):
        """Open a Serial Connection

        Args:
            (*args, **kwargs) -> See pyserial for documentation of args
        """
        logging.debug('Opening port')
        (self._connect)(*args, **kwargs)

    def close(self):
        """Close serial connection

        """
        logging.debug('Closing %s', self._dev.port)
        self._dev.close()

    def readline(self, timeout=None):
        """Read Line from Serial

        Read and decode to utf-8 data from the serial port.  Raises
        TimeoutError exception if an nothing is read.

        Args:
            timeout: Optional timeout value for command specific timeouts
        Returns:
            str: string of utf8 encoded data
        """
        if timeout is None:
            res_bytes = self._dev.readline()
        else:
            default_timeout = self._dev.timeout
            self._dev.timeout = timeout
            res_bytes = self._dev.readline()
            self._dev.timeout = default_timeout
        response = res_bytes.decode('utf-8', errors='replace')
        response = response.strip('\x00')
        if response == '':
            self.close()
            (self._connect)(*self._args, **self._kwargs)
            raise TimeoutError('Timeout during serial readline')
        logging.debug('Response: %s', response.replace('\n', ''))
        return response

    def writeline(self, line):
        """Write Line to Serial
        Writes line to the serial port and adds a newline and encode to utf-8.

        Args:
            line(str): string or list of bytes to send to the driver.
        """
        self._dev.reset_input_buffer()
        logging.debug('Sending: ' + line)
        self._dev.write((line + '\n').encode('utf-8'))