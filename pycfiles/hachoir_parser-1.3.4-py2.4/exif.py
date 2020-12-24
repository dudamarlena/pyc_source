# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/hachoir_parser/image/exif.py
# Compiled at: 2009-09-07 17:44:28
"""
EXIF metadata parser (can be found in a JPEG picture for example)

Author: Victor Stinner
"""
from hachoir_core.field import FieldSet, ParserError, UInt8, UInt16, UInt32, Int32, Enum, String, Bytes, SubFile, NullBytes, createPaddingField
from hachoir_core.endian import LITTLE_ENDIAN, BIG_ENDIAN, NETWORK_ENDIAN
from hachoir_core.text_handler import textHandler, hexadecimal
from hachoir_core.tools import createDict
MAX_COUNT = 1000

def rationalFactory(class_name, size, field_class):

    class Rational(FieldSet):
        __module__ = __name__
        static_size = size

        def createFields(self):
            yield field_class(self, 'numerator')
            yield field_class(self, 'denominator')

        def createValue(self):
            return float(self['numerator'].value) / self['denominator'].value

    cls = Rational
    cls.__name__ = class_name
    return cls


RationalInt32 = rationalFactory('RationalInt32', 64, Int32)
RationalUInt32 = rationalFactory('RationalUInt32', 64, UInt32)

class BasicIFDEntry(FieldSet):
    __module__ = __name__
    TYPE_BYTE = 0
    TYPE_UNDEFINED = 7
    TYPE_RATIONAL = 5
    TYPE_SIGNED_RATIONAL = 10
    TYPE_INFO = {1: (UInt8, 'BYTE (8 bits)'), 2: (String, 'ASCII (8 bits)'), 3: (UInt16, 'SHORT (16 bits)'), 4: (UInt32, 'LONG (32 bits)'), 5: (RationalUInt32, 'RATIONAL (2x LONG, 64 bits)'), 7: (Bytes, 'UNDEFINED (8 bits)'), 9: (Int32, 'SIGNED LONG (32 bits)'), 10: (RationalInt32, 'SRATIONAL (2x SIGNED LONGs, 64 bits)')}
    ENTRY_FORMAT = createDict(TYPE_INFO, 0)
    TYPE_NAME = createDict(TYPE_INFO, 1)

    def createFields(self):
        yield Enum(textHandler(UInt16(self, 'tag', 'Tag'), hexadecimal), self.TAG_NAME)
        yield Enum(textHandler(UInt16(self, 'type', 'Type'), hexadecimal), self.TYPE_NAME)
        yield UInt32(self, 'count', 'Count')
        if self['type'].value not in (self.TYPE_BYTE, self.TYPE_UNDEFINED):
            if MAX_COUNT < self['count'].value:
                raise ParserError('EXIF: Invalid count value (%s)' % self['count'].value)
            (value_size, array_size) = self.getSizes()
            yield value_size or NullBytes(self, 'padding', 4)
        elif value_size <= 32:
            if 1 < array_size:
                name = 'value[]'
            else:
                name = 'value'
            kw = {}
            cls = self.value_cls
            if cls is String:
                args = (
                 self, name, value_size / 8, 'Value')
                kw['strip'] = ' \x00'
                kw['charset'] = 'ISO-8859-1'
            elif cls is Bytes:
                args = (
                 self, name, value_size / 8, 'Value')
            else:
                args = (
                 self, name, 'Value')
            for index in xrange(array_size):
                yield cls(*args, **kw)

            size = array_size * value_size
            if size < 32:
                yield NullBytes(self, 'padding', (32 - size) // 8)
        else:
            yield UInt32(self, 'offset', 'Value offset')

    def getSizes(self):
        """
        Returns (value_size, array_size): value_size in bits and
        array_size in number of items.
        """
        self.value_cls = self.ENTRY_FORMAT.get(self['type'].value, Bytes)
        count = self['count'].value
        if self.value_cls in (String, Bytes):
            return (
             8 * count, 1)
        else:
            return (
             self.value_cls.static_size * count, count)


class ExifEntry(BasicIFDEntry):
    __module__ = __name__
    OFFSET_JPEG_SOI = 513
    EXIF_IFD_POINTER = 34665
    TAG_WIDTH = 40962
    TAG_HEIGHT = 40963
    TAG_GPS_LATITUDE_REF = 1
    TAG_GPS_LATITUDE = 2
    TAG_GPS_LONGITUDE_REF = 3
    TAG_GPS_LONGITUDE = 4
    TAG_GPS_ALTITUDE_REF = 5
    TAG_GPS_ALTITUDE = 6
    TAG_GPS_TIMESTAMP = 7
    TAG_GPS_DATESTAMP = 29
    TAG_IMG_TITLE = 270
    TAG_FILE_TIMESTAMP = 306
    TAG_SOFTWARE = 305
    TAG_CAMERA_MODEL = 272
    TAG_CAMERA_MANUFACTURER = 271
    TAG_ORIENTATION = 274
    TAG_EXPOSURE = 33434
    TAG_FOCAL = 33437
    TAG_BRIGHTNESS = 37379
    TAG_APERTURE = 37381
    TAG_USER_COMMENT = 37510
    TAG_NAME = {0: 'GPS version ID', 1: 'GPS latitude ref', 2: 'GPS latitude', 3: 'GPS longitude ref', 4: 'GPS longitude', 5: 'GPS altitude ref', 6: 'GPS altitude', 7: 'GPS timestamp', 8: 'GPS satellites', 9: 'GPS status', 10: 'GPS measure mode', 11: 'GPS DOP', 12: 'GPS speed ref', 13: 'GPS speed', 14: 'GPS track ref', 15: 'GPS track', 16: 'GPS img direction ref', 17: 'GPS img direction', 18: 'GPS map datum', 19: 'GPS dest latitude ref', 20: 'GPS dest latitude', 21: 'GPS dest longitude ref', 22: 'GPS dest longitude', 23: 'GPS dest bearing ref', 24: 'GPS dest bearing', 25: 'GPS dest distance ref', 26: 'GPS dest distance', 27: 'GPS processing method', 28: 'GPS area information', 29: 'GPS datestamp', 30: 'GPS differential', 256: 'Image width', 257: 'Image height', 258: 'Number of bits per component', 259: 'Compression scheme', 262: 'Pixel composition', TAG_ORIENTATION: 'Orientation of image', 277: 'Number of components', 284: 'Image data arrangement', 530: 'Subsampling ratio Y to C', 531: 'Y and C positioning', 282: 'Image resolution width direction', 283: 'Image resolution in height direction', 296: 'Unit of X and Y resolution', 273: 'Image data location', 278: 'Number of rows per strip', 279: 'Bytes per compressed strip', 513: 'Offset to JPEG SOI', 514: 'Bytes of JPEG data', 301: 'Transfer function', 318: 'White point chromaticity', 319: 'Chromaticities of primaries', 529: 'Color space transformation matrix coefficients', 532: 'Pair of blank and white reference values', TAG_FILE_TIMESTAMP: 'File change date and time', TAG_IMG_TITLE: 'Image title', TAG_CAMERA_MANUFACTURER: 'Camera (Image input equipment) manufacturer', TAG_CAMERA_MODEL: 'Camera (Input input equipment) model', TAG_SOFTWARE: 'Software', 315: 'File change date and time', 33432: 'Copyright holder', 34665: 'Exif IFD Pointer', TAG_EXPOSURE: 'Exposure time', TAG_FOCAL: 'F number', 34850: 'Exposure program', 34852: 'Spectral sensitivity', 34855: 'ISO speed rating', 34856: 'Optoelectric conversion factor OECF', 37377: 'Shutter speed', 37378: 'Aperture', TAG_BRIGHTNESS: 'Brightness', 37380: 'Exposure bias', TAG_APERTURE: 'Maximum lens aperture', 37382: 'Subject distance', 37383: 'Metering mode', 37384: 'Light source', 37385: 'Flash', 37386: 'Lens focal length', 37396: 'Subject area', 41483: 'Flash energy', 41484: 'Spatial frequency response', 41486: 'Focal plane X resolution', 41487: 'Focal plane Y resolution', 41488: 'Focal plane resolution unit', 41492: 'Subject location', 41493: 'Exposure index', 41495: 'Sensing method', 41728: 'File source', 41729: 'Scene type', 41730: 'CFA pattern', 41985: 'Custom image processing', 41986: 'Exposure mode', 41987: 'White balance', 41988: 'Digital zoom ratio', 41989: 'Focal length in 35 mm film', 41990: 'Scene capture type', 41991: 'Gain control', 41992: 'Contrast', 36864: 'Exif version', 40960: 'Supported Flashpix version', 40961: 'Color space information', 37121: 'Meaning of each component', 37122: 'Image compression mode', TAG_WIDTH: 'Valid image width', TAG_HEIGHT: 'Valid image height', 37500: 'Manufacturer notes', TAG_USER_COMMENT: 'User comments', 40964: 'Related audio file', 36867: 'Date and time of original data generation', 36868: 'Date and time of digital data generation', 37520: 'DateTime subseconds', 37521: 'DateTimeOriginal subseconds', 37522: 'DateTimeDigitized subseconds', 42016: 'Unique image ID', 40965: 'Interoperability IFD Pointer'}

    def createDescription(self):
        return 'Entry: %s' % self['tag'].display


def sortExifEntry(a, b):
    return int(a['offset'].value - b['offset'].value)


class ExifIFD(FieldSet):
    __module__ = __name__

    def seek(self, offset):
        """
        Seek to byte address relative to parent address.
        """
        padding = offset - (self.address + self.current_size) / 8
        if 0 < padding:
            return createPaddingField(self, padding * 8)
        else:
            return
        return

    def createFields(self):
        offset_diff = 6
        yield UInt16(self, 'count', 'Number of entries')
        entries = []
        next_chunk_offset = None
        count = self['count'].value
        if not count:
            return
        while count:
            addr = self.absolute_address + self.current_size
            next = self.stream.readBits(addr, 32, NETWORK_ENDIAN)
            if next in (0, 4026531840):
                break
            entry = ExifEntry(self, 'entry[]')
            yield entry
            if entry['tag'].value in (ExifEntry.EXIF_IFD_POINTER, ExifEntry.OFFSET_JPEG_SOI):
                next_chunk_offset = entry['value'].value + offset_diff
            if 32 < entry.getSizes()[0]:
                entries.append(entry)
            count -= 1

        yield UInt32(self, 'next', 'Next IFD offset')
        try:
            entries.sort(sortExifEntry)
        except TypeError:
            raise ParserError('Unable to sort entries!')

        value_index = 0
        for entry in entries:
            padding = self.seek(entry['offset'].value + offset_diff)
            if padding is not None:
                yield padding
            (value_size, array_size) = entry.getSizes()
            if not array_size:
                continue
            cls = entry.value_cls
            if 1 < array_size:
                name = 'value_%s[]' % entry.name
            else:
                name = 'value_%s' % entry.name
            desc = 'Value of "%s"' % entry['tag'].display
            if cls is String:
                for index in xrange(array_size):
                    yield cls(self, name, value_size / 8, desc, strip=' \x00', charset='ISO-8859-1')

            if cls is Bytes:
                for index in xrange(array_size):
                    yield cls(self, name, value_size / 8, desc)

            for index in xrange(array_size):
                yield cls(self, name, desc)

            value_index += 1

        if next_chunk_offset is not None:
            padding = self.seek(next_chunk_offset)
            if padding is not None:
                yield padding
        return

    def createDescription(self):
        return 'Exif IFD (id %s)' % self['id'].value


class Exif(FieldSet):
    __module__ = __name__

    def createFields(self):
        yield String(self, 'header', 6, 'Header (Exif\\0\\0)', charset='ASCII')
        if self['header'].value != 'Exif\x00\x00':
            raise ParserError('Invalid EXIF signature!')
        yield String(self, 'byte_order', 2, 'Byte order', charset='ASCII')
        if self['byte_order'].value not in ('II', 'MM'):
            raise ParserError('Invalid endian!')
        if self['byte_order'].value == 'II':
            self.endian = LITTLE_ENDIAN
        else:
            self.endian = BIG_ENDIAN
        yield UInt16(self, 'version', 'TIFF version number')
        yield UInt32(self, 'img_dir_ofs', 'Next image directory offset')
        while not self.eof:
            addr = self.absolute_address + self.current_size
            tag = self.stream.readBits(addr, 16, NETWORK_ENDIAN)
            if tag == 65496:
                size = (self._size - self.current_size) // 8
                yield SubFile(self, 'thumbnail', size, 'Thumbnail (JPEG file)', mime_type='image/jpeg')
                break
            elif tag == 65535:
                break
            yield ExifIFD(self, 'ifd[]', 'IFD')

        padding = self.seekBit(self._size)
        if padding is not None:
            yield padding
        return