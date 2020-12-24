# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/hachoir_parser/archive/tar.py
# Compiled at: 2009-09-07 17:44:28
"""
Tar archive parser.

Author: Victor Stinner
"""
from hachoir_parser import Parser
from hachoir_core.field import FieldSet, Enum, UInt8, SubFile, String, NullBytes
from hachoir_core.tools import humanFilesize, paddingSize, timestampUNIX
from hachoir_core.endian import BIG_ENDIAN
import re

class FileEntry(FieldSet):
    __module__ = __name__
    type_name = {0: 'Normal disk file (old format)', 48: 'Normal disk file', 49: 'Link to previously dumped file', 50: 'Symbolic link', 51: 'Character special file', 52: 'Block special file', 53: 'Directory', 54: 'FIFO special file', 55: 'Contiguous file'}

    def getOctal(self, name):
        return self.octal2int(self[name].value)

    def getDatetime(self):
        """
        Create modification date as Unicode string, may raise ValueError.
        """
        timestamp = self.getOctal('mtime')
        return timestampUNIX(timestamp)

    def createFields(self):
        yield String(self, 'name', 100, 'Name', strip='\x00', charset='ISO-8859-1')
        yield String(self, 'mode', 8, 'Mode', strip=' \x00', charset='ASCII')
        yield String(self, 'uid', 8, 'User ID', strip=' \x00', charset='ASCII')
        yield String(self, 'gid', 8, 'Group ID', strip=' \x00', charset='ASCII')
        yield String(self, 'size', 12, 'Size', strip=' \x00', charset='ASCII')
        yield String(self, 'mtime', 12, 'Modification time', strip=' \x00', charset='ASCII')
        yield String(self, 'check_sum', 8, 'Check sum', strip=' \x00', charset='ASCII')
        yield Enum(UInt8(self, 'type', 'Type'), self.type_name)
        yield String(self, 'lname', 100, 'Link name', strip=' \x00', charset='ISO-8859-1')
        yield String(self, 'magic', 8, 'Magic', strip=' \x00', charset='ASCII')
        yield String(self, 'uname', 32, 'User name', strip=' \x00', charset='ISO-8859-1')
        yield String(self, 'gname', 32, 'Group name', strip=' \x00', charset='ISO-8859-1')
        yield String(self, 'devmajor', 8, 'Dev major', strip=' \x00', charset='ASCII')
        yield String(self, 'devminor', 8, 'Dev minor', strip=' \x00', charset='ASCII')
        yield NullBytes(self, 'padding', 167, 'Padding (zero)')
        filesize = self.getOctal('size')
        if filesize:
            yield SubFile(self, 'content', filesize, filename=self['name'].value)
        size = paddingSize(self.current_size // 8, 512)
        if size:
            yield NullBytes(self, 'padding_end', size, 'Padding (512 align)')

    def convertOctal(self, chunk):
        return self.octal2int(chunk.value)

    def isEmpty(self):
        return self['name'].value == ''

    def octal2int(self, text):
        try:
            return int(text, 8)
        except ValueError:
            return 0

    def createDescription(self):
        if self.isEmpty():
            desc = '(terminator, empty header)'
        else:
            filename = self['name'].value
            filesize = humanFilesize(self.getOctal('size'))
            desc = '(%s: %s, %s)' % (filename, self['type'].display, filesize)
        return 'Tar File ' + desc


class TarFile(Parser):
    __module__ = __name__
    endian = BIG_ENDIAN
    PARSER_TAGS = {'id': 'tar', 'category': 'archive', 'file_ext': ('tar', ), 'mime': ('application/x-tar', 'application/x-gtar'), 'min_size': 512 * 8, 'magic': (('ustar  \x00', 257 * 8),), 'subfile': 'skip', 'description': 'TAR archive'}
    _sign = re.compile('ustar *\x00|[ \x00]*$')

    def validate(self):
        if not self._sign.match(self.stream.readBytes(257 * 8, 8)):
            return 'Invalid magic number'
        if self[0].name == 'terminator':
            return "Don't contain any file"
        try:
            int(self['file[0]/uid'].value, 8)
            int(self['file[0]/gid'].value, 8)
            int(self['file[0]/size'].value, 8)
        except ValueError:
            return 'Invalid file size'

        return True

    def createFields(self):
        while not self.eof:
            field = FileEntry(self, 'file[]')
            if field.isEmpty():
                yield NullBytes(self, 'terminator', 512)
                break
            yield field

        if self.current_size < self._size:
            yield self.seekBit(self._size, 'end')

    def createContentSize(self):
        return self['terminator'].address + self['terminator'].size