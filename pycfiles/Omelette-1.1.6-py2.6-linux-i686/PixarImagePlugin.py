# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/PIL/PixarImagePlugin.py
# Compiled at: 2007-09-25 20:00:35
__version__ = '0.1'
import Image, ImageFile

def i16(c):
    return ord(c[0]) + (ord(c[1]) << 8)


def i32(c):
    return ord(c[0]) + (ord(c[1]) << 8) + (ord(c[2]) << 16) + (ord(c[3]) << 24)


class PixarImageFile(ImageFile.ImageFile):
    format = 'PIXAR'
    format_description = 'PIXAR raster image'

    def _open(self):
        s = self.fp.read(4)
        if s != b'\x80\xe8\x00\x00':
            raise SyntaxError, 'not a PIXAR file'
        s = s + self.fp.read(508)
        self.size = (
         i16(s[418:420]), i16(s[416:418]))
        mode = (
         i16(s[424:426]), i16(s[426:428]))
        if mode == (14, 2):
            self.mode = 'RGB'
        self.tile = [
         (
          'raw', (0, 0) + self.size, 1024, (self.mode, 0, 1))]


Image.register_open('PIXAR', PixarImageFile)