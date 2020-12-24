# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-intel/egg/respeaker/pixel_ring.py
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
import respeaker.usb_hid
from respeaker.spi import spi

class PixelRing:
    mono_mode = 1
    listening_mode = 2
    waiting_mode = 3
    speaking_mode = 4

    def __init__(self):
        self.hid = respeaker.usb_hid.get()

    def off(self):
        self.set_color(rgb=0)

    def set_color(self, rgb=None, r=0, g=0, b=0):
        if rgb:
            self.write(0, [self.mono_mode, rgb & 255, rgb >> 8 & 255, rgb >> 16 & 255])
        else:
            self.write(0, [self.mono_mode, b, g, r])

    def listen(self, direction=None):
        if direction is None:
            self.write(0, [7, 0, 0, 0])
        else:
            self.write(0, [2, 0, direction & 255, direction >> 8 & 255])
        return

    def wait(self):
        self.write(0, [self.waiting_mode, 0, 0, 0])

    def speak(self, strength, direction):
        self.write(0, [self.speaking_mode, strength, direction & 255, direction >> 8 & 255])

    def set_volume(self, volume):
        self.write(0, [5, 0, 0, volume])

    @staticmethod
    def to_bytearray(data):
        if type(data) is int:
            array = bytearray([data & 255])
        elif type(data) is bytearray:
            array = data
        elif type(data) is str:
            array = bytearray(data)
        elif type(data) is list:
            array = bytearray(data)
        else:
            raise TypeError('%s is not supported' % type(data))
        return array

    def write(self, address, data):
        data = self.to_bytearray(data)
        length = len(data)
        if self.hid:
            packet = bytearray([address & 255, address >> 8 & 255, length & 255, length >> 8 & 255]) + data
            self.hid.write(packet)
            print packet
        spi.write(address=address, data=data)

    def close(self):
        if self.hid:
            self.hid.close()


pixel_ring = PixelRing()
if __name__ == '__main__':
    import time
    pixel_ring.listen()
    time.sleep(3)
    pixel_ring.wait()
    time.sleep(3)
    for level in range(2, 8):
        pixel_ring.speak(level, 0)
        time.sleep(1)

    pixel_ring.set_volume(4)
    time.sleep(3)
    color = 8388608
    while True:
        try:
            pixel_ring.set_color(rgb=color)
            color += 16
            time.sleep(1)
        except KeyboardInterrupt:
            break

    pixel_ring.off()