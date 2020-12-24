# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\sboon\AppData\Local\Temp\pip-install-ptdbtr91\quarchpy\quarchpy\calibration\keithley_2460_control.py
# Compiled at: 2020-03-25 05:10:07
# Size of source mod 2**32: 20733 bytes
import socket, time, logging, os, sys
from quarchpy.calibration.deviceHelpers import locateMdnsInstr
from quarchpy.user_interface import *

def listCalInstruments(scanDictionary):
    if not scanDictionary:
        print('No instruments found to display')
    else:
        x = 1
        for k, v in scanDictionary.items():
            ip = k
            if 'Keithley 2460 ' in v[:14]:
                id = v[:14] + '\t' + v[14:].split('.')[0]
            else:
                id = v
            print(str(x) + ' - ' + id + '\t' + ip)
            x += 1


def userSelectCalInstrument(scanDictionary=None, scanFilterStr=None, title=None, message=None, tableHeaders=None, additionalOptions=None, nice=False):
    originalOptions = additionalOptions
    if User_interface.instance != None:
        if User_interface.instance.selectedInterface == 'testcenter':
            nice = False
    if message is None:
        message = 'Select the calibration instrument to use:'
    if title is None:
        title = 'Select a calibration instrument'
    while True:
        if scanDictionary is None:
            printText('Scanning for instruments...')
            scanDictionary = foundDevices = locateMdnsInstr(scanFilterStr)
        deviceList = []
        if nice:
            if additionalOptions is None:
                additionalOptions = [
                 'Rescan', 'Quit']
            elif not scanDictionary:
                deviceList.append(['No instruments found to display'])
            else:
                for k, v in scanDictionary.items():
                    ip = k
                    if 'Keithley 2460 ' in v[:14]:
                        name = v[:14]
                        serialNo = v[14:].split('.')[0]
                        deviceList.append([name, serialNo, ip])
                    else:
                        id = v
                        deviceList.append([ip + '=' + id + ' ' + ip])

            adOp = []
            for option in additionalOptions:
                adOp.append([option] * 3)

            userStr = listSelection(title=title, message=message, selectionList=deviceList, tableHeaders=['Name', 'Serial', 'IP Address'], nice=nice, indexReq=True, additionalOptions=adOp)[3]
        else:
            if not scanDictionary:
                deviceList.append('1=No instruments found to display')
            else:
                x = 1
                for k, v in scanDictionary.items():
                    ip = k
                    if 'Keithley 2460 ' in v[:14]:
                        id = v[:14] + '\t' + v[14:].split('.')[0]
                    else:
                        id = v
                    deviceList.append(ip + '=' + id + '\t' + ip)
                    x += 1

            if additionalOptions is None:
                additionalOptions = 'Rescan=Rescan,Quit=Quit'
            deviceList = ','.join(deviceList)
            userStr = listSelection(title=title, message=message, selectionList=deviceList, additionalOptions=additionalOptions)
        if userStr == 'q' or userStr.lower() in 'quit':
            printText('User Quit Program')
            sys.exit(0)
        elif userStr == 'r' or userStr.lower() in 'rescan':
            scanDictionary = None
            additionalOptions = originalOptions
        else:
            return userStr


class keithley2460:
    __doc__ = '\n    Static method to locate available instruments. Returns disctionary, "IP_ADDRESS:DESCRIPTION-TEXT"\n    '

    @staticmethod
    def locateDevices():
        pass

    def __init__(self, connectionString):
        self.conString = connectionString
        self.connection = None
        self.idnString = 'MODEL 2460'
        self.BUFFER_SIZE = 1024
        self.TIMEOUT = 5

    def openConnection(self, connectionString=None):
        if connectionString is not None:
            self.conString = connectionString
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.settimeout(self.TIMEOUT)
        self.connection.connect((self.conString, 5025))
        response = self.sendCommand('*RST')
        response = self.sendCommandQuery('*IDN?')
        if response.find(self.idnString) == -1:
            raise ValueError('Connected device does not appear to be a keithley2460')

    def closeConnection(self):
        self.connection.close()

    def closeDeadConnections(self):
        deadSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        deadSocket.settimeout(self.TIMEOUT)
        deadSocket.connect((self.conString, 5030))
        deadSocket.close()

    def sendCommandQuery(self, commandString):
        retries = 1
        while retries < 5:
            try:
                logging.debug(os.path.basename(__file__) + ': sending command: ' + commandString)
                self.connection.send((commandString + '\r\n').encode('latin-1'))
                resultStr = self.connection.recv(self.BUFFER_SIZE).decode('utf-8')
                logging.debug(os.path.basename(__file__) + ': received: ' + resultStr)
                resultStr = resultStr.strip('\r\n\t')
                if resultStr is None:
                    if self.getStatusEavFlag() == True:
                        errorStr = self.getNextError()
                        self.clearErrors()
                        raise ValueError('Keithley query command did not run correctly: ' + errorStr)
                    else:
                        raise ValueError('The Keithley did not return a response')
                return resultStr
            except socket.timeout:
                logging.debug(os.path.basename(__file__) + ': keithley command timed out: ' + commandString + ', closing connection and retrying')
                self.closeDeadConnections()
                self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.connection.settimeout(self.TIMEOUT)
                self.connection.connect((self.conString, 5025))
                retries = retries + 1

        raise TimeoutError(os.path.basename(__file__) + ': timed out while expecting a response')

    def sendCommand(self, commandString, expectedResponse=True):
        retries = 1
        while retries < 5:
            try:
                logging.debug(os.path.basename(__file__) + ': sending command: ' + commandString)
                self.connection.send((commandString + '\r\n').encode('latin-1'))
                if self.getStatusEavFlag() == True:
                    errorStr = self.getNextError()
                    self.clearErrors()
                    return errorStr
                return 'OK'
            except socket.timeout:
                logging.debug(os.path.basename(__file__) + ': keithley command timed out: ' + commandString + ', closing connection and retrying')
                self.closeDeadConnections()
                self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.connection.settimeout(self.TIMEOUT)
                self.connection.connect((self.conString, 5025))
                retries = retries + 1

        raise TimeoutError(os.path.basename(__file__) + ': timed out while sending command to Keithley')

    def reset(self):
        result = self.sendCommand('*RST')
        return result

    def setOutputEnable(self, enableState):
        if enableState == True:
            result = self.sendCommand('OUTP ON')
        else:
            result = self.sendCommand('OUTP OFF')
        return result

    def getOutputEnable(self):
        result = self.sendCommandQuery('OUTP?')
        if int(result) == 1:
            return True
        return False

    def setLoadVoltageLimit(self, voltValue):
        return self.sendCommand('SOUR:CURR:VLIM ' + str(voltValue))

    def getLoadVoltageLimit(self):
        result = self.sendCommandQuery('SOUR:CURR:VLIM?')
        return float(result)

    def setOutputMode(self, modeString):
        modeString = modeString.upper()
        if modeString in ('HIMP', 'NORMAL', 'ZERO'):
            return self.sendCommand('OUTP:CURR:SMOD ' + modeString)
        raise ValueError('Invalid mode type specified: ' + modeString)

    def getOutputMode(self):
        return self.sendCommandQuery('OUTP:CURR:SMOD?')

    def setMeasurementMode(self, measModeString):
        measModeString = measModeString.upper()
        if measModeString == 'VOLT':
            result = self.sendCommand('SENS:FUNC "VOLT"')
        else:
            if measModeString == 'CURR':
                result = self.sendCommand('SENS:FUNC "CURR"')
            else:
                raise ValueError('Invalid mode type specified: ' + measModeString)
        return result

    def getMeasurementMode(self):
        return self.sendCommandQuery('SENS:FUNC?').strip('"')

    def setSourceMode(self, sourceModeString):
        sourceModeString = sourceModeString.upper()
        if sourceModeString in ('VOLT', 'CURR'):
            result = self.sendCommand('SOUR:FUNC ' + sourceModeString)
        else:
            raise ValueError('Invalid mode type specified: ' + sourceModeString)
        return result

    def getSourceMode(self):
        return self.sendCommandQuery('SOUR:FUNC?')

    def setAverageVoltageCount(self, measCount=1):
        self.sendCommand('VOLT:AVER:COUNT ' + str(measCount))
        self.sendCommand('VOLT:AVER ON')

    def setAverageCurrentCount(self, measCount=1):
        self.sendCommand('CURR:AVER:COUNT ' + str(measCount))
        self.sendCommand('CURR:AVER ON')

    def setLoadCurrent(self, ampValue):
        if ampValue <= 0:
            ampValue = -ampValue
        return self.sendCommand('SOUR:CURR -' + str(ampValue))

    def setLoadCurrentLimit(self, ampValue):
        return self.sendCommand('SOUR:VOLT:ILIM ' + str(ampValue))

    def getLoadCurrentLimit(self):
        return self.sendCommandQuery('SOUR:VOLT:ILIM?')

    def getLoadCurrent(self):
        result = float(self.sendCommandQuery('SOUR:CURR?'))
        return -result

    def measureLoadCurrent(self, count=4):
        self.setAverageCurrentCount(count)
        result = float(self.sendCommandQuery('MEAS:CURR?'))
        return -result

    def setLoadVoltage(self, voltValue):
        return self.sendCommand('SOUR:VOLT ' + str(voltValue))

    def getLoadVoltage(self):
        result = float(self.sendCommandQuery('SOUR:VOLT?'))
        return result

    def measureLoadVoltage(self, count=4):
        self.setAverageVoltageCount(count)
        result = float(self.sendCommandQuery('MEAS:VOLT?'))
        return result

    def getStatusByte(self):
        resultStr = self.sendCommandQuery('*STB?')
        try:
            statInt = int(resultStr)
            return statInt
        except:
            resultStr = self.sendCommandQuery('*STB?')

        try:
            statInt = int(resultStr)
            return statInt
        except:
            raise ValueError('Keithley is not responding with valid data')

    def printInstrumentStatus(self):
        stat = self.getStatusByte()
        if stat & 1 != 0:
            print('Measurement Summary Flag Set')
        if stat & 2 != 0:
            print('Reserved Flag 1 Set')
        if stat & 4 != 0:
            print('Error Available Flag Set')
        if stat & 8 != 0:
            print('Questionable Event Flag Set')
        if stat & 16 != 0:
            print('Message Available Flag Set')
        if stat & 32 != 0:
            print('Enabled Standard Event Flag Set')
        if stat & 64 != 0:
            print('Enabled Summary Bit Flag Set')
        if stat & 128 != 0:
            print('Enabled Operation event Flag Set')
        if stat == 0:
            print('Status flags are clear')

    def getStatusMsbFlag(self):
        stat = self.getStatusByte()
        if stat & 1 != 0:
            return True
        return False

    def getStatusQsbFlag(self):
        stat = self.getStatusByte()
        if stat & 8 != 0:
            return True
        return False

    def getStatusEavFlag(self):
        stat = self.getStatusByte()
        if stat & 4 != 0:
            return True
        return False

    def getNextError(self):
        errorStr = self.sendCommandQuery('SYSTem:ERRor:NEXT?')
        return errorStr

    def clearErrors(self):
        self.sendCommand(':SYSTem:CLEar')

    def measureNoLoadVoltage(self):
        self.setSourceMode('CURR')
        self.setLoadCurrent(0)
        self.setLoadVoltageLimit(15)
        self.setOutputEnable(True)
        return self.measureLoadVoltage()

    def setReferenceCurrent(self, value):
        if value >= 0:
            self.setSourceMode('CURR')
            self.setLoadVoltageLimit(15)
            self.setOutputEnable(True)
            self.setLoadCurrent(value)
        else:
            raise ValueError('negative load current requested')

    def setReferenceVoltage(self, value):
        if value >= 0:
            self.setSourceMode('VOLT')
            self.setLoadCurrentLimit('1e-1')
            self.setLoadVoltageLimit(15)
            self.setOutputEnable(True)
            self.setLoadVoltage(value)
        else:
            raise ValueError('negative voltage requested')

    def disable(self):
        self.setOutputEnable(False)
        self.setLoadCurrent(0)