# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/PIL/TgaImagePlugin.py
# Compiled at: 2007-09-25 20:00:35
__version__ = '0.3'
import Image, ImageFile, ImagePalette

def i16(c):
    return ord(c[0]) + (ord(c[1]) << 8)


def i32(c):
    return ord(c[0]) + (ord(c[1]) << 8) + (ord(c[2]) << 16) + (ord(c[3]) << 24)


MODES = {(1, 8): 'P', 
   (3, 1): '1', 
   (3, 8): 'L', 
   (2, 16): 'BGR;5', 
   (2, 24): 'BGR', 
   (2, 32): 'BGRA'}

def _accept(prefix):
    return prefix[0] == '\x00'


class TgaImageFile(ImageFile.ImageFile):
    format = 'TGA'
    format_description = 'Targa'

    def _open(self):
        s = self.fp.read(18)
        id = ord(s[0])
        colormaptype = ord(s[1])
        imagetype = ord(s[2])
        depth = ord(s[16])
        flags = ord(s[17])
        self.size = (
         i16(s[12:]), i16(s[14:]))
        if id != 0 or colormaptype not in (0, 1) or self.size[0] <= 0 or self.size[1] <= 0 or depth not in (8,
                                                                                                            16,
                                                                                                            24,
                                                                                                            32):
            raise SyntaxError, 'not a TGA file'
        if imagetype in (3, 11):
            self.mode = 'L'
            if depth == 1:
                self.mode = '1'
        elif imagetype in (1, 9):
            self.mode = 'P'
        elif imagetype in (2, 10):
            self.mode = 'RGB'
            if depth == 32:
                self.mode = 'RGBA'
        else:
            raise SyntaxError, 'unknown TGA mode'
        orientation = flags & 48
        if orientation == 32:
            orientation = 1
        elif not orientation:
            orientation = -1
        else:
            raise SyntaxError, 'unknown TGA orientation'
        if imagetype & 8:
            self.info['compression'] = 'tga_rle'
        if colormaptype:
            start, size, mapdepth = i16(s[3:]), i16(s[5:]), i16(s[7:])
            if mapdepth == 16:
                self.palette = ImagePalette.raw('BGR;16', '\x00\x00' * start + self.fp.read(2 * size))
            elif mapdepth == 24:
                self.palette = ImagePalette.raw('BGR', '\x00\x00\x00' * start + self.fp.read(3 * size))
            elif mapdepth == 32:
                self.palette = ImagePalette.raw('BGRA', '\x00\x00\x00\x00' * start + self.fp.read(4 * size))
        try:
            rawmode = MODES[(imagetype & 7, depth)]
            if imagetype & 8:
                self.tile = [
                 ('tga_rle', (0, 0) + self.size,
                  self.fp.tell(), (rawmode, orientation, depth))]
            else:
                self.tile = [
                 (
                  'raw', (0, 0) + self.size,
                  self.fp.tell(), (rawmode, 0, orientation))]
        except KeyError:
            pass


Image.register_open('TGA', TgaImageFile, _accept)
Image.register_extension('TGA', '.tga')