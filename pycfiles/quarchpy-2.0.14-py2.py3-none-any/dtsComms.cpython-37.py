# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\sboon\AppData\Local\Temp\pip-install-ptdbtr91\quarchpy\quarchpy\disk_test\dtsComms.py
# Compiled at: 2020-03-25 05:10:07
# Size of source mod 2**32: 8726 bytes
import platform, time, socket, threading
from datetime import datetime
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
import quarchpy.disk_test.dtsGlobals as dtsGlobals

class DTSCommms:

    def __init__(self):
        self.standardHeader = 'QuarchCSSelection'
        self.versionNumber = '1.01'

    def newNotifyChoiceOption(self, type, dict, dictValue, moduleType=None, outputMode=None):
        sendString = ''
        if type == 'qpsmodule':
            sendString = self.createXMLSelectionModule(dict, dictValue, outputMode, itemType='qpsmodule')
        elif type == 'module':
            sendString = self.createXMLSelectionModule(dict, dictValue)
        else:
            if 'drive' in type:
                sendString = self.createXMLSelectionDrive(dict, dictValue, moduleType)
        sendString = 'QuarchDTS::' + sendString
        self.sendMsgToGUI(sendString)

    def sendMsgToGUI(self, toSend, timeToWait=5):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((dtsGlobals.GUI_TCP_IP, 9921))
        toSend = str.encode(toSend)
        s.sendall(toSend + b'\n')
        if timeToWait is None:
            timeToWait = 999999
        self.processTimeoutAndResult(s, timeToWait)
        s.close()

    def processTimeoutAndResult(self, socket, timeToWait):
        processObject = threading.Thread(target=(self.getReturnPacket(socket)))
        processObject.start()
        start = time.time()
        while 1:
            if time.time() - start <= timeToWait:
                if processObject.is_alive():
                    time.sleep(0.1)
                else:
                    break
        else:
            processObject.terminate()
            processObject.join()

    def getReturnPacket(self, socket):
        BUFFER_SIZE = 4096
        data = ''
        while 1:
            data = socket.recv(BUFFER_SIZE)
            if 'OK' in bytes.decode(data):
                if 'QCSVersion' in bytes.decode(data):
                    dtsGlobals.QCSVersionValid = self.isVersionCompat(bytes.decode(data))
                break
            if 'choiceResponse' in bytes.decode(data):
                dtsGlobals.choiceResponse = data
                break
            if 'STOP' in bytes.decode(data):
                dtsGlobals.continueTest = False
                break
            if 'INVALID VERSION' in bytes.decode(data):
                dtsGlobals.validVersion = False
                break

    def isVersionCompat(self, data):
        versionNumber = data.split('=')
        if versionNumber == dtsGlobals.minQCSVersion:
            return True
        versionNumbers = versionNumber[1].split('.')
        minVersionNumbers = dtsGlobals.minQCSVersion.split('.')
        for i, number in enumerate(versionNumbers):
            if versionNumbers[i] > minVersionNumbers[i]:
                return True
                if versionNumbers[i] < minVersionNumbers[i]:
                    return False
                if i == len(versionNumbers) - 1 and versionNumbers[i] == minVersionNumbers[i]:
                    return True

        return True

    def createXMLSelectionDrive(self, key, values, driveType):
        top = Element(self.standardHeader)
        retString = ''
        if 'pcie' in driveType:
            child = SubElement(top, 'Name')
            child.text = str(values['vendor'])
            child = SubElement(top, 'Standard')
            child.text = str(key)
            child = SubElement(top, 'ConnType')
            child.text = str('PCIe')
            child = SubElement(top, 'Description')
            child.text = str(values['device'])
            child = SubElement(top, 'XmlVersion')
            child.text = str(self.versionNumber)
            child = SubElement(top, 'itemType')
            child.text = str('Drive')
        else:
            if 'sas' in driveType:
                if platform.system() == 'Windows':
                    child = SubElement(top, 'Name')
                    child.text = str(values['model'])
                    child = SubElement(top, 'Standard')
                    child.text = str(key)
                    child = SubElement(top, 'ConnType')
                    child.text = str('SAS')
                    child = SubElement(top, 'itemType')
                    child.text = str('Drive')
                    child = SubElement(top, 'XmlVersion')
                    child.text = str(self.versionNumber)
                else:
                    child = SubElement(top, 'Name')
                    child.text = str(values['vendor'])
                    child = SubElement(top, 'Standard')
                    child.text = str(key)
                    child = SubElement(top, 'ConnType')
                    child.text = str('SAS')
                    child = SubElement(top, 'Description')
                    child.text = str(values['model'] + ', ' + values['size'])
                    child = SubElement(top, 'itemType')
                    child.text = str('Drive')
                    child = SubElement(top, 'XmlVersion')
                    child.text = str(self.versionNumber)
            retString = bytes.decode(tostring(top))
            return retString

    def createXMLSelectionModule(self, dict, dictValue, outputMode=None, itemType='Module'):
        top = Element(self.standardHeader)
        indexOfColon = dict.find(':')
        conType = str(dict[:indexOfColon])
        IpAddress = str(dict[indexOfColon + 1:])
        child = SubElement(top, 'ConnType')
        child.text = str(conType)
        child = SubElement(top, 'QtlNum')
        child.text = str(dictValue)
        if outputMode is not None:
            child = SubElement(top, 'OutputMode')
            child.text = str(outputMode)
        child = SubElement(top, 'XmlVersion')
        child.text = str(self.versionNumber)
        child = SubElement(top, 'itemType')
        child.text = str(itemType)
        child = SubElement(top, 'IpAddress')
        child.text = str(dict[indexOfColon + 1:])
        return bytes.decode(tostring(top))