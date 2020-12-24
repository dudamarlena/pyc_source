# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/hachoir_parser/image/wmf.py
# Compiled at: 2010-01-20 18:01:50
"""
Hachoir parser of Microsoft Windows Metafile (WMF) file format.

Documentation:
 - Microsoft Windows Metafile; also known as: WMF,
   Enhanced Metafile, EMF, APM
   http://wvware.sourceforge.net/caolan/ora-wmf.html
 - libwmf source code:
     - include/libwmf/defs.h: enums
     - src/player/meta.h: arguments parsers
 - libemf source code

Author: Victor Stinner
Creation date: 26 december 2006
"""
MAX_FILESIZE = 50 * 1024 * 1024
from hachoir_parser import Parser
from hachoir_core.field import FieldSet, StaticFieldSet, Enum, MissingField, ParserError, UInt32, Int32, UInt16, Int16, UInt8, NullBytes, RawBytes, String
from hachoir_core.endian import LITTLE_ENDIAN
from hachoir_core.text_handler import textHandler, hexadecimal
from hachoir_core.tools import createDict
from hachoir_parser.image.common import RGBA
POLYFILL_MODE = {1: 'Alternate', 2: 'Winding'}
BRUSH_STYLE = {0: 'Solid', 1: 'Null', 2: 'Hollow', 3: 'Pattern', 4: 'Indexed', 5: 'DIB pattern', 6: 'DIB pattern point', 7: 'Pattern 8x8', 8: 'DIB pattern 8x8'}
HATCH_STYLE = {0: 'Horizontal', 1: 'Vertical', 2: 'FDIAGONAL', 3: 'BDIAGONAL', 4: 'Cross', 5: 'Diagonal cross'}
PEN_STYLE = {0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dash dot', 4: 'Dash dot dot', 5: 'Null', 6: 'Inside frame', 7: 'User style', 8: 'Alternate'}
ROP2_DESC = {1: 'Black (0)', 2: 'Not merge pen (DPon)', 3: 'Mask not pen (DPna)', 4: 'Not copy pen (PN)', 5: 'Mask pen not (PDna)', 6: 'Not (Dn)', 7: 'Xor pen (DPx)', 8: 'Not mask pen (DPan)', 9: 'Mask pen (DPa)', 10: 'Not xor pen (DPxn)', 11: 'No operation (D)', 12: 'Merge not pen (DPno)', 13: 'Copy pen (P)', 14: 'Merge pen not (PDno)', 15: 'Merge pen (DPo)', 16: 'White (1)'}

def parseXY(parser):
    yield Int16(parser, 'x')
    yield Int16(parser, 'y')


def parseCreateBrushIndirect(parser):
    yield Enum(UInt16(parser, 'brush_style'), BRUSH_STYLE)
    yield RGBA(parser, 'color')
    yield Enum(UInt16(parser, 'brush_hatch'), HATCH_STYLE)


def parsePenIndirect(parser):
    yield Enum(UInt16(parser, 'pen_style'), PEN_STYLE)
    yield UInt16(parser, 'pen_width')
    yield UInt16(parser, 'pen_height')
    yield RGBA(parser, 'color')


def parsePolyFillMode(parser):
    yield Enum(UInt16(parser, 'operation'), POLYFILL_MODE)


def parseROP2(parser):
    yield Enum(UInt16(parser, 'operation'), ROP2_DESC)


def parseObjectID(parser):
    yield UInt16(parser, 'object_id')


class Point(FieldSet):
    __module__ = __name__
    static_size = 32

    def createFields(self):
        yield Int16(self, 'x')
        yield Int16(self, 'y')

    def createDescription(self):
        return 'Point (%s, %s)' % (self['x'].value, self['y'].value)


def parsePolygon(parser):
    yield UInt16(parser, 'count')
    for index in xrange(parser['count'].value):
        yield Point(parser, 'point[]')


META = {0: ('EOF', 'End of file', None), 30: ('SAVEDC', 'Save device context', None), 53: ('REALIZEPALETTE', 'Realize palette', None), 55: ('SETPALENTRIES', 'Set palette entries', None), 247: ('CREATEPALETTE', 'Create palette', None), 258: ('SETBKMODE', 'Set background mode', None), 259: ('SETMAPMODE', 'Set mapping mode', None), 260: ('SETROP2', 'Set foreground mix mode', parseROP2), 262: ('SETPOLYFILLMODE', 'Set polygon fill mode', parsePolyFillMode), 263: ('SETSTRETCHBLTMODE', 'Set bitmap streching mode', None), 264: ('SETTEXTCHAREXTRA', 'Set text character extra', None), 295: ('RESTOREDC', 'Restore device context', None), 298: ('INVERTREGION', 'Invert region', None), 299: ('PAINTREGION', 'Paint region', None), 300: ('SELECTCLIPREGION', 'Select clipping region', None), 301: ('SELECTOBJECT', 'Select object', parseObjectID), 302: ('SETTEXTALIGN', 'Set text alignment', None), 322: ('CREATEDIBPATTERNBRUSH', 'Create DIB brush with specified pattern', None), 496: ('DELETEOBJECT', 'Delete object', parseObjectID), 513: ('SETBKCOLOR', 'Set background color', None), 521: ('SETTEXTCOLOR', 'Set text color', None), 522: ('SETTEXTJUSTIFICATION', 'Set text justification', None), 523: ('SETWINDOWORG', 'Set window origin', parseXY), 524: ('SETWINDOWEXT', 'Set window extends', parseXY), 525: ('SETVIEWPORTORG', 'Set view port origin', None), 526: ('SETVIEWPORTEXT', 'Set view port extends', None), 527: ('OFFSETWINDOWORG', 'Offset window origin', None), 529: ('OFFSETVIEWPORTORG', 'Offset view port origin', None), 531: ('LINETO', 'Draw a line to', None), 532: ('MOVETO', 'Move to', None), 544: ('OFFSETCLIPRGN', 'Offset clipping rectangle', None), 552: ('FILLREGION', 'Fill region', None), 561: ('SETMAPPERFLAGS', 'Set mapper flags', None), 564: ('SELECTPALETTE', 'Select palette', None), 763: ('CREATEFONTINDIRECT', 'Create font indirect', None), 762: ('CREATEPENINDIRECT', 'Create pen indirect', parsePenIndirect), 764: ('CREATEBRUSHINDIRECT', 'Create brush indirect', parseCreateBrushIndirect), 804: ('POLYGON', 'Draw a polygon', parsePolygon), 805: ('POLYLINE', 'Draw a polyline', None), 1040: ('SCALEWINDOWEXT', 'Scale window extends', None), 1042: ('SCALEVIEWPORTEXT', 'Scale view port extends', None), 1045: ('EXCLUDECLIPRECT', 'Exclude clipping rectangle', None), 1046: ('INTERSECTCLIPRECT', 'Intersect clipping rectangle', None), 1048: ('ELLIPSE', 'Draw an ellipse', None), 1049: ('FLOODFILL', 'Flood fill', None), 1051: ('RECTANGLE', 'Draw a rectangle', None), 1055: ('SETPIXEL', 'Set pixel', None), 1065: ('FRAMEREGION', 'Fram region', None), 1313: ('TEXTOUT', 'Draw text', None), 1336: ('POLYPOLYGON', 'Draw multiple polygons', None), 1352: ('EXTFLOODFILL', 'Extend flood fill', None), 1564: ('ROUNDRECT', 'Draw a rounded rectangle', None), 1565: ('PATBLT', 'Pattern blitting', None), 1574: ('ESCAPE', 'Escape', None), 1791: ('CREATEREGION', 'Create region', None), 2071: ('ARC', 'Draw an arc', None), 2074: ('PIE', 'Draw a pie', None), 2096: ('CHORD', 'Draw a chord', None), 2368: ('DIBBITBLT', 'DIB bit blitting', None), 2610: ('EXTTEXTOUT', 'Draw text (extra)', None), 2881: ('DIBSTRETCHBLT', 'DIB stretch blitting', None), 3379: ('SETDIBTODEV', 'Set DIB to device', None), 3907: ('STRETCHDIB', 'Stretch DIB', None)}
META_NAME = createDict(META, 0)
META_DESC = createDict(META, 1)
EMF_MAPPING_MODE = {1: 'TEXT', 2: 'LOMETRIC', 3: 'HIMETRIC', 4: 'LOENGLISH', 5: 'HIENGLISH', 6: 'TWIPS', 7: 'ISOTROPIC', 8: 'ANISOTROPIC'}

def parseEmfMappingMode(parser):
    yield Enum(Int32(parser, 'mapping_mode'), EMF_MAPPING_MODE)


def parseXY32(parser):
    yield Int32(parser, 'x')
    yield Int32(parser, 'y')


def parseObjectID32(parser):
    yield textHandler(UInt32(parser, 'object_id'), hexadecimal)


def parseBrushIndirect(parser):
    yield UInt32(parser, 'ihBrush')
    yield UInt32(parser, 'style')
    yield RGBA(parser, 'color')
    yield Int32(parser, 'hatch')


class Point16(FieldSet):
    __module__ = __name__
    static_size = 32

    def createFields(self):
        yield Int16(self, 'x')
        yield Int16(self, 'y')

    def createDescription(self):
        return 'Point16: (%i,%i)' % (self['x'].value, self['y'].value)


def parsePoint16array(parser):
    yield RECT32(parser, 'bounds')
    yield UInt32(parser, 'count')
    for index in xrange(parser['count'].value):
        yield Point16(parser, 'point[]')


def parseGDIComment(parser):
    yield UInt32(parser, 'data_size')
    size = parser['data_size'].value
    if size:
        yield RawBytes(parser, 'data', size)


def parseICMMode(parser):
    yield UInt32(parser, 'icm_mode')


def parseExtCreatePen(parser):
    yield UInt32(parser, 'ihPen')
    yield UInt32(parser, 'offBmi')
    yield UInt32(parser, 'cbBmi')
    yield UInt32(parser, 'offBits')
    yield UInt32(parser, 'cbBits')
    yield UInt32(parser, 'pen_style')
    yield UInt32(parser, 'width')
    yield UInt32(parser, 'brush_style')
    yield RGBA(parser, 'color')
    yield UInt32(parser, 'hatch')
    yield UInt32(parser, 'nb_style')
    for index in xrange(parser['nb_style'].value):
        yield UInt32(parser, 'style')


EMF_META = {1: ('HEADER', 'Header', None), 2: ('POLYBEZIER', 'Draw poly bezier', None), 3: ('POLYGON', 'Draw polygon', None), 4: ('POLYLINE', 'Draw polyline', None), 5: ('POLYBEZIERTO', 'Draw poly bezier to', None), 6: ('POLYLINETO', 'Draw poly line to', None), 7: ('POLYPOLYLINE', 'Draw poly polyline', None), 8: ('POLYPOLYGON', 'Draw poly polygon', None), 9: ('SETWINDOWEXTEX', 'Set window extend EX', parseXY32), 10: ('SETWINDOWORGEX', 'Set window origin EX', parseXY32), 11: ('SETVIEWPORTEXTEX', 'Set viewport extend EX', parseXY32), 12: ('SETVIEWPORTORGEX', 'Set viewport origin EX', parseXY32), 13: ('SETBRUSHORGEX', 'Set brush org EX', None), 14: ('EOF', 'End of file', None), 15: ('SETPIXELV', 'Set pixel V', None), 16: ('SETMAPPERFLAGS', 'Set mapper flags', None), 17: ('SETMAPMODE', 'Set mapping mode', parseEmfMappingMode), 18: ('SETBKMODE', 'Set background mode', None), 19: ('SETPOLYFILLMODE', 'Set polyfill mode', None), 20: ('SETROP2', 'Set ROP2', None), 21: ('SETSTRETCHBLTMODE', 'Set stretching blitting mode', None), 22: ('SETTEXTALIGN', 'Set text align', None), 23: ('SETCOLORADJUSTMENT', 'Set color adjustment', None), 24: ('SETTEXTCOLOR', 'Set text color', None), 25: ('SETBKCOLOR', 'Set background color', None), 26: ('OFFSETCLIPRGN', 'Offset clipping region', None), 27: ('MOVETOEX', 'Move to EX', parseXY32), 28: ('SETMETARGN', 'Set meta region', None), 29: ('EXCLUDECLIPRECT', 'Exclude clipping rectangle', None), 30: ('INTERSECTCLIPRECT', 'Intersect clipping rectangle', None), 31: ('SCALEVIEWPORTEXTEX', 'Scale viewport extend EX', None), 32: ('SCALEWINDOWEXTEX', 'Scale window extend EX', None), 33: ('SAVEDC', 'Save device context', None), 34: ('RESTOREDC', 'Restore device context', None), 35: ('SETWORLDTRANSFORM', 'Set world transform', None), 36: ('MODIFYWORLDTRANSFORM', 'Modify world transform', None), 37: ('SELECTOBJECT', 'Select object', parseObjectID32), 38: ('CREATEPEN', 'Create pen', None), 39: ('CREATEBRUSHINDIRECT', 'Create brush indirect', parseBrushIndirect), 40: ('DELETEOBJECT', 'Delete object', parseObjectID32), 41: ('ANGLEARC', 'Draw angle arc', None), 42: ('ELLIPSE', 'Draw ellipse', None), 43: ('RECTANGLE', 'Draw rectangle', None), 44: ('ROUNDRECT', 'Draw rounded rectangle', None), 45: ('ARC', 'Draw arc', None), 46: ('CHORD', 'Draw chord', None), 47: ('PIE', 'Draw pie', None), 48: ('SELECTPALETTE', 'Select palette', None), 49: ('CREATEPALETTE', 'Create palette', None), 50: ('SETPALETTEENTRIES', 'Set palette entries', None), 51: ('RESIZEPALETTE', 'Resize palette', None), 52: ('REALIZEPALETTE', 'Realize palette', None), 53: ('EXTFLOODFILL', 'EXT flood fill', None), 54: ('LINETO', 'Draw line to', parseXY32), 55: ('ARCTO', 'Draw arc to', None), 56: ('POLYDRAW', 'Draw poly draw', None), 57: ('SETARCDIRECTION', 'Set arc direction', None), 58: ('SETMITERLIMIT', 'Set miter limit', None), 59: ('BEGINPATH', 'Begin path', None), 60: ('ENDPATH', 'End path', None), 61: ('CLOSEFIGURE', 'Close figure', None), 62: ('FILLPATH', 'Fill path', None), 63: ('STROKEANDFILLPATH', 'Stroke and fill path', None), 64: ('STROKEPATH', 'Stroke path', None), 65: ('FLATTENPATH', 'Flatten path', None), 66: ('WIDENPATH', 'Widen path', None), 67: ('SELECTCLIPPATH', 'Select clipping path', None), 68: ('ABORTPATH', 'Arbort path', None), 70: ('GDICOMMENT', 'GDI comment', parseGDIComment), 71: ('FILLRGN', 'Fill region', None), 72: ('FRAMERGN', 'Frame region', None), 73: ('INVERTRGN', 'Invert region', None), 74: ('PAINTRGN', 'Paint region', None), 75: ('EXTSELECTCLIPRGN', 'EXT select clipping region', None), 76: ('BITBLT', 'Bit blitting', None), 77: ('STRETCHBLT', 'Stretch blitting', None), 78: ('MASKBLT', 'Mask blitting', None), 79: ('PLGBLT', 'PLG blitting', None), 80: ('SETDIBITSTODEVICE', 'Set DIB bits to device', None), 81: ('STRETCHDIBITS', 'Stretch DIB bits', None), 82: ('EXTCREATEFONTINDIRECTW', 'EXT create font indirect W', None), 83: ('EXTTEXTOUTA', 'EXT text out A', None), 84: ('EXTTEXTOUTW', 'EXT text out W', None), 85: ('POLYBEZIER16', 'Draw poly bezier (16-bit)', None), 86: ('POLYGON16', 'Draw polygon (16-bit)', parsePoint16array), 87: ('POLYLINE16', 'Draw polyline (16-bit)', parsePoint16array), 88: ('POLYBEZIERTO16', 'Draw poly bezier to (16-bit)', parsePoint16array), 89: ('POLYLINETO16', 'Draw polyline to (16-bit)', parsePoint16array), 90: ('POLYPOLYLINE16', 'Draw poly polyline (16-bit)', None), 91: ('POLYPOLYGON16', 'Draw poly polygon (16-bit)', parsePoint16array), 92: ('POLYDRAW16', 'Draw poly draw (16-bit)', None), 93: ('CREATEMONOBRUSH', 'Create monobrush', None), 94: ('CREATEDIBPATTERNBRUSHPT', 'Create DIB pattern brush PT', None), 95: ('EXTCREATEPEN', 'EXT create pen', parseExtCreatePen), 96: ('POLYTEXTOUTA', 'Poly text out A', None), 97: ('POLYTEXTOUTW', 'Poly text out W', None), 98: ('SETICMMODE', 'Set ICM mode', parseICMMode), 99: ('CREATECOLORSPACE', 'Create color space', None), 100: ('SETCOLORSPACE', 'Set color space', None), 101: ('DELETECOLORSPACE', 'Delete color space', None), 102: ('GLSRECORD', 'GLS record', None), 103: ('GLSBOUNDEDRECORD', 'GLS bound ED record', None), 104: ('PIXELFORMAT', 'Pixel format', None)}
EMF_META_NAME = createDict(EMF_META, 0)
EMF_META_DESC = createDict(EMF_META, 1)

class Function(FieldSet):
    __module__ = __name__

    def __init__(self, *args):
        FieldSet.__init__(self, *args)
        if self.root.isEMF():
            self._size = self['size'].value * 8
        else:
            self._size = self['size'].value * 16

    def createFields(self):
        if self.root.isEMF():
            yield Enum(UInt32(self, 'function'), EMF_META_NAME)
            yield UInt32(self, 'size')
            try:
                parser = EMF_META[self['function'].value][2]
            except KeyError:
                parser = None

        else:
            yield UInt32(self, 'size')
            yield Enum(UInt16(self, 'function'), META_NAME)
            try:
                parser = META[self['function'].value][2]
            except KeyError:
                parser = None

            if parser:
                for field in parser(self):
                    yield field

            else:
                size = (self.size - self.current_size) // 8
                if size:
                    yield RawBytes(self, 'data', size)
        return

    def isValid(self):
        func = self['function']
        return func.value in func.getEnum()

    def createDescription(self):
        if self.root.isEMF():
            return EMF_META_DESC[self['function'].value]
        try:
            return META_DESC[self['function'].value]
        except KeyError:
            return 'Function %s' % self['function'].display


class RECT16(StaticFieldSet):
    __module__ = __name__
    format = ((Int16, 'left'), (Int16, 'top'), (Int16, 'right'), (Int16, 'bottom'))

    def createDescription(self):
        return '%s: %ux%u at (%u,%u)' % (self.__class__.__name__, self['right'].value - self['left'].value, self['bottom'].value - self['top'].value, self['left'].value, self['top'].value)


class RECT32(RECT16):
    __module__ = __name__
    format = ((Int32, 'left'), (Int32, 'top'), (Int32, 'right'), (Int32, 'bottom'))


class PlaceableHeader(FieldSet):
    """
    Header of Placeable Metafile (file extension .APM),
    created by Aldus Corporation
    """
    __module__ = __name__
    MAGIC = b'\xd7\xcd\xc6\x9a\x00\x00'

    def createFields(self):
        yield textHandler(UInt32(self, 'signature', 'Placeable Metafiles signature (0x9AC6CDD7)'), hexadecimal)
        yield UInt16(self, 'handle')
        yield RECT16(self, 'rect')
        yield UInt16(self, 'inch')
        yield NullBytes(self, 'reserved', 4)
        yield textHandler(UInt16(self, 'checksum'), hexadecimal)


class EMF_Header(FieldSet):
    __module__ = __name__
    MAGIC = ' EMF\x00\x00'

    def __init__(self, *args):
        FieldSet.__init__(self, *args)
        self._size = self['size'].value * 8

    def createFields(self):
        LONG = Int32
        yield UInt32(self, 'type', 'Record type (always 1)')
        yield UInt32(self, 'size', 'Size of the header in bytes')
        yield RECT32(self, 'Bounds', 'Inclusive bounds')
        yield RECT32(self, 'Frame', 'Inclusive picture frame')
        yield textHandler(UInt32(self, 'signature', 'Signature ID (always 0x464D4520)'), hexadecimal)
        yield UInt16(self, 'min_ver', 'Minor version')
        yield UInt16(self, 'maj_ver', 'Major version')
        yield UInt32(self, 'file_size', 'Size of the file in bytes')
        yield UInt32(self, 'NumOfRecords', 'Number of records in the metafile')
        yield UInt16(self, 'NumOfHandles', 'Number of handles in the handle table')
        yield NullBytes(self, 'reserved', 2)
        yield UInt32(self, 'desc_size', 'Size of description in 16-bit words')
        yield UInt32(self, 'desc_ofst', 'Offset of description string in metafile')
        yield UInt32(self, 'nb_colors', 'Number of color palette entries')
        yield LONG(self, 'width_px', 'Width of reference device in pixels')
        yield LONG(self, 'height_px', 'Height of reference device in pixels')
        yield LONG(self, 'width_mm', 'Width of reference device in millimeters')
        yield LONG(self, 'height_mm', 'Height of reference device in millimeters')
        offset = self['desc_ofst'].value
        current = (self.absolute_address + self.current_size) // 8
        size = self['desc_size'].value * 2
        if offset == current and size:
            yield String(self, 'description', size, charset='UTF-16-LE', strip='\x00 ')
        size = self['size'].value - self.current_size // 8
        if size:
            yield RawBytes(self, 'padding', size)


class WMF_File(Parser):
    __module__ = __name__
    PARSER_TAGS = {'id': 'wmf', 'category': 'image', 'file_ext': ('wmf', 'apm', 'emf'), 'mime': ('image/wmf', 'image/x-wmf', 'image/x-win-metafile', 'application/x-msmetafile', 'application/wmf',
 'application/x-wmf', 'image/x-emf'), 'magic': ((PlaceableHeader.MAGIC, 0), (EMF_Header.MAGIC, 40 * 8), ('\x00\x00\t\x00\x00\x03', 0), ('\x01\x00\t\x00\x00\x03', 0)), 'min_size': 40 * 8, 'description': 'Microsoft Windows Metafile (WMF)'}
    endian = LITTLE_ENDIAN
    FILE_TYPE = {0: 'memory', 1: 'disk'}

    def validate(self):
        if self.isEMF():
            emf = self['emf_header']
            if emf['signature'].value != 1179469088:
                return 'Invalid signature'
            if emf['type'].value != 1:
                return 'Invalid record type'
            if emf['reserved'].value != '\x00\x00':
                return 'Invalid reserved'
        else:
            if self.isAPM():
                amf = self['amf_header']
                if amf['handle'].value != 0:
                    return 'Invalid handle'
                if amf['reserved'].value != '\x00\x00\x00\x00':
                    return 'Invalid reserved'
            if self['file_type'].value not in (0, 1):
                return 'Invalid file type'
            if self['header_size'].value != 9:
                return 'Invalid header size'
            if self['nb_params'].value != 0:
                return 'Invalid number of parameters'
        for index in xrange(5):
            try:
                func = self[('func[%u]' % index)]
            except MissingField:
                if self.done:
                    return True
                return 'Unable to get function #%u' % index
            except ParserError:
                return 'Unable to create function #%u' % index

            if not func.isValid():
                return 'Function #%u is invalid' % index

        return True

    def createFields(self):
        if self.isEMF():
            yield EMF_Header(self, 'emf_header')
        else:
            if self.isAPM():
                yield PlaceableHeader(self, 'amf_header')
            yield Enum(UInt16(self, 'file_type'), self.FILE_TYPE)
            yield UInt16(self, 'header_size', 'Size of header in 16-bit words (always 9)')
            yield UInt8(self, 'win_ver_min', 'Minor version of Microsoft Windows')
            yield UInt8(self, 'win_ver_maj', 'Major version of Microsoft Windows')
            yield UInt32(self, 'file_size', 'Total size of the metafile in 16-bit words')
            yield UInt16(self, 'nb_obj', 'Number of objects in the file')
            yield UInt32(self, 'max_record_size', 'The size of largest record in 16-bit words')
            yield UInt16(self, 'nb_params', 'Not Used (always 0)')
        while not self.eof:
            yield Function(self, 'func[]')

    def isEMF(self):
        """File is in EMF format?"""
        if 1 <= self.current_length:
            return self[0].name == 'emf_header'
        if self.size < 44 * 8:
            return False
        magic = EMF_Header.MAGIC
        return self.stream.readBytes(40 * 8, len(magic)) == magic

    def isAPM(self):
        """File is in Aldus Placeable Metafiles format?"""
        if 1 <= self.current_length:
            return self[0].name == 'amf_header'
        else:
            magic = PlaceableHeader.MAGIC
            return self.stream.readBytes(0, len(magic)) == magic

    def createDescription(self):
        if self.isEMF():
            return 'Microsoft Enhanced Metafile (EMF) picture'
        elif self.isAPM():
            return 'Aldus Placeable Metafile (APM) picture'
        else:
            return 'Microsoft Windows Metafile (WMF) picture'

    def createMimeType(self):
        if self.isEMF():
            return 'image/x-emf'
        else:
            return 'image/wmf'

    def createContentSize(self):
        if self.isEMF():
            return
        start = self['func[0]'].absolute_address
        end = self.stream.searchBytes('\x03\x00\x00\x00\x00\x00', start, MAX_FILESIZE * 8)
        if end is not None:
            return end + 6 * 8
        return