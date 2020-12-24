# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/kaa/metadata/image/tiff.py
# Compiled at: 2008-10-26 20:23:09
__all__ = [
 'Parser']
import struct, logging, core, IPTC
log = logging.getLogger('metadata')
MOTOROLASIGNATURE = 'MM\x00*'
INTELSIGNATURE = 'II*\x00'

class TIFF(core.Image):
    table_mapping = {'IPTC': IPTC.mapping}

    def __init__(self, file):
        core.Image.__init__(self)
        self.iptc = None
        self.mime = 'image/tiff'
        self.type = 'TIFF image'
        self.intel = 0
        iptc = {}
        header = file.read(8)
        if header[:4] == MOTOROLASIGNATURE:
            self.intel = 0
            (offset,) = struct.unpack('>I', header[4:8])
            file.seek(offset)
            (len,) = struct.unpack('>H', file.read(2))
            app = file.read(len * 12)
            for i in range(len):
                (tag, type, length, value, offset) = struct.unpack('>HHIHH', app[i * 12:i * 12 + 12])
                if tag == 34377:
                    file.seek(offset, 0)
                    iptc = IPTC.parseiptc(file.read(1000))
                elif tag == 256:
                    if value != 0:
                        self.width = value
                    else:
                        self.width = offset
                elif tag == 257:
                    if value != 0:
                        self.height = value
                    else:
                        self.height = offset

        elif header[:4] == INTELSIGNATURE:
            self.intel = 1
            (offset,) = struct.unpack('<I', header[4:8])
            file.seek(offset, 0)
            (len,) = struct.unpack('<H', file.read(2))
            app = file.read(len * 12)
            for i in range(len):
                (tag, type, length, offset, value) = struct.unpack('<HHIHH', app[i * 12:i * 12 + 12])
                if tag == 34377:
                    file.seek(offset)
                    iptc = IPTC.parseiptc(file.read(1000))
                elif tag == 256:
                    if value != 0:
                        self.width = value
                    else:
                        self.width = offset
                elif tag == 257:
                    if value != 0:
                        self.height = value
                    else:
                        self.height = offset

        else:
            raise core.ParseError()
        if iptc:
            self._appendtable('IPTC', iptc)
        return


Parser = TIFF