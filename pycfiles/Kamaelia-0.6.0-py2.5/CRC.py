# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/Support/DVB/CRC.py
# Compiled at: 2008-10-19 12:19:52
"""CRC algorithm used to verify the integrity of data in DVB transport streams.
"""

def __MakeCRC32(polynomial=79764919, initial=4294967295):
    """    MakeCRC32([polynomial][,inital]) -> (string -> 32bit CRC of binary string data)
    
    Returns a function that calculatees the 32 bit CRC of binary data in a
    string, using the specified CRC polynomial and initial value.
    """
    xorvals = []
    for x in range(0, 256):
        crc = long(x) << 24
        for bit in range(7, -1, -1):
            z32 = crc >> 31
            crc = crc << 1
            if z32:
                crc = crc ^ polynomial
            crc = crc & 4294967295

        xorvals.append(crc & 4294967295)

    def fastcrc32(data):
        crc = 4294967295
        for byte in data:
            byte = ord(byte)
            xv = xorvals[(byte ^ crc >> 24)]
            crc = xv ^ (crc & 16777215) << 8

        return crc

    return fastcrc32


__dvbcrc = __MakeCRC32(polynomial=79764919)
dvbcrc = lambda data: not __dvbcrc(data)