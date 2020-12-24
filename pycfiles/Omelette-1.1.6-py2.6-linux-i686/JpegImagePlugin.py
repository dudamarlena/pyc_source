# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/PIL/JpegImagePlugin.py
# Compiled at: 2007-09-25 20:00:35
__version__ = '0.5'
import array, string, Image, ImageFile

def i16(c, o=0):
    return ord(c[(o + 1)]) + (ord(c[o]) << 8)


def i32(c, o=0):
    return ord(c[(o + 3)]) + (ord(c[(o + 2)]) << 8) + (ord(c[(o + 1)]) << 16) + (ord(c[o]) << 24)


def Skip(self, marker):
    n = i16(self.fp.read(2)) - 2
    ImageFile._safe_read(self.fp, n)


def APP(self, marker):
    n = i16(self.fp.read(2)) - 2
    s = ImageFile._safe_read(self.fp, n)
    app = 'APP%d' % (marker & 15)
    self.app[app] = s
    self.applist.append((app, s))
    if marker == 65504 and s[:4] == 'JFIF':
        self.info['jfif'] = version = i16(s, 5)
        self.info['jfif_version'] = divmod(version, 256)
        try:
            jfif_unit = ord(s[7])
            jfif_density = (i16(s, 8), i16(s, 10))
        except:
            pass
        else:
            if jfif_unit == 1:
                self.info['dpi'] = jfif_density
            self.info['jfif_unit'] = jfif_unit
            self.info['jfif_density'] = jfif_density
    elif marker == 65505 and s[:5] == 'Exif\x00':
        self.info['exif'] = s
    elif marker == 65506 and s[:5] == 'FPXR\x00':
        self.info['flashpix'] = s
    elif marker == 65518 and s[:5] == 'Adobe':
        self.info['adobe'] = i16(s, 5)
        try:
            adobe_transform = ord(s[1])
        except:
            pass
        else:
            self.info['adobe_transform'] = adobe_transform


def COM(self, marker):
    n = i16(self.fp.read(2)) - 2
    s = ImageFile._safe_read(self.fp, n)
    self.app['COM'] = s
    self.applist.append(('COM', s))


def SOF(self, marker):
    n = i16(self.fp.read(2)) - 2
    s = ImageFile._safe_read(self.fp, n)
    self.size = (i16(s[3:]), i16(s[1:]))
    self.bits = ord(s[0])
    if self.bits != 8:
        raise SyntaxError('cannot handle %d-bit layers' % self.bits)
    self.layers = ord(s[5])
    if self.layers == 1:
        self.mode = 'L'
    elif self.layers == 3:
        self.mode = 'RGB'
    elif self.layers == 4:
        self.mode = 'CMYK'
    else:
        raise SyntaxError('cannot handle %d-layer images' % self.layers)
    if marker in (65474, 65478, 65482, 65486):
        self.info['progression'] = 1
    for i in range(6, len(s), 3):
        t = s[i:i + 3]
        self.layer.append((t[0], ord(t[1]) / 16, ord(t[1]) & 15, ord(t[2])))


def DQT(self, marker):
    n = i16(self.fp.read(2)) - 2
    s = ImageFile._safe_read(self.fp, n)
    while len(s):
        if len(s) < 65:
            raise SyntaxError('bad quantization table marker')
        v = ord(s[0])
        if v / 16 == 0:
            self.quantization[v & 15] = array.array('b', s[1:65])
            s = s[65:]
        else:
            return


MARKER = {65472: (
         'SOF0', 'Baseline DCT', SOF), 
   65473: (
         'SOF1', 'Extended Sequential DCT', SOF), 
   65474: (
         'SOF2', 'Progressive DCT', SOF), 
   65475: (
         'SOF3', 'Spatial lossless', SOF), 
   65476: (
         'DHT', 'Define Huffman table', Skip), 
   65477: (
         'SOF5', 'Differential sequential DCT', SOF), 
   65478: (
         'SOF6', 'Differential progressive DCT', SOF), 
   65479: (
         'SOF7', 'Differential spatial', SOF), 
   65480: ('JPG', 'Extension', None), 
   65481: (
         'SOF9', 'Extended sequential DCT (AC)', SOF), 
   65482: (
         'SOF10', 'Progressive DCT (AC)', SOF), 
   65483: (
         'SOF11', 'Spatial lossless DCT (AC)', SOF), 
   65484: (
         'DAC', 'Define arithmetic coding conditioning', Skip), 
   65485: (
         'SOF13', 'Differential sequential DCT (AC)', SOF), 
   65486: (
         'SOF14', 'Differential progressive DCT (AC)', SOF), 
   65487: (
         'SOF15', 'Differential spatial (AC)', SOF), 
   65488: ('RST0', 'Restart 0', None), 
   65489: ('RST1', 'Restart 1', None), 
   65490: ('RST2', 'Restart 2', None), 
   65491: ('RST3', 'Restart 3', None), 
   65492: ('RST4', 'Restart 4', None), 
   65493: ('RST5', 'Restart 5', None), 
   65494: ('RST6', 'Restart 6', None), 
   65495: ('RST7', 'Restart 7', None), 
   65496: ('SOI', 'Start of image', None), 
   65497: ('EOI', 'End of image', None), 
   65498: (
         'SOS', 'Start of scan', Skip), 
   65499: (
         'DQT', 'Define quantization table', DQT), 
   65500: (
         'DNL', 'Define number of lines', Skip), 
   65501: (
         'DRI', 'Define restart interval', Skip), 
   65502: (
         'DHP', 'Define hierarchical progression', SOF), 
   65503: (
         'EXP', 'Expand reference component', Skip), 
   65504: (
         'APP0', 'Application segment 0', APP), 
   65505: (
         'APP1', 'Application segment 1', APP), 
   65506: (
         'APP2', 'Application segment 2', APP), 
   65507: (
         'APP3', 'Application segment 3', APP), 
   65508: (
         'APP4', 'Application segment 4', APP), 
   65509: (
         'APP5', 'Application segment 5', APP), 
   65510: (
         'APP6', 'Application segment 6', APP), 
   65511: (
         'APP7', 'Application segment 7', APP), 
   65512: (
         'APP8', 'Application segment 8', APP), 
   65513: (
         'APP9', 'Application segment 9', APP), 
   65514: (
         'APP10', 'Application segment 10', APP), 
   65515: (
         'APP11', 'Application segment 11', APP), 
   65516: (
         'APP12', 'Application segment 12', APP), 
   65517: (
         'APP13', 'Application segment 13', APP), 
   65518: (
         'APP14', 'Application segment 14', APP), 
   65519: (
         'APP15', 'Application segment 15', APP), 
   65520: ('JPG0', 'Extension 0', None), 
   65521: ('JPG1', 'Extension 1', None), 
   65522: ('JPG2', 'Extension 2', None), 
   65523: ('JPG3', 'Extension 3', None), 
   65524: ('JPG4', 'Extension 4', None), 
   65525: ('JPG5', 'Extension 5', None), 
   65526: ('JPG6', 'Extension 6', None), 
   65527: ('JPG7', 'Extension 7', None), 
   65528: ('JPG8', 'Extension 8', None), 
   65529: ('JPG9', 'Extension 9', None), 
   65530: ('JPG10', 'Extension 10', None), 
   65531: ('JPG11', 'Extension 11', None), 
   65532: ('JPG12', 'Extension 12', None), 
   65533: ('JPG13', 'Extension 13', None), 
   65534: (
         'COM', 'Comment', COM)}

def _accept(prefix):
    return prefix[0] == b'\xff'


class JpegImageFile(ImageFile.ImageFile):
    format = 'JPEG'
    format_description = 'JPEG (ISO 10918)'

    def _open(self):
        s = self.fp.read(1)
        if ord(s[0]) != 255:
            raise SyntaxError('not a JPEG file')
        self.bits = self.layers = 0
        self.layer = []
        self.huffman_dc = {}
        self.huffman_ac = {}
        self.quantization = {}
        self.app = {}
        self.applist = []
        while 1:
            s = s + self.fp.read(1)
            i = i16(s)
            if MARKER.has_key(i):
                (name, description, handler) = MARKER[i]
                if handler is not None:
                    handler(self, i)
                if i == 65498:
                    rawmode = self.mode
                    if self.mode == 'CMYK':
                        rawmode = 'CMYK;I'
                    self.tile = [
                     (
                      'jpeg', (0, 0) + self.size, 0, (rawmode, ''))]
                    break
                s = self.fp.read(1)
            elif i == 0 or i == 65535:
                s = b'\xff'
            else:
                raise SyntaxError('no marker found')

        return

    def draft(self, mode, size):
        if len(self.tile) != 1:
            return
        (d, e, o, a) = self.tile[0]
        scale = 0
        if a[0] == 'RGB' and mode in ('L', 'YCbCr'):
            self.mode = mode
            a = (mode, '')
        if size:
            scale = max(self.size[0] / size[0], self.size[1] / size[1])
            for s in [8, 4, 2, 1]:
                if scale >= s:
                    break

            e = (
             e[0], e[1], (e[2] - e[0] + s - 1) / s + e[0], (e[3] - e[1] + s - 1) / s + e[1])
            self.size = ((self.size[0] + s - 1) / s, (self.size[1] + s - 1) / s)
            scale = s
        self.tile = [(d, e, o, a)]
        self.decoderconfig = (scale, 1)
        return self

    def load_djpeg(self):
        import tempfile, os
        file = tempfile.mktemp()
        os.system('djpeg %s >%s' % (self.filename, file))
        try:
            self.im = Image.core.open_ppm(file)
        finally:
            try:
                os.unlink(file)
            except:
                pass

        self.mode = self.im.mode
        self.size = self.im.size
        self.tile = []

    def _getexif(self):
        import TiffImagePlugin, StringIO

        def fixup(value):
            if len(value) == 1:
                return value[0]
            return value

        try:
            data = self.info['exif']
        except KeyError:
            return
        else:
            file = StringIO.StringIO(data[6:])
            head = file.read(8)
            exif = {}
            info = TiffImagePlugin.ImageFileDirectory(head)
            info.load(file)
            for (key, value) in info.items():
                exif[key] = fixup(value)

            file.seek(exif[34665])
            info = TiffImagePlugin.ImageFileDirectory(head)
            info.load(file)
            for (key, value) in info.items():
                exif[key] = fixup(value)

            try:
                file.seek(exif[34853])
            except KeyError:
                pass
            else:
                info = TiffImagePlugin.ImageFileDirectory(head)
                info.load(file)
                exif[34853] = gps = {}
                for (key, value) in info.items():
                    gps[key] = fixup(value)

        return exif


RAWMODE = {'1': 'L', 
   'L': 'L', 
   'RGB': 'RGB', 
   'RGBA': 'RGB', 
   'RGBX': 'RGB', 
   'CMYK': 'CMYK;I', 
   'YCbCr': 'YCbCr'}

def _save(im, fp, filename):
    try:
        rawmode = RAWMODE[im.mode]
    except KeyError:
        raise IOError('cannot write mode %s as JPEG' % im.mode)

    info = im.encoderinfo
    dpi = info.get('dpi', (0, 0))
    im.encoderconfig = (
     info.get('quality', 0),
     info.has_key('progressive') or info.has_key('progression'),
     info.get('smooth', 0),
     info.has_key('optimize'),
     info.get('streamtype', 0),
     dpi[0], dpi[1])
    ImageFile._save(im, fp, [('jpeg', (0, 0) + im.size, 0, rawmode)])


def _save_cjpeg(im, fp, filename):
    import os
    file = im._dump()
    os.system('cjpeg %s >%s' % (file, filename))
    try:
        os.unlink(file)
    except:
        pass


Image.register_open('JPEG', JpegImageFile, _accept)
Image.register_save('JPEG', _save)
Image.register_extension('JPEG', '.jfif')
Image.register_extension('JPEG', '.jpe')
Image.register_extension('JPEG', '.jpg')
Image.register_extension('JPEG', '.jpeg')
Image.register_mime('JPEG', 'image/jpeg')