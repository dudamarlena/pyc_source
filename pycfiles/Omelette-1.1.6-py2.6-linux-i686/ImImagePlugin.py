# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/PIL/ImImagePlugin.py
# Compiled at: 2007-09-25 20:00:35
__version__ = '0.7'
import re, string, Image, ImageFile, ImagePalette
COMMENT = 'Comment'
DATE = 'Date'
EQUIPMENT = 'Digitalization equipment'
FRAMES = 'File size (no of images)'
LUT = 'Lut'
NAME = 'Name'
SCALE = 'Scale (x,y)'
SIZE = 'Image size (x*y)'
MODE = 'Image type'
TAGS = {COMMENT: 0, DATE: 0, EQUIPMENT: 0, FRAMES: 0, LUT: 0, NAME: 0, SCALE: 0, 
   SIZE: 0, MODE: 0}
OPEN = {'0 1 image': ('1', '1'), 
   'L 1 image': ('1', '1'), 
   'Greyscale image': ('L', 'L'), 
   'Grayscale image': ('L', 'L'), 
   'RGB image': ('RGB', 'RGB;L'), 
   'RLB image': ('RGB', 'RLB'), 
   'RYB image': ('RGB', 'RLB'), 
   'B1 image': ('1', '1'), 
   'B2 image': ('P', 'P;2'), 
   'B4 image': ('P', 'P;4'), 
   'X 24 image': ('RGB', 'RGB'), 
   'L 32 S image': ('I', 'I;32'), 
   'L 32 F image': ('F', 'F;32'), 
   'RGB3 image': ('RGB', 'RGB;T'), 
   'RYB3 image': ('RGB', 'RYB;T'), 
   'LA image': ('LA', 'LA;L'), 
   'RGBA image': ('RGBA', 'RGBA;L'), 
   'RGBX image': ('RGBX', 'RGBX;L'), 
   'CMYK image': ('CMYK', 'CMYK;L'), 
   'YCC image': ('YCbCr', 'YCbCr;L')}
for i in ['8', '8S', '16', '16S', '32', '32F']:
    OPEN['L %s image' % i] = (
     'F', 'F;%s' % i)
    OPEN['L*%s image' % i] = ('F', 'F;%s' % i)

for i in ['16', '16B']:
    OPEN['L %s image' % i] = (
     'I;%s' % i, 'I;%s' % i)
    OPEN['L*%s image' % i] = ('I;%s' % i, 'I;%s' % i)

for i in ['32S']:
    OPEN['L %s image' % i] = (
     'I', 'I;%s' % i)
    OPEN['L*%s image' % i] = ('I', 'I;%s' % i)

for i in range(2, 33):
    OPEN['L*%s image' % i] = (
     'F', 'F;%s' % i)

split = re.compile('^([A-Za-z][^:]*):[ \\t]*(.*)[ \\t]*$')

def number(s):
    try:
        return int(s)
    except ValueError:
        return float(s)


class ImImageFile(ImageFile.ImageFile):
    format = 'IM'
    format_description = 'IFUNC Image Memory'

    def _open(self):
        if '\n' not in self.fp.read(100):
            raise SyntaxError, 'not an IM file'
        self.fp.seek(0)
        n = 0
        self.info[MODE] = 'L'
        self.info[SIZE] = (512, 512)
        self.info[FRAMES] = 1
        self.rawmode = 'L'
        while 1:
            s = self.fp.read(1)
            if s == '\r':
                continue
            if not s or s[0] == chr(0) or s[0] == chr(26):
                break
            s = s + self.fp.readline()
            if len(s) > 100:
                raise SyntaxError, 'not an IM file'
            if s[-2:] == '\r\n':
                s = s[:-2]
            elif s[-1:] == '\n':
                s = s[:-1]
            try:
                m = split.match(s)
            except re.error, v:
                raise SyntaxError, 'not an IM file'

            if m:
                (k, v) = m.group(1, 2)
                if k in [FRAMES, SCALE, SIZE]:
                    v = string.replace(v, '*', ',')
                    v = tuple(map(number, string.split(v, ',')))
                    if len(v) == 1:
                        v = v[0]
                elif k == MODE and OPEN.has_key(v):
                    (v, self.rawmode) = OPEN[v]
                if k == COMMENT:
                    if self.info.has_key(k):
                        self.info[k].append(v)
                    else:
                        self.info[k] = [
                         v]
                else:
                    self.info[k] = v
                if TAGS.has_key(k):
                    n = n + 1
            else:
                raise SyntaxError, 'Syntax error in IM header: ' + s

        if not n:
            raise SyntaxError, 'Not an IM file'
        self.size = self.info[SIZE]
        self.mode = self.info[MODE]
        while s and s[0] != chr(26):
            s = self.fp.read(1)

        if not s:
            raise SyntaxError, 'File truncated'
        if self.info.has_key(LUT):
            palette = self.fp.read(768)
            greyscale = 1
            linear = 1
            for i in range(256):
                if palette[i] == palette[(i + 256)] == palette[(i + 512)]:
                    if palette[i] != chr(i):
                        linear = 0
                else:
                    greyscale = 0

            if self.mode == 'L' or self.mode == 'LA':
                if greyscale:
                    if not linear:
                        self.lut = map(ord, palette[:256])
                else:
                    if self.mode == 'L':
                        self.mode = self.rawmode = 'P'
                    elif self.mode == 'LA':
                        self.mode = self.rawmode = 'PA'
                    self.palette = ImagePalette.raw('RGB;L', palette)
            elif self.mode == 'RGB':
                if not greyscale or not linear:
                    self.lut = map(ord, palette)
        self.frame = 0
        self.__offset = offs = self.fp.tell()
        self.__fp = self.fp
        if self.rawmode[:2] == 'F;':
            try:
                bits = int(self.rawmode[2:])
                if bits not in (8, 16, 32):
                    self.tile = [(
                      'bit', (0, 0) + self.size, offs,
                      (
                       bits, 8, 3, 0, -1))]
                    return
            except ValueError:
                pass

        if self.rawmode in ('RGB;T', 'RYB;T'):
            size = self.size[0] * self.size[1]
            self.tile = [('raw', (0, 0) + self.size, offs, ('G', 0, -1)),
             (
              'raw', (0, 0) + self.size, offs + size, ('R', 0, -1)),
             (
              'raw', (0, 0) + self.size, offs + 2 * size, ('B', 0, -1))]
        else:
            self.tile = [
             (
              'raw', (0, 0) + self.size, offs, (self.rawmode, 0, -1))]

    def seek(self, frame):
        if frame < 0 or frame >= self.info[FRAMES]:
            raise EOFError, 'seek outside sequence'
        if self.frame == frame:
            return
        self.frame = frame
        if self.mode == '1':
            bits = 1
        else:
            bits = 8 * len(self.mode)
        size = (self.size[0] * bits + 7) / 8 * self.size[1]
        offs = self.__offset + frame * size
        self.fp = self.__fp
        self.tile = [
         (
          'raw', (0, 0) + self.size, offs, (self.rawmode, 0, -1))]

    def tell(self):
        return self.frame


SAVE = {'1': ('0 1', '1'), 
   'L': ('Greyscale', 'L'), 
   'LA': ('LA', 'LA;L'), 
   'P': ('Greyscale', 'P'), 
   'PA': ('LA', 'PA;L'), 
   'I': ('L 32S', 'I;32S'), 
   'I;16': ('L 16', 'I;16'), 
   'I;16B': ('L 16B', 'I;16B'), 
   'F': ('L 32F', 'F;32F'), 
   'RGB': ('RGB', 'RGB;L'), 
   'RGBA': ('RGBA', 'RGBA;L'), 
   'RGBX': ('RGBX', 'RGBX;L'), 
   'CMYK': ('CMYK', 'CMYK;L'), 
   'YCbCr': ('YCC', 'YCbCr;L')}

def _save(im, fp, filename, check=0):
    try:
        (type, rawmode) = SAVE[im.mode]
    except KeyError:
        raise ValueError, 'Cannot save %s images as IM' % im.mode

    try:
        frames = im.encoderinfo['frames']
    except KeyError:
        frames = 1

    if check:
        return check
    fp.write('Image type: %s image\r\n' % type)
    if filename:
        fp.write('Name: %s\r\n' % filename)
    fp.write('Image size (x*y): %d*%d\r\n' % im.size)
    fp.write('File size (no of images): %d\r\n' % frames)
    if im.mode == 'P':
        fp.write('Lut: 1\r\n')
    fp.write('\x00' * (511 - fp.tell()) + '\x1a')
    if im.mode == 'P':
        fp.write(im.im.getpalette('RGB', 'RGB;L'))
    ImageFile._save(im, fp, [('raw', (0, 0) + im.size, 0, (rawmode, 0, -1))])


Image.register_open('IM', ImImageFile)
Image.register_save('IM', _save)
Image.register_extension('IM', '.im')