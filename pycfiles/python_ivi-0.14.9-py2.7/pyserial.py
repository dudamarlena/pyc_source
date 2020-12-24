# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ivi/interface/pyserial.py
# Compiled at: 2014-09-01 23:09:59
"""

Python Interchangeable Virtual Instrument Library

Copyright (c) 2012-2014 Alex Forencich

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

"""
import serial, time, re

def parse_visa_resource_string(resource_string):
    m = re.match('^(?P<prefix>(?P<type>ASRL)\\d*)(::(?P<arg1>[^\\s:]+))?(::(?P<suffix>INSTR))$', resource_string, re.I)
    if m is not None:
        return dict(type=m.group('type').upper(), prefix=m.group('prefix'), arg1=m.group('arg1'), suffix=m.group('suffix'))
    else:
        return


class SerialInstrument:
    """Serial instrument interface client"""

    def __init__(self, port=None, baudrate=9600, bytesize=8, paritymode=0, stopbits=1, timeout=None, xonxoff=False, rtscts=False, dsrdtr=False):
        if port.upper().startswith('ASRL') and '::' in port:
            res = parse_visa_resource_string(port)
            if res is None:
                raise IOError('Invalid resource string')
            index = res['prefix'][4:]
            if len(index) > 0:
                port = int(index)
            else:
                t = res['arg1'].split(',')
                port = t[0]
                if len(t) > 1:
                    baudrate = int(t[1])
        self.serial = serial.Serial(port)
        self.term_char = '\n'
        self.port = port
        self.baudrate = baudrate
        self.bytesize = bytesize
        self.paritymode = paritymode
        self.stopbits = stopbits
        self.timeout = timeout
        self.xonxoff = xonxoff
        self.rtscts = rtscts
        self.dsrdtr = dsrdtr
        self.wait_dsr = False
        self.message_delay = 0
        self.update_settings()
        return

    def update_settings(self):
        self.serial.baudrate = self.baudrate
        if self.bytesize == 5:
            self.serial.bytesize = serial.FIVEBITS
        elif self.bytesize == 6:
            self.serial.bytesize = serial.SIXBITS
        elif self.bytesize == 7:
            self.serial.bytesize = serial.SEVENBITS
        else:
            self.serial.bytesize = serial.EIGHTBITS
        if self.paritymode == 1:
            self.serial.paritymode = serial.PARITY_ODD
        elif self.paritymode == 2:
            self.serial.paritymode = serial.PARITY_EVEN
        elif self.paritymode == 3:
            self.serial.paritymode = serial.PARITY_MARK
        elif self.paritymode == 4:
            self.serial.paritymode = serial.PARITY_SPACE
        else:
            self.serial.paritymode = serial.PARITY_NONE
        if self.stopbits == 1.5:
            self.serial.stopbits = serial.STOPBITS_ONE_POINT_FIVE
        elif self.stopbits == 2:
            self.serial.stopbits = serial.STOPBITS_TWO
        else:
            self.serial.stopbits = serial.STOPBITS_ONE
        self.serial.timeout = self.timeout
        self.serial.xonxoff = self.xonxoff
        self.serial.rtscts = self.rtscts
        self.serial.dsrdtr = self.dsrdtr
        if self.dsrdtr:
            self.wait_dsr = True
            self.message_delay = 0.1

    def write_raw(self, data):
        """Write binary data to instrument"""
        if self.term_char is not None:
            data += str(self.term_char).encode('utf-8')[0:1]
        self.serial.write(data)
        if self.message_delay > 0:
            time.sleep(self.message_delay)
        if self.wait_dsr:
            while not self.serial.getDSR():
                time.sleep(0.01)

        return

    def read_raw(self, num=-1):
        """Read binary data from instrument"""
        data = ''
        term_char = str(self.term_char).encode('utf-8')[0:1]
        while True:
            c = self.serial.read(1)
            data += c
            num -= 1
            if c == term_char:
                break
            if num == 0:
                break

        return data

    def ask_raw(self, data, num=-1):
        """Write then read binary data"""
        self.write_raw(data)
        return self.read_raw(num)

    def write(self, message, encoding='utf-8'):
        """Write string to instrument"""
        if type(message) is tuple or type(message) is list:
            for message_i in message:
                self.write(message_i, encoding)

            return
        self.write_raw(str(message).encode(encoding))

    def read(self, num=-1, encoding='utf-8'):
        """Read string from instrument"""
        return self.read_raw(num).decode(encoding).rstrip('\r\n')

    def ask(self, message, num=-1, encoding='utf-8'):
        """Write then read string"""
        if type(message) is tuple or type(message) is list:
            val = list()
            for message_i in message:
                val.append(self.ask(message_i, num, encoding))

            return val
        self.write(message, encoding)
        return self.read(num, encoding)

    def read_stb(self):
        """Read status byte"""
        raise NotImplementedError()

    def trigger(self):
        """Send trigger command"""
        self.write('*TRG')

    def clear(self):
        """Send clear command"""
        self.write('*CLS')

    def remote(self):
        """Send remote command"""
        raise NotImplementedError()

    def local(self):
        """Send local command"""
        raise NotImplementedError()

    def lock(self):
        """Send lock command"""
        raise NotImplementedError()

    def unlock(self):
        """Send unlock command"""
        raise NotImplementedError()