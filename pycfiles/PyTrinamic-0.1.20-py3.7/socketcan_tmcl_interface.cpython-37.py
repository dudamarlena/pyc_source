# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\PyTrinamic\connections\socketcan_tmcl_interface.py
# Compiled at: 2020-01-29 04:36:38
# Size of source mod 2**32: 3380 bytes
"""
Created on 03.01.2020

@author: SW

Use following command under linux to activate can socket
sudo ip link set can0 down type can bitrate 1000000

"""
import can
import PyTrinamic.connections.tmcl_interface as tmcl_interface
from can import CanError
_CHANNELS = [
 'can0', 'can1', 'can2', 'can3', 'can4', 'can5', 'can6', 'can7']

class socketcan_tmcl_interface(tmcl_interface):
    __doc__ = '\n    This class implements a TMCL connection over a SocketCAN adapter.\n    '

    def __init__(self, port, datarate=1000000, hostID=2, moduleID=1, debug=False):
        if type(port) != str:
            raise TypeError
        else:
            if port not in _CHANNELS:
                raise ValueError('Invalid port')
            tmcl_interface.__init__(self, hostID, moduleID, debug)
            self._socketcan_tmcl_interface__debug = debug
            self._socketcan_tmcl_interface__channel = port
            self._socketcan_tmcl_interface__bitrate = datarate
            try:
                self._socketcan_tmcl_interface__connection = can.Bus(interface='socketcan', channel=(self._socketcan_tmcl_interface__channel), bitrate=(self._socketcan_tmcl_interface__bitrate))
                self._socketcan_tmcl_interface__connection.set_filters([{'can_id':hostID,  'can_mask':127}])
            except CanError as e:
                try:
                    self._socketcan_tmcl_interface__connection = None
                    raise ConnectionError('Failed to connect to SocketCAN bus') from e
                finally:
                    e = None
                    del e

        if self._socketcan_tmcl_interface__debug:
            print('Opened bus on channel ' + self._socketcan_tmcl_interface__channel)

    def close(self):
        if self._socketcan_tmcl_interface__debug:
            print('Closing PCAN bus')
        self._socketcan_tmcl_interface__connection.shutdown()

    def _send(self, hostID, moduleID, data):
        """
            Send the bytearray parameter [data].

            This is a required override function for using the tmcl_interface
            class.
        """
        del hostID
        msg = can.Message(arbitration_id=moduleID, is_extended_id=False, data=(data[1:]))
        try:
            self._socketcan_tmcl_interface__connection.send(msg)
        except CanError as e:
            try:
                raise ConnectionError('Failed to send a TMCL message') from e
            finally:
                e = None
                del e

    def _recv(self, hostID, moduleID):
        """
            Read 9 bytes and return them as a bytearray.

            This is a required override function for using the tmcl_interface
            class.
        """
        del moduleID
        try:
            msg = self._socketcan_tmcl_interface__connection.recv(timeout=3)
        except CanError as e:
            try:
                raise ConnectionError('Failed to receive a TMCL message') from e
            finally:
                e = None
                del e

        if not msg:
            raise ConnectionError('Recv timed out')
        if msg.arbitration_id != hostID:
            raise ConnectionError('Received wrong ID')
        return bytearray([msg.arbitration_id]) + msg.data

    def printInfo(self):
        print('Connection: type=pcan_tmcl_interface channel=' + self._socketcan_tmcl_interface__channel + ' bitrate=' + str(self._socketcan_tmcl_interface__bitrate))

    def enableDebug(self, enable):
        self._socketcan_tmcl_interface__debug = enable

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
        return _CHANNELS