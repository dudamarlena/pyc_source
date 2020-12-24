# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/PIL/DcxImagePlugin.py
# Compiled at: 2007-09-25 20:00:35
__version__ = '0.2'
import Image, ImageFile
from PcxImagePlugin import PcxImageFile
MAGIC = 987654321

def i32(c):
    return ord(c[0]) + (ord(c[1]) << 8) + (ord(c[2]) << 16) + (ord(c[3]) << 24)


def _accept(prefix):
    return i32(prefix) == MAGIC


class DcxImageFile(PcxImageFile):
    format = 'DCX'
    format_description = 'Intel DCX'

    def _open(self):
        s = self.fp.read(4)
        if i32(s) != MAGIC:
            raise SyntaxError, 'not a DCX file'
        self._offset = []
        for i in range(1024):
            offset = i32(self.fp.read(4))
            if not offset:
                break
            self._offset.append(offset)

        self.__fp = self.fp
        self.seek(0)

    def seek(self, frame):
        if frame >= len(self._offset):
            raise EOFError('attempt to seek outside DCX directory')
        self.frame = frame
        self.fp = self.__fp
        self.fp.seek(self._offset[frame])
        PcxImageFile._open(self)

    def tell(self):
        return self.frame


Image.register_open('DCX', DcxImageFile, _accept)
Image.register_extension('DCX', '.dcx')