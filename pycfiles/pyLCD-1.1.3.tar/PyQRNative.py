# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mezgrman/projects/pyLCD/pylcd/PyQRNative.py
# Compiled at: 2015-08-08 07:02:10
import math
from PIL import Image, ImageDraw

class QR8bitByte():

    def __init__(self, data):
        self.mode = QRMode.MODE_8BIT_BYTE
        self.data = data

    def getLength(self):
        return len(self.data)

    def write(self, buffer):
        for i in range(len(self.data)):
            buffer.put(ord(self.data[i]), 8)

    def __repr__(self):
        return self.data


class QRCode():

    def __init__(self, typeNumber, errorCorrectLevel):
        self.typeNumber = typeNumber
        self.errorCorrectLevel = errorCorrectLevel
        self.modules = None
        self.moduleCount = 0
        self.dataCache = None
        self.dataList = []
        return

    def addData(self, data):
        newData = QR8bitByte(data)
        self.dataList.append(newData)
        self.dataCache = None
        return

    def isDark(self, row, col):
        if row < 0 or self.moduleCount <= row or col < 0 or self.moduleCount <= col:
            raise Exception('%s,%s - %s' % (row, col, self.moduleCount))
        return self.modules[row][col]

    def getModuleCount(self):
        return self.moduleCount

    def make(self):
        self.makeImpl(False, self.getBestMaskPattern())

    def makeImpl(self, test, maskPattern):
        self.moduleCount = self.typeNumber * 4 + 17
        self.modules = [ None for x in range(self.moduleCount) ]
        for row in range(self.moduleCount):
            self.modules[row] = [ None for x in range(self.moduleCount) ]
            for col in range(self.moduleCount):
                self.modules[row][col] = None

        self.setupPositionProbePattern(0, 0)
        self.setupPositionProbePattern(self.moduleCount - 7, 0)
        self.setupPositionProbePattern(0, self.moduleCount - 7)
        self.setupPositionAdjustPattern()
        self.setupTimingPattern()
        self.setupTypeInfo(test, maskPattern)
        if self.typeNumber >= 7:
            self.setupTypeNumber(test)
        if self.dataCache == None:
            self.dataCache = QRCode.createData(self.typeNumber, self.errorCorrectLevel, self.dataList)
        self.mapData(self.dataCache, maskPattern)
        return

    def setupPositionProbePattern(self, row, col):
        for r in range(-1, 8):
            if row + r <= -1 or self.moduleCount <= row + r:
                continue
            for c in range(-1, 8):
                if col + c <= -1 or self.moduleCount <= col + c:
                    continue
                if 0 <= r and r <= 6 and (c == 0 or c == 6) or 0 <= c and c <= 6 and (r == 0 or r == 6) or 2 <= r and r <= 4 and 2 <= c and c <= 4:
                    self.modules[(row + r)][col + c] = True
                else:
                    self.modules[(row + r)][col + c] = False

    def getBestMaskPattern(self):
        minLostPoint = 0
        pattern = 0
        for i in range(8):
            self.makeImpl(True, i)
            lostPoint = QRUtil.getLostPoint(self)
            if i == 0 or minLostPoint > lostPoint:
                minLostPoint = lostPoint
                pattern = i

        return pattern

    def createMovieClip(self):
        raise Exception('Method not relevant to Python port')

    def makeImage(self):
        boxsize = 10
        offset = 4
        pixelsize = (self.getModuleCount() + offset + offset) * boxsize
        im = Image.new('RGB', (pixelsize, pixelsize), 'white')
        d = ImageDraw.Draw(im)
        for r in range(self.getModuleCount()):
            for c in range(self.getModuleCount()):
                if self.isDark(r, c):
                    x = (c + offset) * boxsize
                    y = (r + offset) * boxsize
                    b = [(x, y), (x + boxsize, y + boxsize)]
                    d.rectangle(b, fill='black')

        del d
        return im

    def setupTimingPattern(self):
        for r in range(8, self.moduleCount - 8):
            if self.modules[r][6] != None:
                continue
            self.modules[r][6] = r % 2 == 0

        for c in range(8, self.moduleCount - 8):
            if self.modules[6][c] != None:
                continue
            self.modules[6][c] = c % 2 == 0

        return

    def setupPositionAdjustPattern(self):
        pos = QRUtil.getPatternPosition(self.typeNumber)
        for i in range(len(pos)):
            for j in range(len(pos)):
                row = pos[i]
                col = pos[j]
                if self.modules[row][col] != None:
                    continue
                for r in range(-2, 3):
                    for c in range(-2, 3):
                        if r == -2 or r == 2 or c == -2 or c == 2 or r == 0 and c == 0:
                            self.modules[(row + r)][col + c] = True
                        else:
                            self.modules[(row + r)][col + c] = False

        return

    def setupTypeNumber(self, test):
        bits = QRUtil.getBCHTypeNumber(self.typeNumber)
        for i in range(18):
            mod = not test and bits >> i & 1 == 1
            self.modules[(i // 3)][i % 3 + self.moduleCount - 8 - 3] = mod

        for i in range(18):
            mod = not test and bits >> i & 1 == 1
            self.modules[(i % 3 + self.moduleCount - 8 - 3)][i // 3] = mod

    def setupTypeInfo(self, test, maskPattern):
        data = self.errorCorrectLevel << 3 | maskPattern
        bits = QRUtil.getBCHTypeInfo(data)
        for i in range(15):
            mod = not test and bits >> i & 1 == 1
            if i < 6:
                self.modules[i][8] = mod
            elif i < 8:
                self.modules[(i + 1)][8] = mod
            else:
                self.modules[(self.moduleCount - 15 + i)][8] = mod

        for i in range(15):
            mod = not test and bits >> i & 1 == 1
            if i < 8:
                self.modules[8][self.moduleCount - i - 1] = mod
            elif i < 9:
                self.modules[8][15 - i - 1 + 1] = mod
            else:
                self.modules[8][15 - i - 1] = mod

        self.modules[(self.moduleCount - 8)][8] = not test

    def mapData(self, data, maskPattern):
        inc = -1
        row = self.moduleCount - 1
        bitIndex = 7
        byteIndex = 0
        for col in range(self.moduleCount - 1, 0, -2):
            if col == 6:
                col -= 1
            while True:
                for c in range(2):
                    if self.modules[row][(col - c)] == None:
                        dark = False
                        if byteIndex < len(data):
                            dark = data[byteIndex] >> bitIndex & 1 == 1
                        mask = QRUtil.getMask(maskPattern, row, col - c)
                        if mask:
                            dark = not dark
                        self.modules[row][col - c] = dark
                        bitIndex -= 1
                        if bitIndex == -1:
                            byteIndex += 1
                            bitIndex = 7

                row += inc
                if row < 0 or self.moduleCount <= row:
                    row -= inc
                    inc = -inc
                    break

        return

    PAD0 = 236
    PAD1 = 17

    @staticmethod
    def createData(typeNumber, errorCorrectLevel, dataList):
        rsBlocks = QRRSBlock.getRSBlocks(typeNumber, errorCorrectLevel)
        buffer = QRBitBuffer()
        for i in range(len(dataList)):
            data = dataList[i]
            buffer.put(data.mode, 4)
            buffer.put(data.getLength(), QRUtil.getLengthInBits(data.mode, typeNumber))
            data.write(buffer)

        totalDataCount = 0
        for i in range(len(rsBlocks)):
            totalDataCount += rsBlocks[i].dataCount

        if buffer.getLengthInBits() > totalDataCount * 8:
            raise Exception('code length overflow. (' + buffer.getLengthInBits() + '>' + totalDataCount * 8 + ')')
        if buffer.getLengthInBits() + 4 <= totalDataCount * 8:
            buffer.put(0, 4)
        while buffer.getLengthInBits() % 8 != 0:
            buffer.putBit(False)

        while True:
            if buffer.getLengthInBits() >= totalDataCount * 8:
                break
            buffer.put(QRCode.PAD0, 8)
            if buffer.getLengthInBits() >= totalDataCount * 8:
                break
            buffer.put(QRCode.PAD1, 8)

        return QRCode.createBytes(buffer, rsBlocks)

    @staticmethod
    def createBytes(buffer, rsBlocks):
        offset = 0
        maxDcCount = 0
        maxEcCount = 0
        dcdata = [ 0 for x in range(len(rsBlocks)) ]
        ecdata = [ 0 for x in range(len(rsBlocks)) ]
        for r in range(len(rsBlocks)):
            dcCount = rsBlocks[r].dataCount
            ecCount = rsBlocks[r].totalCount - dcCount
            maxDcCount = max(maxDcCount, dcCount)
            maxEcCount = max(maxEcCount, ecCount)
            dcdata[r] = [ 0 for x in range(dcCount) ]
            for i in range(len(dcdata[r])):
                dcdata[r][i] = 255 & buffer.buffer[(i + offset)]

            offset += dcCount
            rsPoly = QRUtil.getErrorCorrectPolynomial(ecCount)
            rawPoly = QRPolynomial(dcdata[r], rsPoly.getLength() - 1)
            modPoly = rawPoly.mod(rsPoly)
            ecdata[r] = [ 0 for x in range(rsPoly.getLength() - 1) ]
            for i in range(len(ecdata[r])):
                modIndex = i + modPoly.getLength() - len(ecdata[r])
                if modIndex >= 0:
                    ecdata[r][i] = modPoly.get(modIndex)
                else:
                    ecdata[r][i] = 0

        totalCodeCount = 0
        for i in range(len(rsBlocks)):
            totalCodeCount += rsBlocks[i].totalCount

        data = [ None for x in range(totalCodeCount) ]
        index = 0
        for i in range(maxDcCount):
            for r in range(len(rsBlocks)):
                if i < len(dcdata[r]):
                    data[index] = dcdata[r][i]
                    index += 1

        for i in range(maxEcCount):
            for r in range(len(rsBlocks)):
                if i < len(ecdata[r]):
                    data[index] = ecdata[r][i]
                    index += 1

        return data


class QRMode():
    MODE_NUMBER = 1
    MODE_ALPHA_NUM = 2
    MODE_8BIT_BYTE = 4
    MODE_KANJI = 8


class QRErrorCorrectLevel():
    L = 1
    M = 0
    Q = 3
    H = 2


class QRMaskPattern():
    PATTERN000 = 0
    PATTERN001 = 1
    PATTERN010 = 2
    PATTERN011 = 3
    PATTERN100 = 4
    PATTERN101 = 5
    PATTERN110 = 6
    PATTERN111 = 7


class QRUtil(object):
    PATTERN_POSITION_TABLE = [[],
     [
      6, 18],
     [
      6, 22],
     [
      6, 26],
     [
      6, 30],
     [
      6, 34],
     [
      6, 22, 38],
     [
      6, 24, 42],
     [
      6, 26, 46],
     [
      6, 28, 50],
     [
      6, 30, 54],
     [
      6, 32, 58],
     [
      6, 34, 62],
     [
      6, 26, 46, 66],
     [
      6, 26, 48, 70],
     [
      6, 26, 50, 74],
     [
      6, 30, 54, 78],
     [
      6, 30, 56, 82],
     [
      6, 30, 58, 86],
     [
      6, 34, 62, 90],
     [
      6, 28, 50, 72, 94],
     [
      6, 26, 50, 74, 98],
     [
      6, 30, 54, 78, 102],
     [
      6, 28, 54, 80, 106],
     [
      6, 32, 58, 84, 110],
     [
      6, 30, 58, 86, 114],
     [
      6, 34, 62, 90, 118],
     [
      6, 26, 50, 74, 98, 122],
     [
      6, 30, 54, 78, 102, 126],
     [
      6, 26, 52, 78, 104, 130],
     [
      6, 30, 56, 82, 108, 134],
     [
      6, 34, 60, 86, 112, 138],
     [
      6, 30, 58, 86, 114, 142],
     [
      6, 34, 62, 90, 118, 146],
     [
      6, 30, 54, 78, 102, 126, 150],
     [
      6, 24, 50, 76, 102, 128, 154],
     [
      6, 28, 54, 80, 106, 132, 158],
     [
      6, 32, 58, 84, 110, 136, 162],
     [
      6, 26, 54, 82, 110, 138, 166],
     [
      6, 30, 58, 86, 114, 142, 170]]
    G15 = 1024 | 256 | 32 | 16 | 4 | 2 | 1
    G18 = 4096 | 2048 | 1024 | 512 | 256 | 32 | 4 | 1
    G15_MASK = 16384 | 4096 | 1024 | 16 | 2

    @staticmethod
    def getBCHTypeInfo(data):
        d = data << 10
        while QRUtil.getBCHDigit(d) - QRUtil.getBCHDigit(QRUtil.G15) >= 0:
            d ^= QRUtil.G15 << QRUtil.getBCHDigit(d) - QRUtil.getBCHDigit(QRUtil.G15)

        return (data << 10 | d) ^ QRUtil.G15_MASK

    @staticmethod
    def getBCHTypeNumber(data):
        d = data << 12
        while QRUtil.getBCHDigit(d) - QRUtil.getBCHDigit(QRUtil.G18) >= 0:
            d ^= QRUtil.G18 << QRUtil.getBCHDigit(d) - QRUtil.getBCHDigit(QRUtil.G18)

        return data << 12 | d

    @staticmethod
    def getBCHDigit(data):
        digit = 0
        while data != 0:
            digit += 1
            data >>= 1

        return digit

    @staticmethod
    def getPatternPosition(typeNumber):
        return QRUtil.PATTERN_POSITION_TABLE[(typeNumber - 1)]

    @staticmethod
    def getMask(maskPattern, i, j):
        if maskPattern == QRMaskPattern.PATTERN000:
            return (i + j) % 2 == 0
        if maskPattern == QRMaskPattern.PATTERN001:
            return i % 2 == 0
        if maskPattern == QRMaskPattern.PATTERN010:
            return j % 3 == 0
        if maskPattern == QRMaskPattern.PATTERN011:
            return (i + j) % 3 == 0
        if maskPattern == QRMaskPattern.PATTERN100:
            return (math.floor(i / 2) + math.floor(j / 3)) % 2 == 0
        if maskPattern == QRMaskPattern.PATTERN101:
            return i * j % 2 + i * j % 3 == 0
        if maskPattern == QRMaskPattern.PATTERN110:
            return (i * j % 2 + i * j % 3) % 2 == 0
        if maskPattern == QRMaskPattern.PATTERN111:
            return (i * j % 3 + (i + j) % 2) % 2 == 0
        raise Exception('bad maskPattern:' + maskPattern)

    @staticmethod
    def getErrorCorrectPolynomial(errorCorrectLength):
        a = QRPolynomial([1], 0)
        for i in range(errorCorrectLength):
            a = a.multiply(QRPolynomial([1, QRMath.gexp(i)], 0))

        return a

    @staticmethod
    def getLengthInBits(mode, type):
        if 1 <= type and type < 10:
            if mode == QRMode.MODE_NUMBER:
                return 10
            if mode == QRMode.MODE_ALPHA_NUM:
                return 9
            if mode == QRMode.MODE_8BIT_BYTE:
                return 8
            if mode == QRMode.MODE_KANJI:
                return 8
            raise Exception('mode:' + mode)
        elif type < 27:
            if mode == QRMode.MODE_NUMBER:
                return 12
            if mode == QRMode.MODE_ALPHA_NUM:
                return 11
            if mode == QRMode.MODE_8BIT_BYTE:
                return 16
            if mode == QRMode.MODE_KANJI:
                return 10
            raise Exception('mode:' + mode)
        elif type < 41:
            if mode == QRMode.MODE_NUMBER:
                return 14
            if mode == QRMode.MODE_ALPHA_NUM:
                return 13
            if mode == QRMode.MODE_8BIT_BYTE:
                return 16
            if mode == QRMode.MODE_KANJI:
                return 12
            raise Exception('mode:' + mode)
        else:
            raise Exception('type:' + type)

    @staticmethod
    def getLostPoint(qrCode):
        moduleCount = qrCode.getModuleCount()
        lostPoint = 0
        for row in range(moduleCount):
            for col in range(moduleCount):
                sameCount = 0
                dark = qrCode.isDark(row, col)
                for r in range(-1, 2):
                    if row + r < 0 or moduleCount <= row + r:
                        continue
                    for c in range(-1, 2):
                        if col + c < 0 or moduleCount <= col + c:
                            continue
                        if r == 0 and c == 0:
                            continue
                        if dark == qrCode.isDark(row + r, col + c):
                            sameCount += 1

                if sameCount > 5:
                    lostPoint += 3 + sameCount - 5

        for row in range(moduleCount - 1):
            for col in range(moduleCount - 1):
                count = 0
                if qrCode.isDark(row, col):
                    count += 1
                if qrCode.isDark(row + 1, col):
                    count += 1
                if qrCode.isDark(row, col + 1):
                    count += 1
                if qrCode.isDark(row + 1, col + 1):
                    count += 1
                if count == 0 or count == 4:
                    lostPoint += 3

        for row in range(moduleCount):
            for col in range(moduleCount - 6):
                if qrCode.isDark(row, col) and not qrCode.isDark(row, col + 1) and qrCode.isDark(row, col + 2) and qrCode.isDark(row, col + 3) and qrCode.isDark(row, col + 4) and not qrCode.isDark(row, col + 5) and qrCode.isDark(row, col + 6):
                    lostPoint += 40

        for col in range(moduleCount):
            for row in range(moduleCount - 6):
                if qrCode.isDark(row, col) and not qrCode.isDark(row + 1, col) and qrCode.isDark(row + 2, col) and qrCode.isDark(row + 3, col) and qrCode.isDark(row + 4, col) and not qrCode.isDark(row + 5, col) and qrCode.isDark(row + 6, col):
                    lostPoint += 40

        darkCount = 0
        for col in range(moduleCount):
            for row in range(moduleCount):
                if qrCode.isDark(row, col):
                    darkCount += 1

        ratio = abs(100 * darkCount / moduleCount / moduleCount - 50) / 5
        lostPoint += ratio * 10
        return lostPoint


class QRMath():

    @staticmethod
    def glog(n):
        if n < 1:
            raise Exception('glog(' + n + ')')
        return LOG_TABLE[n]

    @staticmethod
    def gexp(n):
        while n < 0:
            n += 255

        while n >= 256:
            n -= 255

        return EXP_TABLE[n]


EXP_TABLE = [ x for x in range(256) ]
LOG_TABLE = [ x for x in range(256) ]
for i in range(8):
    EXP_TABLE[i] = 1 << i

for i in range(8, 256):
    EXP_TABLE[i] = EXP_TABLE[(i - 4)] ^ EXP_TABLE[(i - 5)] ^ EXP_TABLE[(i - 6)] ^ EXP_TABLE[(i - 8)]

for i in range(255):
    LOG_TABLE[EXP_TABLE[i]] = i

class QRPolynomial():

    def __init__(self, num, shift):
        if len(num) == 0:
            raise Exception(num.length + '/' + shift)
        offset = 0
        while offset < len(num) and num[offset] == 0:
            offset += 1

        self.num = [ 0 for x in range(len(num) - offset + shift) ]
        for i in range(len(num) - offset):
            self.num[i] = num[(i + offset)]

    def get(self, index):
        return self.num[index]

    def getLength(self):
        return len(self.num)

    def multiply(self, e):
        num = [ 0 for x in range(self.getLength() + e.getLength() - 1) ]
        for i in range(self.getLength()):
            for j in range(e.getLength()):
                num[(i + j)] ^= QRMath.gexp(QRMath.glog(self.get(i)) + QRMath.glog(e.get(j)))

        return QRPolynomial(num, 0)

    def mod(self, e):
        if self.getLength() - e.getLength() < 0:
            return self
        ratio = QRMath.glog(self.get(0)) - QRMath.glog(e.get(0))
        num = [ 0 for x in range(self.getLength()) ]
        for i in range(self.getLength()):
            num[i] = self.get(i)

        for i in range(e.getLength()):
            num[i] ^= QRMath.gexp(QRMath.glog(e.get(i)) + ratio)

        return QRPolynomial(num, 0).mod(e)


class QRRSBlock():
    RS_BLOCK_TABLE = [
     [
      1, 26, 19],
     [
      1, 26, 16],
     [
      1, 26, 13],
     [
      1, 26, 9],
     [
      1, 44, 34],
     [
      1, 44, 28],
     [
      1, 44, 22],
     [
      1, 44, 16],
     [
      1, 70, 55],
     [
      1, 70, 44],
     [
      2, 35, 17],
     [
      2, 35, 13],
     [
      1, 100, 80],
     [
      2, 50, 32],
     [
      2, 50, 24],
     [
      4, 25, 9],
     [
      1, 134, 108],
     [
      2, 67, 43],
     [
      2, 33, 15, 2, 34, 16],
     [
      2, 33, 11, 2, 34, 12],
     [
      2, 86, 68],
     [
      4, 43, 27],
     [
      4, 43, 19],
     [
      4, 43, 15],
     [
      2, 98, 78],
     [
      4, 49, 31],
     [
      2, 32, 14, 4, 33, 15],
     [
      4, 39, 13, 1, 40, 14],
     [
      2, 121, 97],
     [
      2, 60, 38, 2, 61, 39],
     [
      4, 40, 18, 2, 41, 19],
     [
      4, 40, 14, 2, 41, 15],
     [
      2, 146, 116],
     [
      3, 58, 36, 2, 59, 37],
     [
      4, 36, 16, 4, 37, 17],
     [
      4, 36, 12, 4, 37, 13],
     [
      2, 86, 68, 2, 87, 69],
     [
      4, 69, 43, 1, 70, 44],
     [
      6, 43, 19, 2, 44, 20],
     [
      6, 43, 15, 2, 44, 16],
     [
      4, 101, 81],
     [
      1, 80, 50, 4, 81, 51],
     [
      4, 50, 22, 4, 51, 23],
     [
      3, 36, 12, 8, 37, 13],
     [
      2, 116, 92, 2, 117, 93],
     [
      6, 58, 36, 2, 59, 37],
     [
      4, 46, 20, 6, 47, 21],
     [
      7, 42, 14, 4, 43, 15],
     [
      4, 133, 107],
     [
      8, 59, 37, 1, 60, 38],
     [
      8, 44, 20, 4, 45, 21],
     [
      12, 33, 11, 4, 34, 12],
     [
      3, 145, 115, 1, 146, 116],
     [
      4, 64, 40, 5, 65, 41],
     [
      11, 36, 16, 5, 37, 17],
     [
      11, 36, 12, 5, 37, 13],
     [
      5, 109, 87, 1, 110, 88],
     [
      5, 65, 41, 5, 66, 42],
     [
      5, 54, 24, 7, 55, 25],
     [
      11, 36, 12],
     [
      5, 122, 98, 1, 123, 99],
     [
      7, 73, 45, 3, 74, 46],
     [
      15, 43, 19, 2, 44, 20],
     [
      3, 45, 15, 13, 46, 16],
     [
      1, 135, 107, 5, 136, 108],
     [
      10, 74, 46, 1, 75, 47],
     [
      1, 50, 22, 15, 51, 23],
     [
      2, 42, 14, 17, 43, 15],
     [
      5, 150, 120, 1, 151, 121],
     [
      9, 69, 43, 4, 70, 44],
     [
      17, 50, 22, 1, 51, 23],
     [
      2, 42, 14, 19, 43, 15],
     [
      3, 141, 113, 4, 142, 114],
     [
      3, 70, 44, 11, 71, 45],
     [
      17, 47, 21, 4, 48, 22],
     [
      9, 39, 13, 16, 40, 14],
     [
      3, 135, 107, 5, 136, 108],
     [
      3, 67, 41, 13, 68, 42],
     [
      15, 54, 24, 5, 55, 25],
     [
      15, 43, 15, 10, 44, 16],
     [
      4, 144, 116, 4, 145, 117],
     [
      17, 68, 42],
     [
      17, 50, 22, 6, 51, 23],
     [
      19, 46, 16, 6, 47, 17],
     [
      2, 139, 111, 7, 140, 112],
     [
      17, 74, 46],
     [
      7, 54, 24, 16, 55, 25],
     [
      34, 37, 13],
     [
      4, 151, 121, 5, 152, 122],
     [
      4, 75, 47, 14, 76, 48],
     [
      11, 54, 24, 14, 55, 25],
     [
      16, 45, 15, 14, 46, 16],
     [
      6, 147, 117, 4, 148, 118],
     [
      6, 73, 45, 14, 74, 46],
     [
      11, 54, 24, 16, 55, 25],
     [
      30, 46, 16, 2, 47, 17],
     [
      8, 132, 106, 4, 133, 107],
     [
      8, 75, 47, 13, 76, 48],
     [
      7, 54, 24, 22, 55, 25],
     [
      22, 45, 15, 13, 46, 16],
     [
      10, 142, 114, 2, 143, 115],
     [
      19, 74, 46, 4, 75, 47],
     [
      28, 50, 22, 6, 51, 23],
     [
      33, 46, 16, 4, 47, 17],
     [
      8, 152, 122, 4, 153, 123],
     [
      22, 73, 45, 3, 74, 46],
     [
      8, 53, 23, 26, 54, 24],
     [
      12, 45, 15, 28, 46, 16],
     [
      3, 147, 117, 10, 148, 118],
     [
      3, 73, 45, 23, 74, 46],
     [
      4, 54, 24, 31, 55, 25],
     [
      11, 45, 15, 31, 46, 16],
     [
      7, 146, 116, 7, 147, 117],
     [
      21, 73, 45, 7, 74, 46],
     [
      1, 53, 23, 37, 54, 24],
     [
      19, 45, 15, 26, 46, 16],
     [
      5, 145, 115, 10, 146, 116],
     [
      19, 75, 47, 10, 76, 48],
     [
      15, 54, 24, 25, 55, 25],
     [
      23, 45, 15, 25, 46, 16],
     [
      13, 145, 115, 3, 146, 116],
     [
      2, 74, 46, 29, 75, 47],
     [
      42, 54, 24, 1, 55, 25],
     [
      23, 45, 15, 28, 46, 16],
     [
      17, 145, 115],
     [
      10, 74, 46, 23, 75, 47],
     [
      10, 54, 24, 35, 55, 25],
     [
      19, 45, 15, 35, 46, 16],
     [
      17, 145, 115, 1, 146, 116],
     [
      14, 74, 46, 21, 75, 47],
     [
      29, 54, 24, 19, 55, 25],
     [
      11, 45, 15, 46, 46, 16],
     [
      13, 145, 115, 6, 146, 116],
     [
      14, 74, 46, 23, 75, 47],
     [
      44, 54, 24, 7, 55, 25],
     [
      59, 46, 16, 1, 47, 17],
     [
      12, 151, 121, 7, 152, 122],
     [
      12, 75, 47, 26, 76, 48],
     [
      39, 54, 24, 14, 55, 25],
     [
      22, 45, 15, 41, 46, 16],
     [
      6, 151, 121, 14, 152, 122],
     [
      6, 75, 47, 34, 76, 48],
     [
      46, 54, 24, 10, 55, 25],
     [
      2, 45, 15, 64, 46, 16],
     [
      17, 152, 122, 4, 153, 123],
     [
      29, 74, 46, 14, 75, 47],
     [
      49, 54, 24, 10, 55, 25],
     [
      24, 45, 15, 46, 46, 16],
     [
      4, 152, 122, 18, 153, 123],
     [
      13, 74, 46, 32, 75, 47],
     [
      48, 54, 24, 14, 55, 25],
     [
      42, 45, 15, 32, 46, 16],
     [
      20, 147, 117, 4, 148, 118],
     [
      40, 75, 47, 7, 76, 48],
     [
      43, 54, 24, 22, 55, 25],
     [
      10, 45, 15, 67, 46, 16],
     [
      19, 148, 118, 6, 149, 119],
     [
      18, 75, 47, 31, 76, 48],
     [
      34, 54, 24, 34, 55, 25],
     [
      20, 45, 15, 61, 46, 16]]

    def __init__(self, totalCount, dataCount):
        self.totalCount = totalCount
        self.dataCount = dataCount

    @staticmethod
    def getRSBlocks(typeNumber, errorCorrectLevel):
        rsBlock = QRRSBlock.getRsBlockTable(typeNumber, errorCorrectLevel)
        if rsBlock == None:
            raise Exception('bad rs block @ typeNumber:' + typeNumber + '/errorCorrectLevel:' + errorCorrectLevel)
        length = len(rsBlock) / 3
        list = []
        for i in range(length):
            count = rsBlock[(i * 3 + 0)]
            totalCount = rsBlock[(i * 3 + 1)]
            dataCount = rsBlock[(i * 3 + 2)]
            for j in range(count):
                list.append(QRRSBlock(totalCount, dataCount))

        return list

    @staticmethod
    def getRsBlockTable(typeNumber, errorCorrectLevel):
        if errorCorrectLevel == QRErrorCorrectLevel.L:
            return QRRSBlock.RS_BLOCK_TABLE[((typeNumber - 1) * 4 + 0)]
        else:
            if errorCorrectLevel == QRErrorCorrectLevel.M:
                return QRRSBlock.RS_BLOCK_TABLE[((typeNumber - 1) * 4 + 1)]
            else:
                if errorCorrectLevel == QRErrorCorrectLevel.Q:
                    return QRRSBlock.RS_BLOCK_TABLE[((typeNumber - 1) * 4 + 2)]
                if errorCorrectLevel == QRErrorCorrectLevel.H:
                    return QRRSBlock.RS_BLOCK_TABLE[((typeNumber - 1) * 4 + 3)]
                return

            return


class QRBitBuffer():

    def __init__(self):
        self.buffer = []
        self.length = 0

    def __repr__(self):
        return ('.').join([ str(n) for n in self.buffer ])

    def get(self, index):
        bufIndex = math.floor(index / 8)
        val = self.buffer[bufIndex] >> 7 - index % 8 & 1 == 1
        print 'get ', val
        return self.buffer[bufIndex] >> 7 - index % 8 & 1 == 1

    def put(self, num, length):
        for i in range(length):
            self.putBit(num >> length - i - 1 & 1 == 1)

    def getLengthInBits(self):
        return self.length

    def putBit(self, bit):
        bufIndex = self.length // 8
        if len(self.buffer) <= bufIndex:
            self.buffer.append(0)
        if bit:
            self.buffer[bufIndex] |= 128 >> self.length % 8
        self.length += 1