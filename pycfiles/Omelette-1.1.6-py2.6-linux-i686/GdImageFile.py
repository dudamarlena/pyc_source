# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/PIL/GdImageFile.py
# Compiled at: 2007-09-25 20:00:35
__version__ = '0.1'
import string, Image, ImageFile, ImagePalette

def i16(c):
    return ord(c[1]) + (ord(c[0]) << 8)


class GdImageFile(ImageFile.ImageFile):
    format = 'GD'
    format_description = 'GD uncompressed images'

    def _open(self):
        s = self.fp.read(775)
        self.mode = 'L'
        self.size = (i16(s[0:2]), i16(s[2:4]))
        tindex = i16(s[5:7])
        if tindex < 256:
            self.info['transparent'] = tindex
        self.palette = ImagePalette.raw('RGB', s[7:])
        self.tile = [
         (
          'raw', (0, 0) + self.size, 775, ('L', 0, -1))]


def open(fp, mode='r'):
    if mode != 'r':
        raise ValueError('bad mode')
    if type(fp) == type(''):
        import __builtin__
        filename = fp
        fp = __builtin__.open(fp, 'rb')
    else:
        filename = ''
    try:
        return GdImageFile(fp, filename)
    except SyntaxError:
        raise IOError('cannot identify this image file')