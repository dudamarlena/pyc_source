# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/gopro2gpx/klvdata.py
# Compiled at: 2020-04-24 06:21:51
# Size of source mod 2**32: 2160 bytes
import struct
from gopro2gpx.fourCC import Manage, skip_labels

class KLVData:
    __doc__ = '\n    format: Header: 32-bit, 8-bit, 8-bit, 16-bit\n            Data: 32-bit aligned, padded with 0\n    '
    binary_format = '>4sBBH'

    def __init__(self, data, offset):
        s = struct.Struct(KLVData.binary_format)
        self.fourCC, self.type, self.size, self.repeat = s.unpack_from(data, offset=offset)
        self.fourCC = self.fourCC.decode()
        self.type = int(self.type)
        self.length = self.size * self.repeat
        self.padded_length = self.pad(self.length)
        self.rawdata = self.readRawData(data, offset)
        self.data = Manage(self)

    def __str__(self):
        stype = chr(self.type)
        if self.type == 0:
            stype = 'null'
        elif self.rawdata:
            rawdata = self.rawdata
            rawdata = ' '.join((format(x, '02x') for x in rawdata))
            rawdatas = self.rawdata[0:10]
        else:
            rawdata = 'null'
            rawdatas = 'null'
        s = '%s %s %d %s {%s} |%s| [%s]' % (self.fourCC, stype, self.size, self.repeat, self.data, rawdatas, rawdata)
        return s

    def pad(self, n, base=4):
        """padd the number so is % base == 0"""
        i = n
        while i % base != 0:
            i += 1

        return i

    def skip(self):
        return self.fourCC in skip_labels

    def readRawData(self, data, offset):
        """read the raw data, don't process anything, just get the bytes"""
        if self.type == 0:
            return
        else:
            num_bytes = self.pad(self.size * self.repeat)
            if num_bytes == 0:
                rawdata = None
            else:
                fmt = '>' + str(num_bytes) + 's'
            s = struct.Struct(fmt)
            rawdata, = s.unpack_from(data, offset=(offset + 8))
        return rawdata