# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/PIL/BmpImagePlugin.py
# Compiled at: 2007-09-25 20:00:35
__version__ = '0.7'
import string, Image, ImageFile, ImagePalette

def i16(c):
    return ord(c[0]) + (ord(c[1]) << 8)


def i32(c):
    return ord(c[0]) + (ord(c[1]) << 8) + (ord(c[2]) << 16) + (ord(c[3]) << 24)


BIT2MODE = {1: ('P', 'P;1'), 
   4: ('P', 'P;4'), 
   8: ('P', 'P'), 
   16: ('RGB', 'BGR;16'), 
   24: ('RGB', 'BGR'), 
   32: ('RGB', 'BGRX')}

def _accept(prefix):
    return prefix[:2] == 'BM'


class BmpImageFile(ImageFile.ImageFile):
    format = 'BMP'
    format_description = 'Windows Bitmap'

    def _bitmap(self, header=0, offset=0):
        if header:
            self.fp.seek(header)
        read = self.fp.read
        s = read(4)
        s = s + ImageFile._safe_read(self.fp, i32(s) - 4)
        if len(s) == 12:
            bits = i16(s[10:])
            self.size = (i16(s[4:]), i16(s[6:]))
            compression = 0
            lutsize = 3
            colors = 0
        elif len(s) in (40, 64):
            bits = i16(s[14:])
            self.size = (i32(s[4:]), i32(s[8:]))
            compression = i32(s[16:])
            lutsize = 4
            colors = i32(s[32:])
        else:
            raise IOError('Unsupported BMP header type (%d)' % len(s))
        if not colors:
            colors = 1 << bits
        try:
            (self.mode, rawmode) = BIT2MODE[bits]
        except KeyError:
            raise IOError('Unsupported BMP pixel depth (%d)' % bits)

        if compression == 3:
            mask = (i32(read(4)), i32(read(4)), i32(read(4)))
            if bits == 32 and mask == (16711680, 65280, 255):
                rawmode = 'BGRX'
            elif bits == 16 and mask == (63488, 2016, 31):
                rawmode = 'BGR;16'
            elif bits == 16 and mask == (31744, 992, 31):
                rawmode = 'BGR;15'
            else:
                raise IOError('Unsupported BMP bitfields layout')
        elif compression != 0:
            raise IOError('Unsupported BMP compression (%d)' % compression)
        if self.mode == 'P':
            palette = []
            greyscale = 1
            if colors == 2:
                indices = (0, 255)
            else:
                indices = range(colors)
            for i in indices:
                rgb = read(lutsize)[:3]
                if rgb != chr(i) * 3:
                    greyscale = 0
                palette.append(rgb)

            if greyscale:
                if colors == 2:
                    self.mode = rawmode = '1'
                else:
                    self.mode = rawmode = 'L'
            else:
                self.mode = 'P'
                self.palette = ImagePalette.raw('BGR', string.join(palette, ''))
        if not offset:
            offset = self.fp.tell()
        self.tile = [
         ('raw',
          (0, 0) + self.size,
          offset,
          (
           rawmode, self.size[0] * bits + 31 >> 3 & -4, -1))]
        self.info['compression'] = compression

    def _open(self):
        s = self.fp.read(14)
        if s[:2] != 'BM':
            raise SyntaxError('Not a BMP file')
        offset = i32(s[10:])
        self._bitmap(offset=offset)


class DibImageFile(BmpImageFile):
    format = 'DIB'
    format_description = 'Windows Bitmap'

    def _open(self):
        self._bitmap()


def o16(i):
    return chr(i & 255) + chr(i >> 8 & 255)


def o32(i):
    return chr(i & 255) + chr(i >> 8 & 255) + chr(i >> 16 & 255) + chr(i >> 24 & 255)


SAVE = {'1': ('1', 1, 2), 
   'L': ('L', 8, 256), 
   'P': ('P', 8, 256), 
   'RGB': ('BGR', 24, 0)}

def _save(im, fp, filename, check=0):
    try:
        (rawmode, bits, colors) = SAVE[im.mode]
    except KeyError:
        raise IOError('cannot write mode %s as BMP' % im.mode)

    if check:
        return check
    stride = (im.size[0] * bits + 7) / 8 + 3 & -4
    header = 40
    offset = 14 + header + colors * 4
    image = stride * im.size[1]
    fp.write('BM' + o32(offset + image) + o32(0) + o32(offset))
    fp.write(o32(header) + o32(im.size[0]) + o32(im.size[1]) + o16(1) + o16(bits) + o32(0) + o32(image) + o32(1) + o32(1) + o32(colors) + o32(colors))
    fp.write('\x00' * (header - 40))
    if im.mode == '1':
        for i in (0, 255):
            fp.write(chr(i) * 4)

    else:
        if im.mode == 'L':
            for i in range(256):
                fp.write(chr(i) * 4)

        elif im.mode == 'P':
            fp.write(im.im.getpalette('RGB', 'BGRX'))
        ImageFile._save(im, fp, [('raw', (0, 0) + im.size, 0, (rawmode, stride, -1))])


Image.register_open(BmpImageFile.format, BmpImageFile, _accept)
Image.register_save(BmpImageFile.format, _save)
Image.register_extension(BmpImageFile.format, '.bmp')