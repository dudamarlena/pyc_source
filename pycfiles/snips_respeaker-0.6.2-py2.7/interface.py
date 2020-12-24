# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-intel/egg/respeaker/usb_hid/interface.py
# Compiled at: 2017-08-02 09:57:35
"""
 USB HID API from pyOCD project
 Copyright (c) 2006-2013 ARM Limited

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

class Interface(object):

    def __init__(self):
        self.vid = 0
        self.pid = 0
        self.vendor_name = ''
        self.product_name = ''
        self.packet_count = 1

    def init(self):
        pass

    def write(self, data):
        pass

    def read(self, size=-1, timeout=-1):
        pass

    def getInfo(self):
        return self.vendor_name + ' ' + self.product_name + ' (' + str(hex(self.vid)) + ', ' + str(hex(self.pid)) + ')'

    def setPacketCount(self, count):
        pass

    def getPacketCount(self):
        return self.packet_count

    def close(self):
        pass