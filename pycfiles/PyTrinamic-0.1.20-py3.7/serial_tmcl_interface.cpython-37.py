# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\PyTrinamic\connections\serial_tmcl_interface.py
# Compiled at: 2019-11-06 04:59:01
# Size of source mod 2**32: 2220 bytes
"""
Created on 30.12.2018

@author: ED
"""
from serial import Serial, SerialException
import serial.tools.list_ports
import PyTrinamic.connections.tmcl_interface as tmcl_interface

class serial_tmcl_interface(tmcl_interface):
    __doc__ = '\n    Opens a serial TMCL connection\n    '

    def __init__(self, comPort, datarate=115200, hostID=2, moduleID=1, debug=False):
        if type(comPort) != str:
            raise TypeError
        super().__init__(hostID, moduleID, debug)
        self._baudrate = datarate
        try:
            self._serial = Serial(comPort, self._baudrate)
        except SerialException as e:
            try:
                raise ConnectionError from e
            finally:
                e = None
                del e

        if self._debug:
            print('Open port: ' + self._serial.portstr)

    def close(self):
        if self._debug:
            print('Close port: ' + self._serial.portstr)
        self._serial.close()
        return 0

    def _send(self, hostID, moduleID, data):
        """
            Send the bytearray parameter [data].

            This is a required override function for using the tmcl_interface
            class.
        """
        del hostID
        del moduleID
        self._serial.write(data)

    def _recv(self, hostID, moduleID):
        """
            Read 9 bytes and return them as a bytearray.

            This is a required override function for using the tmcl_interface
            class.
        """
        del hostID
        del moduleID
        return self._serial.read(9)

    def printInfo(self):
        print('Connection: type=serial_tmcl_interface com=' + self._serial.portstr + ' baud=' + str(self._baudrate))

    def enableDebug(self, enable):
        self._debug = enable

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
            connected.append(element.device)

        return connected