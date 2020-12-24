# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\sboon\AppData\Local\Temp\pip-install-ptdbtr91\quarchpy\quarchpy\calibration\QTL2347.py
# Compiled at: 2020-03-25 05:10:07
# Size of source mod 2**32: 72489 bytes
"""
Quarch Power Module Calibration Functions
Written for Python 3.6 64 bit

M Dearman April 2019
"""
from functools import reduce
from quarchpy.calibration.deviceHelpers import returnMeasurement
import quarchpy.calibration.calibrationConfig, types
from time import sleep, time
from math import ceil
from quarchpy.calibration.PowerModuleCalibration import *
import threading
from quarchpy.user_interface import *
from quarchpy.user_interface import logSimpleResult
from quarchpy.device.device import *

def setBit(hexString, bit):
    newVal = int(hexString, 16) | 2 ** bit
    return '0x{:04x}'.format(newVal)


def clearBit(hexString, bit):
    mask = 65535 - 2 ** bit
    newVal = int(hexString, 16) & mask
    return '0x{:04x}'.format(newVal)


def parseFixtureData(response, start, length):
    response = response.splitlines()
    result = ''
    for line in response:
        line = line[4:6] + line[2:4]
        line = '{0:016b}'.format(int(line, 16))
        result += line

    result = int(result[start:start + length], 2)
    if result >= 2 ** (length - 1):
        result -= 2 ** length
    return result


def getFixtureData(device, channel):
    response = device.sendCommand('read 0x0000')
    device.sendCommand('write 0x0000' + setBit(response, 3))
    data = device.sendCommand('read 0x1000 to 0x1007')
    response = device.sendCommand('read 0x0000')
    device.sendCommand('write 0x000' + clearBit(response, 3))
    if channel == '3V3 VOLT':
        return parseFixtureData(data, 0, 16)
    if channel == '3V3 CUR':
        return parseFixtureData(data, 16, 25)
    if channel == '12V VOLT':
        return parseFixtureData(data, 41, 16)
    if channel == '12V CUR':
        return parseFixtureData(data, 57, 25)
    if channel == '3V3_AUX VOLT':
        return parseFixtureData(data, 82, 16)
    if channel == '3V3_AUX CUR':
        return parseFixtureData(data, 98, 20)


class QTL2347(PowerModule):
    CALIBRATION_MODE_ADDR = '0xA100'
    CALIBRATION_CONTROL_ADDR = '0xA101'
    V3_3_LOW_MULTIPLIER_ADDR = '0xA103'
    V3_3_LOW_OFFSET_ADDR = '0xA104'
    V3_3_HIGH_MULTIPLIER_ADDR = '0xA105'
    V3_3_HIGH_OFFSET_ADDR = '0xA106'
    V3_3_VOLT_MULTIPLIER_ADDR = '0xA107'
    V3_3_VOLT_OFFSET_ADDR = '0xA108'
    V3_3_LEAKAGE_MULTIPLIER_ADDR = '0xA109'
    V12_LOW_MULTIPLIER_ADDR = '0xA10A'
    V12_LOW_OFFSET_ADDR = '0xA10B'
    V12_HIGH_MULTIPLIER_ADDR = '0xA10C'
    V12_HIGH_OFFSET_ADDR = '0xA10D'
    V12_VOLT_MULTIPLIER_ADDR = '0xA10E'
    V12_VOLT_OFFSET_ADDR = '0xA10F'
    V12_LEAKAGE_MULTIPLIER_ADDR = '0xA110'
    V3_3_AUX_MULTIPLIER_ADDR = '0xA111'
    V3_3_AUX_OFFSET_ADDR = '0xA112'
    V3_3_AUX_VOLT_MULTIPLIER_ADDR = '0xA113'
    V3_3_AUX_VOLT_OFFSET_ADDR = '0xA114'
    V3_3_AUX_LEAKAGE_MULTIPLIER_ADDR = '0xA115'

    def specific_requirements(self):
        pass

    def open_module(self):
        self.dut.sendCommand('write ' + QTL2347.CALIBRATION_MODE_ADDR + ' 0xaa55')
        self.dut.sendCommand('write ' + QTL2347.CALIBRATION_MODE_ADDR + ' 0x55aa')

    def clear_calibration(self):
        self.dut.sendCommand('write ' + QTL2347.CALIBRATION_MODE_ADDR + ' 0xaa55')
        self.dut.sendCommand('write ' + QTL2347.CALIBRATION_MODE_ADDR + ' 0x55aa')
        self.dut.sendAndVerifyCommand('write ' + QTL2347.V3_3_VOLT_OFFSET_ADDR + ' 0x0000')
        self.dut.sendAndVerifyCommand('write ' + QTL2347.V3_3_VOLT_MULTIPLIER_ADDR + ' 0x0000')
        self.dut.sendAndVerifyCommand('write ' + QTL2347.V3_3_LOW_OFFSET_ADDR + ' 0x0000')
        self.dut.sendAndVerifyCommand('write ' + QTL2347.V3_3_LOW_MULTIPLIER_ADDR + ' 0x0000')
        self.dut.sendAndVerifyCommand('write ' + QTL2347.V3_3_HIGH_OFFSET_ADDR + ' 0x0000')
        self.dut.sendAndVerifyCommand('write ' + QTL2347.V3_3_HIGH_MULTIPLIER_ADDR + ' 0x0000')
        self.dut.sendAndVerifyCommand('write ' + QTL2347.V3_3_LEAKAGE_MULTIPLIER_ADDR + ' 0x0000')
        self.dut.sendAndVerifyCommand('write ' + QTL2347.V12_VOLT_OFFSET_ADDR + ' 0x0000')
        self.dut.sendAndVerifyCommand('write ' + QTL2347.V12_VOLT_MULTIPLIER_ADDR + ' 0x0000')
        self.dut.sendAndVerifyCommand('write ' + QTL2347.V12_LOW_OFFSET_ADDR + ' 0x0000')
        self.dut.sendAndVerifyCommand('write ' + QTL2347.V12_LOW_MULTIPLIER_ADDR + ' 0x0000')
        self.dut.sendAndVerifyCommand('write ' + QTL2347.V12_HIGH_OFFSET_ADDR + ' 0x0000')
        self.dut.sendAndVerifyCommand('write ' + QTL2347.V12_HIGH_MULTIPLIER_ADDR + ' 0x0000')
        self.dut.sendAndVerifyCommand('write ' + QTL2347.V12_LEAKAGE_MULTIPLIER_ADDR + ' 0x0000')
        self.dut.sendAndVerifyCommand('write ' + QTL2347.V3_3_AUX_VOLT_OFFSET_ADDR + ' 0x0000')
        self.dut.sendAndVerifyCommand('write ' + QTL2347.V3_3_AUX_VOLT_MULTIPLIER_ADDR + ' 0x0000')
        self.dut.sendAndVerifyCommand('write ' + QTL2347.V3_3_AUX_OFFSET_ADDR + ' 0x0000')
        self.dut.sendAndVerifyCommand('write ' + QTL2347.V3_3_AUX_MULTIPLIER_ADDR + ' 0x0000')
        self.dut.sendAndVerifyCommand('write ' + QTL2347.V3_3_AUX_LEAKAGE_MULTIPLIER_ADDR + ' 0x0000')

    def write_calibration(self):
        self.dut.sendCommand('write 0xa200 0x0020')
        printText('Erasing TAG memory..')
        sleep(2.0)
        printText('Programming TAG memory...')
        self.dut.sendCommand('write 0xa200 0x0040')

    def close_module(self):
        pass

    class QTL2347Calibration(Calibration):

        def __init__(self):
            super().__init__()

        def init_cal(self, voltage):
            if self.powerModule.dut.sendCommand('rec:ave?').find('32k') != 0:
                self.powerModule.dut.sendAndVerifyCommand('rec:ave 32k')
            self.powerModule.dut.sendCommand('write ' + QTL2347.CALIBRATION_MODE_ADDR + ' 0xaa55')
            self.powerModule.dut.sendCommand('write ' + QTL2347.CALIBRATION_MODE_ADDR + ' 0x55aa')
            self.powerModule.load.reset()

        def meas_12v_volt(self):
            result = getFixtureData(self.powerModule.dut, '12V VOLT')
            return result

        def meas_12v_cur(self):
            result = getFixtureData(self.powerModule.dut, '12V CUR')
            return result

        def meas_3v3_volt(self):
            result = getFixtureData(self.powerModule.dut, '3V3 VOLT')
            return result

        def meas_3v3_cur(self):
            result = getFixtureData(self.powerModule.dut, '3V3 CUR')
            return result

        def meas_3v3_aux_volt(self):
            result = getFixtureData(self.powerModule.dut, '3V3_AUX VOLT')
            return result

        def meas_3v3_aux_cur(self):
            result = getFixtureData(self.powerModule.dut, '3V3_AUX CUR')
            return result

        def checkLoadVoltage(self, voltage, tolerance):
            self.powerModule.load.setReferenceCurrent(0)
            result = self.powerModule.load.measureLoadVoltage() * 1000
            if result >= voltage - tolerance:
                if result <= voltage + tolerance:
                    return True
            return False

        def finish_cal(self):
            self.powerModule.load.disable()
            self.powerModule.dut.sendAndVerifyCommand('write ' + QTL2347.CALIBRATION_CONTROL_ADDR + ' 0x00F0')

        def report(self, action, data):
            report = []
            report.append('\n')
            if action == 'calibrate':
                report.append('\t' + '{0:>11}'.format('Reference ') + self.units + '   ' + '{0:>10}'.format('Raw Value ') + self.units + '   ' + '{0:>10}'.format('Result ') + self.units + '   ' + '{0:>10}'.format('Error ') + self.units + '   ' + '{0:>13}'.format('+/-(Abs Error,% Error)') + ' ' + '{0:>10}'.format('Pass'))
            else:
                if action == 'verify':
                    report.append('\t' + '{0:>11}'.format('Reference ') + self.units + '   ' + '{0:>10}'.format('Result ') + self.units + '   ' + '{0:>10}'.format('Error ') + self.units + '   ' + '{0:>13}'.format('+/-(Abs Error,% Error)') + '   ' + '{0:>10}'.format('Pass'))
            report.append('==================================================================================================')
            worstAbsError = 0
            worstRelError = 0
            worstRef = None
            overallResult = True
            for thisLine in data:
                reference = thisLine[1]
                ppmValue = thisLine[0]
                if action == 'calibrate':
                    calibratedValue = self.getResult(ppmValue)
                else:
                    calibratedValue = ppmValue
                actError, errorSign, absError, relError, result = getError(reference, calibratedValue, self.absErrorLimit, self.relErrorLimit)
                if absError >= worstAbsError:
                    if relError >= worstRelError:
                        worstAbsError = absError
                        worstRelError = relError
                        worstCase = errorSign + '(' + str(absError) + self.units + ',' + '{:.3f}'.format(relError) + '%) @ ' + '{:.3f}'.format(reference) + self.units
                    if result != True:
                        overallResult = False
                    passfail = lambda x:                     if x:
'Pass' # Avoid dead code: 'Fail'
                    if action == 'calibrate':
                        report.append('\t' + '{:>11.3f}'.format(reference) + '     ' + '{:>10.1f}'.format(ppmValue) + '     ' + '{:>10.1f}'.format(calibratedValue) + '     ' + '{:>10.3f}'.format(actError) + '     ' + '{0:>16}'.format(errorSign + '(' + str(absError) + self.units + ',' + '{:.3f}'.format(relError) + '%)') + '     ' + '{0:>10}'.format(passfail(result)))
                    elif action == 'verify':
                        report.append('\t' + '{:>11.3f}'.format(reference) + '     ' + '{:>10.1f}'.format(ppmValue) + '     ' + '{:>10.3f}'.format(actError) + '     ' + '{0:>16}'.format(errorSign + '(' + str(absError) + self.units + ',' + '{:.3f}'.format(relError) + '%)') + '     ' + '{0:>10}'.format(passfail(result)))

            report.append('==================================================================================================')
            report.append('\n')
            if action == 'calibrate':
                report.append('Calculated Multiplier: ' + str(self.multiplier.originalValue()) + ', Calculated Offset: ' + str(self.offset.originalValue()))
                report.append('Stored Multiplier: ' + str(self.multiplier.storedValue()) + ', Stored Offset: ' + str(self.offset.storedValue()))
                report.append('Multiplier Register: ' + self.multiplier.hexString(4) + ', Offset Register: ' + self.offset.hexString(4))
            return {'result':overallResult,  'worst case':worstCase,  'report':'\n'.join(report),  'calObj':self}

    class QTL2347_12V_VoltageCalibration(QTL2347Calibration):

        def __init__(self, powerModule):
            self.powerModule = powerModule
            self.absErrorLimit = 1
            self.relErrorLimit = 1
            self.test_min = 40
            self.test_max = 14400
            self.test_steps = 20
            self.units = 'mV'
            self.scaling = 4
            self.multiplier_signed = False
            self.multiplier_int_width = 1
            self.multiplier_frac_width = 16
            self.offset_signed = True
            self.offset_int_width = 10
            self.offset_frac_width = 6
            self.unitTemp = self.powerModule.dut.sendCommand('meas:temp unit?')
            self.v5Temp = self.powerModule.dut.sendCommand('meas:temp 5v?')
            self.v12Temp = self.powerModule.dut.sendCommand('meas:temp 12v?')

        def init(self):
            super().init_cal('12v')
            self.powerModule.dut.sendCommand('write ' + QTL2347.CALIBRATION_MODE_ADDR + ' 0xaa55')
            self.powerModule.dut.sendCommand('write ' + QTL2347.CALIBRATION_MODE_ADDR + ' 0x55aa')
            self.powerModule.dut.sendAndVerifyCommand('write ' + QTL2347.V12_VOLT_MULTIPLIER_ADDR + ' 0x0000')
            self.powerModule.dut.sendAndVerifyCommand('write ' + QTL2347.V12_VOLT_OFFSET_ADDR + ' 0x0000')
            showDialog(title='Setup 12V Voltage Calibration', message='\x07Please connect the load to the 12v channel and disconnect host power')
            while super().checkLoadVoltage(500, 500) != True:
                showDialog(title='Disconnnect Host Power', message='\x07Please disconnect host power from the fixture on the 12v Channel')

        def setRef(self, value):
            return load_set_volt(self.powerModule.load, value)

        def readRef(self):
            return load_meas_volt(self.powerModule.load)

        def readVal(self):
            return super().meas_12v_volt()

        def setCoefficients(self):
            result1 = self.powerModule.dut.sendAndVerifyCommand('write ' + QTL2347.V12_VOLT_MULTIPLIER_ADDR + ' ' + self.multiplier.hexString(4))
            result2 = self.powerModule.dut.sendAndVerifyCommand('write ' + QTL2347.V12_VOLT_OFFSET_ADDR + ' ' + self.offset.hexString(4))
            if result1 and result2:
                result = True
            else:
                result = False
            logSimpleResult('Set 12v voltage', result)

        def finish(self):
            super().finish_cal()

        def report(self, data):
            return super().report('calibrate', data)

        def readCoefficients(self):
            coefficients = {}
            coefficients['multiplier'] = self.powerModule.dut.sendCommand('read ' + QTL2347.V12_VOLT_MULTIPLIER_ADDR)
            coefficients['offset'] = self.powerModule.dut.sendCommand('read ' + QTL2347.V12_VOLT_OFFSET_ADDR)
            return coefficients

        def writeCoefficients(self, coefficients):
            self.powerModule.dut.sendAndVerifyCommand('write ' + QTL2347.V12_VOLT_MULTIPLIER_ADDR + ' ' + coefficients['multiplier'])
            self.powerModule.dut.sendAndVerifyCommand('write ' + QTL2347.V12_VOLT_OFFSET_ADDR + ' ' + coefficients['offset'])

    class QTL2347_12V_LeakageCalibration(QTL2347Calibration):

        def __init__(self, powerModule):
            self.powerModule = powerModule
            self.absErrorLimit = 50
            self.relErrorLimit = 0
            self.test_min = 1000
            self.test_max = 14400
            self.test_steps = 20
            self.units = 'uA'
            self.scaling = 1
            self.multiplier_signed = False
            self.multiplier_int_width = 1
            self.multiplier_frac_width = 16
            self.offset_signed = False
            self.offset_int_width = 16
            self.offset_frac_width = 16
            self.unitTemp = self.powerModule.dut.sendCommand('meas:temp unit?')
            self.v5Temp = self.powerModule.dut.sendCommand('meas:temp 5v?')
            self.v12Temp = self.powerModule.dut.sendCommand('meas:temp 12v?')

        def init(self):
            super().init_cal('12v')
            self.powerModule.dut.sendAndVerifyCommand('write ' + QTL2347.CALIBRATION_CONTROL_ADDR + ' 0x00F5')
            self.powerModule.dut.sendAndVerifyCommand('write ' + QTL2347.V12_LEAKAGE_MULTIPLIER_ADDR + ' 0x0000')
            showDialog(title='Setup 12V Leakage Calibration', message='\x07Please connect the load to the 12v channel and disconnect host power')
            while super().checkLoadVoltage(500, 500) != True:
                showDialog(title='Disconnnect Host Power', message='\x07Please disconnect host power from the fixture on the 12v Channel')

        def setRef(self, value):
            return load_set_volt(self.powerModule.load, value)

        def readRef(self):
            return -load_meas_cur(self.powerModule.load)

        def readVal(self):
            return load_get_volt(self.powerModule.load)

        def setCoefficients(self):
            pass

        def finish(self):
            super().finish_cal()

        def report(self, data):
            return super().report('calibrate', data)

        def readCoefficients(self):
            coefficients = {}
            coefficients['multiplier'] = self.powerModule.dut.sendCommand('read ' + QTL2347.V12_LEAKAGE_MULTIPLIER_ADDR)
            return coefficients

        def writeCoefficients(self, coefficents):
            self.powerModule.dut.sendAndVerifyCommand('write ' + QTL2347.V12_LEAKAGE_MULTIPLIER_ADDR + ' ' + coefficents['multiplier'])

    class QTL2347_12V_LowCurrentCalibration(QTL2347Calibration):

        def __init__(self, powerModule):
            self.powerModule = powerModule
            self.absErrorLimit = 2
            self.relErrorLimit = 2
            self.test_min = 10
            self.test_max = 85000
            self.test_steps = 20
            self.units = 'uA'
            self.scaling = 32
            self.multiplier_signed = False
            self.multiplier_int_width = 1
            self.multiplier_frac_width = 16
            self.offset_signed = True
            self.offset_int_width = 10
            self.offset_frac_width = 6
            self.unitTemp = self.powerModule.dut.sendCommand('meas:temp unit?')
            self.v5Temp = self.powerModule.dut.sendCommand('meas:temp 5v?')
            self.v12Temp = self.powerModule.dut.sendCommand('meas:temp 12v?')

        def init(self):
            super().init_cal('12v')
            self.powerModule.dut.sendAndVerifyCommand('write ' + QTL2347.CALIBRATION_CONTROL_ADDR + ' 0x00F4')
            self.powerModule.dut.sendAndVerifyCommand('write ' + QTL2347.V12_LOW_MULTIPLIER_ADDR + ' 0x0000')
            self.powerModule.dut.sendAndVerifyCommand('write ' + QTL2347.V12_LOW_OFFSET_ADDR + ' 0x0000')
            showDialog(title='Setup 12V Current Calibration', message='\x07Please connect host power and load to the 12v channel')
            while super().checkLoadVoltage(12000, 1000) != True:
                showDialog(title='Connect Host Power', message='\x07Please connect host power and load to the 12v channel on the fixture')

        def setRef(self, value):
            load_set_cur(self.powerModule.load, value)

        def readRef(self):
            voltage = super().meas_12v_volt()
            leakage = voltage * self.powerModule.calibrations['12V']['Leakage'].multiplier.originalValue() + self.powerModule.calibrations['12V']['Leakage'].offset.originalValue()
            return load_meas_cur(self.powerModule.load) + leakage

        def readVal(self):
            return super().meas_12v_cur()

        def setCoefficients(self):
            result1 = self.powerModule.dut.sendAndVerifyCommand('write ' + QTL2347.V12_LOW_MULTIPLIER_ADDR + ' ' + self.multiplier.hexString(4))
            result2 = self.powerModule.dut.sendAndVerifyCommand('write ' + QTL2347.V12_LOW_OFFSET_ADDR + ' ' + self.offset.hexString(4))
            if result1 and result2:
                result = True
            else:
                result = False
            logSimpleResult('Set 12v Low Current', result)

        def finish(self):
            super().finish_cal()

        def report(self, data):
            return super().report('calibrate', data)

        def readCoefficients(self):
            coefficients = {}
            coefficients['multiplier'] = self.powerModule.dut.sendCommand('read ' + QTL2347.V12_LOW_MULTIPLIER_ADDR)
            coefficients['offset'] = self.powerModule.dut.sendCommand('read ' + QTL2347.V12_LOW_OFFSET_ADDR)
            return coefficients

        def writeCoefficients(self, coefficients):
            self.powerModule.dut.sendAndVerifyCommand('write ' + QTL2347.V12_LOW_MULTIPLIER_ADDR + ' ' + coefficients['multiplier'])
            self.powerModule.dut.sendAndVerifyCommand('write ' + QTL2347.V12_LOW_OFFSET_ADDR + ' ' + coefficients['offset'])

    class QTL2347_12V_HighCurrentCalibration(QTL2347Calibration):

        def __init__(self, powerModule):
            self.powerModule = powerModule
            self.absErrorLimit = 2000
            self.relErrorLimit = 1
            self.test_min = 1000
            self.test_max = 4000000
            self.test_steps = 20
            self.units = 'uA'
            self.scaling = 2048
            self.multiplier_signed = False
            self.multiplier_int_width = 1
            self.multiplier_frac_width = 16
            self.offset_signed = True
            self.offset_int_width = 10
            self.offset_frac_width = 6
            self.unitTemp = self.powerModule.dut.sendCommand('meas:temp unit?')
            self.v5Temp = self.powerModule.dut.sendCommand('meas:temp 5v?')
            self.v12Temp = self.powerModule.dut.sendCommand('meas:temp 12v?')

        def init(self):
            super().init_cal('12v')
            self.powerModule.dut.sendAndVerifyCommand('write ' + QTL2347.CALIBRATION_CONTROL_ADDR + ' 0x00F8')
            self.powerModule.dut.sendAndVerifyCommand('write ' + QTL2347.V12_HIGH_MULTIPLIER_ADDR + ' 0x0000')
            self.powerModule.dut.sendAndVerifyCommand('write ' + QTL2347.V12_HIGH_OFFSET_ADDR + ' 0x0000')
            showDialog(title='Setup 12V Current Calibration', message='\x07Please connect host power and load to the 12v channel')
            while super().checkLoadVoltage(12000, 1000) != True:
                showDialog(title='Connect Host Power', message='\x07Please connect host power and load to the 12v channel on the fixture')

        def setRef(self, value):
            load_set_cur(self.powerModule.load, value)

        def readRef(self):
            voltage = super().meas_12v_volt()
            leakage = voltage * self.powerModule.calibrations['12V']['Leakage'].multiplier.originalValue() + self.powerModule.calibrations['12V']['Leakage'].offset.originalValue()
            return load_meas_cur(self.powerModule.load) + leakage

        def readVal(self):
            return super().meas_12v_cur()

        def setCoefficients(self):
            result1 = self.powerModule.dut.sendAndVerifyCommand('write ' + QTL2347.V12_HIGH_MULTIPLIER_ADDR + ' ' + self.multiplier.hexString(4))
            result2 = self.powerModule.dut.sendAndVerifyCommand('write ' + QTL2347.V12_HIGH_OFFSET_ADDR + ' ' + self.offset.hexString(4))
            if result1 and result2:
                result = True
            else:
                result = False
            logSimpleResult('Set 12v high current', result)
            result = self.powerModule.dut.sendAndVerifyCommand('write ' + QTL2347.V12_LEAKAGE_MULTIPLIER_ADDR + ' ' + self.powerModule.calibrations['12V']['Leakage'].multiplier.hexString(4))

        def finish(self):
            super().finish_cal()

        def report(self, data):
            return super().report('calibrate', data)

        def readCoefficients(self):
            coefficients = {}
            coefficients['multiplier'] = self.powerModule.dut.sendCommand('read ' + QTL2347.V12_HIGH_MULTIPLIER_ADDR)
            coefficients['offset'] = self.powerModule.dut.sendCommand('read ' + QTL2347.V12_HIGH_OFFSET_ADDR)
            return coefficients

        def writeCoefficients(self, coefficients):
            self.powerModule.dut.sendAndVerifyCommand('write ' + QTL2347.V12_HIGH_MULTIPLIER_ADDR + ' ' + coefficients['multiplier'])
            self.powerModule.dut.sendAndVerifyCommand('write ' + QTL2347.V12_HIGH_OFFSET_ADDR + ' ' + coefficients['offset'])

    class QTL2347_3V3_VoltageCalibration(QTL2347Calibration):

        def __init__(self, powerModule):
            self.powerModule = powerModule
            self.absErrorLimit = 1
            self.relErrorLimit = 1
            self.test_min = 40
            self.test_max = 14400
            self.test_steps = 20
            self.units = 'mV'
            self.scaling = 4
            self.multiplier_signed = False
            self.multiplier_int_width = 1
            self.multiplier_frac_width = 16
            self.offset_signed = True
            self.offset_int_width = 10
            self.offset_frac_width = 6
            self.unitTemp = self.powerModule.dut.sendCommand('meas:temp unit?')
            self.v5Temp = self.powerModule.dut.sendCommand('meas:temp 5v?')
            self.v12Temp = self.powerModule.dut.sendCommand('meas:temp 12v?')

        def init(self):
            super().init_cal('3v3')
            self.powerModule.dut.sendAndVerifyCommand('write ' + QTL2347.V3_3_VOLT_MULTIPLIER_ADDR + ' 0x0000')
            self.powerModule.dut.sendAndVerifyCommand('write ' + QTL2347.V3_3_VOLT_OFFSET_ADDR + ' 0x0000')
            showDialog(title='Setup 3.3V Voltage Calibration', message='\x07Please connect the load to the 3.3v channel and disconnect host power')
            while super().checkLoadVoltage(500, 500) != True:
                showDialog(title='Disconnnect Host Power', message='\x07Please disconnect host power from the fixture on the 3.3v Channel')

        def setRef(self, value):
            return load_set_volt(self.powerModule.load, value)

        def readRef(self):
            return load_meas_volt(self.powerModule.load)

        def readVal(self):
            return super().meas_3v3_volt()

        def setCoefficients(self):
            result1 = self.powerModule.dut.sendAndVerifyCommand('write ' + QTL2347.V3_3_VOLT_MULTIPLIER_ADDR + ' ' + self.multiplier.hexString(4))
            result2 = self.powerModule.dut.sendAndVerifyCommand('write ' + QTL2347.V3_3_VOLT_OFFSET_ADDR + ' ' + self.offset.hexString(4))
            if result1 and result2:
                result = True
            else:
                result = False
            logSimpleResult('Set 3.3v voltage', result)

        def finish(self):
            super().finish_cal()

        def report(self, data):
            return super().report('calibrate', data)

        def readCoefficients(self):
            coefficients = {}
            coefficients['multiplier'] = self.powerModule.dut.sendCommand('read ' + QTL2347.V3_3_VOLT_MULTIPLIER_ADDR)
            coefficients['offset'] = self.powerModule.dut.sendCommand('read ' + QTL2347.V3_3_VOLT_OFFSET_ADDR)
            return coefficients

        def writeCoefficients(self, coefficients):
            self.powerModule.dut.sendAndVerifyCommand('write ' + QTL2347.V3_3_VOLT_MULTIPLIER_ADDR + ' ' + coefficients['multiplier'])
            self.powerModule.dut.sendAndVerifyCommand('write ' + QTL2347.V3_3_VOLT_OFFSET_ADDR + ' ' + coefficients['offset'])

    class QTL2347_3V3_LeakageCalibration(QTL2347Calibration):

        def __init__(self, powerModule):
            self.powerModule = powerModule
            self.absErrorLimit = 50
            self.relErrorLimit = 0
            self.test_min = 1000
            self.test_max = 14400
            self.test_steps = 20
            self.units = 'uA'
            self.scaling = 1
            self.multiplier_signed = False
            self.multiplier_int_width = 1
            self.multiplier_frac_width = 16
            self.offset_signed = False
            self.offset_int_width = 16
            self.offset_frac_width = 16
            self.unitTemp = self.powerModule.dut.sendCommand('meas:temp unit?')
            self.v5Temp = self.powerModule.dut.sendCommand('meas:temp 5v?')
            self.v12Temp = self.powerModule.dut.sendCommand('meas:temp 12v?')

        def init(self):
            super().init_cal('3v3')
            self.powerModule.dut.sendAndVerifyCommand('write ' + QTL2347.CALIBRATION_CONTROL_ADDR + ' 0x00F5')
            self.powerModule.dut.sendAndVerifyCommand('write ' + QTL2347.V3_3_LEAKAGE_MULTIPLIER_ADDR + ' 0x0000')
            showDialog(title='Setup 3.3V Leakage Calibration', message='\x07Please connect the load to the 3.3v channel and disconnect host power')
            while super().checkLoadVoltage(500, 500) != True:
                showDialog(title='Disconnnect Host Power', message='\x07Please disconnect host power from the fixture on the 3.3v Channel')

        def setRef(self, value):
            return load_set_volt(self.powerModule.load, value)

        def readRef(self):
            return -load_meas_cur(self.powerModule.load)

        def readVal(self):
            return load_get_volt(self.powerModule.load)

        def setCoefficients(self):
            pass

        def finish(self):
            super().finish_cal()

        def report(self, data):
            return super().report('calibrate', data)

        def readCoefficients(self):
            coefficients = {}
            coefficients['multiplier'] = self.powerModule.dut.sendCommand('read ' + QTL2347.V3_3_LEAKAGE_MULTIPLIER_ADDR)
            return coefficients

        def writeCoefficients(self, coefficents):
            self.powerModule.dut.sendAndVerifyCommand('write ' + QTL2347.V3_3_LEAKAGE_MULTIPLIER_ADDR + ' ' + coefficents['multiplier'])

    class QTL2347_3V3_LowCurrentCalibration(QTL2347Calibration):

        def __init__(self, powerModule):
            self.powerModule = powerModule
            self.absErrorLimit = 2
            self.relErrorLimit = 2
            self.test_min = 10
            self.test_max = 85000
            self.test_steps = 20
            self.units = 'uA'
            self.scaling = 32
            self.multiplier_signed = False
            self.multiplier_int_width = 1
            self.multiplier_frac_width = 16
            self.offset_signed = True
            self.offset_int_width = 10
            self.offset_frac_width = 6
            self.unitTemp = self.powerModule.dut.sendCommand('meas:temp unit?')
            self.v5Temp = self.powerModule.dut.sendCommand('meas:temp 5v?')
            self.v12Temp = self.powerModule.dut.sendCommand('meas:temp 12v?')

        def init(self):
            super().init_cal('3v3')
            self.powerModule.dut.sendAndVerifyCommand('write ' + QTL2347.CALIBRATION_CONTROL_ADDR + ' 0x00F1')
            self.powerModule.dut.sendAndVerifyCommand('write ' + QTL2347.V3_3_LOW_MULTIPLIER_ADDR + ' 0x0000')
            self.powerModule.dut.sendAndVerifyCommand('write ' + QTL2347.V3_3_LOW_OFFSET_ADDR + ' 0x0000')
            showDialog(title='Setup 12V Current Calibration', message='\x07Please connect host power and load to the 3.3v channel')
            while super().checkLoadVoltage(12000, 1000) != True:
                showDialog(title='Connect Host Power', message='\x07Please connect host power and load to the 3.3v channel on the fixture')

        def setRef(self, value):
            load_set_cur(self.powerModule.load, value)

        def readRef(self):
            voltage = super().meas_3v3_volt()
            leakage = voltage * self.powerModule.calibrations['3.3V']['Leakage'].multiplier.originalValue() + self.powerModule.calibrations['3.3V']['Leakage'].offset.originalValue()
            return load_meas_cur(self.powerModule.load) + leakage

        def readVal(self):
            return super().meas_3v3_cur()

        def setCoefficients(self):
            result1 = self.powerModule.dut.sendAndVerifyCommand('write ' + QTL2347.V3_3_LOW_MULTIPLIER_ADDR + ' ' + self.multiplier.hexString(4))
            result2 = self.powerModule.dut.sendAndVerifyCommand('write ' + QTL2347.V3_3_LOW_OFFSET_ADDR + ' ' + self.offset.hexString(4))
            if result1 and result2:
                result = True
            else:
                result = False
            logSimpleResult('Set 3.3v low current', result)

        def finish(self):
            super().finish_cal()

        def report(self, data):
            return super().report('calibrate', data)

        def readCoefficients(self):
            coefficients = {}
            coefficients['multiplier'] = self.powerModule.dut.sendCommand('read ' + QTL2347.V3_3_LOW_MULTIPLIER_ADDR)
            coefficients['offset'] = self.powerModule.dut.sendCommand('read ' + QTL2347.V3_3_LOW_OFFSET_ADDR)
            return coefficients

        def writeCoefficients(self, coefficients):
            self.powerModule.dut.sendAndVerifyCommand('write ' + QTL2347.V3_3_LOW_MULTIPLIER_ADDR + ' ' + coefficients['multiplier'])
            self.powerModule.dut.sendAndVerifyCommand('write ' + QTL2347.V3_3_LOW_OFFSET_ADDR + ' ' + coefficients['offset'])

    class QTL2347_3V3_HighCurrentCalibration(QTL2347Calibration):

        def __init__(self, powerModule):
            self.powerModule = powerModule
            self.absErrorLimit = 2000
            self.relErrorLimit = 1
            self.test_min = 1000
            self.test_max = 4000000
            self.test_steps = 20
            self.units = 'uA'
            self.scaling = 2048
            self.multiplier_signed = False
            self.multiplier_int_width = 1
            self.multiplier_frac_width = 16
            self.offset_signed = True
            self.offset_int_width = 10
            self.offset_frac_width = 6
            self.unitTemp = self.powerModule.dut.sendCommand('meas:temp unit?')
            self.v5Temp = self.powerModule.dut.sendCommand('meas:temp 5v?')
            self.v12Temp = self.powerModule.dut.sendCommand('meas:temp 12v?')

        def init(self):
            super().init_cal('3v3')
            self.powerModule.dut.sendAndVerifyCommand('write ' + QTL2347.CALIBRATION_CONTROL_ADDR + ' 0x00F2')
            self.powerModule.dut.sendAndVerifyCommand('write ' + QTL2347.V3_3_HIGH_MULTIPLIER_ADDR + ' 0x0000')
            self.powerModule.dut.sendAndVerifyCommand('write ' + QTL2347.V3_3_HIGH_OFFSET_ADDR + ' 0x0000')
            showDialog(title='Setup 12V Current Calibration', message='\x07Please connect host power and load to the 3.3v channel')
            while super().checkLoadVoltage(12000, 1000) != True:
                showDialog(title='Connect Host Power', message='\x07Please connect host power and load to the 3.3v channel on the fixture')

        def setRef(self, value):
            load_set_cur(self.powerModule.load, value)

        def readRef(self):
            voltage = super().meas_3v3_volt()
            leakage = voltage * self.powerModule.calibrations['3.3V']['Leakage'].multiplier.originalValue() + self.powerModule.calibrations['3.3V']['Leakage'].offset.originalValue()
            return load_meas_cur(self.powerModule.load) + leakage

        def readVal(self):
            return super().meas_3v3_cur()

        def setCoefficients(self):
            result1 = self.powerModule.dut.sendAndVerifyCommand('write ' + QTL2347.V3_3_HIGH_MULTIPLIER_ADDR + ' ' + self.multiplier.hexString(4))
            result2 = self.powerModule.dut.sendAndVerifyCommand('write ' + QTL2347.V3_3_HIGH_OFFSET_ADDR + ' ' + self.offset.hexString(4))
            if result1 and result2:
                result = True
            else:
                result = False
            logSimpleResult('Set 3.3v high current', result)
            result = self.powerModule.dut.sendAndVerifyCommand('write ' + QTL2347.V3_3_LEAKAGE_MULTIPLIER_ADDR + ' ' + self.powerModule.calibrations['3.3V']['Leakage'].multiplier.hexString(4))

        def finish(self):
            super().finish_cal()

        def report(self, data):
            return super().report('calibrate', data)

        def readCoefficients(self):
            coefficients = {}
            coefficients['multiplier'] = self.powerModule.dut.sendCommand('read ' + QTL2347.V3_3_HIGH_MULTIPLIER_ADDR)
            coefficients['offset'] = self.powerModule.dut.sendCommand('read ' + QTL2347.V3_3_HIGH_OFFSET_ADDR)
            return coefficients

        def writeCoefficients(self, coefficients):
            self.powerModule.dut.sendAndVerifyCommand('write ' + QTL2347.V3_3_HIGH_MULTIPLIER_ADDR + ' ' + coefficients['multiplier'])
            self.powerModule.dut.sendAndVerifyCommand('write ' + QTL2347.V3_3_HIGH_OFFSET_ADDR + ' ' + coefficients['offset'])

    class QTL2347_3V3_AUX_VoltageCalibration(QTL2347Calibration):

        def __init__(self, powerModule):
            self.powerModule = powerModule
            self.absErrorLimit = 1
            self.relErrorLimit = 1
            self.test_min = 40
            self.test_max = 14400
            self.test_steps = 20
            self.units = 'mV'
            self.scaling = 4
            self.multiplier_signed = False
            self.multiplier_int_width = 1
            self.multiplier_frac_width = 16
            self.offset_signed = True
            self.offset_int_width = 10
            self.offset_frac_width = 6
            self.unitTemp = self.powerModule.dut.sendCommand('meas:temp unit?')
            self.v5Temp = self.powerModule.dut.sendCommand('meas:temp 5v?')
            self.v12Temp = self.powerModule.dut.sendCommand('meas:temp 12v?')

        def init(self):
            super().init_cal('3V3_AUX')
            self.powerModule.dut.sendAndVerifyCommand('write ' + QTL2347.V3_3_AUX_VOLT_MULTIPLIER_ADDR + ' 0x0000')
            self.powerModule.dut.sendAndVerifyCommand('write ' + QTL2347.V3_3_AUX_VOLT_OFFSET_ADDR + ' 0x0000')
            showDialog(title='Setup 3.3V Aux Voltage Calibration', message='\x07Please connect the load to the 3.3v Aux channel and disconnect host power')
            while super().checkLoadVoltage(500, 500) != True:
                showDialog(title='Disconnnect Host Power', message='\x07Please disconnect host power from the fixture on the 3.3v Aux Channel')

        def setRef(self, value):
            return load_set_volt(self.powerModule.load, value)

        def readRef(self):
            return load_meas_volt(self.powerModule.load)

        def readVal(self):
            return super().meas_3v3_aux_volt()

        def setCoefficients(self):
            result1 = self.powerModule.dut.sendAndVerifyCommand('write ' + QTL2347.V3_3_AUX_VOLT_MULTIPLIER_ADDR + ' ' + self.multiplier.hexString(4))
            result2 = self.powerModule.dut.sendAndVerifyCommand('write ' + QTL2347.V3_3_AUX_VOLT_OFFSET_ADDR + ' ' + self.offset.hexString(4))
            if result1 and result2:
                result = True
            else:
                result = False
            logSimpleResult('Set 3.3v voltage', result)

        def finish(self):
            super().finish_cal()

        def report(self, data):
            return super().report('calibrate', data)

        def readCoefficients(self):
            coefficients = {}
            coefficients['multiplier'] = self.powerModule.dut.sendCommand('read ' + QTL2347.V3_3_AUX_VOLT_MULTIPLIER_ADDR)
            coefficients['offset'] = self.powerModule.dut.sendCommand('read ' + QTL2347.V3_3_AUX_VOLT_OFFSET_ADDR)
            return coefficients

        def writeCoefficients(self, coefficients):
            self.powerModule.dut.sendAndVerifyCommand('write ' + QTL2347.V3_3_AUX_VOLT_MULTIPLIER_ADDR + ' ' + coefficients['multiplier'])
            self.powerModule.dut.sendAndVerifyCommand('write ' + QTL2347.V3_3_AUX_VOLT_OFFSET_ADDR + ' ' + coefficients['offset'])

    class QTL2347_3V3_AUX_LeakageCalibration(QTL2347Calibration):

        def __init__(self, powerModule):
            self.powerModule = powerModule
            self.absErrorLimit = 50
            self.relErrorLimit = 0
            self.test_min = 1000
            self.test_max = 14400
            self.test_steps = 20
            self.units = 'uA'
            self.scaling = 1
            self.multiplier_signed = False
            self.multiplier_int_width = 1
            self.multiplier_frac_width = 16
            self.offset_signed = False
            self.offset_int_width = 16
            self.offset_frac_width = 16
            self.unitTemp = self.powerModule.dut.sendCommand('meas:temp unit?')
            self.v5Temp = self.powerModule.dut.sendCommand('meas:temp 5v?')
            self.v12Temp = self.powerModule.dut.sendCommand('meas:temp 12v?')

        def init(self):
            super().init_cal('3V3_AUX')
            self.powerModule.dut.sendAndVerifyCommand('write ' + QTL2347.CALIBRATION_CONTROL_ADDR + ' 0x00F5')
            self.powerModule.dut.sendAndVerifyCommand('write ' + QTL2347.V3_3_AUX_LEAKAGE_MULTIPLIER_ADDR + ' 0x0000')
            showDialog(title='Setup 3.3V Leakage Calibration', message='\x07Please connect the load to the 3.3v channel and disconnect host power')
            while super().checkLoadVoltage(500, 500) != True:
                showDialog(title='Disconnnect Host Power', message='\x07Please disconnect host power from the fixture on the 3.3v Channel')

        def setRef(self, value):
            return load_set_volt(self.powerModule.load, value)

        def readRef(self):
            return -load_meas_cur(self.powerModule.load)

        def readVal(self):
            return load_get_volt(self.powerModule.load)

        def setCoefficients(self):
            pass

        def finish(self):
            super().finish_cal()

        def report(self, data):
            return super().report('calibrate', data)

        def readCoefficients(self):
            coefficients = {}
            coefficients['multiplier'] = self.powerModule.dut.sendCommand('read ' + QTL2347.V3_3_AUX_LEAKAGE_MULTIPLIER_ADDR)
            return coefficients

        def writeCoefficients(self, coefficents):
            self.powerModule.dut.sendAndVerifyCommand('write ' + QTL2347.V3_3_AUX_LEAKAGE_MULTIPLIER_ADDR + ' ' + coefficents['multiplier'])

    class QTL2347_3V3_AUX_CurrentCalibration(QTL2347Calibration):

        def __init__(self, powerModule):
            self.powerModule = powerModule
            self.absErrorLimit = 2
            self.relErrorLimit = 2
            self.test_min = 100
            self.test_max = 400000
            self.test_steps = 20
            self.units = 'uA'
            self.scaling = 64
            self.multiplier_signed = False
            self.multiplier_int_width = 1
            self.multiplier_frac_width = 16
            self.offset_signed = True
            self.offset_int_width = 10
            self.offset_frac_width = 6
            self.unitTemp = self.powerModule.dut.sendCommand('meas:temp unit?')
            self.v5Temp = self.powerModule.dut.sendCommand('meas:temp 5v?')
            self.v12Temp = self.powerModule.dut.sendCommand('meas:temp 12v?')

        def init(self):
            super().init_cal('3V3_AUX')
            self.powerModule.dut.sendAndVerifyCommand('write ' + QTL2347.V3_3_AUX_MULTIPLIER_ADDR + ' 0x0000')
            self.powerModule.dut.sendAndVerifyCommand('write ' + QTL2347.V3_3_AUX_OFFSET_ADDR + ' 0x0000')
            showDialog(title='Setup 3.3V Aux Current Calibration', message='\x07Please connect host power and load to the 3.3v Aux channel')
            while super().checkLoadVoltage(12000, 1000) != True:
                showDialog(title='Connect Host Power', message='\x07Please connect host power and load to the 3.3v Aux channel on the fixture')

        def setRef(self, value):
            load_set_cur(self.powerModule.load, value)

        def readRef(self):
            voltage = super().meas_3v3_aux_volt()
            leakage = voltage * self.powerModule.calibrations['3.3V Aux']['Leakage'].multiplier.originalValue() + self.powerModule.calibrations['3.3V Aux']['Leakage'].offset.originalValue()
            return load_meas_cur(self.powerModule.load) + leakage

        def readVal(self):
            return super().meas_3v3_aux_cur()

        def setCoefficients(self):
            result1 = self.powerModule.dut.sendAndVerifyCommand('write ' + QTL2347.V3_3_AUX_MULTIPLIER_ADDR + ' ' + self.multiplier.hexString(4))
            result2 = self.powerModule.dut.sendAndVerifyCommand('write ' + QTL2347.V3_3_AUX_OFFSET_ADDR + ' ' + self.offset.hexString(4))
            if result1 and result2:
                result = True
            else:
                result = False
            logSimpleResult('Set 3.3v Aux low current', result)
            result = self.powerModule.dut.sendAndVerifyCommand('write ' + QTL2347.V3_3_AUX_LEAKAGE_MULTIPLIER_ADDR + ' ' + self.powerModule.calibrations['3.3V Aux']['Leakage'].multiplier.hexString(4))

        def finish(self):
            super().finish_cal()

        def report(self, data):
            return super().report('calibrate', data)

        def readCoefficients(self):
            coefficients = {}
            coefficients['multiplier'] = self.powerModule.dut.sendCommand('read ' + QTL2347.V3_3_AUX_MULTIPLIER_ADDR)
            coefficients['offset'] = self.powerModule.dut.sendCommand('read ' + QTL2347.V3_3_AUX_OFFSET_ADDR)
            return coefficients

        def writeCoefficients(self, coefficients):
            self.powerModule.dut.sendAndVerifyCommand('write ' + QTL2347.V3_3_AUX_MULTIPLIER_ADDR + ' ' + coefficients['multiplier'])
            self.powerModule.dut.sendAndVerifyCommand('write ' + QTL2347.V3_3_AUX_OFFSET_ADDR + ' ' + coefficients['offset'])

    class QTL2347_12V_VoltageVerification(QTL2347Calibration):

        def __init__(self, powerModule):
            self.powerModule = powerModule
            self.absErrorLimit = 1
            self.relErrorLimit = 1
            self.test_min = 40
            self.test_max = 14400
            self.test_steps = 20
            self.units = 'mV'
            self.unitTemp = self.powerModule.dut.sendCommand('meas:temp unit?')
            self.v5Temp = self.powerModule.dut.sendCommand('meas:temp 5v?')
            self.v12Temp = self.powerModule.dut.sendCommand('meas:temp 12v?')

        def init(self):
            super().init_cal('12V')
            showDialog(title='Setup 12V Voltage Verification', message='\x07Please connect the load to the 12v channel and disconnect host power')
            while super().checkLoadVoltage(500, 500) != True:
                showDialog(title='Disconnnect Host Power', message='\x07Please disconnect host power from the fixture on the 12v Channel')

        def setRef(self, value):
            return load_set_volt(self.powerModule.load, value)

        def readRef(self):
            return load_meas_volt(self.powerModule.load)

        def readVal(self):
            return super().meas_12v_volt()

        def finish(self):
            super().finish_cal()

        def report(self, data):
            return super().report('verify', data)

    class QTL2347_12V_LowCurrentVerification(QTL2347Calibration):

        def __init__(self, powerModule):
            self.powerModule = powerModule
            self.absErrorLimit = 2
            self.relErrorLimit = 2
            self.test_min = 100
            self.test_max = 1000
            self.test_steps = 20
            self.units = 'uA'
            self.unitTemp = self.powerModule.dut.sendCommand('meas:temp unit?')
            self.v5Temp = self.powerModule.dut.sendCommand('meas:temp 5v?')
            self.v12Temp = self.powerModule.dut.sendCommand('meas:temp 12v?')

        def init(self):
            super().init_cal('12V')
            showDialog(title='Setup 12V Current Verification', message='\x07Please connect the load to the 12v channel and connect host power')
            while super().checkLoadVoltage(12000, 1000) != True:
                showDialog(title='Connnect Host Power', message='\x07Please connect host power to the fixture on the 12v Channel')

        def setRef(self, value):
            load_set_cur(self.powerModule.load, value)

        def readRef(self):
            return load_meas_cur(self.powerModule.load)

        def readVal(self):
            return super().meas_12v_cur()

        def finish(self):
            super().finish_cal()

        def report(self, data):
            return super().report('verify', data)

    class QTL2347_12V_HighCurrentVerification(QTL2347Calibration):

        def __init__(self, powerModule):
            self.powerModule = powerModule
            self.absErrorLimit = 2000
            self.relErrorLimit = 1
            self.test_min = 1000
            self.test_max = 4000000
            self.test_steps = 20
            self.units = 'uA'
            self.unitTemp = self.powerModule.dut.sendCommand('meas:temp unit?')
            self.v5Temp = self.powerModule.dut.sendCommand('meas:temp 5v?')
            self.v12Temp = self.powerModule.dut.sendCommand('meas:temp 12v?')

        def init(self):
            super().init_cal('12v')
            showDialog(title='Setup 12V Current Verification', message='\x07Please connect the load to the 12v channel and connect host power')
            while super().checkLoadVoltage(12000, 1000) != True:
                showDialog(title='Connnect Host Power', message='\x07Please connect host power to the fixture on the 12v Channel')

        def setRef(self, value):
            load_set_cur(self.powerModule.load, value)

        def readRef(self):
            return load_meas_cur(self.powerModule.load)

        def readVal(self):
            return super().meas_12v_cur()

        def finish(self):
            super().finish_cal()

        def report(self, data):
            return super().report('verify', data)

    class QTL2347_3V3_VoltageVerification(QTL2347Calibration):

        def __init__(self, powerModule):
            self.powerModule = powerModule
            self.absErrorLimit = 1
            self.relErrorLimit = 1
            self.test_min = 40
            self.test_max = 6000
            self.test_steps = 20
            self.units = 'mV'
            self.unitTemp = self.powerModule.dut.sendCommand('meas:temp unit?')
            self.v5Temp = self.powerModule.dut.sendCommand('meas:temp 5v?')
            self.v12Temp = self.powerModule.dut.sendCommand('meas:temp 12v?')

        def init(self):
            super().init_cal('3V3')
            showDialog(title='Setup 3.3V Voltage Verification', message='\x07Please connect the load to the 3.3v channel and disconnect host power')
            while super().checkLoadVoltage(500, 500) != True:
                showDialog(title='Disconnnect Host Power', message='\x07Please disconnect host power from the fixture on the 3.3v Channel')

        def setRef(self, value):
            return load_set_volt(self.powerModule.load, value)

        def readRef(self):
            return load_meas_volt(self.powerModule.load)

        def readVal(self):
            return super().meas_3v3_volt()

        def finish(self):
            super().finish_cal()

        def report(self, data):
            return super().report('verify', data)

    class QTL2347_3V3_LowCurrentVerification(QTL2347Calibration):

        def __init__(self, powerModule):
            self.powerModule = powerModule
            self.absErrorLimit = 2
            self.relErrorLimit = 2
            self.test_min = 100
            self.test_max = 1000
            self.test_steps = 20
            self.units = 'uA'
            self.unitTemp = self.powerModule.dut.sendCommand('meas:temp unit?')
            self.v5Temp = self.powerModule.dut.sendCommand('meas:temp 5v?')
            self.v12Temp = self.powerModule.dut.sendCommand('meas:temp 12v?')

        def init(self):
            super().init_cal('3V3')
            showDialog(title='Setup 3.3V Current Verification', message='\x07Please connect the load to the 3.3v channel and connect host power')
            while super().checkLoadVoltage(12000, 1000) != True:
                showDialog(title='Connnect Host Power', message='\x07Please connect host power to the fixture on the 3.3v Channel')

        def setRef(self, value):
            load_set_cur(self.powerModule.load, value)

        def readRef(self):
            return load_meas_cur(self.powerModule.load)

        def readVal(self):
            return super().meas_3v3_cur()

        def finish(self):
            super().finish_cal()

        def report(self, data):
            return super().report('verify', data)

    class QTL2347_3V3_HighCurrentVerification(QTL2347Calibration):

        def __init__(self, powerModule):
            self.powerModule = powerModule
            self.absErrorLimit = 2000
            self.relErrorLimit = 1
            self.test_min = 1000
            self.test_max = 4000000
            self.test_steps = 20
            self.units = 'uA'
            self.unitTemp = self.powerModule.dut.sendCommand('meas:temp unit?')
            self.v5Temp = self.powerModule.dut.sendCommand('meas:temp 5v?')
            self.v12Temp = self.powerModule.dut.sendCommand('meas:temp 12v?')

        def init(self):
            super().init_cal('3V3')
            showDialog(title='Setup 3.3V Current Verification', message='\x07Please connect the load to the 3.3v channel and connect host power')
            while super().checkLoadVoltage(12000, 1000) != True:
                showDialog(title='Connnect Host Power', message='\x07Please connect host power to the fixture on the 3.3v Channel')

        def setRef(self, value):
            load_set_cur(self.powerModule.load, value)

        def readRef(self):
            return load_meas_cur(self.powerModule.load)

        def readVal(self):
            return super().meas_3v3_cur()

        def finish(self):
            super().finish_cal()

        def report(self, data):
            return super().report('verify', data)

    class QTL2347_3V3_AUX_VoltageVerification(QTL2347Calibration):

        def __init__(self, powerModule):
            self.powerModule = powerModule
            self.absErrorLimit = 1
            self.relErrorLimit = 1
            self.test_min = 40
            self.test_max = 14400
            self.test_steps = 20
            self.units = 'mV'
            self.unitTemp = self.powerModule.dut.sendCommand('meas:temp unit?')
            self.v5Temp = self.powerModule.dut.sendCommand('meas:temp 5v?')
            self.v12Temp = self.powerModule.dut.sendCommand('meas:temp 12v?')

        def init(self):
            super().init_cal('3V3_AUX')
            showDialog(title='Setup 3.3V Aux Voltage Verification', message='\x07Please connect the load to the 3.3v Aux channel and disconnect host power')
            while super().checkLoadVoltage(500, 500) != True:
                showDialog(title='Disconnnect Host Power', message='\x07Please disconnect host power from the fixture on the 3.3v Aux Channel')

        def setRef(self, value):
            return load_set_volt(self.powerModule.load, value)

        def readRef(self):
            return load_meas_volt(self.powerModule.load)

        def readVal(self):
            return super().meas_3v3_aux_volt()

        def finish(self):
            super().finish_cal()

        def report(self, data):
            return super().report('verify', data)

    class QTL2347_3V3_AUX_CurrentVerification(QTL2347Calibration):

        def __init__(self, powerModule):
            self.powerModule = powerModule
            self.absErrorLimit = 2
            self.relErrorLimit = 2
            self.test_min = 100
            self.test_max = 400000
            self.test_steps = 20
            self.units = 'uA'
            self.unitTemp = self.powerModule.dut.sendCommand('meas:temp unit?')
            self.v5Temp = self.powerModule.dut.sendCommand('meas:temp 5v?')
            self.v12Temp = self.powerModule.dut.sendCommand('meas:temp 12v?')

        def init(self):
            super().init_cal('3V3_AUX')
            showDialog(title='Setup 3.3V Aux Current Verification', message='\x07Please connect the load to the 3.3v Aux channel and connect host power')
            while super().checkLoadVoltage(12000, 1000) != True:
                showDialog(title='Connnect Host Power', message='\x07Please connect host power to the fixture on the 3.3v Aux Channel')

        def setRef(self, value):
            load_set_cur(self.powerModule.load, value)

        def readRef(self):
            return load_meas_cur(self.powerModule.load)

        def readVal(self):
            return super().meas_3v3_aux_cur()

        def finish(self):
            super().finish_cal()

        def report(self, data):
            return super().report('verify', data)

    def __init__(self, dut):
        self.name = 'PCIe x16 Power Measurement Fixture'
        self.dut = dut
        self.calibrations = {}
        self.calibrations['12V'] = {'Voltage':self.QTL2347_12V_VoltageCalibration(self), 
         'Leakage':self.QTL2347_12V_LeakageCalibration(self), 
         'Low Current':self.QTL2347_12V_LowCurrentCalibration(self), 
         'High Current':self.QTL2347_12V_HighCurrentCalibration(self)}
        self.calibrations['3.3V'] = {'Voltage':self.QTL2347_3V3_VoltageCalibration(self), 
         'Leakage':self.QTL2347_3V3_LeakageCalibration(self), 
         'Low Current':self.QTL2347_3V3_LowCurrentCalibration(self), 
         'High Current':self.QTL2347_3V3_HighCurrentCalibration(self)}
        self.calibrations['3.3V Aux'] = {'Voltage':self.QTL2347_3V3_AUX_VoltageCalibration(self), 
         'Leakage':self.QTL2347_3V3_AUX_LeakageCalibration(self), 
         'Current':self.QTL2347_3V3_AUX_CurrentCalibration(self)}
        self.verifications = {}
        self.verifications['12V'] = {'Voltage':self.QTL2347_12V_VoltageVerification(self), 
         'Low Current':self.QTL2347_12V_LowCurrentVerification(self), 
         'High Current':self.QTL2347_12V_HighCurrentVerification(self)}
        self.verifications['3.3V'] = {'Voltage':self.QTL2347_3V3_VoltageVerification(self), 
         'Low Current':self.QTL2347_3V3_LowCurrentVerification(self), 
         'High Current':self.QTL2347_3V3_HighCurrentVerification(self)}
        self.verifications['3.3V Aux'] = {'Voltage':self.QTL2347_3V3_AUX_VoltageVerification(self), 
         'Current':self.QTL2347_3V3_AUX_CurrentVerification(self)}


if __name__ == '__main__':
    main()