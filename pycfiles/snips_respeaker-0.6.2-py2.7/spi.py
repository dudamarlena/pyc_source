# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-intel/egg/respeaker/spi.py
# Compiled at: 2017-08-02 09:57:35
"""
 ReSpeaker Python Library
 Copyright (c) 2016 Seeed Technology Limited.

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
"""
import platform
CRC8_TABLE = (0, 7, 14, 9, 28, 27, 18, 21, 56, 63, 54, 49, 36, 35, 42, 45, 112, 119,
              126, 121, 108, 107, 98, 101, 72, 79, 70, 65, 84, 83, 90, 93, 224, 231,
              238, 233, 252, 251, 242, 245, 216, 223, 214, 209, 196, 195, 202, 205,
              144, 151, 158, 153, 140, 139, 130, 133, 168, 175, 166, 161, 180, 179,
              186, 189, 199, 192, 201, 206, 219, 220, 213, 210, 255, 248, 241, 246,
              227, 228, 237, 234, 183, 176, 185, 190, 171, 172, 165, 162, 143, 136,
              129, 134, 147, 148, 157, 154, 39, 32, 41, 46, 59, 60, 53, 50, 31, 24,
              17, 22, 3, 4, 13, 10, 87, 80, 89, 94, 75, 76, 69, 66, 111, 104, 97,
              102, 115, 116, 125, 122, 137, 142, 135, 128, 149, 146, 155, 156, 177,
              182, 191, 184, 173, 170, 163, 164, 249, 254, 247, 240, 229, 226, 235,
              236, 193, 198, 207, 200, 221, 218, 211, 212, 105, 110, 103, 96, 117,
              114, 123, 124, 81, 86, 95, 88, 77, 74, 67, 68, 25, 30, 23, 16, 5, 2,
              11, 12, 33, 38, 47, 40, 61, 58, 51, 52, 78, 73, 64, 71, 82, 85, 92,
              91, 118, 113, 120, 127, 106, 109, 100, 99, 62, 57, 48, 55, 34, 37,
              44, 43, 6, 1, 8, 15, 26, 29, 20, 19, 174, 169, 160, 167, 178, 181,
              188, 187, 150, 145, 152, 159, 138, 141, 132, 131, 222, 217, 208, 215,
              194, 197, 204, 203, 230, 225, 232, 239, 250, 253, 244, 243)

def crc8(data):
    result = 0
    for b in data:
        result = CRC8_TABLE[(result ^ b)]

    return result


if platform.machine() == 'mips':
    from gpio import *
    from threading import RLock
    import time

    class SPI:

        def __init__(self, sck=15, mosi=17, miso=16, cs=14):
            self.sck = Gpio(sck, OUTPUT)
            self.mosi = Gpio(mosi, OUTPUT)
            self.miso = Gpio(miso, INPUT)
            self.cs = Gpio(cs, OUTPUT)
            self.cs.write(1)
            self.frequency(10000000)
            self.format(8, 0)
            self.lock = RLock()

        def frequency(self, hz=10000000):
            self.freq = hz

        def format(self, bits=8, mode=0):
            self.bits = bits
            self.mode = mode
            self.polarity = mode >> 1 & 1
            self.phase = mode & 1
            self.sck.write(self.polarity)

        def _exchange(self, data):
            read = 0
            for bit in range(self.bits - 1, -1, -1):
                self.mosi.write(data >> bit & 1)
                if 0 == self.phase:
                    read |= self.miso.read() << bit
                self.sck.write(1 - self.polarity)
                if 1 == self.phase:
                    read |= self.miso.read() << bit
                self.sck.write(self.polarity)

            return read

        def _write(self, data):
            response = bytearray()
            self.cs.write(0)
            if type(data) is int:
                response.append(self._exchange(data))
            elif type(data) is bytearray:
                for b in data:
                    response.append(self._exchange(b))

            elif type(data) is str:
                for b in bytearray(data):
                    response.append(self._exchange(b))

            elif type(data) is list:
                for item in data:
                    self.write(item)

            else:
                self.cs.write(1)
                raise TypeError('%s is not supported' % type(data))
            self.cs.write(1)
            return response

        def write(self, data=None, address=None):
            with self.lock:
                if address is not None:
                    data = bytearray([165, address & 255, len(data) & 255]) + data + bytearray([crc8(data)])
                    response = self._write(data)[3:-1]
                else:
                    response = self._write(data)
                return response
            return

        def close(self):
            pass


else:

    class SPI:

        def __init__(self):
            pass

        def write(self, data=None, address=None):
            pass

        def close(self):
            pass


spi = SPI()
if __name__ == '__main__':
    while True:
        spi.write('hello\n')
        time.sleep(1)