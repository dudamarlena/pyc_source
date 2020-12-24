# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fpga_i2c_bridge/util/crc.py
# Compiled at: 2019-10-20 11:03:39
# Size of source mod 2**32: 890 bytes
"""Utility functions for calculating CRC16."""
GENERATOR = 12053
LOOKUP = [
 0] * 256

def __generate_lookup() -> None:
    """Generates the lookup table that is used in CRC calculation."""
    crc = 32768
    i = 1
    while i < 256:
        if crc & 32768:
            crc = crc << 1 ^ GENERATOR
        else:
            crc = crc << 1
        for j in range(i):
            LOOKUP[i + j] = (crc ^ LOOKUP[j]) & 65535
        else:
            i <<= 1


__generate_lookup()

def crc16(data: bytes) -> int:
    """
    Calculates and returns the CRC16 value of the supplied byte string.
    :param data: Bytestring to digest
    :return: CRC16 value of bytes
    """
    crc = 0
    for b in data:
        crc = (crc << 8 ^ LOOKUP[(b ^ crc >> 8)]) & 65535
    else:
        return crc