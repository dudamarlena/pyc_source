# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/PIL/FpxImagePlugin.py
# Compiled at: 2007-09-25 20:00:35
__version__ = '0.1'
import string, Image, ImageFile
from OleFileIO import *
MODES = {32766: ('A', 'L'), 
   (65536, ): ('L', 'L'), 
   (98304, 98302): ('RGBA', 'LA'), 
   (131072, 131073, 131074): ('RGB', 'YCC;P'), 
   (163840, 163841, 163842, 163838): ('RGBA', 'YCCA;P'), 
   (196608, 196609, 196610): ('RGB', 'RGB'), 
   (229376, 229377, 229378, 229374): ('RGBA', 'RGBA')}

def _accept(prefix):
    return prefix[:8] == MAGIC


class FpxImageFile(ImageFile.ImageFile):
    format = 'FPX'
    format_description = 'FlashPix'

    def _open(self):
        try:
            self.ole = OleFileIO(self.fp)
        except IOError:
            raise SyntaxError, 'not an FPX file; invalid OLE file'

        if self.ole.root.clsid != '56616700-C154-11CE-8553-00AA00A1F95B':
            raise SyntaxError, 'not an FPX file; bad root CLSID'
        self._open_index(1)

    def _open_index(self, index=1):
        prop = self.ole.getproperties([
         'Data Object Store %06d' % index,
         '\x05Image Contents'])
        self.size = (
         prop[16777218], prop[16777219])
        size = max(self.size)
        i = 1
        while size > 64:
            size = size / 2
            i = i + 1

        self.maxid = i - 1
        id = self.maxid << 16
        s = prop[(33554434 | id)]
        colors = []
        for i in range(i32(s, 4)):
            colors.append(i32(s, 8 + i * 4) & 2147483647)

        (self.mode, self.rawmode) = MODES[tuple(colors)]
        self.jpeg = {}
        for i in range(256):
            id = 50331649 | i << 16
            if prop.has_key(id):
                self.jpeg[i] = prop[id]

        self._open_subimage(1, self.maxid)

    def _open_subimage(self, index=1, subimage=0):
        stream = [
         'Data Object Store %06d' % index,
         'Resolution %04d' % subimage,
         'Subimage 0000 Header']
        fp = self.ole.openstream(stream)
        p = fp.read(28)
        s = fp.read(36)
        size = (
         i32(s, 4), i32(s, 8))
        tilecount = i32(s, 12)
        tilesize = (i32(s, 16), i32(s, 20))
        channels = i32(s, 24)
        offset = i32(s, 28)
        length = i32(s, 32)
        if size != self.size:
            raise IOError, 'subimage mismatch'
        fp.seek(28 + offset)
        s = fp.read(i32(s, 12) * length)
        x = y = 0
        (xsize, ysize) = size
        (xtile, ytile) = tilesize
        self.tile = []
        for i in range(0, len(s), length):
            compression = i32(s, i + 8)
            if compression == 0:
                self.tile.append(('raw', (x, y, x + xtile, y + ytile),
                 i32(s, i) + 28, self.rawmode))
            elif compression == 1:
                self.tile.append(('fill', (x, y, x + xtile, y + ytile),
                 i32(s, i) + 28, (self.rawmode, s[12:16])))
            elif compression == 2:
                internal_color_conversion = ord(s[14])
                jpeg_tables = ord(s[15])
                rawmode = self.rawmode
                if internal_color_conversion:
                    if rawmode == 'RGBA':
                        (jpegmode, rawmode) = ('YCbCrK', 'CMYK')
                    else:
                        jpegmode = None
                else:
                    jpegmode = rawmode
                self.tile.append(('jpeg', (x, y, x + xtile, y + ytile),
                 i32(s, i) + 28, (rawmode, jpegmode)))
                if jpeg_tables:
                    self.tile_prefix = self.jpeg[jpeg_tables]
            else:
                raise IOError, 'unknown/invalid compression'
            x = x + xtile
            if x >= xsize:
                x, y = 0, y + ytile
                if y >= ysize:
                    break

        self.stream = stream
        self.fp = None
        return

    def load(self):
        if not self.fp:
            self.fp = self.ole.openstream(self.stream[:2] + ['Subimage 0000 Data'])
        ImageFile.ImageFile.load(self)


Image.register_open('FPX', FpxImageFile, _accept)
Image.register_extension('FPX', '.fpx')