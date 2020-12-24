# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\sboon\AppData\Local\Temp\pip-install-ptdbtr91\quarchpy\quarchpy\calibration\calibration_classes.py
# Compiled at: 2020-03-25 05:10:07
# Size of source mod 2**32: 8937 bytes
import pkg_resources, datetime, xml.etree.ElementTree, quarchpy

class TestSummary:

    def __init__(self, calibrationType=None, channel=None, testName=None, passed=None, worstCase=None):
        self.calibrationType = calibrationType
        self.channel = channel
        self.testName = testName
        self.passed = passed
        self.worstCase = worstCase

    def niceToString(self):
        retString = str(self.calibrationType) + str(self.channel) + str(self.testName)
        return retString


class CalibrationHeaderInformation:

    def __init__(self):
        self.quarchEnclosureSerial = None
        self.quarchInternalSerial = None
        self.quarchEnclosurePosition = None
        self.idnStr = None
        self.quarchFirmware = None
        self.quarchFpga = None
        self.calInstrumentId = None
        self.quarchpyVersion = None
        self.calCoreVersion = None
        self.calTime = None
        self.calNotes = ''
        self.calTemperature = 'NA'
        self.calFileVersion = '1.0'
        self.calibrationType = None
        self.result = None
        self.testSummaryList = []

    def toXmlText(self):
        headerObject = ElementTree.Element('Header')
        quarchModuleObject = ElementTree.SubElement(headerObject, 'QuarchModule')
        ElementTree.SubElement(quarchModuleObject, 'EnclosureSerial').text = self.quarchEnclosureSerial
        ElementTree.SubElement(quarchModuleObject, 'InternalSerial').text = self.quarchInternalSerial
        if 'QTL1995' in self.quarchEnclosureSerial.upper():
            ElementTree.SubElement(quarchModuleObject, 'EnclosurePosition').text = self.quarchEnclosurePosition
        ElementTree.SubElement(quarchModuleObject, 'ModuleFirmware').text = self.quarchFirmware
        ElementTree.SubElement(quarchModuleObject, 'ModuleFpga').text = self.quarchFpga
        calInstrumentObject = ElementTree.SubElement(headerObject, 'CalInstrument')
        ElementTree.SubElement(calInstrumentObject, 'Identity').text = self.calInstrumentId
        CalSoftwareObject = ElementTree.SubElement(headerObject, 'CalSoftware')
        ElementTree.SubElement(CalSoftwareObject, 'QuarchPy').text = self.quarchpyVersion
        ElementTree.SubElement(CalSoftwareObject, 'CalCoreVersion').text = self.calCoreVersion
        ElementTree.SubElement(CalSoftwareObject, 'CalFileVersion').text = self.calFileVersion
        ElementTree.SubElement(headerObject, 'CalTime').text = self.calTime
        ElementTree.SubElement(headerObject, 'calNotes').text = self.calNotes
        return ElementTree.tostring(headerObject)

    def toReportText(self):
        reportTitle = 'CALIBRATION REPORT\n' if 'cal' in str(self.calibrationType).lower() else 'VERIFICATION REPORT\n'
        reportText = ''
        reportText += reportTitle
        reportText += '---------------------------------\n'
        reportText += '\n'
        reportText += 'Quarch Enclosure#: '
        reportText += self.quarchEnclosureSerial + '\n'
        reportText += 'Quarch Serial#: '
        reportText += self.quarchInternalSerial + '\n'
        if 'QTL1995' in self.quarchEnclosureSerial.upper():
            reportText += 'Quarch Enclosure Position#: '
            reportText += self.quarchEnclosurePosition + '\n'
        reportText += 'Quarch Versions: '
        reportText += 'FW:' + self.quarchFirmware + ', FPGA: ' + self.quarchFpga + '\n'
        reportText += '\n'
        reportText += 'Calibration Instrument#:\n'
        reportText += self.calInstrumentId + '\n'
        reportText += '\n'
        reportText += 'Calibration Versions:\n'
        reportText += 'QuarchPy Version: ' + str(self.quarchpyVersion) + '\n'
        reportText += 'Calibration Version: ' + str(self.calCoreVersion) + '\n'
        reportText += '\n'
        reportText += 'Calibration Details:\n'
        reportText += 'Calibration Type: ' + str(self.calibrationType) + '\n'
        reportText += 'Calibration Time: ' + str(self.calTime) + '\n'
        reportText += 'Calibration Notes: ' + str(self.calNotes) + '\n'
        reportText += '\n'
        reportText += '---------------------------------\n'
        reportText += '\n'
        return reportText


def populateCalHeader_Keithley(calHeader, myCalInstrument):
    calHeader.calInstrumentId = myCalInstrument.sendCommandQuery('*IDN?')


def populateCalHeader_POM(calHeader, myDevice, calAction):
    pass


def populateCalHeader_HdPpm(calHeader, myDevice, calAction):
    calHeader.quarchEnclosureSerial = myDevice.sendCommand('*ENCLOSURE?')
    if calHeader.quarchEnclosureSerial.find('QTL') == -1:
        calHeader.quarchEnclosureSerial = 'QTL' + calHeader.quarchEnclosureSerial
    else:
        calHeader.quarchEnclosurePosition = myDevice.sendCommand('*POSITION?')
        calHeader.quarchInternalSerial = myDevice.sendCommand('*SERIAL?')
        if calHeader.quarchInternalSerial.find('QTL') == -1:
            calHeader.quarchInternalSerial = 'QTL' + calHeader.quarchInternalSerial
        else:
            calHeader.idnStr = myDevice.sendCommand('*IDN?')
            pos = calHeader.idnStr.upper().find('FPGA 1:')
            if pos != -1:
                versionStr = calHeader.idnStr[pos + 7:]
                pos = versionStr.find('\n')
                if pos != -1:
                    versionStr = versionStr[:pos].strip()
            else:
                versionStr = 'NOT-FOUND'
            calHeader.quarchFpga = versionStr.strip()
            pos = calHeader.idnStr.upper().find('PROCESSOR:')
            if pos != -1:
                versionStr = calHeader.idnStr[pos + 10:]
                pos = versionStr.find('\n')
                if pos != -1:
                    versionStr = versionStr[:pos].strip()
                else:
                    pass
            else:
                versionStr = 'NOT-FOUND'
    calHeader.quarchFirmware = versionStr.strip()
    calHeader.calibrationType = calAction


def populateCalHeader_System(calHeader):
    calHeader.calCoreVersion = quarchpy.calibration.calCodeVersion
    calHeader.quarchpyVersion = pkg_resources.get_distribution('quarchpy').version
    calHeader.calTime = datetime.datetime.now()


def addTestSummary(calHeader):
    print('')


class ModuleResultsInformation:

    def __init__(self):
        self.calibrationStatus = False
        self.channelResults = []
        self.calibrationHeader = None

    def saveTextReport(self, outputPath):
        if 'QTL1995' in self.quarchEnclosureSerial.upper():
            fileName = calibrationHeader.quarchEnclosureSerial + ' - ' + calibrationHeader.quarchEnclosurePosition + ' - ' + self.calibrationType + ' - ' + self.calTime + '.txt'
        else:
            fileName = calibrationHeader.quarchEnclosureSerial + ' - ' + self.calibrationType + ' - ' + self.calTime + '.txt'
        f = open(fileName, 'w')
        f.write(calibrationHeader.toReportText())


class CalibrationResultsInformation:

    def __init__(self):
        self.calibrationName = None
        self.calibrationStatus = None
        self.calibrationSummary = None
        self.reportText = None
        self.reportXml = None