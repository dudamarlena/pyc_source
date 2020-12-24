# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/hachoir_parser/archive/mar.py
# Compiled at: 2009-09-07 17:44:28
"""
Microsoft Archive parser

Author: Victor Stinner
Creation date: 2007-03-04
"""
MAX_NB_FILE = 100000
from hachoir_parser import Parser
from hachoir_core.field import FieldSet, String, UInt32, SubFile
from hachoir_core.endian import LITTLE_ENDIAN
from hachoir_core.text_handler import textHandler, filesizeHandler, hexadecimal

class FileIndex(FieldSet):
    __module__ = __name__
    static_size = 68 * 8

    def createFields(self):
        yield String(self, 'filename', 56, truncate='\x00', charset='ASCII')
        yield filesizeHandler(UInt32(self, 'filesize'))
        yield textHandler(UInt32(self, 'crc32'), hexadecimal)
        yield UInt32(self, 'offset')

    def createDescription(self):
        return 'File %s (%s) at %s' % (self['filename'].value, self['filesize'].display, self['offset'].value)


class MarFile(Parser):
    __module__ = __name__
    MAGIC = 'MARC'
    PARSER_TAGS = {'id': 'mar', 'category': 'archive', 'file_ext': ('mar', ), 'min_size': 80 * 8, 'magic': ((MAGIC, 0),), 'description': 'Microsoft Archive'}
    endian = LITTLE_ENDIAN

    def validate(self):
        if self.stream.readBytes(0, 4) != self.MAGIC:
            return 'Invalid magic'
        if self['version'].value != 3:
            return 'Invalid version'
        if not 1 <= self['nb_file'].value <= MAX_NB_FILE:
            return 'Invalid number of file'
        return True

    def createFields(self):
        yield String(self, 'magic', 4, 'File signature (MARC)', charset='ASCII')
        yield UInt32(self, 'version')
        yield UInt32(self, 'nb_file')
        files = []
        for index in xrange(self['nb_file'].value):
            item = FileIndex(self, 'file[]')
            yield item
            if item['filesize'].value:
                files.append(item)

        files.sort(key=lambda item: item['offset'].value)
        for index in files:
            padding = self.seekByte(index['offset'].value)
            if padding:
                yield padding
            size = index['filesize'].value
            desc = 'File %s' % index['filename'].value
            yield SubFile(self, 'data[]', size, desc, filename=index['filename'].value)