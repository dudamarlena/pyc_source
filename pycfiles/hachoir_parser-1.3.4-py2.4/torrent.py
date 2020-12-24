# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/hachoir_parser/misc/torrent.py
# Compiled at: 2009-09-07 17:44:28
"""
.torrent metainfo file parser

http://wiki.theory.org/BitTorrentSpecification#Metainfo_File_Structure

Status: To statufy
Author: Christophe Gisquet <christophe.gisquet@free.fr>
"""
from hachoir_parser import Parser
from hachoir_core.field import FieldSet, ParserError, String, RawBytes
from hachoir_core.endian import LITTLE_ENDIAN
from hachoir_core.tools import makePrintable, timestampUNIX, humanFilesize
MAX_STRING_LENGTH = 6
MAX_INTEGER_SIZE = 21

class Integer(FieldSet):
    __module__ = __name__

    def createFields(self):
        yield String(self, 'start', 1, 'Integer start delimiter (i)', charset='ASCII')
        addr = self.absolute_address + self.current_size
        len = self.stream.searchBytesLength('e', False, addr, addr + (MAX_INTEGER_SIZE + 1) * 8)
        if len is None:
            raise ParserError('Torrent: Unable to find integer end delimiter (e)!')
        if not len:
            raise ParserError('Torrent: error, empty integer!')
        yield String(self, 'value', len, 'Integer value', charset='ASCII')
        yield String(self, 'end', 1, 'Integer end delimiter')
        return

    def createValue(self):
        """Read integer value (may raise ValueError)"""
        return int(self['value'].value)


class TorrentString(FieldSet):
    __module__ = __name__

    def createFields(self):
        addr = self.absolute_address
        len = self.stream.searchBytesLength(':', False, addr, addr + (MAX_STRING_LENGTH + 1) * 8)
        if len is None:
            raise ParserError("Torrent: unable to find string separator (':')")
        if not len:
            raise ParserError('Torrent: error: no string length!')
        val = String(self, 'length', len, 'String length')
        yield val
        try:
            len = int(val.value)
        except ValueError:
            len = -1

        if len < 0:
            raise ParserError('Invalid string length (%s)' % makePrintable(val.value, 'ASCII', to_unicode=True))
        yield String(self, 'separator', 1, 'String length/value separator')
        if not len:
            self.info('Empty string: len=%i' % len)
            return
        if len < 512:
            yield String(self, 'value', len, 'String value', charset='ISO-8859-1')
        else:
            yield RawBytes(self, 'value', len, 'Raw data')
        return

    def createValue(self):
        if 'value' in self:
            field = self['value']
            if field.__class__ != RawBytes:
                return field.value
            else:
                return
        else:
            return
        return


class Dictionary(FieldSet):
    __module__ = __name__

    def createFields(self):
        yield String(self, 'start', 1, 'Dictionary start delimiter (d)', charset='ASCII')
        while self.stream.readBytes(self.absolute_address + self.current_size, 1) != 'e':
            yield DictionaryItem(self, 'item[]')

        yield String(self, 'end', 1, 'Dictionary end delimiter')


class List(FieldSet):
    __module__ = __name__

    def createFields(self):
        yield String(self, 'start', 1, 'List start delimiter')
        while self.stream.readBytes(self.absolute_address + self.current_size, 1) != 'e':
            yield Entry(self, 'item[]')

        yield String(self, 'end', 1, 'List end delimiter')


class DictionaryItem(FieldSet):
    __module__ = __name__

    def __init__(self, *args):
        FieldSet.__init__(self, *args)
        key = self['key']
        if not key.hasValue():
            return
        key = key.value
        self._name = str(key).replace(' ', '_')

    def createDisplay(self):
        if not self['value'].hasValue():
            return
        if self._name in ('length', 'piece_length'):
            return humanFilesize(self.value)
        return FieldSet.createDisplay(self)

    def createValue(self):
        if not self['value'].hasValue():
            return
        if self._name == 'creation_date':
            return self.createTimestampValue()
        else:
            return self['value'].value
        return

    def createFields(self):
        yield Entry(self, 'key')
        yield Entry(self, 'value')

    def createTimestampValue(self):
        return timestampUNIX(self['value'].value)


TAGS = {'d': Dictionary, 'i': Integer, 'l': List}
for index in xrange(1, 9 + 1):
    TAGS[str(index)] = TorrentString

def Entry(parent, name):
    addr = parent.absolute_address + parent.current_size
    tag = parent.stream.readBytes(addr, 1)
    if tag not in TAGS:
        raise ParserError('Torrent: Entry of type %r not handled' % type)
    cls = TAGS[tag]
    return cls(parent, name)


class TorrentFile(Parser):
    __module__ = __name__
    endian = LITTLE_ENDIAN
    MAGIC = 'd8:announce'
    PARSER_TAGS = {'id': 'torrent', 'category': 'misc', 'file_ext': ('torrent', ), 'min_size': 50 * 8, 'mime': ('application/x-bittorrent', ), 'magic': ((MAGIC, 0),), 'description': 'Torrent metainfo file'}

    def validate(self):
        if self.stream.readBytes(0, len(self.MAGIC)) != self.MAGIC:
            return 'Invalid magic'
        return True

    def createFields(self):
        yield Dictionary(self, 'root', size=self.size)