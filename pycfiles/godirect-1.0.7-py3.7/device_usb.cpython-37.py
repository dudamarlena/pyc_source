# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/godirect/device_usb.py
# Compiled at: 2019-01-28 13:02:59
# Size of source mod 2**32: 2660 bytes
import hid, logging
from .device import GoDirectDevice

class GoDirectDeviceUSB(GoDirectDevice):
    __doc__ = ' GoDirectDeviceUSB overrides GoDirectDevice with USB specific functions for connecting,\n\tdisconnecting, writing, and reading.\n\t'
    VID = 2295
    PID = 16

    def __init__(self, backend):
        self._logger = logging.getLogger('godirect')
        self._device = None
        self._connected = False
        super().__init__(backend)

    def is_connected(self):
        """ Returns True if connected, False otherwise.
                """
        return self._connected

    def _connect(self):
        """ Open this device
                Returns:
                        True on success, False otherwise
                """
        self._connected = False
        self._device = hid.device()
        self._device.open_path(self._id)
        if self._device == None:
            self._connected = False
            return False
        self._connected = True
        return True

    def _disconnect(self):
        """ Close this device
                """
        self._connected = False
        try:
            self._device.close()
        except:
            self._logger.error('hid close failed')

    def _write(self, buff):
        """ Write data to this device
                Args:
                        buff: byte[] data to send
                """
        packet = []
        packet.append(0)
        packet.append(len(buff))
        for i in range(0, len(buff)):
            packet.append(buff[i])

        for i in range(len(packet), 65):
            packet.append(0)

        self._device.write(packet)
        str = 'HID WRITE: >>>'
        str += ' '.join(['%02X ' % c for c in packet]).strip()
        self._logger.debug(str)
        return True

    def _read(self, timeout):
        """ Read data from this device while blocking for up to timeout ms
                Args:
                        timeout: ms to wait for data before failing the read
                Returns:
                        bytearray: data received from device
                """
        buff = self._device.read(65, timeout)
        if len(buff) <= 1:
            print('ERROR: HID read timeout!', timeout)
            return bytearray()
        buff = buff[1:]
        packet_len = buff[1]
        while len(buff) < packet_len:
            buff += self._device.read(65, timeout)[1:buff[0]]
            if len(buff) >= 1 and len(buff) >= packet_len:
                break

        if len(buff) > packet_len:
            buff = buff[:packet_len]
        str = 'HID READ: <<<'
        str += ' '.join(['%02X ' % c for c in buff]).strip()
        self._logger.debug(str)
        return bytearray(buff)