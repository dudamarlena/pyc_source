# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/PIL/PsdImagePlugin.py
# Compiled at: 2007-09-25 20:00:35
__version__ = '0.4'
import string, Image, ImageFile, ImagePalette
MODES = {(0, 1): ('1', 1), 
   (0, 8): ('L', 1), 
   (1, 8): ('L', 1), 
   (2, 8): ('P', 1), 
   (3, 8): ('RGB', 3), 
   (4, 8): ('CMYK', 4), 
   (7, 8): ('L', 1), 
   (8, 8): ('L', 1), 
   (9, 8): ('LAB', 3)}

def i16(c):
    return ord(c[1]) + (ord(c[0]) << 8)


def i32(c):
    return ord(c[3]) + (ord(c[2]) << 8) + (ord(c[1]) << 16) + (ord(c[0]) << 24)


def _accept(prefix):
    return prefix[:4] == '8BPS'


class PsdImageFile(ImageFile.ImageFile):
    format = 'PSD'
    format_description = 'Adobe Photoshop'

    def _open(self):
        read = self.fp.read
        s = read(26)
        if s[:4] != '8BPS' or i16(s[4:]) != 1:
            raise SyntaxError, 'not a PSD file'
        psd_bits = i16(s[22:])
        psd_channels = i16(s[12:])
        psd_mode = i16(s[24:])
        (mode, channels) = MODES[(psd_mode, psd_bits)]
        if channels > psd_channels:
            raise IOError, 'not enough channels'
        self.mode = mode
        self.size = (i32(s[18:]), i32(s[14:]))
        size = i32(read(4))
        if size:
            data = read(size)
            if mode == 'P' and size == 768:
                self.palette = ImagePalette.raw('RGB;L', data)
        self.resources = []
        size = i32(read(4))
        if size:
            end = self.fp.tell() + size
            while self.fp.tell() < end:
                signature = read(4)
                id = i16(read(2))
                name = read(ord(read(1)))
                if not len(name) & 1:
                    read(1)
                data = read(i32(read(4)))
                if len(data) & 1:
                    read(1)
                self.resources.append((id, name, data))

        self.layers = []
        size = i32(read(4))
        if size:
            end = self.fp.tell() + size
            size = i32(read(4))
            if size:
                self.layers = _layerinfo(self.fp)
            self.fp.seek(end)
        self.tile = _maketile(self.fp, mode, (0, 0) + self.size, channels)
        self._fp = self.fp
        self.frame = 0

    def seek(self, layer):
        if layer == self.frame:
            return
        try:
            if layer <= 0:
                raise IndexError
            (name, mode, bbox, tile) = self.layers[(layer - 1)]
            self.mode = mode
            self.tile = tile
            self.frame = layer
            self.fp = self._fp
            return (name, bbox)
        except IndexError:
            raise EOFError, 'no such layer'

    def tell(self):
        return self.frame

    def load_prepare(self):
        if not self.im or self.im.mode != self.mode or self.im.size != self.size:
            self.im = Image.core.fill(self.mode, self.size, 0)
        if self.mode == 'P':
            Image.Image.load(self)


def _layerinfo(file):
    layers = []
    read = file.read
    for i in range(abs(i16(read(2)))):
        y0 = i32(read(4))
        x0 = i32(read(4))
        y1 = i32(read(4))
        x1 = i32(read(4))
        info = []
        mode = []
        for i in range(i16(read(2))):
            type = i16(read(2))
            if type == 65535:
                m = 'A'
            else:
                m = 'RGB'[type]
            mode.append(m)
            size = i32(read(4))
            info.append((m, size))

        mode.sort()
        if mode == ['R']:
            mode = 'L'
        elif mode == ['B', 'G', 'R']:
            mode = 'RGB'
        elif mode == ['A', 'B', 'G', 'R']:
            mode = 'RGBA'
        else:
            mode = None
        filler = read(12)
        name = None
        file.seek(i32(read(4)), 1)
        layers.append((name, mode, (x0, y0, x1, y1)))

    i = 0
    for (name, mode, bbox) in layers:
        tile = []
        for m in mode:
            t = _maketile(file, m, bbox, 1)
            if t:
                tile.extend(t)

        layers[i] = (
         name, mode, bbox, tile)
        i = i + 1

    return layers


def _maketile(file, mode, bbox, channels):
    tile = None
    read = file.read
    compression = i16(read(2))
    xsize = bbox[2] - bbox[0]
    ysize = bbox[3] - bbox[1]
    offset = file.tell()
    if compression == 0:
        tile = []
        for channel in range(channels):
            layer = mode[channel]
            if mode == 'CMYK':
                layer = layer + ';I'
            tile.append(('raw', bbox, offset, layer))
            offset = offset + xsize * ysize

    elif compression == 1:
        i = 0
        tile = []
        bytecount = read(channels * ysize * 2)
        offset = file.tell()
        for channel in range(channels):
            layer = mode[channel]
            if mode == 'CMYK':
                layer = layer + ';I'
            tile.append((
             'packbits', bbox, offset, layer))
            for y in range(ysize):
                offset = offset + i16(bytecount[i:i + 2])
                i = i + 2

    file.seek(offset)
    if offset & 1:
        read(1)
    return tile


Image.register_open('PSD', PsdImageFile, _accept)
Image.register_extension('PSD', '.psd')