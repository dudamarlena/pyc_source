# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\PyTrinamic\connections\usb_tmcl_interface.py
# Compiled at: 2020-02-03 05:12:15
# Size of source mod 2**32: 1975 bytes
"""
Created on 29.05.2019

@author: LH
"""
import serial.tools.list_ports
import PyTrinamic.connections.serial_tmcl_interface as serial_tmcl_interface

class usb_tmcl_interface(serial_tmcl_interface):
    __doc__ = '\n    Opens a USB TMCL connection.\n\n    This class is almost the same as the class for serial TMCL connections.\n    The only difference are the functions for the connection manager, which\n    filter the available serial connections to only include the serial over\n    USB ones.\n    '
    _usb_tmcl_interface__USB_IDS = [
     {'VID':10812, 
      'PID':1792},
     {'VID':5840, 
      'PID':1121},
     {'VID':5840, 
      'PID':2020},
     {'VID':10812, 
      'PID':512},
     {'VID':10812, 
      'PID':256}]

    def __init__(self, comPort, datarate=115200, hostID=2, moduleID=1, debug=False):
        super().__init__(comPort, datarate, hostID, moduleID, debug)

    def printInfo(self):
        print('Connection: type=usb_tmcl_interface com=' + self._serial.portstr + ' baud=' + str(self._baudrate))

    @staticmethod
    def supportsTMCL():
        return True

    @staticmethod
    def list():
        """
            Return a list of available connection ports as a list of strings.

            This function is required for using this interface with the
            connection manager.
        """
        connected = []
        for element in sorted(serial.tools.list_ports.comports()):
            for entry in usb_tmcl_interface._usb_tmcl_interface__USB_IDS:
                if entry['VID'] == element.vid and entry['PID'] == element.pid:
                    connected.append(element.device)

        return connected