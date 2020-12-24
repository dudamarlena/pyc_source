# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/hachoir_parser/image/photoshop_metadata.py
# Compiled at: 2009-09-07 17:44:28
from hachoir_core.field import FieldSet, ParserError, UInt8, UInt16, UInt32, String, CString, PascalString8, NullBytes, RawBytes
from hachoir_core.text_handler import textHandler, hexadecimal
from hachoir_core.tools import alignValue, createDict
from hachoir_parser.image.iptc import IPTC
from hachoir_parser.common.win32 import PascalStringWin32

class Version(FieldSet):
    __module__ = __name__

    def createFields(self):
        yield UInt32(self, 'version')
        yield UInt8(self, 'has_realm')
        yield PascalStringWin32(self, 'writer_name', charset='UTF-16-BE')
        yield PascalStringWin32(self, 'reader_name', charset='UTF-16-BE')
        yield UInt32(self, 'file_version')
        size = (self.size - self.current_size) // 8
        if size:
            yield NullBytes(self, 'padding', size)


class Photoshop8BIM(FieldSet):
    __module__ = __name__
    TAG_INFO = {1005: ('res_info', None, 'Resolution information'), 1011: ('print_flag', None, 'Print flags: labels, crop marks, colour bars, etc.'), 1013: ('col_half_info', None, 'Colour half-toning information'), 1016: ('color_trans_func', None, 'Colour transfer function'), 1028: ('iptc', IPTC, 'IPTC/NAA'), 1030: ('jpeg_qual', None, 'JPEG quality'), 1032: ('grid_guide', None, 'Grid guides informations'), 1034: ('copyright_flag', None, 'Copyright flag'), 1036: ('thumb_res2', None, 'Thumbnail resource (2)'), 1037: ('glob_angle', None, 'Global lighting angle for effects'), 1041: ('icc_tagged', None, 'ICC untagged (1 means intentionally untagged)'), 1044: ('base_layer_id', None, "Base value for new layers ID's"), 1049: ('glob_altitude', None, 'Global altitude'), 1050: ('slices', None, 'Slices'), 1054: ('url_list', None, "Unicode URL's"), 1057: ('version', Version, 'Version information'), 10000: ('print_flag2', None, 'Print flags (2)')}
    TAG_NAME = createDict(TAG_INFO, 0)
    CONTENT_HANDLER = createDict(TAG_INFO, 1)
    TAG_DESC = createDict(TAG_INFO, 2)

    def __init__(self, *args, **kw):
        FieldSet.__init__(self, *args, **kw)
        try:
            (self._name, self.handler, self._description) = self.TAG_INFO[self['tag'].value]
        except KeyError:
            self.handler = None

        size = self['size']
        self._size = size.address + size.size + alignValue(size.value, 2) * 8
        return

    def createFields(self):
        yield String(self, 'signature', 4, '8BIM signature', charset='ASCII')
        if self['signature'].value != '8BIM':
            raise ParserError("Stream doesn't look like 8BIM item (wrong signature)!")
        yield textHandler(UInt16(self, 'tag'), hexadecimal)
        if self.stream.readBytes(self.absolute_address + self.current_size, 4) != '\x00\x00\x00\x00':
            yield PascalString8(self, 'name')
            size = 2 + self['name'].size // 8 % 2
            yield NullBytes(self, 'name_padding', size)
        else:
            yield String(self, 'name', 4, strip='\x00')
        yield UInt16(self, 'size')
        size = alignValue(self['size'].value, 2)
        if not size:
            return
        if self.handler:
            yield self.handler(self, 'content', size=size * 8)
        else:
            yield RawBytes(self, 'content', size)


class PhotoshopMetadata(FieldSet):
    __module__ = __name__

    def createFields(self):
        yield CString(self, 'signature', 'Photoshop version')
        if self['signature'].value == 'Photoshop 3.0':
            while not self.eof:
                yield Photoshop8BIM(self, 'item[]')

        else:
            size = (self._size - self.current_size) / 8
            yield RawBytes(self, 'rawdata', size)