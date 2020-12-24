# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/instrumentino/controllers/arduino/tecan.py
# Compiled at: 2015-11-23 10:12:58
from __future__ import division
from instrumentino.controllers.arduino import SysCompArduino
from collections import OrderedDict
__author__ = 'yoelk'
from instrumentino import cfg

class TecanSia(SysCompArduino):
    strokeToSeconds = OrderedDict({'N1': {0: 1.25, 1: 1.3, 
              2: 1.39, 
              3: 1.52, 
              4: 1.71, 
              5: 1.97, 
              6: 2.37, 
              7: 2.77, 
              8: 3.03, 
              9: 3.36, 
              10: 3.77, 
              11: 4.3, 
              12: 5.0, 
              13: 6.0, 
              14: 7.5, 
              15: 10.0, 
              16: 15.0, 
              17: 30.0, 
              18: 31.58, 
              19: 33.33, 
              20: 35.29, 
              21: 37.5, 
              22: 40.0, 
              23: 42.86, 
              24: 46.15, 
              25: 50.0, 
              26: 54.55, 
              27: 60.0, 
              28: 66.67, 
              29: 75.0, 
              30: 85.71, 
              31: 100.0, 
              32: 120.0, 
              33: 150.0, 
              34: 200.0, 
              35: 300.0, 
              36: 333.33, 
              37: 375.0, 
              38: 428.57, 
              39: 500.0, 
              40: 600.0}, 
       'N2': {}})
    DtCmdStart = '/'
    DtCmdEnd = '\r'
    DtCmdExecute = 'R'
    serialBaudrate = 9600
    pumpMaxMicroSteps = 48000

    def __init__(self, name, pumpVolumeMiliLit, addressPump, addressMultivalve, pinRx=None, pinTx=None, serialPort=1):
        SysCompArduino.__init__(self, 'SIA', (), 'send commands to the SIA')
        self.serialPort = serialPort
        if pinRx != None and pinTx != None:
            self.pinRx = pinRx
            self.pinTx = pinTx
            self.useSoftSer = True
        else:
            self.useSoftSer = False
        self.pumpVolumeMiliLit = pumpVolumeMiliLit
        self.addressPump = addressPump
        self.addressMultivalve = addressMultivalve
        return

    def sendCommand(self, address, command, waitForAnswerSec=None):
        self.GetController().SerSend(self.DtCmdStart + address + command + self.DtCmdExecute + self.DtCmdEnd, waitForAnswerSec, self.useSoftSer, self.serialPort)

    def miliLitToMicroSteps(self, miliLit):
        return str(int(miliLit * self.pumpMaxMicroSteps / self.pumpVolumeMiliLit))

    def InitPumpAndMultivalve(self, pumpInitCmd='N1ZJ0', valveInitCmd='ZJ0'):
        self.sendCommand(self.addressPump, pumpInitCmd, waitForAnswerSec=3)
        self.sendCommand(self.addressMultivalve, valveInitCmd, waitForAnswerSec=1)

    def selectMultivalvePort(self, port, moveDirection='O', waitForAnswerSec=1):
        self.sendCommand(self.addressMultivalve, moveDirection + str(port), waitForAnswerSec)

    def _pullOrDispenseAtMultivalvePort(self, pullOrDispense, port, miliLit, speed, moveDirection, waitForAnswerSec):
        self.selectMultivalvePort(port, moveDirection, waitForAnswerSec)
        volumeFraction = miliLit / self.pumpVolumeMiliLit
        speedIndex = self.speedToSecondsPerStrokeIndex(speed)
        self.sendCommand(self.addressPump, 'OS' + str(speedIndex) + 'M1000' + pullOrDispense + self.miliLitToMicroSteps(miliLit), self.strokeToSeconds['N1'][speedIndex] * volumeFraction + 2)

    def _pullOrDispenseAtPumpInputPort(self, pullOrDispense, miliLit, speed):
        volumeFraction = miliLit / self.pumpVolumeMiliLit
        speedIndex = self.speedToSecondsPerStrokeIndex(speed)
        self.sendCommand(self.addressPump, 'IS' + str(speedIndex) + 'M1000' + pullOrDispense + self.miliLitToMicroSteps(miliLit), self.strokeToSeconds['N1'][speedIndex] * volumeFraction + 2)

    def pullFromMultivalvePort(self, port, miliLit, speed, moveDirection='I', waitForAnswerSec=1):
        self._pullOrDispenseAtMultivalvePort('P', port, miliLit, speed, moveDirection, waitForAnswerSec)

    def dispenseToMultivalvePort(self, port, miliLit, speed, moveDirection='I', waitForAnswerSec=1):
        self._pullOrDispenseAtMultivalvePort('D', port, miliLit, speed, moveDirection, waitForAnswerSec)

    def pullFromPumpInputPort(self, miliLit, speed):
        self._pullOrDispenseAtPumpInputPort('P', miliLit, speed)

    def dispenseToPumpInputPort(self, miliLit, speed):
        self._pullOrDispenseAtPumpInputPort('D', miliLit, speed)

    def TransferFromInputToMultivalvePort(self, port, miliLit, speed, moveDirection='I', waitForAnswerSec=1):
        self.selectMultivalvePort(port, moveDirection, waitForAnswerSec)
        volumeFraction = miliLit * 2 / self.pumpVolumeMiliLit
        speedIndex = self.speedToSecondsPerStrokeIndex(speed)
        self.sendCommand(self.addressPump, 'IS' + str(speedIndex) + 'M1000P' + self.miliLitToMicroSteps(miliLit) + 'OD' + self.miliLitToMicroSteps(miliLit), self.strokeToSeconds['N1'][speedIndex] * volumeFraction + 2)

    def FirstTimeOnline(self):
        if self.useSoftSer:
            self.GetController().SoftSerConnect(self.pinRx, self.pinTx, self.serialBaudrate, self.serialPort)
        else:
            self.GetController().HardSerConnect(self.serialBaudrate, self.serialPort)
        return super(TecanSia, self).FirstTimeOnline()

    def speedToSecondsPerStrokeIndex(self, microLitPerSec, microstepMode='N1'):
        miliLitPerSec = microLitPerSec / 1000
        secPerStroke = 1 / (miliLitPerSec / self.pumpVolumeMiliLit)
        for indexString, val in self.strokeToSeconds[microstepMode].items():
            if secPerStroke < val:
                return indexString

        return self.strokeToSeconds[microstepMode].keys()[(-1)]