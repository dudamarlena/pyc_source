# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/PIL/SunImagePlugin.py
# Compiled at: 2007-09-25 20:00:35
__version__ = '0.3'
import string, Image, ImageFile, ImagePalette

def i16(c):
    return ord(c[1]) + (ord(c[0]) << 8)


def i32(c):
    return ord(c[3]) + (ord(c[2]) << 8) + (ord(c[1]) << 16) + (ord(c[0]) << 24)


def _accept(prefix):
    return i32(prefix) == 1504078485


class SunImageFile(ImageFile.ImageFile):
    format = 'SUN'
    format_description = 'Sun Raster File'

    def _open(self):
        s = self.fp.read(32)
        if i32(s) != 1504078485:
            raise SyntaxError, 'not an SUN raster file'
        offset = 32
        self.size = (
         i32(s[4:8]), i32(s[8:12]))
        depth = i32(s[12:16])
        if depth == 1:
            (self.mode, rawmode) = ('1', '1;I')
        elif depth == 8:
            self.mode = rawmode = 'L'
        elif depth == 24:
            (self.mode, rawmode) = ('RGB', 'BGR')
        else:
            raise SyntaxError, 'unsupported mode'
        compression = i32(s[20:24])
        if i32(s[24:28]) != 0:
            length = i32(s[28:32])
            offset = offset + length
            self.palette = ImagePalette.raw('RGB;L', self.fp.read(length))
            if self.mode == 'L':
                self.mode = rawmode = 'P'
        stride = (self.size[0] * depth + 7) / 8 + 3 & -4
        if compression == 1:
            self.tile = [
             (
              'raw', (0, 0) + self.size, offset, (rawmode, stride))]
        elif compression == 2:
            self.tile = [
             (
              'sun_rle', (0, 0) + self.size, offset, rawmode)]


Image.register_open('SUN', SunImageFile, _accept)
Image.register_extension('SUN', '.ras')