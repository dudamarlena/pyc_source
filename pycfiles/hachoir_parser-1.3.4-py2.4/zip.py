# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/hachoir_parser/archive/zip.py
# Compiled at: 2010-01-20 17:59:00
"""
Zip splitter.

Status: can read most important headers
Authors: Christophe Gisquet and Victor Stinner
"""
from hachoir_parser import Parser
from hachoir_core.field import FieldSet, ParserError, Bit, Bits, Enum, TimeDateMSDOS32, SubFile, UInt8, UInt16, UInt32, UInt64, String, PascalString16, RawBytes
from hachoir_core.text_handler import textHandler, filesizeHandler, hexadecimal
from hachoir_core.error import HACHOIR_ERRORS
from hachoir_core.tools import makeUnicode
from hachoir_core.endian import LITTLE_ENDIAN
from hachoir_parser.common.deflate import Deflate
MAX_FILESIZE = 1000 * 1024 * 1024
COMPRESSION_DEFLATE = 8
COMPRESSION_METHOD = {0: 'no compression', 1: 'Shrunk', 2: 'Reduced (factor 1)', 3: 'Reduced (factor 2)', 4: 'Reduced (factor 3)', 5: 'Reduced (factor 4)', 6: 'Imploded', 7: 'Tokenizing', 8: 'Deflate', 9: 'Deflate64', 10: 'PKWARE Imploding', 11: 'Reserved by PKWARE', 12: 'File is compressed using BZIP2 algorithm', 13: 'Reserved by PKWARE', 14: 'LZMA (EFS)', 15: 'Reserved by PKWARE', 16: 'Reserved by PKWARE', 17: 'Reserved by PKWARE', 18: 'File is compressed using IBM TERSE (new)', 19: 'IBM LZ77 z Architecture (PFS)', 98: 'PPMd version I, Rev 1'}

def ZipRevision(field):
    return '%u.%u' % divmod(field.value, 10)


class ZipVersion(FieldSet):
    __module__ = __name__
    static_size = 16
    HOST_OS = {0: 'FAT file system (DOS, OS/2, NT)', 1: 'Amiga', 2: 'VMS (VAX or Alpha AXP)', 3: 'Unix', 4: 'VM/CMS', 5: 'Atari', 6: 'HPFS file system (OS/2, NT 3.x)', 7: 'Macintosh', 8: 'Z-System', 9: 'CP/M', 10: 'TOPS-20', 11: 'NTFS file system (NT)', 12: 'SMS/QDOS', 13: 'Acorn RISC OS', 14: 'VFAT file system (Win95, NT)', 15: 'MVS', 16: 'BeOS (BeBox or PowerMac)', 17: 'Tandem'}

    def createFields(self):
        yield textHandler(UInt8(self, 'zip_version', 'ZIP version'), ZipRevision)
        yield Enum(UInt8(self, 'host_os', 'ZIP Host OS'), self.HOST_OS)


class ZipGeneralFlags(FieldSet):
    __module__ = __name__
    static_size = 16

    def createFields(self):
        method = self.stream.readBits(self.absolute_address + 16, 16, LITTLE_ENDIAN)
        yield Bits(self, 'unused[]', 2, 'Unused')
        yield Bit(self, 'encrypted_central_dir', 'Selected data values in the Local Header are masked')
        yield Bit(self, 'incomplete', 'Reserved by PKWARE for enhanced compression.')
        yield Bit(self, 'uses_unicode', 'Filename and comments are in UTF-8')
        yield Bits(self, 'unused[]', 4, 'Unused')
        yield Bit(self, 'strong_encrypt', 'Strong encryption (version >= 50)')
        yield Bit(self, 'is_patched', 'File is compressed with patched data?')
        yield Bit(self, 'enhanced_deflate', 'Reserved for use with method 8')
        yield Bit(self, 'has_descriptor', 'Compressed data followed by descriptor?')
        if method == 6:
            yield Bit(self, 'use_8k_sliding', 'Use 8K sliding dictionary (instead of 4K)')
            yield Bit(self, 'use_3shannon', 'Use a 3 Shannon-Fano tree (instead of 2 Shannon-Fano)')
        elif method in (8, 9):
            NAME = {0: 'Normal compression', 1: 'Maximum compression', 2: 'Fast compression', 3: 'Super Fast compression'}
            yield Enum(Bits(self, 'method', 2), NAME)
        elif method == 14:
            yield Bit(self, 'lzma_eos', 'LZMA stream is ended with a EndOfStream marker')
            yield Bit(self, 'unused[]')
        else:
            yield Bits(self, 'compression_info', 2)
        yield Bit(self, 'is_encrypted', 'File is encrypted?')


class ExtraField(FieldSet):
    __module__ = __name__
    EXTRA_FIELD_ID = {7: 'AV Info', 9: 'OS/2 extended attributes (also Info-ZIP)', 10: 'PKWARE Win95/WinNT FileTimes', 12: 'PKWARE VAX/VMS (also Info-ZIP)', 13: 'PKWARE Unix', 15: 'Patch Descriptor', 1992: 'Info-ZIP Macintosh (old, J. Lee)', 9733: 'ZipIt Macintosh (first version)', 9989: 'ZipIt Macintosh v 1.3.5 and newer (w/o full filename)', 13133: 'Info-ZIP Macintosh (new, D. Haase Mac3 field)', 17217: 'Acorn/SparkFS (David Pilling)', 17491: 'Windows NT security descriptor (binary ACL)', 18180: 'VM/CMS', 18191: 'MVS', 19270: 'FWKCS MD5 (third party, see below)', 19521: 'OS/2 access control list (text ACL)', 19785: 'Info-ZIP VMS (VAX or Alpha)', 21334: 'AOS/VS (binary ACL)', 21589: 'extended timestamp', 22613: 'Info-ZIP Unix (original; also OS/2, NT, etc.)', 25922: 'BeOS (BeBox, PowerMac, etc.)', 30062: 'ASi Unix', 30805: 'Info-ZIP Unix (new)', 64330: 'SMS/QDOS'}

    def createFields(self):
        yield Enum(UInt16(self, 'field_id', 'Extra field ID'), self.EXTRA_FIELD_ID)
        size = UInt16(self, 'field_data_size', 'Extra field data size')
        yield size
        if size.value > 0:
            yield RawBytes(self, 'field_data', size, 'Unknown field data')


def ZipStartCommonFields(self):
    yield ZipVersion(self, 'version_needed', 'Version needed')
    yield ZipGeneralFlags(self, 'flags', 'General purpose flag')
    yield Enum(UInt16(self, 'compression', 'Compression method'), COMPRESSION_METHOD)
    yield TimeDateMSDOS32(self, 'last_mod', 'Last modification file time')
    yield textHandler(UInt32(self, 'crc32', 'CRC-32'), hexadecimal)
    yield UInt32(self, 'compressed_size', 'Compressed size')
    yield UInt32(self, 'uncompressed_size', 'Uncompressed size')
    yield UInt16(self, 'filename_length', 'Filename length')
    yield UInt16(self, 'extra_length', 'Extra fields length')


def zipGetCharset(self):
    if self['flags/uses_unicode'].value:
        return 'UTF-8'
    else:
        return 'ISO-8859-15'


class ZipCentralDirectory(FieldSet):
    __module__ = __name__
    HEADER = 33639248

    def createFields(self):
        yield ZipVersion(self, 'version_made_by', 'Version made by')
        for field in ZipStartCommonFields(self):
            yield field

        charset = zipGetCharset(self)
        yield UInt16(self, 'comment_length', 'Comment length')
        yield UInt16(self, 'disk_number_start', 'Disk number start')
        yield UInt16(self, 'internal_attr', 'Internal file attributes')
        yield UInt32(self, 'external_attr', 'External file attributes')
        yield UInt32(self, 'offset_header', 'Relative offset of local header')
        yield String(self, 'filename', self['filename_length'].value, 'Filename', charset=charset)
        if 0 < self['extra_length'].value:
            yield RawBytes(self, 'extra', self['extra_length'].value, 'Extra fields')
        if 0 < self['comment_length'].value:
            yield String(self, 'comment', self['comment_length'].value, 'Comment', charset=charset)

    def createDescription(self):
        return 'Central directory: %s' % self['filename'].display


class Zip64EndCentralDirectory(FieldSet):
    __module__ = __name__
    HEADER = 101075792

    def createFields(self):
        yield UInt64(self, 'zip64_end_size', 'Size of zip64 end of central directory record')
        yield ZipVersion(self, 'version_made_by', 'Version made by')
        yield ZipVersion(self, 'version_needed', 'Version needed to extract')
        yield UInt32(self, 'number_disk', 'Number of this disk')
        yield UInt32(self, 'number_disk2', 'Number of the disk with the start of the central directory')
        yield UInt64(self, 'number_entries', 'Total number of entries in the central directory on this disk')
        yield UInt64(self, 'number_entries2', 'Total number of entries in the central directory')
        yield UInt64(self, 'size', 'Size of the central directory')
        yield UInt64(self, 'offset', 'Offset of start of central directory')
        if 0 < self['zip64_end_size'].value:
            yield RawBytes(self, 'data_sector', self['zip64_end_size'].value, 'zip64 extensible data sector')


class ZipEndCentralDirectory(FieldSet):
    __module__ = __name__
    HEADER = 101010256

    def createFields(self):
        yield UInt16(self, 'number_disk', 'Number of this disk')
        yield UInt16(self, 'number_disk2', 'Number in the central dir')
        yield UInt16(self, 'total_number_disk', 'Total number of entries in this disk')
        yield UInt16(self, 'total_number_disk2', 'Total number of entries in the central dir')
        yield UInt32(self, 'size', 'Size of the central directory')
        yield UInt32(self, 'offset', 'Offset of start of central directory')
        yield PascalString16(self, 'comment', 'ZIP comment')


class ZipDataDescriptor(FieldSet):
    __module__ = __name__
    HEADER_STRING = 'PK\x07\x08'
    HEADER = 134695760
    static_size = 96

    def createFields(self):
        yield textHandler(UInt32(self, 'file_crc32', 'Checksum (CRC32)'), hexadecimal)
        yield filesizeHandler(UInt32(self, 'file_compressed_size', 'Compressed size (bytes)'))
        yield filesizeHandler(UInt32(self, 'file_uncompressed_size', 'Uncompressed size (bytes)'))


class FileEntry(FieldSet):
    __module__ = __name__
    HEADER = 67324752
    filename = None

    def data(self, size):
        compression = self['compression'].value
        if compression == 0:
            return SubFile(self, 'data', size, filename=self.filename)
        compressed = SubFile(self, 'compressed_data', size, filename=self.filename)
        if compression == COMPRESSION_DEFLATE:
            return Deflate(compressed)
        else:
            return compressed

    def resync(self):
        size = self.stream.searchBytesLength(ZipDataDescriptor.HEADER_STRING, False, self.absolute_address + self.current_size)
        if size <= 0:
            raise ParserError("Couldn't resync to %s" % ZipDataDescriptor.HEADER_STRING)
        yield self.data(size)
        yield textHandler(UInt32(self, 'header[]', 'Header'), hexadecimal)
        data_desc = ZipDataDescriptor(self, 'data_desc', 'Data descriptor')
        yield data_desc
        if self['crc32'].value == 0 and data_desc['file_compressed_size'].value != size:
            raise ParserError('Bad resync: position=>%i but data_desc=>%i' % (size, data_desc['file_compressed_size'].value))

    def createFields(self):
        for field in ZipStartCommonFields(self):
            yield field

        length = self['filename_length'].value
        if length:
            filename = String(self, 'filename', length, 'Filename', charset=zipGetCharset(self))
            yield filename
            self.filename = filename.value
        if self['extra_length'].value:
            yield RawBytes(self, 'extra', self['extra_length'].value, 'Extra')
        size = self['compressed_size'].value
        if size > 0:
            yield self.data(size)
        elif self['flags/incomplete'].value:
            for field in self.resync():
                yield field

        if self['flags/has_descriptor'].value:
            yield ZipDataDescriptor(self, 'data_desc', 'Data descriptor')

    def createDescription(self):
        return 'File entry: %s (%s)' % (self['filename'].value, self['compressed_size'].display)

    def validate(self):
        if self['compression'].value not in COMPRESSION_METHOD:
            return 'Unknown compression method (%u)' % self['compression'].value
        return ''


class ZipSignature(FieldSet):
    __module__ = __name__
    HEADER = 84233040

    def createFields(self):
        yield PascalString16(self, 'signature', 'Signature')


class Zip64EndCentralDirectoryLocator(FieldSet):
    __module__ = __name__
    HEADER = 117853008

    def createFields(self):
        yield UInt32(self, 'disk_number', 'Number of the disk with the start of the zip64 end of central directory')
        yield UInt64(self, 'relative_offset', 'Relative offset of the zip64 end of central directory record')
        yield UInt32(self, 'disk_total_number', 'Total number of disks')


class ZipFile(Parser):
    __module__ = __name__
    endian = LITTLE_ENDIAN
    MIME_TYPES = {'application/zip': 'zip', 'application/x-zip': 'zip', 'application/x-jar': 'jar', 'application/java-archive': 'jar', 'application/vnd.sun.xml.calc': 'sxc', 'application/vnd.sun.xml.draw': 'sxd', 'application/vnd.sun.xml.impress': 'sxi', 'application/vnd.sun.xml.writer': 'sxw', 'application/vnd.sun.xml.math': 'sxm', 'application/vnd.sun.xml.calc.template': 'stc', 'application/vnd.sun.xml.draw.template': 'std', 'application/vnd.sun.xml.impress.template': 'sti', 'application/vnd.sun.xml.writer.template': 'stw', 'application/vnd.sun.xml.writer.global': 'sxg', 'application/vnd.oasis.opendocument.chart': 'odc', 'application/vnd.oasis.opendocument.image': 'odi', 'application/vnd.oasis.opendocument.database': 'odb', 'application/vnd.oasis.opendocument.formula': 'odf', 'application/vnd.oasis.opendocument.graphics': 'odg', 'application/vnd.oasis.opendocument.presentation': 'odp', 'application/vnd.oasis.opendocument.spreadsheet': 'ods', 'application/vnd.oasis.opendocument.text': 'odt', 'application/vnd.oasis.opendocument.text-master': 'odm', 'application/vnd.oasis.opendocument.graphics-template': 'otg', 'application/vnd.oasis.opendocument.presentation-template': 'otp', 'application/vnd.oasis.opendocument.spreadsheet-template': 'ots', 'application/vnd.oasis.opendocument.text-template': 'ott'}
    PARSER_TAGS = {'id': 'zip', 'category': 'archive', 'file_ext': tuple(MIME_TYPES.itervalues()), 'mime': tuple(MIME_TYPES.iterkeys()), 'magic': (('PK\x03\x04', 0), ), 'subfile': 'skip', 'min_size': (4 + 26) * 8, 'description': 'ZIP archive'}

    def validate(self):
        if self['header[0]'].value != FileEntry.HEADER:
            return 'Invalid magic'
        try:
            file0 = self['file[0]']
        except HACHOIR_ERRORS, err:
            return 'Unable to get file #0'

        err = file0.validate()
        if err:
            return 'File #0: %s' % err
        return True

    def createFields(self):
        self.signature = None
        self.central_directory = []
        while not self.eof:
            header = textHandler(UInt32(self, 'header[]', 'Header'), hexadecimal)
            yield header
            header = header.value
            if header == FileEntry.HEADER:
                yield FileEntry(self, 'file[]')
            elif header == ZipDataDescriptor.HEADER:
                yield ZipDataDescriptor(self, 'spanning[]')
            elif header == 808471376:
                yield ZipDataDescriptor(self, 'temporary_spanning[]')
            elif header == ZipCentralDirectory.HEADER:
                yield ZipCentralDirectory(self, 'central_directory[]')
            elif header == ZipEndCentralDirectory.HEADER:
                yield ZipEndCentralDirectory(self, 'end_central_directory', 'End of central directory')
            elif header == Zip64EndCentralDirectory.HEADER:
                yield Zip64EndCentralDirectory(self, 'end64_central_directory', 'ZIP64 end of central directory')
            elif header == ZipSignature.HEADER:
                yield ZipSignature(self, 'signature', 'Signature')
            elif header == Zip64EndCentralDirectoryLocator.HEADER:
                yield Zip64EndCentralDirectoryLocator(self, 'end_locator', 'ZIP64 Enf of central directory locator')
            else:
                raise ParserError('Error, unknown ZIP header (0x%08X).' % header)

        return

    def createMimeType(self):
        if self['file[0]/filename'].value == 'mimetype':
            return makeUnicode(self['file[0]/data'].value)
        else:
            return 'application/zip'

    def createFilenameSuffix(self):
        if self['file[0]/filename'].value == 'mimetype':
            mime = self['file[0]/compressed_data'].value
            if mime in self.MIME_TYPES:
                return '.' + self.MIME_TYPES[mime]
        return '.zip'

    def createContentSize(self):
        start = 0
        end = MAX_FILESIZE * 8
        end = self.stream.searchBytes('PK\x05\x06', start, end)
        if end is not None:
            return end + 22 * 8
        return