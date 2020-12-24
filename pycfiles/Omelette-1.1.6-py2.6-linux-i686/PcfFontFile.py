# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/PIL/PcfFontFile.py
# Compiled at: 2007-09-25 20:00:35
import Image, FontFile, string
PCF_MAGIC = 1885562369
PCF_PROPERTIES = 1
PCF_ACCELERATORS = 2
PCF_METRICS = 4
PCF_BITMAPS = 8
PCF_INK_METRICS = 16
PCF_BDF_ENCODINGS = 32
PCF_SWIDTHS = 64
PCF_GLYPH_NAMES = 128
PCF_BDF_ACCELERATORS = 256
BYTES_PER_ROW = [
 lambda bits: bits + 7 >> 3,
 lambda bits: bits + 15 >> 3 & -2,
 lambda bits: bits + 31 >> 3 & -4,
 lambda bits: bits + 63 >> 3 & -8]

def l16(c):
    return ord(c[0]) + (ord(c[1]) << 8)


def l32(c):
    return ord(c[0]) + (ord(c[1]) << 8) + (ord(c[2]) << 16) + (ord(c[3]) << 24)


def b16(c):
    return ord(c[1]) + (ord(c[0]) << 8)


def b32(c):
    return ord(c[3]) + (ord(c[2]) << 8) + (ord(c[1]) << 16) + (ord(c[0]) << 24)


def sz(s, o):
    return s[o:string.index(s, '\x00', o)]


class PcfFontFile(FontFile.FontFile):
    name = 'name'

    def __init__(self, fp):
        magic = l32(fp.read(4))
        if magic != PCF_MAGIC:
            raise SyntaxError, 'not a PCF file'
        FontFile.FontFile.__init__(self)
        count = l32(fp.read(4))
        self.toc = {}
        for i in range(count):
            type = l32(fp.read(4))
            self.toc[type] = (l32(fp.read(4)), l32(fp.read(4)), l32(fp.read(4)))

        self.fp = fp
        self.info = self._load_properties()
        metrics = self._load_metrics()
        bitmaps = self._load_bitmaps(metrics)
        encoding = self._load_encoding()
        for ch in range(256):
            ix = encoding[ch]
            if ix is not None:
                (x, y, l, r, w, a, d, f) = metrics[ix]
                glyph = ((w, 0), (l, d - y, x + l, d), (0, 0, x, y), bitmaps[ix])
                self.glyph[ch] = glyph

        return

    def _getformat(self, tag):
        (format, size, offset) = self.toc[tag]
        fp = self.fp
        fp.seek(offset)
        format = l32(fp.read(4))
        if format & 4:
            i16, i32 = b16, b32
        else:
            i16, i32 = l16, l32
        return (fp, format, i16, i32)

    def _load_properties(self):
        properties = {}
        (fp, format, i16, i32) = self._getformat(PCF_PROPERTIES)
        nprops = i32(fp.read(4))
        p = []
        for i in range(nprops):
            p.append((i32(fp.read(4)), ord(fp.read(1)), i32(fp.read(4))))

        if nprops & 3:
            fp.seek(4 - (nprops & 3), 1)
        data = fp.read(i32(fp.read(4)))
        for (k, s, v) in p:
            k = sz(data, k)
            if s:
                v = sz(data, v)
            properties[k] = v

        return properties

    def _load_metrics(self):
        metrics = []
        (fp, format, i16, i32) = self._getformat(PCF_METRICS)
        append = metrics.append
        if format & 65280 == 256:
            for i in range(i16(fp.read(2))):
                left = ord(fp.read(1)) - 128
                right = ord(fp.read(1)) - 128
                width = ord(fp.read(1)) - 128
                ascent = ord(fp.read(1)) - 128
                descent = ord(fp.read(1)) - 128
                xsize = right - left
                ysize = ascent + descent
                append((
                 xsize, ysize, left, right, width,
                 ascent, descent, 0))

        for i in range(i32(fp.read(4))):
            left = i16(fp.read(2))
            right = i16(fp.read(2))
            width = i16(fp.read(2))
            ascent = i16(fp.read(2))
            descent = i16(fp.read(2))
            attributes = i16(fp.read(2))
            xsize = right - left
            ysize = ascent + descent
            append((
             xsize, ysize, left, right, width,
             ascent, descent, attributes))

        return metrics

    def _load_bitmaps(self, metrics):
        bitmaps = []
        (fp, format, i16, i32) = self._getformat(PCF_BITMAPS)
        nbitmaps = i32(fp.read(4))
        if nbitmaps != len(metrics):
            raise IOError, 'Wrong number of bitmaps'
        offsets = []
        for i in range(nbitmaps):
            offsets.append(i32(fp.read(4)))

        bitmapSizes = []
        for i in range(4):
            bitmapSizes.append(i32(fp.read(4)))

        byteorder = format & 4
        bitorder = format & 8
        padindex = format & 3
        bitmapsize = bitmapSizes[padindex]
        offsets.append(bitmapsize)
        data = fp.read(bitmapsize)
        pad = BYTES_PER_ROW[padindex]
        mode = '1;R'
        if bitorder:
            mode = '1'
        for i in range(nbitmaps):
            (x, y, l, r, w, a, d, f) = metrics[i]
            b, e = offsets[i], offsets[(i + 1)]
            bitmaps.append(Image.fromstring('1', (x, y), data[b:e], 'raw', mode, pad(x)))

        return bitmaps

    def _load_encoding(self):
        encoding = [
         None] * 256
        (fp, format, i16, i32) = self._getformat(PCF_BDF_ENCODINGS)
        firstCol, lastCol = i16(fp.read(2)), i16(fp.read(2))
        firstRow, lastRow = i16(fp.read(2)), i16(fp.read(2))
        default = i16(fp.read(2))
        nencoding = (lastCol - firstCol + 1) * (lastRow - firstRow + 1)
        for i in range(nencoding):
            encodingOffset = i16(fp.read(2))
            if encodingOffset != 65535:
                try:
                    encoding[i + firstCol] = encodingOffset
                except IndexError:
                    break

        return encoding