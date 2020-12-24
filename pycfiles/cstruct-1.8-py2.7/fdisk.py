# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/cstruct/examples/fdisk.py
# Compiled at: 2018-09-18 16:58:02
import cstruct, sys

class Position(cstruct.CStruct):
    __byte_order__ = cstruct.LITTLE_ENDIAN
    __struct__ = '\n        unsigned char head;\n        unsigned char sector;\n        unsigned char cyl;\n    '


class Partition(cstruct.CStruct):
    __byte_order__ = cstruct.LITTLE_ENDIAN
    __struct__ = '\n        unsigned char status;       /* 0x80 - active */\n        struct Position start;\n        unsigned char partition_type;\n        struct Position end;\n        unsigned int start_sect;    /* starting sector counting from 0 */\n        unsigned int sectors;       /* nr of sectors in partition */\n    '

    def print_info(self):
        print 'bootable: %s' % (self.status & 128 and 'Y' or 'N')
        print 'partition_type: %02X' % self.partition_type
        print 'start: head: %X sectory: %X cyl: %X' % (self.start.head, self.start.sector, self.start.cyl)
        print 'end: head: %X sectory: %X cyl: %X' % (self.end.head, self.end.sector, self.end.cyl)
        print 'starting sector: %08X' % self.start_sect
        print 'size MB: %s' % (self.sectors / 2 / 1024)


class MBR(cstruct.CStruct):
    __byte_order__ = cstruct.LITTLE_ENDIAN
    __struct__ = '\n        char unused[440];\n        unsigned char disk_signature[4];\n        unsigned char usualy_nulls[2];\n        struct Partition partitions[4];\n        char signature[2];\n    '

    def print_info(self):
        print 'disk signature: %s' % ('').join([ '%02X' % x for x in self.disk_signature ])
        print 'usualy nulls: %s' % ('').join([ '%02X' % x for x in self.usualy_nulls ])
        for i, partition in enumerate(self.partitions):
            print ''
            print 'partition: %s' % i
            partition.print_info()


def main():
    if len(sys.argv) != 2:
        print 'usage: %s disk' % sys.argv[0]
        sys.exit(2)
    with open(sys.argv[1], 'rb') as (f):
        mbr = MBR()
        data = f.read(len(mbr))
        mbr.unpack(data)
        mbr.print_info()


if __name__ == '__main__':
    main()