# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/hachoir_parser/file_system/mbr.py
# Compiled at: 2010-01-20 18:06:00
"""
Master Boot Record.

"""
from hachoir_parser import Parser
from hachoir_core.field import FieldSet, Enum, Bits, UInt8, UInt16, UInt32, RawBytes
from hachoir_core.endian import LITTLE_ENDIAN
from hachoir_core.tools import humanFilesize
from hachoir_core.text_handler import textHandler, hexadecimal
BLOCK_SIZE = 512

class CylinderNumber(Bits):
    __module__ = __name__

    def __init__(self, parent, name, description=None):
        Bits.__init__(self, parent, name, 10, description)

    def createValue(self):
        i = self.parent.stream.readInteger(self.absolute_address, False, self._size, self.parent.endian)
        return i >> 2 | i % 4 << 8


class PartitionHeader(FieldSet):
    __module__ = __name__
    static_size = 16 * 8
    system_name = {0: 'Empty', 1: 'FAT12', 2: 'XENIX root', 3: 'XENIX usr', 4: 'FAT16 <32M', 5: 'Extended', 6: 'FAT16', 7: 'HPFS/NTFS', 8: 'AIX', 9: 'AIX bootable', 10: 'OS/2 Boot Manager', 11: 'W95 FAT32', 12: 'W95 FAT32 (LBA)', 14: 'W95 FAT16 (LBA)', 15: "W95 Ext'd (LBA)", 16: 'OPUS', 17: 'Hidden FAT12', 18: 'Compaq diagnostics', 20: 'Hidden FAT16 <32M', 22: 'Hidden FAT16', 23: 'Hidden HPFS/NTFS', 24: 'AST SmartSleep', 27: 'Hidden W95 FAT32', 28: 'Hidden W95 FAT32 (LBA)', 30: 'Hidden W95 FAT16 (LBA)', 36: 'NEC DOS', 57: 'Plan 9', 60: 'PartitionMagic recovery', 64: 'Venix 80286', 65: 'PPC PReP Boot', 66: 'SFS', 77: 'QNX4.x', 78: 'QNX4.x 2nd part', 79: 'QNX4.x 3rd part', 80: 'OnTrack DM', 81: 'OnTrack DM6 Aux1', 82: 'CP/M', 83: 'OnTrack DM6 Aux3', 84: 'OnTrackDM6', 85: 'EZ-Drive', 86: 'Golden Bow', 92: 'Priam Edisk', 97: 'SpeedStor', 99: 'GNU HURD or SysV', 100: 'Novell Netware 286', 101: 'Novell Netware 386', 112: 'DiskSecure Multi-Boot', 117: 'PC/IX', 128: 'Old Minix', 129: 'Minix / old Linux', 130: 'Linux swap / Solaris', 131: 'Linux (ext2/ext3)', 132: 'OS/2 hidden C: drive', 133: 'Linux extended', 134: 'NTFS volume set', 135: 'NTFS volume set', 136: 'Linux plaintext', 142: 'Linux LVM', 147: 'Amoeba', 148: 'Amoeba BBT', 159: 'BSD/OS', 160: 'IBM Thinkpad hibernation', 165: 'FreeBSD', 166: 'OpenBSD', 167: 'NeXTSTEP', 168: 'Darwin UFS', 169: 'NetBSD', 171: 'Darwin boot', 183: 'BSDI fs', 184: 'BSDI swap', 187: 'Boot Wizard hidden', 190: 'Solaris boot', 191: 'Solaris', 193: 'DRDOS/sec (FAT-12)', 196: 'DRDOS/sec (FAT-16 < 32M)', 198: 'DRDOS/sec (FAT-16)', 199: 'Syrinx', 218: 'Non-FS data', 219: 'CP/M / CTOS / ...', 222: 'Dell Utility', 223: 'BootIt', 225: 'DOS access', 227: 'DOS R/O', 228: 'SpeedStor', 235: 'BeOS fs', 238: 'EFI GPT', 239: 'EFI (FAT-12/16/32)', 240: 'Linux/PA-RISC boot', 241: 'SpeedStor', 244: 'SpeedStor', 242: 'DOS secondary', 253: 'Linux raid autodetect', 254: 'LANstep', 255: 'BBT'}

    def createFields(self):
        yield UInt8(self, 'bootable', 'Bootable flag (true if equals to 0x80)')
        if self['bootable'].value not in (0, 128):
            self.warning("Stream doesn't look like master boot record (partition bootable error)!")
        yield UInt8(self, 'start_head', 'Starting head number of the partition')
        yield Bits(self, 'start_sector', 6, 'Starting sector number of the partition')
        yield CylinderNumber(self, 'start_cylinder', 'Starting cylinder number of the partition')
        yield Enum(UInt8(self, 'system', 'System indicator'), self.system_name)
        yield UInt8(self, 'end_head', 'Ending head number of the partition')
        yield Bits(self, 'end_sector', 6, 'Ending sector number of the partition')
        yield CylinderNumber(self, 'end_cylinder', 'Ending cylinder number of the partition')
        yield UInt32(self, 'LBA', 'LBA (number of sectors before this partition)')
        yield UInt32(self, 'size', 'Size (block count)')

    def isUsed(self):
        return self['system'].value != 0

    def createDescription(self):
        desc = 'Partition header: '
        if self.isUsed():
            system = self['system'].display
            size = self['size'].value * BLOCK_SIZE
            desc += '%s, %s' % (system, humanFilesize(size))
        else:
            desc += '(unused)'
        return desc


class MasterBootRecord(FieldSet):
    __module__ = __name__
    static_size = 512 * 8

    def createFields(self):
        yield RawBytes(self, 'program', 446, 'Boot program (Intel x86 machine code)')
        yield PartitionHeader(self, 'header[0]')
        yield PartitionHeader(self, 'header[1]')
        yield PartitionHeader(self, 'header[2]')
        yield PartitionHeader(self, 'header[3]')
        yield textHandler(UInt16(self, 'signature', 'Signature (0xAA55)'), hexadecimal)

    def _getPartitions(self):
        return (self[index] for index in xrange(1, 5))

    headers = property(_getPartitions)


class Partition(FieldSet):
    __module__ = __name__

    def createFields(self):
        mbr = MasterBootRecord(self, 'mbr')
        yield mbr
        if self.eof:
            return
        for (start, index, header) in sorted(((hdr['LBA'].value, index, hdr) for (index, hdr) in enumerate(mbr.headers) if hdr.isUsed())):
            padding = self.seekByte(start * BLOCK_SIZE, 'padding[]')
            if padding:
                yield padding
            name = 'partition[%u]' % index
            size = BLOCK_SIZE * header['size'].value
            desc = header['system'].display
            if header['system'].value == 5:
                yield Partition(self, name, desc, size * 8)
            else:
                yield RawBytes(self, name, size, desc)

        if self.current_size < self._size:
            yield self.seekBit(self._size, 'end')


class MSDos_HardDrive(Parser, Partition):
    __module__ = __name__
    endian = LITTLE_ENDIAN
    MAGIC = b'U\xaa'
    PARSER_TAGS = {'id': 'msdos_harddrive', 'category': 'file_system', 'description': 'MS-DOS hard drive with Master Boot Record (MBR)', 'min_size': 512 * 8, 'file_ext': ('', )}

    def validate(self):
        if self.stream.readBytes(510 * 8, 2) != self.MAGIC:
            return 'Invalid signature'
        used = False
        for hdr in self['mbr'].headers:
            if hdr['bootable'].value not in (0, 128):
                return 'Wrong boot flag'
            used |= hdr.isUsed()

        return used or 'No partition found'