# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-intel/egg/respeaker/usb_hid/pyusb_backend.py
# Compiled at: 2017-08-16 07:40:18
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
import logging, os, threading
try:
    import usb.core, usb.util
except:
    if os.name == 'posix' and not os.uname()[0] == 'Darwin':
        logging.error('PyUSB is required on a Linux Machine')
    isAvailable = False
else:
    isAvailable = True

class PyUSB(Interface):
    """
    This class provides basic functions to access
    a USB HID device using pyusb:
        - write/read an endpoint
    """
    vid = 0
    pid = 0
    intf_number = 0
    isAvailable = isAvailable

    def __init__(self):
        super(PyUSB, self).__init__()
        self.ep_out = None
        self.ep_in = None
        self.dev = None
        self.closed = False
        self.rcv_data = []
        self.read_sem = threading.Semaphore(0)
        return

    def start_rx(self):
        self.thread = threading.Thread(target=self.rx_task)
        self.thread.daemon = True
        self.thread.start()

    def rx_task(self):
        while not self.closed:
            self.read_sem.acquire()
            if not self.closed:
                self.rcv_data.append(self.ep_in.read(self.ep_in.wMaxPacketSize, -1))

    @staticmethod
    def getAllConnectedInterface():
        """
        returns all the connected devices which matches PyUSB.vid/PyUSB.pid.
        returns an array of PyUSB (Interface) objects
        """
        all_devices = usb.core.find(find_all=True)
        if not all_devices:
            logging.debug('No device connected')
            return []
        else:
            boards = []
            for board in all_devices:
                interface_number = -1
                try:
                    product = board.iProduct
                except usb.core.USBError as error:
                    logging.warning('Exception getting product string: %s', error)
                    continue

                if product is None or board.idVendor != 10374:
                    usb.util.dispose_resources(board)
                    continue
                config = board.get_active_configuration()
                for interface in config:
                    if interface.bInterfaceClass == 3:
                        interface_number = interface.bInterfaceNumber
                        break

                if interface_number == -1:
                    continue
                try:
                    if board.is_kernel_driver_active(interface_number):
                        board.detach_kernel_driver(interface_number)
                except Exception as e:
                    pass

                ep_in, ep_out = (None, None)
                for ep in interface:
                    if ep.bEndpointAddress & 128:
                        ep_in = ep
                    else:
                        ep_out = ep

                if not ep_in:
                    logging.error('Endpoints not found')
                    return
                new_board = PyUSB()
                new_board.ep_in = ep_in
                new_board.ep_out = ep_out
                new_board.dev = board
                new_board.vid = board.idVendor
                new_board.pid = board.idProduct
                new_board.intf_number = interface_number
                new_board.product_name = product
                new_board.vendor_name = board.manufacturer
                new_board.serial_number = board.serial_number
                new_board.start_rx()
                boards.append(new_board)

            return boards

    def write(self, data):
        """
        write data on the OUT endpoint associated to the HID interface
        """
        self.read_sem.release()
        if not self.ep_out:
            bmRequestType = 33
            bmRequest = 9
            wValue = 512
            wIndex = self.intf_number
            self.dev.ctrl_transfer(bmRequestType, bmRequest, wValue, wIndex, data)
            return
        self.ep_out.write(data)

    def read(self):
        """
        read data on the IN endpoint associated to the HID interface
        """
        while len(self.rcv_data) == 0:
            pass

        return self.rcv_data.pop(0)

    def setPacketCount(self, count):
        self.packet_count = count

    def getSerialNumber(self):
        return self.serial_number

    def close(self):
        """
        close the interface
        """
        logging.debug('closing interface')
        self.closed = True
        self.read_sem.release()
        self.thread.join()
        usb.util.dispose_resources(self.dev)