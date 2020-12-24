# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-intel/egg/respeaker/usb_hid/pywinusb_backend.py
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
import logging, os, collections
from time import time
try:
    import pywinusb.hid as hid
except:
    if os.name == 'nt':
        logging.error('PyWinUSB is required on a Windows Machine')
    isAvailable = False
else:
    isAvailable = True

class PyWinUSB(Interface):
    """
    This class provides basic functions to access
    a USB HID device using pywinusb:
        - write/read an endpoint
    """
    vid = 0
    pid = 0
    isAvailable = isAvailable

    def __init__(self):
        super(PyWinUSB, self).__init__()
        self.report = []
        self.rcv_data = collections.deque()
        self.device = None
        return

    def rx_handler(self, data):
        self.rcv_data.append(data[1:])

    def open(self):
        self.device.set_raw_data_handler(self.rx_handler)
        self.device.open(shared=False)

    @staticmethod
    def getAllConnectedInterface():
        """
        returns all the connected CMSIS-DAP devices
        """
        all_devices = hid.find_all_hid_devices()
        all_mbed_devices = []
        for d in all_devices:
            if d.product_name.find('MicArray') >= 0:
                all_mbed_devices.append(d)

        boards = []
        for dev in all_mbed_devices:
            try:
                dev.open(shared=False)
                report = dev.find_output_reports()
                if len(report) == 1:
                    new_board = PyWinUSB()
                    new_board.report = report[0]
                    new_board.vendor_name = dev.vendor_name
                    new_board.product_name = dev.product_name
                    new_board.serial_number = dev.serial_number
                    new_board.vid = dev.vendor_id
                    new_board.pid = dev.product_id
                    new_board.device = dev
                    new_board.device.set_raw_data_handler(new_board.rx_handler)
                    boards.append(new_board)
            except Exception as e:
                logging.error('Receiving Exception: %s', e)
                dev.close()

        return boards

    def write(self, data):
        """
        write data on the OUT endpoint associated to the HID interface
        """
        for _ in range(64 - len(data)):
            data.append(0)

        self.report.send(bytearray([0]) + data)

    def read(self, timeout=1.0):
        """
        read data on the IN endpoint associated to the HID interface
        """
        start = time()
        while len(self.rcv_data) == 0:
            if time() - start > timeout:
                raise Exception('Read timed out')

        return self.rcv_data.popleft()

    def setPacketCount(self, count):
        self.packet_count = count

    def getSerialNumber(self):
        return self.serial_number

    def close(self):
        """
        close the interface
        """
        logging.debug('closing interface')
        self.device.close()