# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/hachoir_parser/image/tga.py
# Compiled at: 2009-09-07 17:44:28
"""
Truevision Targa Graphic (TGA) picture parser.

Author: Victor Stinner
Creation: 18 december 2006
"""
from hachoir_parser import Parser
from hachoir_core.field import FieldSet, UInt8, UInt16, Enum, RawBytes
from hachoir_core.endian import LITTLE_ENDIAN
from hachoir_parser.image.common import PaletteRGB

class Line(FieldSet):
    __module__ = __name__

    def __init__(self, *args):
        FieldSet.__init__(self, *args)
        self._size = self['/width'].value * self['/bpp'].value

    def createFields(self):
        for x in xrange(self['/width'].value):
            yield UInt8(self, 'pixel[]')


class Pixels(FieldSet):
    __module__ = __name__

    def __init__(self, *args):
        FieldSet.__init__(self, *args)
        self._size = self['/width'].value * self['/height'].value * self['/bpp'].value

    def createFields(self):
        if self['/options'].value == 0:
            RANGE = xrange(self['/height'].value - 1, -1, -1)
        else:
            RANGE = xrange(self['/height'].value)
        for y in RANGE:
            yield Line(self, 'line[%u]' % y)


class TargaFile(Parser):
    __module__ = __name__
    PARSER_TAGS = {'id': 'targa', 'category': 'image', 'file_ext': ('tga', ), 'mime': ('image/targa', 'image/tga', 'image/x-tga'), 'min_size': 18 * 8, 'description': 'Truevision Targa Graphic (TGA)'}
    CODEC_NAME = {1: '8-bit uncompressed', 2: '24-bit uncompressed', 9: '8-bit RLE', 10: '24-bit RLE'}
    endian = LITTLE_ENDIAN

    def validate(self):
        if self['version'].value != 1:
            return 'Unknown version'
        if self['codec'].value not in self.CODEC_NAME:
            return 'Unknown codec'
        if self['x_min'].value != 0 or self['y_min'].value != 0:
            return '(x_min, y_min) is not (0,0)'
        if self['bpp'].value not in (8, 24):
            return 'Unknown bits/pixel value'
        return True

    def createFields(self):
        yield UInt8(self, 'hdr_size', 'Header size in bytes')
        yield UInt8(self, 'version', 'Targa version (always one)')
        yield Enum(UInt8(self, 'codec', 'Pixels encoding'), self.CODEC_NAME)
        yield UInt16(self, 'palette_ofs', 'Palette absolute file offset')
        yield UInt16(self, 'nb_color', 'Number of color')
        yield UInt8(self, 'color_map_size', 'Color map entry size')
        yield UInt16(self, 'x_min')
        yield UInt16(self, 'y_min')
        yield UInt16(self, 'width')
        yield UInt16(self, 'height')
        yield UInt8(self, 'bpp', 'Bits per pixel')
        yield UInt8(self, 'options', 'Options (0: vertical mirror)')
        if self['bpp'].value == 8:
            yield PaletteRGB(self, 'palette', 256)
        if self['codec'].value == 1:
            yield Pixels(self, 'pixels')
        else:
            size = (self.size - self.current_size) // 8
            if size:
                yield RawBytes(self, 'raw_pixels', size)