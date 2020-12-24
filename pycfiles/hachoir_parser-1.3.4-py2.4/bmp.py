# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/hachoir_parser/image/bmp.py
# Compiled at: 2009-09-07 17:44:28
"""
Microsoft Bitmap picture parser.
- file extension: ".bmp"

Author: Victor Stinner
Creation: 16 december 2005
"""
from hachoir_parser import Parser
from hachoir_core.field import FieldSet, UInt8, UInt16, UInt32, Bits, String, RawBytes, Enum, PaddingBytes, NullBytes, createPaddingField
from hachoir_core.endian import LITTLE_ENDIAN
from hachoir_core.text_handler import textHandler, hexadecimal
from hachoir_parser.image.common import RGB, PaletteRGBA
from hachoir_core.tools import alignValue

class Pixel4bit(Bits):
    __module__ = __name__
    static_size = 4

    def __init__(self, parent, name):
        Bits.__init__(self, parent, name, 4)


class ImageLine(FieldSet):
    __module__ = __name__

    def __init__(self, parent, name, width, pixel_class):
        FieldSet.__init__(self, parent, name)
        self._pixel = pixel_class
        self._width = width
        self._size = alignValue(self._width * self._pixel.static_size, 32)

    def createFields(self):
        for x in xrange(self._width):
            yield self._pixel(self, 'pixel[]')

        size = self.size - self.current_size
        if size:
            yield createPaddingField(self, size)


class ImagePixels(FieldSet):
    __module__ = __name__

    def __init__(self, parent, name, width, height, pixel_class, size=None):
        FieldSet.__init__(self, parent, name, size=size)
        self._width = width
        self._height = height
        self._pixel = pixel_class

    def createFields(self):
        for y in xrange(self._height - 1, -1, -1):
            yield ImageLine(self, 'line[%u]' % y, self._width, self._pixel)

        size = (self.size - self.current_size) // 8
        if size:
            yield NullBytes(self, 'padding', size)


class CIEXYZ(FieldSet):
    __module__ = __name__

    def createFields(self):
        yield UInt32(self, 'x')
        yield UInt32(self, 'y')
        yield UInt32(self, 'z')


class BmpHeader(FieldSet):
    __module__ = __name__
    color_space_name = {1: 'Business (Saturation)', 2: 'Graphics (Relative)', 4: 'Images (Perceptual)', 8: 'Absolute colormetric (Absolute)'}

    def getFormatVersion(self):
        if 'gamma_blue' in self:
            return 4
        if 'important_color' in self:
            return 3
        return 2

    def createFields(self):
        yield UInt32(self, 'header_size', 'Header size')
        yield UInt32(self, 'width', 'Width (pixels)')
        yield UInt32(self, 'height', 'Height (pixels)')
        yield UInt16(self, 'nb_plan', 'Number of plan (=1)')
        yield UInt16(self, 'bpp', 'Bits per pixel')
        if self['header_size'].value < 40:
            return
        yield Enum(UInt32(self, 'compression', 'Compression method'), BmpFile.COMPRESSION_NAME)
        yield UInt32(self, 'image_size', 'Image size (bytes)')
        yield UInt32(self, 'horizontal_dpi', 'Horizontal DPI')
        yield UInt32(self, 'vertical_dpi', 'Vertical DPI')
        yield UInt32(self, 'used_colors', 'Number of color used')
        yield UInt32(self, 'important_color', 'Number of import colors')
        if self['header_size'].value < 108:
            return
        yield textHandler(UInt32(self, 'red_mask'), hexadecimal)
        yield textHandler(UInt32(self, 'green_mask'), hexadecimal)
        yield textHandler(UInt32(self, 'blue_mask'), hexadecimal)
        yield textHandler(UInt32(self, 'alpha_mask'), hexadecimal)
        yield Enum(UInt32(self, 'color_space'), self.color_space_name)
        yield CIEXYZ(self, 'red_primary')
        yield CIEXYZ(self, 'green_primary')
        yield CIEXYZ(self, 'blue_primary')
        yield UInt32(self, 'gamma_red')
        yield UInt32(self, 'gamma_green')
        yield UInt32(self, 'gamma_blue')


def parseImageData(parent, name, size, header):
    if 'compression' not in header or header['compression'].value in (0, 3):
        width = header['width'].value
        height = header['height'].value
        bpp = header['bpp'].value
        if bpp == 32:
            cls = UInt32
        elif bpp == 24:
            cls = RGB
        elif bpp == 8:
            cls = UInt8
        elif bpp == 4:
            cls = Pixel4bit
        else:
            cls = None
        if cls:
            return ImagePixels(parent, name, width, height, cls, size=size * 8)
    return RawBytes(parent, name, size)


class BmpFile(Parser):
    __module__ = __name__
    PARSER_TAGS = {'id': 'bmp', 'category': 'image', 'file_ext': ('bmp', ), 'mime': ('image/x-ms-bmp', 'image/x-bmp'), 'min_size': 30 * 8, 'magic_regex': (('BM.{4}.{8}[\x0c(l]\x00{3}', 0), ), 'description': 'Microsoft bitmap (BMP) picture'}
    endian = LITTLE_ENDIAN
    COMPRESSION_NAME = {0: 'Uncompressed', 1: 'RLE 8-bit', 2: 'RLE 4-bit', 3: 'Bitfields', 4: 'JPEG', 5: 'PNG'}

    def validate(self):
        if self.stream.readBytes(0, 2) != 'BM':
            return 'Wrong file signature'
        if self['header/header_size'].value not in (12, 40, 108):
            return 'Unknown header size (%s)' % self['header_size'].value
        if self['header/nb_plan'].value != 1:
            return 'Invalid number of planes'
        return True

    def createFields(self):
        yield String(self, 'signature', 2, 'Header ("BM")', charset='ASCII')
        yield UInt32(self, 'file_size', 'File size (bytes)')
        yield PaddingBytes(self, 'reserved', 4, 'Reserved')
        yield UInt32(self, 'data_start', 'Data start position')
        yield BmpHeader(self, 'header')
        header = self['header']
        bpp = header['bpp'].value
        if 0 < bpp <= 8:
            if 'used_colors' in header and header['used_colors'].value:
                nb_color = header['used_colors'].value
            else:
                nb_color = 1 << bpp
        else:
            nb_color = 0
        if nb_color:
            yield PaletteRGBA(self, 'palette', nb_color)
        field = self.seekByte(self['data_start'].value)
        if field:
            yield field
        size = min(self['file_size'].value - self['data_start'].value, (self.size - self.current_size) // 8)
        yield parseImageData(self, 'pixels', size, header)

    def createDescription(self):
        return 'Microsoft Bitmap version %s' % self['header'].getFormatVersion()

    def createContentSize(self):
        return self['file_size'].value * 8