# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/PIL/FliImagePlugin.py
# Compiled at: 2007-09-25 20:00:35
__version__ = '0.2'
import Image, ImageFile, ImagePalette, string

def i16(c):
    return ord(c[0]) + (ord(c[1]) << 8)


def i32(c):
    return ord(c[0]) + (ord(c[1]) << 8) + (ord(c[2]) << 16) + (ord(c[3]) << 24)


def _accept(prefix):
    return i16(prefix[4:6]) in (44817, 44818)


class FliImageFile(ImageFile.ImageFile):
    format = 'FLI'
    format_description = 'Autodesk FLI/FLC Animation'

    def _open(self):
        s = self.fp.read(128)
        magic = i16(s[4:6])
        if magic not in (44817, 44818):
            raise SyntaxError, 'not an FLI/FLC file'
        self.mode = 'P'
        self.size = (i16(s[8:10]), i16(s[10:12]))
        duration = i32(s[16:20])
        if magic == 44817:
            duration = duration * 1000 / 70
        self.info['duration'] = duration
        palette = map(lambda a: (a, a, a), range(256))
        s = self.fp.read(16)
        self.__offset = 128
        if i16(s[4:6]) == 61696:
            self.__offset = self.__offset + i32(s)
            s = self.fp.read(16)
        if i16(s[4:6]) == 61946:
            s = self.fp.read(6)
            if i16(s[4:6]) == 11:
                self._palette(palette, 2)
            elif i16(s[4:6]) == 4:
                self._palette(palette, 0)
        palette = map(lambda (r, g, b): chr(r) + chr(g) + chr(b), palette)
        self.palette = ImagePalette.raw('RGB', string.join(palette, ''))
        self.frame = -1
        self.__fp = self.fp
        self.seek(0)

    def _palette(self, palette, shift):
        i = 0
        for e in range(i16(self.fp.read(2))):
            s = self.fp.read(2)
            i = i + ord(s[0])
            n = ord(s[1])
            if n == 0:
                n = 256
            s = self.fp.read(n * 3)
            for n in range(0, len(s), 3):
                r = ord(s[n]) << shift
                g = ord(s[(n + 1)]) << shift
                b = ord(s[(n + 2)]) << shift
                palette[i] = (r, g, b)
                i = i + 1

    def seek(self, frame):
        if frame != self.frame + 1:
            raise ValueError, 'cannot seek to frame %d' % frame
        self.frame = frame
        self.fp = self.__fp
        self.fp.seek(self.__offset)
        s = self.fp.read(4)
        if not s:
            raise EOFError
        framesize = i32(s)
        self.decodermaxblock = framesize
        self.tile = [('fli', (0, 0) + self.size, self.__offset, None)]
        self.__offset = self.__offset + framesize
        return

    def tell(self):
        return self.frame


Image.register_open('FLI', FliImageFile, _accept)
Image.register_extension('FLI', '.fli')
Image.register_extension('FLI', '.flc')