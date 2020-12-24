# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/monitorcontrol/vcp/vcp_linux.py
# Compiled at: 2020-02-29 14:56:52
# Size of source mod 2**32: 8762 bytes
from typing import List, Tuple
import os, sys, time, struct
from .vcp_abc import VCP, VCPError
if sys.platform.startswith('linux'):
    import pyudev, fcntl

class LinuxVCP(VCP):
    __doc__ = "\n    Linux API access to a monitor's virtual control panel.\n\n    References:\n        https://github.com/Informatic/python-ddcci\n        https://github.com/siemer/ddcci/\n    "
    GET_VCP_HEADER_LENGTH = 2
    PROTOCOL_FLAG = 128
    GET_VCP_CMD = 1
    GET_VCP_REPLY = 2
    SET_VCP_CMD = 3
    GET_VCP_TIMEOUT = 0.04
    CMD_RATE = 0.05
    DDCCI_ADDR = 55
    HOST_ADDRESS = 80
    I2C_SLAVE = 1795
    GET_VCP_RESULT_CODES = {0:'No Error', 
     1:'Unsupported VCP code'}

    def __init__(self, bus_number: int):
        """
        Args:
            bus_number: I2C bus number
        """
        self.bus_number = bus_number
        self.fd = None
        self.fp = None

    def __enter__(self):
        self.open()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def open(self):
        """
        Opens the connection to the monitor.

        Raises:
            VCPError: unable to open monitor
        """
        try:
            self.fp = f"/dev/i2c-{self.bus_number}"
            self.fd = os.open(self.fp, os.O_RDWR)
            fcntl.ioctl(self.fd, self.I2C_SLAVE, self.DDCCI_ADDR)
            self.read_bytes(1)
        except PermissionError as e:
            raise VCPError(f"permission error for {self.fp}") from e
        except OSError as e:
            raise VCPError(f"unable to open VCP at {self.fp}") from e

    def close(self):
        """
        Closes the connection to the monitor.

        Raises:
            VCPError: unable to close monitor
        """
        if self.fd is not None:
            try:
                os.close(self.fd)
            except OSError as e:
                raise VCPError('unable to close descriptor') from e

            self.fd = None

    def set_vcp_feature(self, code: int, value: int):
        """
        Sets the value of a feature on the virtual control panel.

        Args:
            code: feature code
            value: feature value

        Raises:
            VCPError: failed to set VCP feature
        """
        self.rate_limt()
        data = bytearray()
        data.append(self.SET_VCP_CMD)
        data.append(code)
        low_byte, high_byte = struct.pack('H', value)
        data.append(high_byte)
        data.append(low_byte)
        data.insert(0, len(data) | self.PROTOCOL_FLAG)
        data.insert(0, self.HOST_ADDRESS)
        data.append(self.get_checksum(data))
        self.write_bytes(data)
        self.last_set = time.time()

    def get_vcp_feature(self, code: int) -> Tuple[(int, int)]:
        """
        Gets the value of a feature from the virtual control panel.

        Args:
            code: feature code

        Returns:
            current feature value, maximum feature value

        Raises:
            VCPError: failed to get VCP feature
        """
        self.rate_limt()
        data = bytearray()
        data.append(self.GET_VCP_CMD)
        data.append(code)
        data.insert(0, len(data) | self.PROTOCOL_FLAG)
        data.insert(0, self.HOST_ADDRESS)
        data.append(self.get_checksum(data))
        self.write_bytes(data)
        time.sleep(self.GET_VCP_TIMEOUT)
        header = self.read_bytes(self.GET_VCP_HEADER_LENGTH)
        source, length = struct.unpack('BB', header)
        length &= ~self.PROTOCOL_FLAG
        payload = self.read_bytes(length + 1)
        payload, checksum = struct.unpack(f"{length}sB", payload)
        calculated_checksum = self.get_checksum(header + payload)
        checksum_xor = checksum ^ calculated_checksum
        if checksum_xor:
            raise VCPError(f"checksum does not match: {checksum_xor}")
        reply_code, result_code, vcp_opcode, vcp_type_code, feature_max, feature_current = struct.unpack('>BBBBHH', payload)
        if reply_code != self.GET_VCP_REPLY:
            raise VCPError(f"received unexpected response code: {reply_code}")
        if vcp_opcode != code:
            raise VCPError(f"received unexpected opcode: {vcp_opcode}")
        if result_code > 0:
            try:
                message = self.GET_VCP_RESULT_CODES[result_code]
            except KeyError:
                message = f"received result with unknown code: {result_code}"

            raise VCPError(message)
        return (feature_current, feature_max)

    def get_checksum(self, data: List, prime: bool=False) -> int:
        """
        Computes the checksum for a set of data, with the option to
        use the virtual host address (per the DDC-CI specification).

        Args:
            data: data array to transmit
            prime: compute checksum using the 0x50 virtual host address

        Returns:
            checksum for the data
        """
        checksum = self.HOST_ADDRESS
        for data_byte in data:
            checksum ^= data_byte

        return checksum

    def rate_limt(self):
        """ Rate limits messages to the VCP. """
        try:
            self.last_set
        except AttributeError:
            return
        else:
            rate_delay = self.CMD_RATE - (time.time() - self.last_set)
            if rate_delay > 0:
                time.sleep(rate_delay)

    def read_bytes(self, num_bytes: int) -> bytes:
        """
        Reads bytes from the I2C bus.

        Args:
            num_bytes: number of bytes to read

        Raises:
            VCPError: unable to read data
        """
        try:
            return os.read(self.fd, num_bytes)
        except OSError as e:
            raise VCPError('unable to read from I2C bus') from e

    def write_bytes(self, data: bytes):
        """
        Writes bytes to the I2C bus.

        Args:
            data: data to write to the I2C bus

        Raises:
            VCPError: unable to write data
        """
        try:
            os.write(self.fd, data)
        except OSError as e:
            raise VCPError('unable write to I2C bus') from e


def get_vcps() -> List[LinuxVCP]:
    """
    Interrogates I2C buses to determine if they are DDC-CI capable.

    Returns:
        List of all VCPs detected.
    """
    vcps = []
    for device in pyudev.Context().list_devices(subsystem='i2c'):
        try:
            try:
                vcp = LinuxVCP(device.sys_number)
                vcp.open()
                vcps.append(vcp)
            except (OSError, VCPError):
                pass

        finally:
            vcp.close()

    return vcps