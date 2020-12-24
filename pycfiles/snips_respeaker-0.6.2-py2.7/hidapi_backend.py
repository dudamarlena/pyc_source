# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-intel/egg/respeaker/usb_hid/hidapi_backend.py
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
from respeaker.usb_hid.interface import Interface
import logging, os
try:
    import hid
except:
    if os.name == 'posix' and os.uname()[0] == 'Darwin':
        logging.error('cython-hidapi is required on a Mac OS X Machine')
    isAvailable = False
else:
    isAvailable = True

class HidApiUSB(Interface):
    """
    This class provides basic functions to access
    a USB HID device using cython-hidapi:
        - write/read an endpoint
    """
    vid = 0
    pid = 0
    isAvailable = isAvailable

    def __init__(self):
        super(HidApiUSB, self).__init__()
        self.device = None
        return

    def open(self):
        pass

    @staticmethod
    def getAllConnectedInterface():
        """
        returns all the connected devices which matches HidApiUSB.vid/HidApiUSB.pid.
        returns an array of HidApiUSB (Interface) objects
        """
        devices = hid.enumerate()
        if not devices:
            logging.debug('No Mbed device connected')
            return []
        boards = []
        for deviceInfo in devices:
            product_name = deviceInfo['product_string']
            if product_name.find('ReSpeaker') < 0 and product_name.find('MicArray') < 0:
                continue
            try:
                dev = hid.device(vendor_id=deviceInfo['vendor_id'], product_id=deviceInfo['product_id'], path=deviceInfo['path'])
            except IOError:
                logging.debug('Failed to open Mbed device')
                continue

            new_board = HidApiUSB()
            new_board.vendor_name = deviceInfo['manufacturer_string']
            new_board.product_name = deviceInfo['product_string']
            new_board.serial_number = deviceInfo['serial_number']
            new_board.vid = deviceInfo['vendor_id']
            new_board.pid = deviceInfo['product_id']
            new_board.device_info = deviceInfo
            new_board.device = dev
            try:
                dev.open_path(deviceInfo['path'])
            except AttributeError:
                pass
            except IOError:
                continue

            boards.append(new_board)

        return boards

    def write(self, data):
        """
        write data on the OUT endpoint associated to the HID interface
        """
        for _ in range(64 - len(data)):
            data.append(0)

        logging.debug('send: %s', data)
        self.device.write([0] + data)

    def read(self, timeout=-1):
        """
        read data on the IN endpoint associated to the HID interface
        """
        return self.device.read(64)

    def getSerialNumber(self):
        return self.serial_number

    def close(self):
        """
        close the interface
        """
        logging.debug('closing interface')
        self.device.close()

    def setPacketCount(self, count):
        self.packet_count = count