# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/hachoir_parser/file_system/reiser_fs.py
# Compiled at: 2009-09-07 17:44:28
"""
ReiserFS file system version 3 parser (version 1, 2 and 4 are not supported).

Author: Frederic Weisbecker
Creation date: 8 december 2006

Sources:
 - http://p-nand-q.com/download/rfstool/reiserfs_docs.html
 - http://homes.cerias.purdue.edu/~florian/reiser/reiserfs.php
 - file://usr/src/linux-2.6.16.19/include/linux/reiserfs_fs.h

NOTES:

The most part of the description of the structures, their fields and their
comments decribed here comes from the file include/linux/reiserfs_fs.h
- written by Hans reiser - located in the Linux kernel 2.6.16.19 and from
the Reiserfs explanations in
http://p-nand-q.com/download/rfstool/reiserfs_docs.html written by Gerson
Kurz.
"""
from hachoir_parser import Parser
from hachoir_core.field import FieldSet, Enum, UInt16, UInt32, String, RawBytes, NullBytes
from hachoir_core.endian import LITTLE_ENDIAN

class Journal_params(FieldSet):
    __module__ = __name__
    static_size = 32 * 8

    def createFields(self):
        yield UInt32(self, '1st_block', 'Journal 1st block number')
        yield UInt32(self, 'dev', 'Journal device number')
        yield UInt32(self, 'size', 'Size of the journal')
        yield UInt32(self, 'trans_max', 'Max number of blocks in a transaction')
        yield UInt32(self, 'magic', 'Random value made on fs creation.')
        yield UInt32(self, 'max_batch', 'Max number of blocks to batch into a trans')
        yield UInt32(self, 'max_commit_age', 'In seconds, how old can an async commit be')
        yield UInt32(self, 'max_trans_age', 'In seconds, how old can a transaction be')

    def createDescription(self):
        return 'Parameters of the journal'


class SuperBlock(FieldSet):
    __module__ = __name__
    static_size = 204 * 8
    UMOUNT_STATE = {1: 'unmounted', 2: 'not unmounted'}
    HASH_FUNCTIONS = {0: 'UNSET_HASH', 1: 'TEA_HASH', 2: 'YURA_HASH', 3: 'R5_HASH'}

    def createFields(self):
        yield UInt32(self, 'block_count', 'Number of blocks')
        yield UInt32(self, 'free_blocks', 'Number of free blocks')
        yield UInt32(self, 'root_block', 'Root block number')
        yield Journal_params(self, 'Journal parameters')
        yield UInt16(self, 'blocksize', 'Size of a block')
        yield UInt16(self, 'oid_maxsize', 'Max size of object id array')
        yield UInt16(self, 'oid_cursize', 'Current size of object id array')
        yield Enum(UInt16(self, 'umount_state', 'Filesystem umounted or not'), self.UMOUNT_STATE)
        yield String(self, 'magic', 10, 'Magic string', strip='\x00')
        yield UInt16(self, 'fs_state', 'Rebuilding phase of fsck ')
        yield Enum(UInt32(self, 'hash_function', 'Hash function to sort names in a directory'), self.HASH_FUNCTIONS)
        yield UInt16(self, 'tree_height', 'Height of disk tree')
        yield UInt16(self, 'bmap_nr', 'Amount of bitmap blocks needed to address each block of file system')
        yield UInt16(self, 'version', 'Field only reliable on filesystem with non-standard journal')
        yield UInt16(self, 'reserved_for_journal', 'Size in blocks of journal area on main device')
        yield UInt32(self, 'inode_generation', 'No description')
        yield UInt32(self, 'flags', 'No description')
        yield RawBytes(self, 'uuid', 16, 'Filesystem unique identifier')
        yield String(self, 'label', 16, 'Filesystem volume label', strip='\x00')
        yield NullBytes(self, 'unused', 88)

    def createDescription(self):
        return 'Superblock: ReiserFs Filesystem'


class REISER_FS(Parser):
    __module__ = __name__
    PARSER_TAGS = {'id': 'reiserfs', 'category': 'file_system', 'min_size': (130 + 513 + 1) * (512 * 8), 'description': 'ReiserFS file system'}
    endian = LITTLE_ENDIAN
    SUPERBLOCK_OFFSET = 64 * 1024
    MAGIC_OFFSET = SUPERBLOCK_OFFSET + 52

    def validate(self):
        magic = self.stream.readBytes(self.MAGIC_OFFSET * 8, 9).rstrip('\x00')
        if magic == 'ReIsEr3Fs':
            return True
        if magic in ('ReIsEr2Fs', 'ReIsErFs'):
            return 'Unsupported version of ReiserFs'
        return 'Invalid magic string'

    def createFields(self):
        yield NullBytes(self, 'padding[]', self.SUPERBLOCK_OFFSET)
        yield SuperBlock(self, 'superblock')