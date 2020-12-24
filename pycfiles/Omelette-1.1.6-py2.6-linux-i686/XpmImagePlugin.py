# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/PIL/XpmImagePlugin.py
# Compiled at: 2007-09-25 20:00:35
__version__ = '0.2'
import re, string, Image, ImageFile, ImagePalette
xpm_head = re.compile('"([0-9]*) ([0-9]*) ([0-9]*) ([0-9]*)')

def _accept(prefix):
    return prefix[:9] == '/* XPM */'


class XpmImageFile(ImageFile.ImageFile):
    format = 'XPM'
    format_description = 'X11 Pixel Map'

    def _open(self):
        if not _accept(self.fp.read(9)):
            raise SyntaxError, 'not an XPM file'
        while 1:
            s = self.fp.readline()
            if not s:
                raise SyntaxError, 'broken XPM file'
            m = xpm_head.match(s)
            if m:
                break

        self.size = (
         int(m.group(1)), int(m.group(2)))
        pal = int(m.group(3))
        bpp = int(m.group(4))
        if pal > 256 or bpp != 1:
            raise ValueError, 'cannot read this XPM file'
        palette = [
         '\x00\x00\x00'] * 256
        for i in range(pal):
            s = self.fp.readline()
            if s[-2:] == '\r\n':
                s = s[:-2]
            elif s[-1:] in '\r\n':
                s = s[:-1]
            c = ord(s[1])
            s = string.split(s[2:-2])
            for i in range(0, len(s), 2):
                if s[i] == 'c':
                    rgb = s[(i + 1)]
                    if rgb == 'None':
                        self.info['transparency'] = c
                    elif rgb[0] == '#':
                        rgb = string.atoi(rgb[1:], 16)
                        palette[c] = chr(rgb >> 16 & 255) + chr(rgb >> 8 & 255) + chr(rgb & 255)
                    else:
                        raise ValueError, 'cannot read this XPM file'
                    break
            else:
                raise ValueError, 'cannot read this XPM file'

        self.mode = 'P'
        self.palette = ImagePalette.raw('RGB', string.join(palette, ''))
        self.tile = [
         (
          'raw', (0, 0) + self.size, self.fp.tell(), ('P', 0, 1))]

    def load_read(self, bytes):
        (xsize, ysize) = self.size
        s = [
         None] * ysize
        for i in range(ysize):
            s[i] = string.ljust(self.fp.readline()[1:xsize + 1], xsize)

        self.fp = None
        return string.join(s, '')


Image.register_open('XPM', XpmImageFile, _accept)
Image.register_extension('XPM', '.xpm')
Image.register_mime('XPM', 'image/xpm')