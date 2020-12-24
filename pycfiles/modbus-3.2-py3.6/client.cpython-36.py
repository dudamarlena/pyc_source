# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/modbus/client.py
# Compiled at: 2019-04-30 09:28:26
# Size of source mod 2**32: 2077 bytes
import socket
from array import array
from struct import unpack, pack
from math import ceil
__all__ = [
 'client', 'fc']

def fc():
    print('Supported Function Codes:\n\t1 = Read Coils or Digital Outputs\n\t2 = Read Digital Inputs\n\t3 = Read Holding Registers\n\t4 = Read Input Registers\n\t5 = Write Single Coil\n\t6 = Write Single Register\n\t15 = Write Coils or Digital Outputs\n\t16 = Write Holding Registers')


class client:

    def __init__(self, host='localhost', unit=1):
        self.host = host
        self.unit = unit
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, 502))
        self.TID = 0

    def read(self, FC=4, ADR=0, LEN=10):
        if FC not in (1, 2, 3, 4):
            return fc()
        else:
            lADR = ADR & 255
            mADR = ADR >> 8
            lLEN = LEN & 255
            mLEN = LEN >> 8
            if FC < 3:
                BYT = ceil(LEN / 8)
            else:
                BYT = LEN * 2
            if self.TID < 255:
                self.TID = self.TID + 1
            else:
                self.TID = 1
            cmd = array('B', [0, self.TID, 0, 0, 0, 6,
             self.unit, FC, mADR, lADR, mLEN, lLEN])
            self.sock.send(cmd)
            buf = array('B', [0] * (BYT + 9))
            self.sock.recv_into(buf)
            if FC > 2:
                return unpack('>' + 'H' * LEN, buf[9:9 + BYT])
            return unpack('B' * BYT, buf[9:9 + BYT])

    def write(self, *DAT, FC=16, ADR=0):
        if FC not in (5, 6, 15, 16):
            return fc()
        else:
            lADR = ADR & 255
            mADR = ADR >> 8
            VAL = b''
            for i in DAT:
                VAL = VAL + pack('>H', i)

            if FC == 5 or FC == 6:
                VAL = VAL[0:2]
            if FC == 5 or FC == 15:
                LEN = len(VAL) * 8
            else:
                LEN = len(VAL) // 2
            lLEN = LEN & 255
            mLEN = LEN >> 8
            if self.TID < 255:
                self.TID = self.TID + 1
            else:
                self.TID = 1
            if FC == 6:
                cmd = array('B', [0, self.TID, 0, 0, 0, 6, self.unit, FC, mADR, lADR])
            else:
                cmd = array('B', [0, self.TID, 0, 0, 0, 7 + len(VAL), self.unit, FC, mADR, lADR, mLEN, lLEN, len(VAL)])
        cmd.extend(VAL)
        buffer = array('B', [0] * 20)
        print('Sent', cmd)
        self.sock.send(cmd)
        self.sock.recv_into(buffer)