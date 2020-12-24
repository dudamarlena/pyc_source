# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/Labtools/MCP4728_class.py
# Compiled at: 2015-06-18 01:11:18
from commands_proto import *
import I2C_class

class MCP4728:
    defaultVDD = 3300
    RESET = 6
    WAKEUP = 9
    UPDATE = 8
    WRITEALL = 64
    WRITEONE = 88
    SEQWRITE = 80
    VREFWRITE = 128
    GAINWRITE = 192
    POWERDOWNWRITE = 160
    GENERALCALL = 0

    def __init__(self, H, vref=3.3, devid=0):
        self.devid = devid
        self.addr = 96 | self.devid
        self.H = H
        self.I2C = I2C_class.I2C(self.H)
        self.SWITCHEDOFF = [0, 0, 0, 0]
        self.VREFS = [0, 0, 0, 0]
        self.VRANGES = [[0.0, 3.3], [0.0, 3.3], [-3.3, 3.3], [-5.0, 5.0]]

    def setVoltage(self, chan, v):
        R = self.VRANGES[chan]
        v = int(4095 * (v - R[0]) / (R[1] - R[0]))
        return self.__setRawVoltage__(chan, v)

    def __setRawVoltage__(self, chan, v):
        """
                self.I2C.start(self.addr,0)
                self.I2C.send(self.WRITEONE | (chan << 1))
                self.I2C.send(self.VREFS[chan] << 7 | self.SWITCHEDOFF[chan] << 5 | 1 << 4 | (v>>8)&0xF )
                self.I2C.send(v&0xFF)
                self.I2C.stop()
                """
        self.H.__sendByte__(DAC)
        self.H.__sendByte__(SET_DAC)
        self.H.__sendByte__(self.addr << 1)
        self.H.__sendByte__(chan)
        self.H.__sendInt__(self.VREFS[chan] << 15 | self.SWITCHEDOFF[chan] << 13 | 4096 | v)
        self.H.__get_ack__()
        R = self.VRANGES[chan]
        return (R[1] - R[0]) * v / 4095.0 + R[0]

    def __writeall__(self, v1, v2, v3, v4):
        self.I2C.start(self.addr, 0)
        self.I2C.send(v1 >> 8 & 15)
        self.I2C.send(v1 & 255)
        self.I2C.send(v2 >> 8 & 15)
        self.I2C.send(v2 & 255)
        self.I2C.send(v3 >> 8 & 15)
        self.I2C.send(v3 & 255)
        self.I2C.send(v4 >> 8 & 15)
        self.I2C.send(v4 & 255)
        self.I2C.stop()

    def stat(self):
        self.I2C.start(self.addr, 0)
        self.I2C.send(0)
        self.I2C.restart(self.addr, 1)
        vals = self.I2C.read(24)
        self.I2C.stop()
        print vals