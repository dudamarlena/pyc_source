# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/cstruct/tests/test_cstruct.py
# Compiled at: 2018-10-30 18:12:03
from unittest import TestCase, main
import cstruct, sys
if sys.version_info >= (3, 0):
    MBR_DATA = bytes([235, 72, 144, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 2, 255, 0, 0, 128, 97, 203, 4, 0, 0, 8, 250, 128, 202, 128, 234, 83, 124, 0, 0, 49, 192, 142, 216, 142, 208, 188, 0, 32, 251, 160, 64, 124, 60, 255, 116, 2, 136, 194, 82, 190, 121, 125, 232, 52, 1, 246, 194, 128, 116, 84, 180, 65, 187, 170, 85, 205, 19, 90, 82, 114, 73, 129, 251, 85, 170, 117, 67, 160, 65, 124, 132, 192, 117, 5, 131, 225, 1, 116, 55, 102, 139, 76, 16, 190, 5, 124, 198, 68, 255, 1, 102, 139, 30, 68, 124, 199, 4, 16, 0, 199, 68, 2, 1, 0, 102, 137, 92, 8, 199, 68, 6, 0, 112, 102, 49, 192, 137, 68, 4, 102, 137, 68, 12, 180, 66, 205, 19, 114, 5, 187, 0, 112, 235, 125, 180, 8, 205, 19, 115, 10, 246, 194, 128, 15, 132, 240, 0, 233, 141, 0, 190, 5, 124, 198, 68, 255, 0, 102, 49, 192, 136, 240, 64, 102, 137, 68, 4, 49, 210, 136, 202, 193, 226, 2, 136, 232, 136, 244, 64, 137, 68, 8, 49, 192, 136, 208, 192, 232, 2, 102, 137, 4, 102, 161, 68, 124, 102, 49, 210, 102, 247, 52, 136, 84, 10, 102, 49, 210, 102, 247, 116, 4, 136, 84, 11, 137, 68, 12, 59, 68, 8, 125, 60, 138, 84, 13, 192, 226, 6, 138, 76, 10, 254, 193, 8, 209, 138, 108, 12, 90, 138, 116, 11, 187, 0, 112, 142, 195, 49, 219, 184, 1, 2, 205, 19, 114, 42, 140, 195, 142, 6, 72, 124, 96, 30, 185, 0, 1, 142, 219, 49, 246, 49, 255, 252, 243, 165, 31, 97, 255, 38, 66, 124, 190, 127, 125, 232, 64, 0, 235, 14, 190, 132, 125, 232, 56, 0, 235, 6, 190, 142, 125, 232, 48, 0, 190, 147, 125, 232, 42, 0, 235, 254, 71, 82, 85, 66, 32, 0, 71, 101, 111, 109, 0, 72, 97, 114, 100, 32, 68, 105, 115, 107, 0, 82, 101, 97, 100, 0, 32, 69, 114, 114, 111, 114, 0, 187, 1, 0, 180, 14, 205, 16, 172, 60, 0, 117, 244, 195, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 128, 0, 2, 0, 131, 254, 63, 134, 1, 0, 0, 0, 198, 23, 33, 0, 0, 0, 1, 135, 142, 254, 255, 255, 199, 23, 33, 0, 77, 211, 222, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 85, 170])
elif sys.version_info >= (2, 6):
    MBR_DATA = bytes(b'\xebH\x90\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03\x02\xff\x00\x00\x80a\xcb\x04\x00\x00\x08\xfa\x80\xca\x80\xeaS|\x00\x001\xc0\x8e\xd8\x8e\xd0\xbc\x00 \xfb\xa0@|<\xfft\x02\x88\xc2R\xbey}\xe84\x01\xf6\xc2\x80tT\xb4A\xbb\xaaU\xcd\x13ZRrI\x81\xfbU\xaauC\xa0A|\x84\xc0u\x05\x83\xe1\x01t7f\x8bL\x10\xbe\x05|\xc6D\xff\x01f\x8b\x1eD|\xc7\x04\x10\x00\xc7D\x02\x01\x00f\x89\\\x08\xc7D\x06\x00pf1\xc0\x89D\x04f\x89D\x0c\xb4B\xcd\x13r\x05\xbb\x00p\xeb}\xb4\x08\xcd\x13s\n\xf6\xc2\x80\x0f\x84\xf0\x00\xe9\x8d\x00\xbe\x05|\xc6D\xff\x00f1\xc0\x88\xf0@f\x89D\x041\xd2\x88\xca\xc1\xe2\x02\x88\xe8\x88\xf4@\x89D\x081\xc0\x88\xd0\xc0\xe8\x02f\x89\x04f\xa1D|f1\xd2f\xf74\x88T\nf1\xd2f\xf7t\x04\x88T\x0b\x89D\x0c;D\x08}<\x8aT\r\xc0\xe2\x06\x8aL\n\xfe\xc1\x08\xd1\x8al\x0cZ\x8at\x0b\xbb\x00p\x8e\xc31\xdb\xb8\x01\x02\xcd\x13r*\x8c\xc3\x8e\x06H|`\x1e\xb9\x00\x01\x8e\xdb1\xf61\xff\xfc\xf3\xa5\x1fa\xff&B|\xbe\x7f}\xe8@\x00\xeb\x0e\xbe\x84}\xe88\x00\xeb\x06\xbe\x8e}\xe80\x00\xbe\x93}\xe8*\x00\xeb\xfeGRUB \x00Geom\x00Hard Disk\x00Read\x00 Error\x00\xbb\x01\x00\xb4\x0e\xcd\x10\xac<\x00u\xf4\xc3\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x80\x00\x02\x00\x83\xfe?\x86\x01\x00\x00\x00\xc6\x17!\x00\x00\x00\x01\x87\x8e\xfe\xff\xff\xc7\x17!\x00M\xd3\xde\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00U\xaa')
else:
    MBR_DATA = b'\xebH\x90\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03\x02\xff\x00\x00\x80a\xcb\x04\x00\x00\x08\xfa\x80\xca\x80\xeaS|\x00\x001\xc0\x8e\xd8\x8e\xd0\xbc\x00 \xfb\xa0@|<\xfft\x02\x88\xc2R\xbey}\xe84\x01\xf6\xc2\x80tT\xb4A\xbb\xaaU\xcd\x13ZRrI\x81\xfbU\xaauC\xa0A|\x84\xc0u\x05\x83\xe1\x01t7f\x8bL\x10\xbe\x05|\xc6D\xff\x01f\x8b\x1eD|\xc7\x04\x10\x00\xc7D\x02\x01\x00f\x89\\\x08\xc7D\x06\x00pf1\xc0\x89D\x04f\x89D\x0c\xb4B\xcd\x13r\x05\xbb\x00p\xeb}\xb4\x08\xcd\x13s\n\xf6\xc2\x80\x0f\x84\xf0\x00\xe9\x8d\x00\xbe\x05|\xc6D\xff\x00f1\xc0\x88\xf0@f\x89D\x041\xd2\x88\xca\xc1\xe2\x02\x88\xe8\x88\xf4@\x89D\x081\xc0\x88\xd0\xc0\xe8\x02f\x89\x04f\xa1D|f1\xd2f\xf74\x88T\nf1\xd2f\xf7t\x04\x88T\x0b\x89D\x0c;D\x08}<\x8aT\r\xc0\xe2\x06\x8aL\n\xfe\xc1\x08\xd1\x8al\x0cZ\x8at\x0b\xbb\x00p\x8e\xc31\xdb\xb8\x01\x02\xcd\x13r*\x8c\xc3\x8e\x06H|`\x1e\xb9\x00\x01\x8e\xdb1\xf61\xff\xfc\xf3\xa5\x1fa\xff&B|\xbe\x7f}\xe8@\x00\xeb\x0e\xbe\x84}\xe88\x00\xeb\x06\xbe\x8e}\xe80\x00\xbe\x93}\xe8*\x00\xeb\xfeGRUB \x00Geom\x00Hard Disk\x00Read\x00 Error\x00\xbb\x01\x00\xb4\x0e\xcd\x10\xac<\x00u\xf4\xc3\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x80\x00\x02\x00\x83\xfe?\x86\x01\x00\x00\x00\xc6\x17!\x00\x00\x00\x01\x87\x8e\xfe\xff\xff\xc7\x17!\x00M\xd3\xde\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00U\xaa'

class Position(cstruct.CStruct):
    __byte_order__ = cstruct.LITTLE_ENDIAN
    __struct__ = '\n        unsigned char head;\n        unsigned char sector;\n        unsigned char cyl;\n    '


class Partition(cstruct.CStruct):
    __byte_order__ = cstruct.LITTLE_ENDIAN
    __struct__ = '\n        unsigned char status;       /* 0x80 - active */\n        struct Position start;\n        unsigned char partition_type;\n        struct Position end;\n        unsigned int start_sect;    /* starting sector counting from 0 */\n        unsigned int sectors;       // nr of sectors in partition\n    '


class MBR(cstruct.CStruct):
    __byte_order__ = cstruct.LITTLE_ENDIAN
    __struct__ = '\n        char unused[440];\n        unsigned char disk_signature[4];\n        unsigned char usualy_nulls[2];\n        struct Partition partitions[4];\n        char signature[2];\n    '


class TestCStruct(TestCase):

    def test_len(self):
        mbr = MBR()
        self.assertEqual(len(mbr), 512)
        self.assertEqual(mbr.size, 512)

    def test_unpack(self):
        mbr = MBR()
        mbr.unpack(MBR_DATA)
        if sys.version_info >= (3, 0):
            self.assertEqual(mbr.signature[0], 85)
            self.assertEqual(mbr.signature[1], 170)
        else:
            self.assertEqual(mbr.signature[0], 'U')
            self.assertEqual(mbr.signature[1], b'\xaa')
        self.assertEqual(mbr.partitions[0].start.head, 0)
        self.assertEqual(mbr.partitions[0].end.head, 254)
        self.assertEqual(mbr.partitions[1].start_sect, 2168775)

    def test_pack(self):
        mbr = MBR(MBR_DATA)
        d = mbr.pack()
        self.assertEqual(MBR_DATA, d)
        mbr.partitions[3].start.head = 123
        d1 = mbr.pack()
        mbr1 = MBR(d1)
        self.assertEqual(mbr1.partitions[3].start.head, 123)

    def test_init(self):
        p = Position(head=254, sector=63, cyl=134)
        mbr = MBR(MBR_DATA)
        self.assertEqual(mbr.partitions[0].end, p)

    def test_none(self):
        mbr = MBR()
        self.assertEqual(mbr.partitions[0].end.sector, 0)
        mbr.unpack(None)
        self.assertEqual(mbr.partitions[0].end.head, 0)
        return

    def test_clear(self):
        mbr = MBR()
        mbr.unpack(MBR_DATA)
        self.assertEqual(mbr.partitions[0].end.head, 254)
        mbr.clear()
        self.assertEqual(mbr.partitions[0].end.head, 0)


if __name__ == '__main__':
    main()