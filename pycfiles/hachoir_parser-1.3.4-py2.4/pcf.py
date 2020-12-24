# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/hachoir_parser/misc/pcf.py
# Compiled at: 2009-09-07 17:44:28
"""
X11 Portable Compiled Font (pcf) parser.

Documents:
- Format for X11 pcf bitmap font files
  http://fontforge.sourceforge.net/pcf-format.html
  (file is based on the X11 sources)

Author: Victor Stinner
Creation date: 2007-03-20
"""
from hachoir_parser import Parser
from hachoir_core.field import FieldSet, Enum, UInt8, UInt32, Bytes, RawBytes, NullBytes, Bit, Bits, PaddingBits, CString
from hachoir_core.endian import LITTLE_ENDIAN, BIG_ENDIAN
from hachoir_core.text_handler import textHandler, hexadecimal, filesizeHandler
from hachoir_core.tools import paddingSize

class TOC(FieldSet):
    __module__ = __name__
    TYPE_NAME = {1: 'Properties', 2: 'Accelerators', 4: 'Metrics', 8: 'Bitmaps', 16: 'Ink metrics', 32: 'BDF encodings', 64: 'SWidths', 128: 'Glyph names', 256: 'BDF accelerators'}
    FORMAT_NAME = {0: 'Default', 512: 'Ink bounds', 256: 'Accelerator W ink bounds'}

    def createFields(self):
        yield Enum(UInt32(self, 'type'), self.TYPE_NAME)
        yield UInt32(self, 'format')
        yield filesizeHandler(UInt32(self, 'size'))
        yield UInt32(self, 'offset')

    def createDescription(self):
        return '%s at %s (%s)' % (self['type'].display, self['offset'].value, self['size'].display)


class PropertiesFormat(FieldSet):
    __module__ = __name__
    static_size = 32
    endian = LITTLE_ENDIAN

    def createFields(self):
        yield Bits(self, 'reserved[]', 2)
        yield Bit(self, 'byte_big_endian')
        yield Bit(self, 'bit_big_endian')
        yield Bits(self, 'scan_unit', 2)
        yield textHandler(PaddingBits(self, 'reserved[]', 26), hexadecimal)


class Property(FieldSet):
    __module__ = __name__

    def createFields(self):
        yield UInt32(self, 'name_offset')
        yield UInt8(self, 'is_string')
        yield UInt32(self, 'value_offset')

    def createDescription(self):
        name = self[('../name[%s]' % (self.index - 2))].value
        return 'Property %s' % name


class GlyphNames(FieldSet):
    __module__ = __name__

    def __init__(self, parent, name, toc, description, size=None):
        FieldSet.__init__(self, parent, name, description, size=size)
        self.toc = toc
        if self['format/byte_big_endian'].value:
            self.endian = BIG_ENDIAN
        else:
            self.endian = LITTLE_ENDIAN

    def createFields(self):
        yield PropertiesFormat(self, 'format')
        yield UInt32(self, 'count')
        offsets = []
        for index in xrange(self['count'].value):
            offset = UInt32(self, 'offset[]')
            yield offset
            offsets.append(offset.value)

        yield UInt32(self, 'total_str_length')
        offsets.sort()
        offset0 = self.current_size // 8
        for offset in offsets:
            padding = self.seekByte(offset0 + offset)
            if padding:
                yield padding
            yield CString(self, 'name[]')

        padding = (self.size - self.current_size) // 8
        if padding:
            yield NullBytes(self, 'end_padding', padding)


class Properties(GlyphNames):
    __module__ = __name__

    def createFields(self):
        yield PropertiesFormat(self, 'format')
        yield UInt32(self, 'nb_prop')
        properties = []
        for index in xrange(self['nb_prop'].value):
            property = Property(self, 'property[]')
            yield property
            properties.append(property)

        padding = paddingSize(self.current_size // 8, 4)
        if padding:
            yield NullBytes(self, 'padding', padding)
        yield UInt32(self, 'total_str_length')
        properties.sort(key=lambda entry: entry['name_offset'].value)
        offset0 = self.current_size // 8
        for property in properties:
            padding = self.seekByte(offset0 + property['name_offset'].value)
            if padding:
                yield padding
            yield CString(self, 'name[]', 'Name of %s' % property.name)
            if property['is_string'].value:
                yield CString(self, 'value[]', 'Value of %s' % property.name)

        padding = (self.size - self.current_size) // 8
        if padding:
            yield NullBytes(self, 'end_padding', padding)


class PcfFile(Parser):
    __module__ = __name__
    MAGIC = '\x01fcp'
    PARSER_TAGS = {'id': 'pcf', 'category': 'misc', 'file_ext': ('pcf', ), 'magic': ((MAGIC, 0),), 'min_size': 32, 'description': 'X11 Portable Compiled Font (pcf)'}
    endian = LITTLE_ENDIAN

    def validate(self):
        if self['signature'].value != self.MAGIC:
            return 'Invalid signature'
        return True

    def createFields(self):
        yield Bytes(self, 'signature', 4, 'File signature ("\\1pcf")')
        yield UInt32(self, 'nb_toc')
        entries = []
        for index in xrange(self['nb_toc'].value):
            entry = TOC(self, 'toc[]')
            yield entry
            entries.append(entry)

        entries.sort(key=lambda entry: entry['offset'].value)
        for entry in entries:
            size = entry['size'].value
            padding = self.seekByte(entry['offset'].value)
            if padding:
                yield padding
            maxsize = (self.size - self.current_size) // 8
            if maxsize < size:
                self.warning('Truncate content of %s to %s bytes (was %s)' % (entry.path, maxsize, size))
                size = maxsize
            if not size:
                continue
            if entry['type'].value == 1:
                yield Properties(self, 'properties', entry, 'Properties', size=size * 8)
            elif entry['type'].value == 128:
                yield GlyphNames(self, 'glyph_names', entry, 'Glyph names', size=size * 8)
            else:
                yield RawBytes(self, 'data[]', size, 'Content of %s' % entry.path)