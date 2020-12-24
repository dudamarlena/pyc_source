# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\reconstruct\formats\filesystem\ext2.py
# Compiled at: 2010-05-01 15:45:14
"""
Extension 2 (ext2)
Used in Linux systems
"""
from construct import *
Char = SLInt8
UChar = ULInt8
Short = SLInt16
UShort = ULInt16
Long = SLInt32
ULong = ULInt32

def BlockPointer(name):
    return Struct(name, ULong('block_number'), OnDemandPointer(lambda ctx: ctx['block_number']))


superblock = Struct('superblock', ULong('inodes_count'), ULong('blocks_count'), ULong('reserved_blocks_count'), ULong('free_blocks_count'), ULong('free_inodes_count'), ULong('first_data_block'), Enum(ULong('log_block_size'), OneKB=0, TwoKB=1, FourKB=2), Long('log_frag_size'), ULong('blocks_per_group'), ULong('frags_per_group'), ULong('inodes_per_group'), ULong('mtime'), ULong('wtime'), UShort('mnt_count'), Short('max_mnt_count'), Const(UShort('magic'), 61267), UShort('state'), UShort('errors'), Padding(2), ULong('lastcheck'), ULong('checkinterval'), ULong('creator_os'), ULong('rev_level'), Padding(940))
group_descriptor = Struct('group_descriptor', ULong('block_bitmap'), ULong('inode_bitmap'), ULong('inode_table'), UShort('free_blocks_count'), UShort('free_inodes_count'), UShort('used_dirs_count'), Padding(14))
inode = Struct('inode', FlagsEnum(UShort('mode'), IXOTH=1, IWOTH=2, IROTH=4, IRWXO=7, IXGRP=8, IWGRP=16, IRGRP=32, IRWXG=56, IXUSR=64, IWUSR=128, IRUSR=256, IRWXU=448, ISVTX=512, ISGID=1024, ISUID=2048, IFIFO=4096, IFCHR=8192, IFDIR=16384, IFBLK=24576, IFREG=32768, IFLNK=49152, IFSOCK=40960, IFMT=61440), UShort('uid'), ULong('size'), ULong('atime'), ULong('ctime'), ULong('mtime'), ULong('dtime'), UShort('gid'), UShort('links_count'), ULong('blocks'), FlagsEnum(ULong('flags'), SecureDelete=1, AllowUndelete=2, Compressed=4, Synchronous=8), Padding(4), StrictRepeater(12, ULong('blocks')), ULong('indirect1_block'), ULong('indirect2_block'), ULong('indirect3_block'), ULong('version'), ULong('file_acl'), ULong('dir_acl'), ULong('faddr'), UChar('frag'), Byte('fsize'), Padding(10))
EXT2_BAD_INO = 1
EXT2_ROOT_INO = 2
EXT2_ACL_IDX_INO = 3
EXT2_ACL_DATA_INO = 4
EXT2_BOOT_LOADER_INO = 5
EXT2_UNDEL_DIR_INO = 6
EXT2_FIRST_INO = 11
directory_record = Struct('directory_entry', ULong('inode'), UShort('rec_length'), UShort('name_length'), Field('name', lambda ctx: ctx['name_length']), Padding(lambda ctx: ctx['rec_length'] - ctx['name_length']))
print superblock.sizeof()