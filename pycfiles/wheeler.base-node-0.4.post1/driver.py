# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\Christian\Documents\GitHub\base-node\base_node\driver.py
# Compiled at: 2016-03-15 16:13:21
from struct import pack, unpack
import numpy as np
PERSISTENT_SERIAL_NUMBER_ADDRESS = 8
INPUT = 0
OUTPUT = 1
INPUT_PULLUP = 2
LOW = 0
HIGH = 1
A0 = 14
A1 = 15
A2 = 16
A3 = 17
A4 = 18
A5 = 19
A6 = 20
A7 = 21
CMD_GET_PROTOCOL_NAME = 128
CMD_GET_PROTOCOL_VERSION = 129
CMD_GET_DEVICE_NAME = 130
CMD_GET_MANUFACTURER = 131
CMD_GET_HARDWARE_VERSION = 132
CMD_GET_SOFTWARE_VERSION = 133
CMD_GET_URL = 134
CMD_PERSISTENT_READ = 144
CMD_PERSISTENT_WRITE = 145
CMD_LOAD_CONFIG = 146
CMD_SET_PIN_MODE = 147
CMD_DIGITAL_READ = 148
CMD_DIGITAL_WRITE = 149
CMD_ANALOG_READ = 150
CMD_ANALOG_WRITE = 151
CMD_SET_PROGRAMMING_MODE = 160
RETURN_OK = 0
RETURN_GENERAL_ERROR = 1
RETURN_UNKNOWN_COMMAND = 2
RETURN_TIMEOUT = 3
RETURN_NOT_CONNECTED = 4
RETURN_BAD_INDEX = 5
RETURN_BAD_PACKET_SIZE = 6
RETURN_BAD_CRC = 7
RETURN_BAD_VALUE = 8
RETURN_MAX_PAYLOAD_EXCEEDED = 9

class BaseNode(object):

    def __init__(self, proxy, address):
        self.proxy = proxy
        self.address = address
        self.write_buffer = []

    def protocol_name(self):
        return self._get_string(CMD_GET_PROTOCOL_NAME)

    def protocol_version(self):
        return self._get_string(CMD_GET_PROTOCOL_VERSION)

    def name(self):
        return self._get_string(CMD_GET_DEVICE_NAME)

    def manufacturer(self):
        return self._get_string(CMD_GET_MANUFACTURER)

    def hardware_version(self):
        return self._get_string(CMD_GET_HARDWARE_VERSION)

    def software_version(self):
        return self._get_string(CMD_GET_SOFTWARE_VERSION)

    def url(self):
        return self._get_string(CMD_GET_URL)

    def pin_mode(self, pin, mode):
        self.serialize_uint8(pin)
        self.serialize_uint8(mode)
        self.send_command(CMD_SET_PIN_MODE)

    def digital_read(self, pin):
        self.serialize_uint8(pin)
        self.send_command(CMD_DIGITAL_READ)
        return self.read_uint8()

    def digital_write(self, pin, value):
        self.serialize_uint8(pin)
        self.serialize_uint8(value)
        self.send_command(CMD_DIGITAL_WRITE)

    def analog_read(self, pin):
        self.serialize_uint8(pin)
        self.send_command(CMD_ANALOG_READ)
        return self.read_uint16()

    def analog_write(self, pin, value):
        self.serialize_uint8(pin)
        self.serialize_uint16(value)
        self.send_command(CMD_ANALOG_WRITE)

    def persistent_read(self, address):
        self.serialize_uint16(address)
        self.send_command(CMD_PERSISTENT_READ)
        return self.read_uint8()

    def persistent_write(self, address, byte, refresh_config=False):
        """
        Write a single byte to an address in persistent memory.
        
        If refresh_config is True, load_config() is called afterward to
        refresh the configuration settings.
        """
        data = list(unpack('BB', pack('H', address)))
        data.append(byte)
        self.write_buffer.extend(data)
        self.send_command(CMD_PERSISTENT_WRITE)
        if refresh_config:
            self.load_config(False)

    def persistent_read_multibyte(self, address, count=None, dtype=np.uint8):
        nbytes = np.dtype(dtype).itemsize
        if count is not None:
            nbytes *= count
        data_bytes = np.array([ self.persistent_read(address + i) for i in xrange(nbytes)
                              ], dtype=np.uint8)
        result = data_bytes.view(dtype)
        if count is None:
            return result[0]
        else:
            return result

    def persistent_write_multibyte(self, address, data, refresh_config=False):
        """
        Write multiple bytes to an address in persistent memory.
        
        If refresh_config is True, load_config() is called afterward to
        refresh the configuration settings.
        """
        for i, byte in enumerate(data.view(np.uint8)):
            self.persistent_write(address + i, int(byte))

        if refresh_config:
            self.load_config(False)

    @property
    def serial_number(self):
        return self.persistent_read_multibyte(PERSISTENT_SERIAL_NUMBER_ADDRESS, dtype=np.uint32)

    @serial_number.setter
    def serial_number(self, value):
        self.persistent_write_multibyte(PERSISTENT_SERIAL_NUMBER_ADDRESS, np.array([value], dtype=np.uint32), True)
        self.__serial_number = value

    def load_config(self, use_defaults=False):
        self.write_buffer.append((0, 1)[use_defaults])
        self.send_command(CMD_LOAD_CONFIG)

    def set_programming_mode(self, on):
        self.write_buffer.append(on)
        self.send_command(CMD_SET_PROGRAMMING_MODE)

    def send_command(self, cmd):
        self.data = self.proxy.i2c_send_command(self.address, cmd, self.write_buffer).tolist()
        self.write_buffer = []

    def _get_string(self, cmd):
        self.send_command(cmd)
        return pack(('B' * len(self.data)), *self.data)

    def read_uint8(self):
        return self.data.pop(0)

    def read_uint16(self):
        num = self.data[0:2]
        self.data = self.data[2:]
        return unpack('H', pack('BB', *num))[0]

    def read_uint32(self):
        num = self.data[0:4]
        self.data = self.data[4:]
        return unpack('I', pack('BBBB', *num))[0]

    def read_float(self):
        num = self.data[0:4]
        self.data = self.data[4:]
        return unpack('f', pack('BBBB', *num))[0]

    def serialize_uint8(self, num):
        self.serialize(np.array([num], dtype=np.uint8))

    def serialize_uint16(self, num):
        self.serialize(np.array([num], dtype=np.uint16))

    def serialize_uint32(self, num):
        self.serialize(np.array([num], dtype=np.uint32))

    def serialize_float(self, num):
        self.serialize(np.array([num], dtype=np.float32))

    def serialize(self, data):
        for byte in data.view(np.uint8):
            self.write_buffer.append(byte)