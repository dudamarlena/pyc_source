# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/PIL/SgiImagePlugin.py
# Compiled at: 2007-09-25 20:00:35
__version__ = '0.1'
import string, Image, ImageFile

def i16(c):
    return ord(c[1]) + (ord(c[0]) << 8)


def i32(c):
    return ord(c[3]) + (ord(c[2]) << 8) + (ord(c[1]) << 16) + (ord(c[0]) << 24)


def _accept(prefix):
    return i16(prefix) == 474


class SgiImageFile(ImageFile.ImageFile):
    format = 'SGI'
    format_description = 'SGI Image File Format'

    def _open(self):
        s = self.fp.read(512)
        if i16(s) != 474:
            raise SyntaxError, 'not an SGI image file'
        compression = ord(s[2])
        layout = (
         ord(s[3]), i16(s[4:]), i16(s[10:]))
        if layout == (1, 2, 1):
            self.mode = 'L'
        elif layout == (1, 3, 3):
            self.mode = 'RGB'
        else:
            raise SyntaxError, 'unsupported SGI image mode'
        self.size = (
         i16(s[6:]), i16(s[8:]))
        if compression == 0:
            if self.mode == 'RGB':
                size = self.size[0] * self.size[1]
                self.tile = [('raw', (0, 0) + self.size, 512, ('R', 0, 1)),
                 (
                  'raw', (0, 0) + self.size, 512 + size, ('G', 0, 1)),
                 (
                  'raw', (0, 0) + self.size, 512 + 2 * size, ('B', 0, 1))]
            else:
                self.tile = [
                 (
                  'raw', (0, 0) + self.size, 512, (self.mode, 0, 1))]
        if compression == 1:
            self.tile = [
             (
              'sgi_rle', (0, 0) + self.size, 512, (self.mode, 0, 1))]


Image.register_open('SGI', SgiImageFile, _accept)
Image.register_extension('SGI', '.bw')
Image.register_extension('SGI', '.rgb')
Image.register_extension('SGI', '.rgba')
Image.register_extension('SGI', '.sgi')