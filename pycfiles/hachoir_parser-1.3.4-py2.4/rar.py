# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/hachoir_parser/archive/rar.py
# Compiled at: 2010-01-20 17:58:43
"""
RAR parser

Status: can only read higher-level attructures
Author: Christophe Gisquet
"""
from hachoir_parser import Parser
from hachoir_core.field import StaticFieldSet, FieldSet, Bit, Bits, Enum, UInt8, UInt16, UInt32, UInt64, String, TimeDateMSDOS32, NullBytes, NullBits, RawBytes
from hachoir_core.text_handler import textHandler, filesizeHandler, hexadecimal
from hachoir_core.endian import LITTLE_ENDIAN
from hachoir_parser.common.msdos import MSDOSFileAttr32
MAX_FILESIZE = 1000 * 1024 * 1024
BLOCK_NAME = {114: 'Marker', 115: 'Archive', 116: 'File', 117: 'Comment', 118: 'Extra info', 119: 'Subblock', 120: 'Recovery record', 121: 'Archive authenticity', 122: 'New-format subblock', 123: 'Archive end'}
COMPRESSION_NAME = {48: 'Storing', 49: 'Fastest compression', 50: 'Fast compression', 51: 'Normal compression', 52: 'Good compression', 53: 'Best compression'}
OS_MSDOS = 0
OS_WIN32 = 2
OS_NAME = {0: 'MS DOS', 1: 'OS/2', 2: 'Win32', 3: 'Unix'}
DICTIONARY_SIZE = {0: 'Dictionary size 64 Kb', 1: 'Dictionary size 128 Kb', 2: 'Dictionary size 256 Kb', 3: 'Dictionary size 512 Kb', 4: 'Dictionary size 1024 Kb', 7: 'File is a directory'}

def formatRARVersion(field):
    """
    Decodes the RAR version stored on 1 byte
    """
    return '%u.%u' % divmod(field.value, 10)


def commonFlags(s):
    yield Bit(s, 'has_added_size', 'Additional field indicating additional size')
    yield Bit(s, 'is_ignorable', 'Old versions of RAR should ignore this block when copying data')


class ArchiveFlags(StaticFieldSet):
    __module__ = __name__
    format = ((Bit, 'vol', 'Archive volume'), (Bit, 'has_comment', 'Whether there is a comment'), (Bit, 'is_locked', 'Archive volume'), (Bit, 'is_solid', 'Whether files can be extracted separately'), (Bit, 'new_numbering', 'New numbering, or compressed comment'), (Bit, 'has_authenticity_information', 'The integrity/authenticity of the archive can be checked'), (Bit, 'is_protected', 'The integrity/authenticity of the archive can be checked'), (Bit, 'is_passworded', 'Needs a password to be decrypted'), (Bit, 'is_first_vol', 'Whether it is the first volume'), (Bit, 'is_encrypted', 'Whether the encryption version is present'), (NullBits, 'internal', 6, "Reserved for 'internal use'"))


def archiveFlags(s):
    yield ArchiveFlags(s, 'flags', 'Archiver block flags')


def archiveHeader(s):
    yield NullBytes(s, 'reserved[]', 2, 'Reserved word')
    yield NullBytes(s, 'reserved[]', 4, 'Reserved dword')


def commentHeader(s):
    yield filesizeHandler(UInt16(s, 'total_size', 'Comment header size + comment size'))
    yield filesizeHandler(UInt16(s, 'uncompressed_size', 'Uncompressed comment size'))
    yield UInt8(s, 'required_version', 'RAR version needed to extract comment')
    yield UInt8(s, 'packing_method', 'Comment packing method')
    yield UInt16(s, 'comment_crc16', 'Comment CRC')


def commentBody(s):
    size = s['total_size'].value - s.current_size
    if size > 0:
        yield RawBytes(s, 'comment_data', size, 'Compressed comment data')


def signatureHeader(s):
    yield TimeDateMSDOS32(s, 'creation_time')
    yield filesizeHandler(UInt16(s, 'arc_name_size'))
    yield filesizeHandler(UInt16(s, 'user_name_size'))


def recoveryHeader(s):
    yield filesizeHandler(UInt32(s, 'total_size'))
    yield textHandler(UInt8(s, 'version'), hexadecimal)
    yield UInt16(s, 'rec_sectors')
    yield UInt32(s, 'total_blocks')
    yield RawBytes(s, 'mark', 8)


def avInfoHeader(s):
    yield filesizeHandler(UInt16(s, 'total_size', 'Total block size'))
    yield UInt8(s, 'version', 'Version needed to decompress', handler=hexadecimal)
    yield UInt8(s, 'method', 'Compression method', handler=hexadecimal)
    yield UInt8(s, 'av_version', 'Version for AV', handler=hexadecimal)
    yield UInt32(s, 'av_crc', 'AV info CRC32', handler=hexadecimal)


def avInfoBody(s):
    size = s['total_size'].value - s.current_size
    if size > 0:
        yield RawBytes(s, 'av_info_data', size, 'AV info')


class FileFlags(FieldSet):
    __module__ = __name__
    static_size = 16

    def createFields(self):
        yield Bit(self, 'continued_from', 'File continued from previous volume')
        yield Bit(self, 'continued_in', 'File continued in next volume')
        yield Bit(self, 'is_encrypted', 'File encrypted with password')
        yield Bit(self, 'has_comment', 'File comment present')
        yield Bit(self, 'is_solid', 'Information from previous files is used (solid flag)')
        yield Enum(Bits(self, 'dictionary_size', 3, 'Dictionary size'), DICTIONARY_SIZE)
        for bit in commonFlags(self):
            yield bit

        yield Bit(self, 'is_large', 'file64 operations needed')
        yield Bit(self, 'is_unicode', 'Filename also encoded using Unicode')
        yield Bit(self, 'has_salt', 'Has salt for encryption')
        yield Bit(self, 'uses_file_version', 'File versioning is used')
        yield Bit(self, 'has_ext_time', 'Extra time ??')
        yield Bit(self, 'has_ext_flags', 'Extra flag ??')


def fileFlags(s):
    yield FileFlags(s, 'flags', 'File block flags')


class ExtTime(FieldSet):
    __module__ = __name__

    def createFields(self):
        yield textHandler(UInt16(self, 'time_flags', 'Flags for extended time'), hexadecimal)
        flags = self['time_flags'].value
        for index in xrange(4):
            rmode = flags >> (3 - index) * 4
            if rmode & 8:
                if index:
                    yield TimeDateMSDOS32(self, 'dos_time[]', 'DOS Time')
                if rmode & 3:
                    yield RawBytes(self, 'remainder[]', rmode & 3, 'Time remainder')


def specialHeader(s, is_file):
    yield filesizeHandler(UInt32(s, 'compressed_size', 'Compressed size (bytes)'))
    yield filesizeHandler(UInt32(s, 'uncompressed_size', 'Uncompressed size (bytes)'))
    yield Enum(UInt8(s, 'host_os', 'Operating system used for archiving'), OS_NAME)
    yield textHandler(UInt32(s, 'crc32', 'File CRC32'), hexadecimal)
    yield TimeDateMSDOS32(s, 'ftime', 'Date and time (MS DOS format)')
    yield textHandler(UInt8(s, 'version', 'RAR version needed to extract file'), formatRARVersion)
    yield Enum(UInt8(s, 'method', 'Packing method'), COMPRESSION_NAME)
    yield filesizeHandler(UInt16(s, 'filename_length', 'File name size'))
    if s['host_os'].value in (OS_MSDOS, OS_WIN32):
        yield MSDOSFileAttr32(s, 'file_attr', 'File attributes')
    else:
        yield textHandler(UInt32(s, 'file_attr', 'File attributes'), hexadecimal)
    if s['flags/is_large'].value:
        yield filesizeHandler(UInt64(s, 'large_size', 'Extended 64bits filesize'))
    size = s['filename_length'].value
    if size > 0:
        if s['flags/is_unicode'].value:
            charset = 'UTF-8'
        else:
            charset = 'ISO-8859-15'
        yield String(s, 'filename', size, 'Filename', charset=charset)
    if is_file:
        if s['flags/has_salt'].value:
            yield textHandler(UInt8(s, 'salt', 'Salt'), hexadecimal)
        if s['flags/has_ext_time'].value:
            yield ExtTime(s, 'extra_time', 'Extra time info')


def fileHeader(s):
    return specialHeader(s, True)


def fileBody(s):
    size = s['compressed_size'].value
    if s['flags/is_large'].value:
        size += s['large_size'].value
    if size > 0:
        yield RawBytes(s, 'compressed_data', size, 'File compressed data')


def fileDescription(s):
    return 'File entry: %s (%s)' % (s['filename'].display, s['compressed_size'].display)


def newSubHeader(s):
    return specialHeader(s, False)


class EndFlags(StaticFieldSet):
    __module__ = __name__
    format = ((Bit, 'has_next_vol', 'Whether there is another next volume'), (Bit, 'has_data_crc', 'Whether a CRC value is present'), (Bit, 'rev_space'), (Bit, 'has_vol_number', 'Whether the volume number is present'), (Bits, 'unused[]', 4), (Bit, 'has_added_size', 'Additional field indicating additional size'), (Bit, 'is_ignorable', 'Old versions of RAR should ignore this block when copying data'), (Bits, 'unused[]', 6))


def endFlags(s):
    yield EndFlags(s, 'flags', 'End block flags')


class BlockFlags(FieldSet):
    __module__ = __name__
    static_size = 16

    def createFields(self):
        yield textHandler(Bits(self, 'unused[]', 8, 'Unused flag bits'), hexadecimal)
        yield Bit(self, 'has_added_size', 'Additional field indicating additional size')
        yield Bit(self, 'is_ignorable', 'Old versions of RAR should ignore this block when copying data')
        yield Bits(self, 'unused[]', 6)


class Block(FieldSet):
    __module__ = __name__
    BLOCK_INFO = {114: ('marker', 'Archive header', None, None, None), 115: ('archive_start', 'Archive info', archiveFlags, archiveHeader, None), 116: ('file[]', fileDescription, fileFlags, fileHeader, fileBody), 117: ('comment[]', 'Stray comment', None, commentHeader, commentBody), 118: ('av_info[]', 'Extra information', None, avInfoHeader, avInfoBody), 119: ('sub_block[]', 'Stray subblock', None, newSubHeader, fileBody), 120: ('recovery[]', 'Recovery block', None, recoveryHeader, None), 121: ('signature', 'Signature block', None, signatureHeader, None), 122: ('new_sub_block[]', 'Stray new-format subblock', fileFlags, newSubHeader, fileBody), 123: ('archive_end', 'Archive end block', endFlags, None, None)}

    def __init__(self, parent, name):
        FieldSet.__init__(self, parent, name)
        t = self['block_type'].value
        if t in self.BLOCK_INFO:
            (self._name, desc, parseFlags, parseHeader, parseBody) = self.BLOCK_INFO[t]
            if callable(desc):
                self.createDescription = lambda : desc(self)
            elif desc:
                self._description = desc
            if parseFlags:
                self.parseFlags = lambda : parseFlags(self)
            if parseHeader:
                self.parseHeader = lambda : parseHeader(self)
            if parseBody:
                self.parseBody = lambda : parseBody(self)
        else:
            self.info('Processing as unknown block block of type %u' % type)
        self._size = 8 * self['block_size'].value
        if t == 116 or t == 122:
            self._size += 8 * self['compressed_size'].value
            if 'is_large' in self['flags'] and self['flags/is_large'].value:
                self._size += 8 * self['large_size'].value
        elif 'has_added_size' in self:
            self._size += 8 * self['added_size'].value

    def createFields(self):
        yield textHandler(UInt16(self, 'crc16', 'Block CRC16'), hexadecimal)
        yield textHandler(UInt8(self, 'block_type', 'Block type'), hexadecimal)
        for field in self.parseFlags():
            yield field

        yield filesizeHandler(UInt16(self, 'block_size', 'Block size'))
        for field in self.parseHeader():
            yield field

        size = self['block_size'].value - self.current_size // 8
        if size > 0:
            yield RawBytes(self, 'unknown', size, 'Unknow data (UInt32 probably)')
        for field in self.parseBody():
            yield field

    def createDescription(self):
        return 'Block entry: %s' % self['type'].display

    def parseFlags(self):
        yield BlockFlags(self, 'flags', 'Block header flags')

    def parseHeader(self):
        if 'has_added_size' in self['flags'] and self['flags/has_added_size'].value:
            yield filesizeHandler(UInt32(self, 'added_size', 'Supplementary block size'))

    def parseBody(self):
        """
        Parse what is left of the block
        """
        size = self['block_size'].value - self.current_size // 8
        if 'has_added_size' in self['flags'] and self['flags/has_added_size'].value:
            size += self['added_size'].value
        if size > 0:
            yield RawBytes(self, 'body', size, 'Body data')


class RarFile(Parser):
    __module__ = __name__
    MAGIC = 'Rar!\x1a\x07\x00'
    PARSER_TAGS = {'id': 'rar', 'category': 'archive', 'file_ext': ('rar', ), 'mime': ('application/x-rar-compressed', ), 'min_size': 7 * 8, 'magic': ((MAGIC, 0),), 'description': 'Roshal archive (RAR)'}
    endian = LITTLE_ENDIAN

    def validate(self):
        magic = self.MAGIC
        if self.stream.readBytes(0, len(magic)) != magic:
            return 'Invalid magic'
        return True

    def createFields(self):
        while not self.eof:
            yield Block(self, 'block[]')

    def createContentSize(self):
        start = 0
        end = MAX_FILESIZE * 8
        pos = self.stream.searchBytes(b'\xc4={\x00@\x07\x00', start, end)
        if pos is not None:
            return pos + 7 * 8
        return