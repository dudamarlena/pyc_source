# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/hachoir_parser/image/xcf.py
# Compiled at: 2009-09-07 17:44:28
r"""
Gimp image parser (XCF file, ".xcf" extension).

You can find informations about XCF file in Gimp source code. URL to read
CVS online:
  http://cvs.gnome.org/viewcvs/gimp/app/xcf/
  \--> files xcf-read.c and xcf-load.c

Author: Victor Stinner
"""
from hachoir_parser import Parser
from hachoir_core.field import StaticFieldSet, FieldSet, ParserError, UInt8, UInt32, Enum, Float32, String, PascalString32, RawBytes
from hachoir_parser.image.common import RGBA
from hachoir_core.endian import NETWORK_ENDIAN

class XcfCompression(FieldSet):
    __module__ = __name__
    static_size = 8
    COMPRESSION_NAME = {0: 'None', 1: 'RLE', 2: 'Zlib', 3: 'Fractal'}

    def createFields(self):
        yield Enum(UInt8(self, 'compression', 'Compression method'), self.COMPRESSION_NAME)


class XcfResolution(StaticFieldSet):
    __module__ = __name__
    format = ((Float32, 'xres', 'X resolution in DPI'), (Float32, 'yres', 'Y resolution in DPI'))


class XcfTattoo(StaticFieldSet):
    __module__ = __name__
    format = ((UInt32, 'tattoo', 'Tattoo'),)


class LayerOffsets(StaticFieldSet):
    __module__ = __name__
    format = ((UInt32, 'ofst_x', 'Offset X'), (UInt32, 'ofst_y', 'Offset Y'))


class LayerMode(FieldSet):
    __module__ = __name__
    static_size = 32
    MODE_NAME = {0: 'Normal', 1: 'Dissolve', 2: 'Behind', 3: 'Multiply', 4: 'Screen', 5: 'Overlay', 6: 'Difference', 7: 'Addition', 8: 'Subtract', 9: 'Darken only', 10: 'Lighten only', 11: 'Hue', 12: 'Saturation', 13: 'Color', 14: 'Value', 15: 'Divide', 16: 'Dodge', 17: 'Burn', 18: 'Hard light', 19: 'Soft light', 20: 'Grain extract', 21: 'Grain merge', 22: 'Color erase'}

    def createFields(self):
        yield Enum(UInt32(self, 'mode', 'Layer mode'), self.MODE_NAME)


class GimpBoolean(UInt32):
    __module__ = __name__

    def __init__(self, parent, name):
        UInt32.__init__(self, parent, name)

    def createValue(self):
        return 1 == UInt32.createValue(self)


class XcfUnit(StaticFieldSet):
    __module__ = __name__
    format = ((UInt32, 'unit', 'Unit'),)


class XcfParasiteEntry(FieldSet):
    __module__ = __name__

    def createFields(self):
        yield PascalString32(self, 'name', 'Name', strip='\x00', charset='UTF-8')
        yield UInt32(self, 'flags', 'Flags')
        yield PascalString32(self, 'data', 'Data', strip=' \x00', charset='UTF-8')


class XcfLevel(FieldSet):
    __module__ = __name__

    def createFields(self):
        yield UInt32(self, 'width', 'Width in pixel')
        yield UInt32(self, 'height', 'Height in pixel')
        yield UInt32(self, 'offset', 'Offset')
        offset = self['offset'].value
        if offset == 0:
            return
        data_offsets = []
        while (self.absolute_address + self.current_size) / 8 < offset:
            chunk = UInt32(self, 'data_offset[]', 'Data offset')
            yield chunk
            if chunk.value == 0:
                break
            data_offsets.append(chunk)

        if (self.absolute_address + self.current_size) / 8 != offset:
            raise ParserError('Problem with level offset.')
        previous = offset
        for chunk in data_offsets:
            data_offset = chunk.value
            size = data_offset - previous
            yield RawBytes(self, 'data[]', size, 'Data content of %s' % chunk.name)
            previous = data_offset


class XcfHierarchy(FieldSet):
    __module__ = __name__

    def createFields(self):
        yield UInt32(self, 'width', 'Width')
        yield UInt32(self, 'height', 'Height')
        yield UInt32(self, 'bpp', 'Bits/pixel')
        offsets = []
        while True:
            chunk = UInt32(self, 'offset[]', 'Level offset')
            yield chunk
            if chunk.value == 0:
                break
            offsets.append(chunk.value)

        for offset in offsets:
            padding = self.seekByte(offset, relative=False)
            if padding is not None:
                yield padding
            yield XcfLevel(self, 'level[]', 'Level')

        return


class XcfChannel(FieldSet):
    __module__ = __name__

    def createFields(self):
        yield UInt32(self, 'width', 'Channel width')
        yield UInt32(self, 'height', 'Channel height')
        yield PascalString32(self, 'name', 'Channel name', strip='\x00', charset='UTF-8')
        for field in readProperties(self):
            yield field

        yield UInt32(self, 'hierarchy_ofs', 'Hierarchy offset')
        yield XcfHierarchy(self, 'hierarchy', 'Hierarchy')

    def createDescription(self):
        return 'Channel "%s"' % self['name'].value


class XcfLayer(FieldSet):
    __module__ = __name__

    def createFields(self):
        yield UInt32(self, 'width', 'Layer width in pixels')
        yield UInt32(self, 'height', 'Layer height in pixels')
        yield Enum(UInt32(self, 'type', 'Layer type'), XcfFile.IMAGE_TYPE_NAME)
        yield PascalString32(self, 'name', 'Layer name', strip='\x00', charset='UTF-8')
        for prop in readProperties(self):
            yield prop

        yield UInt32(self, 'hierarchy_ofs', 'Hierarchy offset')
        yield UInt32(self, 'mask_ofs', 'Layer mask offset')
        padding = self.seekByte(self['hierarchy_ofs'].value, relative=False)
        if padding is not None:
            yield padding
        yield XcfHierarchy(self, 'hierarchy', 'Hierarchy')
        return

    def createDescription(self):
        return 'Layer "%s"' % self['name'].value


class XcfParasites(FieldSet):
    __module__ = __name__

    def createFields(self):
        size = self['../size'].value * 8
        while self.current_size < size:
            yield XcfParasiteEntry(self, 'parasite[]', 'Parasite')


class XcfProperty(FieldSet):
    __module__ = __name__
    PROP_COMPRESSION = 17
    PROP_RESOLUTION = 19
    PROP_PARASITES = 21
    TYPE_NAME = {0: 'End', 1: 'Colormap', 2: 'Active layer', 3: 'Active channel', 4: 'Selection', 5: 'Floating selection', 6: 'Opacity', 7: 'Mode', 8: 'Visible', 9: 'Linked', 10: 'Lock alpha', 11: 'Apply mask', 12: 'Edit mask', 13: 'Show mask', 14: 'Show masked', 15: 'Offsets', 16: 'Color', 17: 'Compression', 18: 'Guides', 19: 'Resolution', 20: 'Tattoo', 21: 'Parasites', 22: 'Unit', 23: 'Paths', 24: 'User unit', 25: 'Vectors', 26: 'Text layer flags'}
    handler = {6: RGBA, 7: LayerMode, 8: GimpBoolean, 9: GimpBoolean, 10: GimpBoolean, 11: GimpBoolean, 12: GimpBoolean, 13: GimpBoolean, 15: LayerOffsets, 17: XcfCompression, 19: XcfResolution, 20: XcfTattoo, 21: XcfParasites, 22: XcfUnit}

    def __init__(self, *args, **kw):
        FieldSet.__init__(self, *args, **kw)
        self._size = (8 + self['size'].value) * 8

    def createFields(self):
        yield Enum(UInt32(self, 'type', 'Property type'), self.TYPE_NAME)
        yield UInt32(self, 'size', 'Property size')
        size = self['size'].value
        if 0 < size:
            cls = self.handler.get(self['type'].value, None)
            if cls:
                yield cls(self, 'data', size=size * 8)
            else:
                yield RawBytes(self, 'data', size, 'Data')
        return

    def createDescription(self):
        return 'Property: %s' % self['type'].display


def readProperties(parser):
    while True:
        prop = XcfProperty(parser, 'property[]')
        yield prop
        if prop['type'].value == 0:
            return


class XcfFile(Parser):
    __module__ = __name__
    PARSER_TAGS = {'id': 'xcf', 'category': 'image', 'file_ext': ('xcf', ), 'mime': ('image/x-xcf', 'application/x-gimp-image'), 'min_size': (26 + 8 + 4 + 4) * 8, 'magic': (('gimp xcf file\x00', 0), ('gimp xcf v002\x00', 0)), 'description': 'Gimp (XCF) picture'}
    endian = NETWORK_ENDIAN
    IMAGE_TYPE_NAME = {0: 'RGB', 1: 'Gray', 2: 'Indexed'}

    def validate(self):
        if self.stream.readBytes(0, 14) not in ('gimp xcf file\x00', 'gimp xcf v002\x00'):
            return 'Wrong signature'
        return True

    def createFields(self):
        yield String(self, 'signature', 14, 'Gimp picture signature (ends with nul byte)', charset='ASCII')
        yield UInt32(self, 'width', 'Image width')
        yield UInt32(self, 'height', 'Image height')
        yield Enum(UInt32(self, 'type', 'Image type'), self.IMAGE_TYPE_NAME)
        for prop in readProperties(self):
            yield prop

        layer_offsets = []
        while True:
            chunk = UInt32(self, 'layer_offset[]', 'Layer offset')
            yield chunk
            if chunk.value == 0:
                break
            layer_offsets.append(chunk.value)

        channel_offsets = []
        while True:
            chunk = UInt32(self, 'channel_offset[]', 'Channel offset')
            yield chunk
            if chunk.value == 0:
                break
            channel_offsets.append(chunk.value)

        for (index, offset) in enumerate(layer_offsets):
            if index + 1 < len(layer_offsets):
                size = (layer_offsets[(index + 1)] - offset) * 8
            else:
                size = None
            padding = self.seekByte(offset, relative=False)
            if padding:
                yield padding
            yield XcfLayer(self, 'layer[]', size=size)

        for (index, offset) in enumerate(channel_offsets):
            if index + 1 < len(channel_offsets):
                size = (channel_offsets[(index + 1)] - offset) * 8
            else:
                size = None
            padding = self.seekByte(offset, relative=False)
            if padding is not None:
                yield padding
            yield XcfChannel(self, 'channel[]', 'Channel', size=size)

        return