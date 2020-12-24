# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.5/dist-packages/visionseed/YtDataLink.py
# Compiled at: 2019-07-24 01:04:26
# Size of source mod 2**32: 10054 bytes
from .YtMsg_pb2 import *

class YtDataLink:

    class YtDataLinkStatus:
        YT_DL_IDLE = 0
        YT_DL_LEN1_PENDING = 1
        YT_DL_LEN2_PENDING = 2
        YT_DL_LEN3_PENDING = 3
        YT_DL_LEN_CRC_H = 4
        YT_DL_LEN_CRC_L = 5
        YT_DL_DATA = 6
        YT_DL_CRC_H = 7
        YT_DL_CRC_L = 8

    SOF = 16
    TRANS = 17
    ytMsgSize = 2097152
    ccittTable = [
     0, 4129, 8258, 12387, 16516, 20645, 24774, 28903,
     33032, 37161, 41290, 45419, 49548, 53677, 57806, 61935,
     4657, 528, 12915, 8786, 21173, 17044, 29431, 25302,
     37689, 33560, 45947, 41818, 54205, 50076, 62463, 58334,
     9314, 13379, 1056, 5121, 25830, 29895, 17572, 21637,
     42346, 46411, 34088, 38153, 58862, 62927, 50604, 54669,
     13907, 9842, 5649, 1584, 30423, 26358, 22165, 18100,
     46939, 42874, 38681, 34616, 63455, 59390, 55197, 51132,
     18628, 22757, 26758, 30887, 2112, 6241, 10242, 14371,
     51660, 55789, 59790, 63919, 35144, 39273, 43274, 47403,
     23285, 19156, 31415, 27286, 6769, 2640, 14899, 10770,
     56317, 52188, 64447, 60318, 39801, 35672, 47931, 43802,
     27814, 31879, 19684, 23749, 11298, 15363, 3168, 7233,
     60846, 64911, 52716, 56781, 44330, 48395, 36200, 40265,
     32407, 28342, 24277, 20212, 15891, 11826, 7761, 3696,
     65439, 61374, 57309, 53244, 48923, 44858, 40793, 36728,
     37256, 33193, 45514, 41451, 53516, 49453, 61774, 57711,
     4224, 161, 12482, 8419, 20484, 16421, 28742, 24679,
     33721, 37784, 41979, 46042, 49981, 54044, 58239, 62302,
     689, 4752, 8947, 13010, 16949, 21012, 25207, 29270,
     46570, 42443, 38312, 34185, 62830, 58703, 54572, 50445,
     13538, 9411, 5280, 1153, 29798, 25671, 21540, 17413,
     42971, 47098, 34713, 38840, 59231, 63358, 50973, 55100,
     9939, 14066, 1681, 5808, 26199, 30326, 17941, 22068,
     55628, 51565, 63758, 59695, 39368, 35305, 47498, 43435,
     22596, 18533, 30726, 26663, 6336, 2273, 14466, 10403,
     52093, 56156, 60223, 64286, 35833, 39896, 43963, 48026,
     19061, 23124, 27191, 31254, 2801, 6864, 10931, 14994,
     64814, 60687, 56684, 52557, 48554, 44427, 40424, 36297,
     31782, 27655, 23652, 19525, 15522, 11395, 7392, 3265,
     61215, 65342, 53085, 57212, 44955, 49082, 36825, 40952,
     28183, 32310, 20053, 24180, 11923, 16050, 3793, 7920]

    def __init__(self, port):
        self.array = bytearray(0)
        self.cursor = 0
        self.mStatus = self.YtDataLinkStatus.YT_DL_IDLE
        self.mMsgLen = 0
        self.mCrc = 0
        self.mCrcCalc = 65535
        self.mTrans = False
        self.mCrcSendCalc = 65535
        self.port = port

    def crcUpdate(self, ch, first):
        if first:
            self.mCrcCalc = 65535
        self.mCrcCalc = self.ccittTable[((self.mCrcCalc >> 8 ^ ch) & 255)] ^ self.mCrcCalc << 8 & 65535

    def toHex(self, d):
        return format(d, '02X')

    def printBuf(self, buf):
        print(''.join('{:02x} '.format(x) for x in buf))

    def recvRunOnce(self):
        if len(self.array) < 10:
            buf = self.port.read(16)
            self.array += buf
        while len(self.array) > 0:
            ch = self.array.pop(0)
            if ch == self.SOF:
                if self.mStatus != self.YtDataLinkStatus.YT_DL_IDLE:
                    print('[YtMsg] unfinished pkg(%d/%d)', self.mBufi, self.mMsgLen)
                self.mStatus = self.YtDataLinkStatus.YT_DL_LEN1_PENDING
            else:
                if ch == self.TRANS:
                    self.mTrans = True
                else:
                    if self.mTrans:
                        ch = ch ^ self.TRANS
                        self.mTrans = False
                    if self.mStatus == self.YtDataLinkStatus.YT_DL_LEN1_PENDING:
                        self.mStatus = self.YtDataLinkStatus.YT_DL_LEN1_PENDING
                        self.mMsgLen = 0
                        self.mCrc = 0
                    if self.mStatus == self.YtDataLinkStatus.YT_DL_LEN1_PENDING or self.mStatus == self.YtDataLinkStatus.YT_DL_LEN2_PENDING or self.mStatus == self.YtDataLinkStatus.YT_DL_LEN3_PENDING:
                        self.crcUpdate(ch, self.mStatus == self.YtDataLinkStatus.YT_DL_LEN1_PENDING)
                        self.mMsgLen = self.mMsgLen << 8 | ch
                        if self.mStatus == self.YtDataLinkStatus.YT_DL_LEN3_PENDING and self.mMsgLen > self.ytMsgSize:
                            self.mStatus = self.YtDataLinkStatus.YT_DL_IDLE
                            continue
                            self.mStatus = self.mStatus + 1
                            continue
                            if self.mStatus == self.YtDataLinkStatus.YT_DL_LEN_CRC_H:
                                self.mCrc = self.mCrc << 8 | ch
                                self.mStatus = self.mStatus + 1
                                continue
                                if self.mStatus == self.YtDataLinkStatus.YT_DL_LEN_CRC_L:
                                    self.mCrc = self.mCrc << 8 | ch
                                    if self.mCrcCalc != self.mCrc:
                                        pass
                    print('[YtMsg] Error: msg len crc 0x%04x != 0x%04x\n', self.toHex(self.mCrcCalc), self.toHex(self.mCrc))
                    self.mStatus = self.YtDataLinkStatus.YT_DL_IDLE
                    continue
                    self.mStatus = self.mStatus + 1
                    self.mBuf = bytearray(self.mMsgLen)
                    self.mBufi = 0
                    self.array += self.port.read(self.mMsgLen)
                    continue
                    if self.mStatus == self.YtDataLinkStatus.YT_DL_DATA:
                        self.crcUpdate(ch, self.mBufi == 0)
                        self.mBuf[self.mBufi] = ch
                        self.mBufi += 1
                        if self.mBufi == self.mMsgLen:
                            self.mStatus = self.mStatus + 1
                        continue
                        if self.mStatus == self.YtDataLinkStatus.YT_DL_CRC_H:
                            self.mCrc = 0
                        if self.mStatus == self.YtDataLinkStatus.YT_DL_CRC_H or self.mStatus == self.YtDataLinkStatus.YT_DL_CRC_L:
                            pass
            self.mCrc = self.mCrc << 8 | ch
            if self.mStatus == self.YtDataLinkStatus.YT_DL_CRC_L:
                if self.mCrcCalc != self.mCrc:
                    print('[YtMsg] Error: msg crc 0x%04x != 0x%04x\n', self.toHex(self.mCrcCalc), self.toHex(self.mCrc))
                    self.mStatus = self.YtDataLinkStatus.YT_DL_IDLE
                    continue
                    self.mStatus = self.YtDataLinkStatus.YT_DL_IDLE
                    target = YtMsg()
                    target.ParseFromString(self.mBuf)
                    return target
                self.mStatus = self.mStatus + 1
                continue

    def sendYtMsg(self, msg):
        data = msg.SerializeToString()
        self.write(data)

    def crcSendUpdate(self, ch, first=False):
        if first:
            self.mCrcSendCalc = 65535
        self.mCrcSendCalc = self.ccittTable[((self.mCrcSendCalc >> 8 ^ ch) & 255)] ^ self.mCrcSendCalc << 8 & 65535

    def write(self, data):
        buf = bytearray(len(data) + 8)
        buf[0] = 16
        buf[1] = len(data) >> 16 & 255
        buf[2] = len(data) >> 8 & 255
        buf[3] = len(data) >> 0 & 255
        self.crcSendUpdate(buf[1], True)
        self.crcSendUpdate(buf[2])
        self.crcSendUpdate(buf[3])
        buf[4] = self.mCrcSendCalc >> 8 & 255
        buf[5] = self.mCrcSendCalc >> 0 & 255
        buf[6:] = data
        buf.append(0)
        buf.append(0)
        transLen = 0
        for i in range(1, len(buf)):
            if i >= 6 and i < len(buf) - 2:
                self.crcSendUpdate(buf[i], i == 6)
            if buf[i] == 16 or buf[i] == 17:
                transLen += 1

        buf[len(buf) - 2] = self.mCrcSendCalc >> 8 & 255
        buf[len(buf) - 1] = self.mCrcSendCalc >> 0 & 255
        for i in range(len(buf) - 2, len(buf)):
            if buf[i] == 16 or buf[i] == 17:
                transLen += 1

        idx = 0
        transedBuffer = bytearray(len(buf) + transLen)
        for i in range(0, len(buf)):
            if (buf[i] == 16 or buf[i] == 17) and i > 0:
                transedBuffer[idx] = 17
                idx += 1
                transedBuffer[idx] = buf[i] ^ 17
                idx += 1
            else:
                transedBuffer[idx] = buf[i]
                idx += 1

        self.port.write(transedBuffer)