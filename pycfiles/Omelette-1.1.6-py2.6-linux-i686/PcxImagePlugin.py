# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/PIL/PcxImagePlugin.py
# Compiled at: 2007-09-25 20:00:35
__version__ = '0.6'
import Image, ImageFile, ImagePalette

def i16(c, o):
    return ord(c[o]) + (ord(c[(o + 1)]) << 8)


def _accept(prefix):
    return ord(prefix[0]) == 10 and ord(prefix[1]) in (0, 2, 3, 5)


class PcxImageFile(ImageFile.ImageFile):
    format = 'PCX'
    format_description = 'Paintbrush'

    def _open(self):
        s = self.fp.read(128)
        if not _accept(s):
            raise SyntaxError, 'not a PCX file'
        bbox = (
         i16(s, 4), i16(s, 6), i16(s, 8) + 1, i16(s, 10) + 1)
        if bbox[2] <= bbox[0] or bbox[3] <= bbox[1]:
            raise SyntaxError, 'bad PCX image size'
        version = ord(s[1])
        bits = ord(s[3])
        planes = ord(s[65])
        stride = i16(s, 66)
        self.info['dpi'] = (
         i16(s, 12), i16(s, 14))
        if bits == 1 and planes == 1:
            mode = rawmode = '1'
        elif bits == 1 and planes in (2, 4):
            mode = 'P'
            rawmode = 'P;%dL' % planes
            self.palette = ImagePalette.raw('RGB', s[16:64])
        elif version == 5 and bits == 8 and planes == 1:
            mode = rawmode = 'L'
            self.fp.seek(-769, 2)
            s = self.fp.read(769)
            if len(s) == 769 and ord(s[0]) == 12:
                for i in range(256):
                    if s[i * 3 + 1:i * 3 + 4] != chr(i) * 3:
                        mode = rawmode = 'P'
                        break

                if mode == 'P':
                    self.palette = ImagePalette.raw('RGB', s[1:])
            self.fp.seek(128)
        elif version == 5 and bits == 8 and planes == 3:
            mode = 'RGB'
            rawmode = 'RGB;L'
        else:
            raise IOError, 'unknown PCX mode'
        self.mode = mode
        self.size = (bbox[2] - bbox[0], bbox[3] - bbox[1])
        bbox = (0, 0) + self.size
        self.tile = [
         (
          'pcx', bbox, self.fp.tell(), (rawmode, planes * stride))]


SAVE = {'1': (2, 1, 1, '1'), 
   'L': (5, 8, 1, 'L'), 
   'P': (5, 8, 1, 'P'), 
   'RGB': (5, 8, 3, 'RGB;L')}

def o16(i):
    return chr(i & 255) + chr(i >> 8 & 255)


def _save(im, fp, filename, check=0):
    try:
        (version, bits, planes, rawmode) = SAVE[im.mode]
    except KeyError:
        raise ValueError, 'Cannot save %s images as PCX' % im.mode

    if check:
        return check
    stride = (im.size[0] * bits + 7) / 8
    screen = im.size
    dpi = (100, 100)
    fp.write(chr(10) + chr(version) + chr(1) + chr(bits) + o16(0) + o16(0) + o16(im.size[0] - 1) + o16(im.size[1] - 1) + o16(dpi[0]) + o16(dpi[1]) + chr(0) * 24 + chr(255) * 24 + chr(0) + chr(planes) + o16(stride) + o16(1) + o16(screen[0]) + o16(screen[1]) + chr(0) * 54)
    assert fp.tell() == 128
    ImageFile._save(im, fp, [
     ('pcx', (0, 0) + im.size, 0,
      (
       rawmode, bits * planes))])
    if im.mode == 'P':
        fp.write(chr(12))
        fp.write(im.im.getpalette('RGB', 'RGB'))
    elif im.mode == 'L':
        fp.write(chr(12))
        for i in range(256):
            fp.write(chr(i) * 3)


Image.register_open('PCX', PcxImageFile, _accept)
Image.register_save('PCX', _save)
Image.register_extension('PCX', '.pcx')