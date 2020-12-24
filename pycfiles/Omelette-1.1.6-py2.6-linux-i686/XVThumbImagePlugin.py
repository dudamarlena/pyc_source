# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/PIL/XVThumbImagePlugin.py
# Compiled at: 2007-09-25 20:00:35
__version__ = '0.1'
import string, Image, ImageFile, ImagePalette
PALETTE = ''
for r in range(8):
    for g in range(8):
        for b in range(4):
            PALETTE = PALETTE + (chr(r * 255 / 7) + chr(g * 255 / 7) + chr(b * 255 / 3))

class XVThumbImageFile(ImageFile.ImageFile):
    format = 'XVThumb'
    format_description = 'XV thumbnail image'

    def _open(self):
        s = self.fp.read(6)
        if s != 'P7 332':
            raise SyntaxError, 'not an XV thumbnail file'
        while 1:
            s = string.strip(self.fp.readline())
            if s == '#END_OF_COMMENTS':
                break

        s = string.split(self.fp.readline())
        self.mode = 'P'
        self.size = (int(s[0]), int(s[1]))
        self.palette = ImagePalette.raw('RGB', PALETTE)
        self.tile = [
         (
          'raw', (0, 0) + self.size,
          self.fp.tell(), (self.mode, 0, 1))]


Image.register_open('XVThumb', XVThumbImageFile)