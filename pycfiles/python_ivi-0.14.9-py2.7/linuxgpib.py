# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ivi/interface/linuxgpib.py
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
import Gpib, re

def parse_visa_resource_string(resource_string):
    m = re.match('^(?P<prefix>(?P<type>GPIB)\\d*)(::(?P<arg1>[^\\s:]+))(::(?P<suffix>INSTR))$', resource_string, re.I)
    if m is not None:
        return dict(type=m.group('type').upper(), prefix=m.group('prefix'), arg1=m.group('arg1'), suffix=m.group('suffix'))
    else:
        return


class LinuxGpibInstrument:
    """Linux GPIB wrapper instrument interface client"""

    def __init__(self, name='gpib0', pad=None, sad=0, timeout=13, send_eoi=1, eos_mode=0):
        if name.upper().startswith('GPIB') and '::' in name:
            res = parse_visa_resource_string(name)
            if res is None:
                raise IOError('Invalid resource string')
            index = res['prefix'][4:]
            if len(index) > 0:
                index = int(index)
            else:
                index = 0
            addr = int(res['arg1'])
            name = index
            pad = addr
        self.gpib = Gpib.Gpib(name, pad, sad, timeout, send_eoi, eos_mode)
        return

    def write_raw(self, data):
        """Write binary data to instrument"""
        self.gpib.write(data)

    def read_raw(self, num=-1):
        """Read binary data from instrument"""
        if num < 0:
            num = 512
        return self.gpib.read(num)

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
        self.gpib.trigger()

    def clear(self):
        """Send clear command"""
        self.gpib.clear()

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