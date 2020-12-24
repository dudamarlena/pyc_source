# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./build/lib.linux-x86_64-2.7/serial/urlhandler/protocol_hwgrep.py
# Compiled at: 2015-08-29 23:24:23
import serial, serial.tools.list_ports
try:
    basestring
except NameError:
    basestring = str

class Serial(serial.Serial):
    """Just inherit the native Serial port implementation and patch the port property."""

    @serial.Serial.port.setter
    def port(self, value):
        """translate port name before storing it"""
        if isinstance(value, basestring) and value.startswith('hwgrep://'):
            serial.Serial.port.__set__(self, self.from_url(value))
        else:
            serial.Serial.port.__set__(self, value)

    def from_url(self, url):
        """extract host and port from an URL string"""
        if url.lower().startswith('hwgrep://'):
            url = url[9:]
        for port, desc, hwid in serial.tools.list_ports.grep(url):
            return port
        else:
            raise serial.SerialException('no ports found matching regexp %r' % (url,))


if __name__ == '__main__':
    s = Serial(None)
    s.port = 'hwgrep://ttyS0'
    print s