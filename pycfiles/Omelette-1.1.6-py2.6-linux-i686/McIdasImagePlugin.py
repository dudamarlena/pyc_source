# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/PIL/McIdasImagePlugin.py
# Compiled at: 2007-09-25 20:00:35
__version__ = '0.1'
import string, Image, ImageFile

def i16(c, i=0):
    return ord(c[(1 + i)]) + (ord(c[i]) << 8)


def i32(c, i=0):
    return ord(c[(3 + i)]) + (ord(c[(2 + i)]) << 8) + (ord(c[(1 + i)]) << 16) + (ord(c[i]) << 24)


def _accept(s):
    return i32(s) == 0 and i32(s, 4) == 4


class McIdasImageFile(ImageFile.ImageFile):
    format = 'MCIDAS'
    format_description = 'McIdas area file'

    def _open(self):
        s = self.fp.read(256)
        if not _accept(s):
            raise SyntaxError, 'not an McIdas area file'
        if i32(s, 40) != 1 or i32(s, 52) != 1:
            raise SyntaxError, 'unsupported McIdas format'
        self.mode = 'L'
        self.size = (
         i32(s, 36), i32(s, 32))
        prefix = i32(s, 56)
        offset = i32(s, 132)
        self.tile = [
         (
          'raw', (0, 0) + self.size, offset,
          (
           'L', prefix + self.size[0], 1))]


Image.register_open('MCIDAS', McIdasImageFile, _accept)