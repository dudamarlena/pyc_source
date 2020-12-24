# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: C:\Work\Python\workplace\pypsd\pypsd\base.py
# Compiled at: 2009-08-05 08:34:04
import unittest, logging, os.path
from ps_parser import PSParser
module_logger = logging.getLogger('pypsd.sectionbase')
INFINITY = 'infinity'
ZERO = 0
MINUS_ZERO = 0

def bytesToInt(bytes):
    shift = 0
    value = 0
    bb = reversed(bytes)
    for b in bb:
        b = ord(b)
        value += b << shift
        shift += 8

    module_logger.debug('bytesToInt method. In: %s, out: %s' % (bytes, value))
    return value


def int2Binary(n):
    """convert integer n to binary string bStr"""
    bStr = ''
    if n < 0:
        raise ValueError('must be a positive integer')
    if n == 0:
        return '0'
    while n > 0:
        bStr = str(n % 2) + bStr
        n = n >> 1

    return bStr


def makeEven(n):
    if n & 1 != 0:
        n += 1
    return n


class PSDParserBase(object):

    def __init__(self, stream=None, psd=None):
        self.logger = logging.getLogger('pypsd.base.PSDParserBase')
        self.debugMethodInOut('__init__')
        if stream is None:
            raise BaseException('File object should be specified.')
        self.stream = stream
        self.psd = psd
        self.SIGNATURE = '8BPS'
        self.SIGNATIRE_8BIM = '8BIM'
        self.VERSION = 1
        self.CHANNELS_RANGE = [1, 56]
        self.SIZE_RANGE = [1, 30000]
        self.DEPTH_LIST = [1, 8, 16]
        self.OPACITY_RANGE = [0, 255]
        self.parse()
        return

    def parse(self):
        pass

    def skip(self, size):
        self.stream.seek(size, 1)
        self.debugMethodInOut('skip', {'size': size})

    def readUnicodeString(self):
        charsNumber = self.readInt()
        unicode_string = ''
        for i in range(charsNumber):
            char_code = self.readShortInt()
            if char_code > 0:
                unicode_string += unichr(char_code)

        return unicode_string

    def skipIntSize(self):
        size = self.readInt()
        self.skip(size)
        self.debugMethodInOut('skipIntSize', result='skipped=%s' % size)

    def readCustomInt(self, size, negative=False):
        bb = self.stream.read(size)
        value = bytesToInt(bb)
        if negative:
            if value > pow(2, size * 8 - 1):
                value = int(-(pow(2, size * 8) - value))
        self.debugMethodInOut('readCustomInt', {'size': size}, result=value)
        return value

    def readDouble(self):
        b1 = self.readInt(4)
        b2 = self.readInt(4)
        long = b1 << 32 | b2
        signbit = long >> 63
        expan = long >> 52 & 2047
        if expan >= 2047:
            return INFINITY
        elif expan == 0:
            return ZERO
        elif expan == 2048:
            return MINUS_ZERO
        signif = (long & 4503599627370495 | 4503599627370496) * pow(2, -52)
        return pow(-1, signbit) * pow(2, expan - 1023) * signif

    def readInt(self, returnEven=False, isLong=True):
        value = self.readCustomInt(4, negative=not isLong)
        if returnEven:
            value = makeEven(value)
        self.debugMethodInOut('readInt', result=value)
        return value

    def readShortInt(self):
        value = self.readCustomInt(2, negative=True)
        self.debugMethodInOut('readShortInt', result=value)
        return value

    def readTinyInt(self):
        tinyInt = self.readCustomInt(1)
        self.debugMethodInOut('readTinyInt', result=tinyInt)
        return tinyInt

    def readBytesList(self, size):
        bytesRead = self.stream.read(size)
        self.logger.debug('Bytes read: %s' % bytesRead)
        result = [ ord(b) for b in bytesRead ]
        self.debugMethodInOut('readBits', {'size': size}, result)
        return result

    def readBits(self, size):
        i = self.readCustomInt(size)
        bits = [ int(b) for b in int2Binary(i) ]
        bits.reverse()
        moreZeros = size * 8 - len(bits)
        bits = bits + [0] * moreZeros
        self.debugMethodInOut('readBits', {'size': size}, bits)
        return bits

    def readPascalString(self):
        size = self.readTinyInt()
        if size == 0:
            self.skip(1)
            return ''
        else:
            size = size & 255
            size = (size + 1 + 3 & -4) - 1
            name = self.readString(size)
        return name

    def readString(self, size):
        dataRead = self.stream.read(size)
        value = str(dataRead)
        value = ('').join([ s for s in value if ord(s) != 0 ])
        self.debugMethodInOut('readString', {'size': size}, value)
        return value

    def getSize(self):
        return os.path.getsize(self.stream.name)

    def getRectangle(self):
        top = self.readInt(isLong=False)
        left = self.readInt(isLong=False)
        bottom = self.readInt(isLong=False)
        right = self.readInt(isLong=False)
        width = right - left
        height = bottom - top
        return {'top': top, 'left': left, 'bottom': bottom, 'right': right, 'width': width, 
           'height': height}

    def getPos(self):
        return self.stream.tell()

    def skipRest(self, blockStart, blockSize):
        toSkip = blockStart + blockSize - self.getPos()
        self.skip(toSkip)

    def getCodeLabelPair(self, code, map):
        return {'code': code, 'label': map[code]}

    def debugMethodInOut(self, label, invars={}, result=None):
        message = '%s method.' % label
        if invars:
            invars = [ '%s=%s' % (name, invars[name]) for name in invars ]
            message += 'In: %s' % (', ').join(invars)
        if result:
            message += ' Out: %s' % result
        self.logger.debug(message)

    def readOsType(self):
        descriptor = {}
        value = None
        osType = self.readString(4)
        if osType == 'TEXT':
            value = self.readUnicodeString()
        elif osType == 'enum':
            typeID = self.readLengthWithString()
            enum = self.readLengthWithString()
            value = {'typeID': typeID, 'enum': enum}
        elif osType in ('Objc', 'GlbO'):
            typeID = self.readLengthWithString()
            enum = self.readLengthWithString()
            value = {'typeID': typeID, 'enum': enum}
        elif osType == 'VlLs':
            list_size = self.readInt()
            value = []
            for k in range(list_size):
                value.append(self.readOsType())

        elif osType == 'doub':
            value = self.readDouble()
        elif osType == 'UntF':
            unitType = self.readString(4)
            unitValue = self.readDouble()
            value = {'type': unitType, 'value': unitValue}
        elif osType == 'long':
            value = self.readInt()
        elif osType == 'bool':
            value = self.readBoolean()
        elif osType in ('type', 'GlbC'):
            name = self.readUnicodeString()
            classID = self.readLengthWithString()
            value = {'name': name, 'classID': classID}
        elif osType == 'alis':
            data_length = self.readInt()
            value = self.readString(data_length)
        elif osType == 'obj ':
            obj_items_num = self.readInt()
            for j in range(obj_items_num):
                ref_obj_type = self.readString(4)
                if ref_obj_type == 'prop':
                    name = self.readUnicodeString()
                    classID = self.readLengthWithString()
                    keyID = self.readLengthWithString()
                elif ref_obj_type == 'Clss':
                    name = self.readUnicodeString()
                    classID = self.readLengthWithString()
                elif ref_obj_type == 'Enmr':
                    name = self.readUnicodeString()
                    classID = self.readLengthWithString()
                    typeID = self.readLengthWithString()
                    enum = self.readLengthWithString()
                elif ref_obj_type == 'rele':
                    name = self.readUnicodeString()
                    classID = self.readLengthWithString()
                    offsetValue = self.readInt()
                elif ref_obj_type == 'Idnt':
                    pass
                elif ref_obj_type == 'indx':
                    pass
                elif ref_obj_type == 'name':
                    pass

        elif osType == 'tdta':
            data_length = self.readInt()
            pos = self.getPos()
            data_string = self.readString(data_length)
            p = PSParser(source=data_string)
            value = p.parse()
            self.skipRest(pos, data_length)
        return {'type': osType, 'value': value}

    def readDescriptorStructure(self):
        name_from_classID = self.readUnicodeString()
        classID = self.readLengthWithString()
        items_num = self.readInt()
        descriptors = {}
        for i in range(items_num):
            txt_key = self.readLengthWithString().strip()
            descriptors[txt_key] = self.readOsType()

        return descriptors

    def readBoolean(self):
        byte = self.readTinyInt()
        return byte != 0

    def readLengthWithString(self, default_length=4):
        length = self.readInt()
        if length == 0:
            value = self.readString(default_length)
        else:
            value = self.readString(length)
        return value


class PSDBaseTest(unittest.TestCase):

    def testBytesToInt(self):
        value1 = bytesToInt('\x00\x01\x02\x03')
        self.failUnlessEqual(66051, value1)
        value2 = bytesToInt(b'\xff\x14*\x10')
        self.failUnlessEqual(4279511568, value2)

    def testReadCustomInt(self):
        from base import PSDParserBase
        from StringIO import StringIO
        stream = StringIO()
        stream.write(b'\xff\xff\xff\xfe')
        stream.write(b'\xff\xff\xff\xff')
        stream.write(b'\xf0\x00\x00\x00')
        stream.write(b'\xff\xff\xff\xfe')
        stream.write(b'\x0f\xff')
        stream.write(b'\xc0\x00\x00\x00\x00\x00\x00\x00')
        stream.write('@\x00\x00\x00\x00\x00\x00\x00')
        stream.write(b'?\xf0\x00\x00\x00\x00\x00\x02')
        stream.write(b'\x7f\xf0\x00\x00\x00\x00\x00\x00')
        stream.write('\x00\x00\x00\x00\x00\x00\x00\x00')
        stream.write(b'\x80\x00\x00\x00\x00\x00\x00\x00')
        stream.seek(0)
        p = PSDParserBase(stream)
        assert p.readCustomInt(4) == 4294967294
        assert p.readCustomInt(4, negative=True) == -1
        assert p.readCustomInt(4, negative=True) == -268435456
        assert p.readCustomInt(4, negative=True) == -2
        assert p.readCustomInt(2, negative=True) == 4095
        d1 = p.readDouble()
        d2 = p.readDouble()
        d3 = p.readDouble()
        infinity = p.readDouble()
        zero = p.readDouble()
        minuszero = p.readDouble()
        assert d1 == -2
        assert d2 == 2
        assert d3 == 1.0000000000000004
        assert d3 != 1.0000000000000007
        assert infinity == INFINITY
        assert zero == ZERO
        assert minuszero == MINUS_ZERO


if __name__ == '__main__':
    unittest.main()