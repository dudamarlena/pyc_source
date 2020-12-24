# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/hachoir_parser/misc/hlp.py
# Compiled at: 2009-09-07 17:44:28
"""
Microsoft Windows Help (HLP) parser for Hachoir project.

Documents:
- Windows Help File Format / Annotation File Format / SHG and MRB File Format
  written by M. Winterhoff (100326.2776@compuserve.com)
  found on http://www.wotsit.org/

Author: Victor Stinner
Creation date: 2007-09-03
"""
from hachoir_parser import Parser
from hachoir_core.field import FieldSet, Bits, Int32, UInt16, UInt32, NullBytes, RawBytes, PaddingBytes, String
from hachoir_core.endian import LITTLE_ENDIAN
from hachoir_core.text_handler import textHandler, hexadecimal, displayHandler, humanFilesize

class FileEntry(FieldSet):
    __module__ = __name__

    def __init__(self, *args, **kw):
        FieldSet.__init__(self, *args, **kw)
        self._size = self['res_space'].value * 8

    def createFields(self):
        yield displayHandler(UInt32(self, 'res_space', 'Reserved space'), humanFilesize)
        yield displayHandler(UInt32(self, 'used_space', 'Used space'), humanFilesize)
        yield Bits(self, 'file_flags', 8, '(=4)')
        yield textHandler(UInt16(self, 'magic'), hexadecimal)
        yield Bits(self, 'flags', 16)
        yield displayHandler(UInt16(self, 'page_size', 'Page size in bytes'), humanFilesize)
        yield String(self, 'structure', 16, strip='\x00', charset='ASCII')
        yield NullBytes(self, 'zero', 2)
        yield UInt16(self, 'nb_page_splits', 'Number of page splits B+ tree has suffered')
        yield UInt16(self, 'root_page', 'Page number of B+ tree root page')
        yield PaddingBytes(self, 'one', 2, pattern=b'\xff')
        yield UInt16(self, 'nb_page', 'Number of B+ tree pages')
        yield UInt16(self, 'nb_level', 'Number of levels of B+ tree')
        yield UInt16(self, 'nb_entry', 'Number of entries in B+ tree')
        size = (self.size - self.current_size) // 8
        if size:
            yield PaddingBytes(self, 'reserved_space', size)


class HlpFile(Parser):
    __module__ = __name__
    PARSER_TAGS = {'id': 'hlp', 'category': 'misc', 'file_ext': ('hlp', ), 'min_size': 32, 'description': 'Microsoft Windows Help (HLP)'}
    endian = LITTLE_ENDIAN

    def validate(self):
        if self['magic'].value != 220991:
            return 'Invalid magic'
        if self['filesize'].value != self.stream.size // 8:
            return 'Invalid magic'
        return True

    def createFields(self):
        yield textHandler(UInt32(self, 'magic'), hexadecimal)
        yield UInt32(self, 'dir_start', 'Directory start')
        yield Int32(self, 'first_free_block', 'First free block')
        yield UInt32(self, 'filesize', 'File size in bytes')
        yield self.seekByte(self['dir_start'].value)
        yield FileEntry(self, 'file[]')
        size = (self.size - self.current_size) // 8
        if size:
            yield RawBytes(self, 'end', size)