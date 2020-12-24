# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\sboon\AppData\Local\Temp\pip-install-ptdbtr91\quarchpy\quarchpy\device\quarchPPM.py
# Compiled at: 2020-03-25 05:10:07
# Size of source mod 2**32: 2726 bytes
from .device import quarchDevice

class quarchPPM(quarchDevice):

    def __init__(self, originObj):
        self.connectionObj = originObj.connectionObj
        self.ConString = originObj.ConString
        self.ConType = originObj.ConType
        numb_colons = self.ConString.count(':')
        if numb_colons == 1:
            self.ConString = self.ConString.replace(':', '::')

    def startStream(self, fileName='streamData.txt', fileMaxMB=2000, streamName='Stream With No Name', streamAverage=None, releaseOnData=False, separator=','):
        return self.connectionObj.qis.startStream(self.ConString, fileName, fileMaxMB, streamName, streamAverage, releaseOnData, separator)

    def streamRunningStatus(self):
        return self.connectionObj.qis.streamRunningStatus(self.ConString)

    def streamBufferStatus(self):
        return self.connectionObj.qis.streamBufferStatus(self.ConString)

    def streamInterrupt(self):
        return self.connectionObj.qis.streamInterrupt()

    def waitStop(self):
        return self.connectionObj.qis.waitStop()

    def streamResampleMode(self, streamCom):
        if streamCom.lower() == 'off' or streamCom[0:-2].isdigit():
            return self.connectionObj.qis.sendAndReceiveCmd(cmd=('stream mode resample ' + streamCom.lower()), device=(self.ConString))
        return 'Invalid resampling argument. Valid options are: off, [x]ms or [x]us.'

    def stopStream(self):
        return self.connectionObj.qis.stopStream(self.ConString)

    def setupPowerOutput(myModule):
        if 'DISABLED' in myModule.sendCommand('config:output Mode?'):
            try:
                drive_voltage = raw_input('\n Either using an HD without an intelligent fixture or an XLC.\n \n>>> Please select a voltage [3V3, 5V]: ') or '3V3' or '5V'
            except NameError:
                drive_voltage = input('\n Either using an HD without an intelligent fixture or an XLC.\n \n>>> Please select a voltage [3V3, 5V]: ') or '3V3' or '5V'

            myModule.sendCommand('config:output:mode:' + drive_voltage)
        powerState = myModule.sendCommand('run power?')
        if 'OFF' in powerState:
            (print('\n Turning the outputs on:'), myModule.sendCommand('run:power up'), '!')