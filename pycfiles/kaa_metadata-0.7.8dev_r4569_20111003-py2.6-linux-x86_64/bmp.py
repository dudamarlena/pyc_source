# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/kaa/metadata/image/bmp.py
# Compiled at: 2009-05-14 14:51:42
__all__ = [
 'Parser']
import struct, logging, core
log = logging.getLogger('metadata')

class BMP(core.Image):

    def __init__(self, file):
        core.Image.__init__(self)
        self.mime = 'image/bmp'
        self.type = 'windows bitmap image'
        try:
            (bfType, bfSize, bfZero, bfOffset, biSize, self.width, self.height) = struct.unpack('<2sIIIIII', file.read(26))
        except struct.error:
            raise core.ParseError()

        file.seek(0, 2)
        if bfType != 'BM' or bfSize != file.tell():
            raise core.ParseError()


Parser = BMP