# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/hachoir_parser/file_system/linux_swap.py
# Compiled at: 2009-09-07 17:44:28
"""
Linux swap file.

Documentation: Linux kernel source code, files:
 - mm/swapfile.c
 - include/linux/swap.h

Author: Victor Stinner
Creation date: 25 december 2006 (christmas ;-))
"""
from hachoir_parser import Parser
from hachoir_core.field import ParserError, GenericVector, UInt32, String, Bytes, NullBytes, RawBytes
from hachoir_core.endian import LITTLE_ENDIAN
from hachoir_core.tools import humanFilesize
from hachoir_core.bits import str2hex
PAGE_SIZE = 4096
MAX_SWAP_BADPAGES = (PAGE_SIZE - 10 - 1536) // 4

class Page(RawBytes):
    __module__ = __name__
    static_size = PAGE_SIZE * 8

    def __init__(self, parent, name):
        RawBytes.__init__(self, parent, name, PAGE_SIZE)


class UUID(Bytes):
    __module__ = __name__
    static_size = 16 * 8

    def __init__(self, parent, name):
        Bytes.__init__(self, parent, name, 16)

    def createDisplay(self):
        text = str2hex(self.value, format='%02x')
        return '%s-%s-%s-%s-%s' % (text[:8], text[8:12], text[12:16], text[16:20], text[20:])


class LinuxSwapFile(Parser):
    __module__ = __name__
    PARSER_TAGS = {'id': 'linux_swap', 'file_ext': ('', ), 'category': 'file_system', 'min_size': PAGE_SIZE * 8, 'description': 'Linux swap file', 'magic': (('SWAP-SPACE', (PAGE_SIZE - 10) * 8), ('SWAPSPACE2', (PAGE_SIZE - 10) * 8), ('S1SUSPEND\x00', (PAGE_SIZE - 10) * 8))}
    endian = LITTLE_ENDIAN

    def validate(self):
        magic = self.stream.readBytes((PAGE_SIZE - 10) * 8, 10)
        if magic not in ('SWAP-SPACE', 'SWAPSPACE2', 'S1SUSPEND\x00'):
            return 'Unknown magic string'
        if MAX_SWAP_BADPAGES < self['nb_badpage'].value:
            return 'Invalid number of bad page (%u)' % self['nb_badpage'].value
        return True

    def getPageCount(self):
        """
        Number of pages which can really be used for swapping:
        number of page minus bad pages minus one page (used for the header)
        """
        return self['last_page'].value - self['nb_badpage'].value - 1

    def createDescription(self):
        if self['magic'].value == 'S1SUSPEND\x00':
            text = 'Suspend swap file version 1'
        elif self['magic'].value == 'SWAPSPACE2':
            text = 'Linux swap file version 2'
        else:
            text = 'Linux swap file version 1'
        nb_page = self.getPageCount()
        return '%s, page size: %s, %s pages' % (text, humanFilesize(PAGE_SIZE), nb_page)

    def createFields(self):
        yield RawBytes(self, 'boot', 1024, 'Space for disklabel etc.')
        yield UInt32(self, 'version')
        yield UInt32(self, 'last_page')
        yield UInt32(self, 'nb_badpage')
        yield UUID(self, 'sws_uuid')
        yield UUID(self, 'sws_volume')
        yield NullBytes(self, 'reserved', 117 * 4)
        count = self['nb_badpage'].value
        if count:
            if MAX_SWAP_BADPAGES < count:
                raise ParserError('Invalid number of bad page (%u)' % count)
            yield GenericVector(self, 'badpages', count, UInt32, 'badpage')
        padding = self.seekByte(PAGE_SIZE - 10, 'padding', null=True)
        if padding:
            yield padding
        yield String(self, 'magic', 10, charset='ASCII')
        yield GenericVector(self, 'pages', self['last_page'].value, Page, 'page')
        padding = self.seekBit(self.size, 'end_padding', null=True)
        if padding:
            yield padding