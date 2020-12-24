# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\sboon\AppData\Local\Temp\pip-install-ptdbtr91\quarchpy\quarchpy\device\quarchArray.py
# Compiled at: 2020-03-25 05:10:07
# Size of source mod 2**32: 2820 bytes
from .device import quarchDevice

def isThisAnArrayController(moduleString):
    if 'QTL1079' in moduleString or 'QTL1461' in moduleString:
        return True
    return False


class quarchArray(quarchDevice):

    def __init__(self, baseDevice):
        self.ConType = baseDevice.ConType
        self.connectionObj = baseDevice.connectionObj

    def getSubDevice(self, port):
        return subDevice(self, port)

    def scanSubModules(self):
        moduleList = dict()
        responseText = self.sendCommand('conf:list:mod?')
        if responseText == '':
            return dict()
        responseList = responseText.split('\n')
        ConType = self.connectionObj.ConnTypeStr
        arrayConnTarget = self.connectionObj.ConnTarget
        if responseText.find('FAIL') == 0:
            raise ValueError('Invalid response from the array controller during sub-module scan')
            return
        for str in responseList:
            pos = str.find(':')
            strAddr = str[:pos]
            strResponse = str[pos + 1:]
            if 'FAIL' in strResponse:
                moduleList[ConType + ':???<' + strAddr + '>'] = 'Module failed to respond correctly to identity scan'
            else:
                subDevice = self.getSubDevice(strAddr)
                subSerial = subDevice.sendCommand('*serial?')
                if 'QTL' not in subSerial:
                    subSerial = 'QTL' + subSerial
                moduleList[ConType + ':' + arrayConnTarget + '<' + strAddr + '>'] = subSerial

        return moduleList


class subDevice(quarchDevice):

    def __init__(self, baseDevice, port):
        self.port = port
        self.connectionObj = baseDevice.connectionObj
        self.ConType = baseDevice.ConType
        self.baseDevice = baseDevice

    def sendCommand(self, CommandString, expectedResponse=True):
        portNumb = str(self.port)
        returnStr = ''
        respStr = quarchDevice.sendCommand(self, CommandString + ' <' + portNumb + '>')
        respLines = respStr.split('\n')
        for x in respLines:
            pos = x.find(':')
            lineNum = x[:pos]
            returnStr += x[pos + 1:].strip() + '\r\n'
            returnStr = returnStr.strip()

        return returnStr