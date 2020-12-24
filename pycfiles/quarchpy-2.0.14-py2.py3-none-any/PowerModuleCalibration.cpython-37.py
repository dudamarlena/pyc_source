# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\sboon\AppData\Local\Temp\pip-install-ptdbtr91\quarchpy\quarchpy\calibration\PowerModuleCalibration.py
# Compiled at: 2020-03-25 05:10:07
# Size of source mod 2**32: 16179 bytes
"""
Quarch Power Module Calibration Functions
Written for Python 3.6 64 bit

M Dearman April 2019
"""
from functools import reduce
from quarchpy.calibration.deviceHelpers import returnMeasurement
from quarchpy.device.device import *
import quarchpy.calibration.calibrationConfig, types
from time import sleep, time
from math import ceil
from quarchpy.user_interface import *
from quarchpy.calibration.calibration_classes import TestSummary

def load_set_volt(load, value):
    return load.setReferenceVoltage(value / 1000)


def load_get_volt(load):
    return load.getLoadVoltage() * 1000


def load_meas_volt(load):
    return load.measureLoadVoltage() * 1000


def load_set_cur(load, value):
    response = load.setReferenceCurrent(value / 1000000)
    return response


def load_meas_cur(load):
    return load.measureLoadCurrent() * 1000000


class Coefficient:

    def __init__(self, value, signed, int_width, frac_width):
        if not (signed == True and abs(value) >= 2 ** (int_width - 1)):
            if not signed == False or abs(value) >= 2 ** int_width:
                self.overflow = True
            else:
                self.overflow = False
        self.value = value
        self.signed = signed
        self.int_width = int_width
        self.frac_width = frac_width

    def originalValue(self):
        return self.value

    def storedValue(self):
        return round(self.value * 2 ** self.frac_width) / 2 ** self.frac_width

    def hexString(self, hex_chars):
        return '{:#0{hex_chars}x}'.format((round(self.value * 2 ** self.frac_width) & 2 ** (self.int_width + self.frac_width) - 1 & 2 ** (hex_chars * 4) - 1), hex_chars=(hex_chars + 2))


class Calibration:

    def __init__(self):
        self.powerModule = None
        self.absErrorLimit = None
        self.relErrorLimit = None
        self.test_min = None
        self.test_max = None
        self.test_steps = None
        self.units = None
        self.scaling = None
        self.multiplier_signed = None
        self.multiplier_int_width = None
        self.multiplier_frac_width = None
        self.offset_signed = None
        self.offset_int_width = None
        self.offset_frac_width = None
        self.unitTemp = ''
        self.v5Temp = ''
        self.v12Temp = ''

    def generate(self, points):
        thisMultiplier, thisOffset = bestFit(points)
        thisOffset /= self.scaling
        self.multiplier = Coefficient(thisMultiplier, self.multiplier_signed, self.multiplier_int_width, self.multiplier_frac_width)
        self.offset = Coefficient(-thisOffset, self.offset_signed, self.offset_int_width, self.offset_frac_width)

    def getResult(self, value):
        return round((float(value) / self.scaling * self.multiplier.storedValue() - self.offset.storedValue()) * self.scaling)

    def getStepMultiplier(self):
        return (self.test_max / self.test_min) ** (1 / (self.test_steps - 1))


class PowerModule:

    def __init__(self):
        self.name = None
        self.dut = None
        self.calibrations = {}
        self.verifications = {}
        self.voltageMode = None

    def specific_requirements(self):
        pass

    def open_module(self):
        pass

    def clear_calibration(self):
        pass

    def write_calibration(self):
        pass

    def close_module(self):
        pass

    def readCalibration(self):
        calValues = {}
        for channel in self.calibrations:
            calValues[channel] = {}
            for calibration in self.calibrations[channel]:
                calValues[channel][calibration] = self.calibrations[channel][calibration].readCoefficients()

        return calValues

    def writeCalibration(self, calValues):
        self.dut.sendCommand('write 0xf000 0xaa55')
        self.dut.sendCommand('write 0xf000 0x55aa')
        for channel in calValues:
            for calibration in calValues[channel]:
                self.calibrations[channel][calibration].writeCoefficients(calValues[channel][calibration])

    def calibrate(self, load, reportFile, calHeader):
        return self.calibrateOrVerify('calibrate', load, reportFile, calHeader)

    def verify(self, load, reportFile, calHeader):
        return self.calibrateOrVerify('verify', load, reportFile, calHeader)

    def calibrateOrVerify(self, action, load, reportFile, calHeader):
        if action == 'calibrate':
            list = self.calibrations
        else:
            if action == 'verify':
                list = self.verifications
            else:
                raise Exception('calibrateOrVerify() called with invalid action: ' + action)
        self.load = load
        self.open_module()
        if action == 'calibrate':
            self.clear_calibration()
        passed = True
        result = True
        for channel in list:
            for calibration in list[channel]:
                thisItem = list[channel][calibration]
                if action == 'calibrate':
                    startTestBlock('Calibrating ' + channel + ' ' + calibration)
                else:
                    startTestBlock('Verifying ' + channel + ' ' + calibration)
                thisItem.init()
                iteration = 1
                data = []
                steps = thisItem.test_steps
                test_value = thisItem.test_min
                while test_value <= thisItem.test_max:
                    thisItem.setRef(int(test_value))
                    reference = thisItem.readRef()
                    value = thisItem.readVal()
                    data.append([value, reference])
                    progressBar(iteration, steps)
                    iteration += 1
                    test_value = int(test_value * thisItem.getStepMultiplier())

                thisItem.finish()
                if action == 'calibrate':
                    thisItem.generate(data)
                    thisItem.setCoefficients()
                else:
                    report = thisItem.report(data)
                    if action == 'calibrate':
                        title = channel + ' ' + calibration + ' Calibration'
                        logCalibrationResult(title, report)
                        reportFile.write('\n\n' + channel + ' ' + calibration + ' Calibration')
                    else:
                        title = channel + ' ' + calibration + ' Verification'
                        logCalibrationResult(title, report)
                        reportFile.write('\n\n' + channel + ' ' + calibration + ' Verification')
                    myTestSummary = TestSummary(calibrationType=action, channel=channel, testName=calibration, passed=(report['result']),
                      worstCase=(report['worst case']))
                    calHeader.testSummaryList.append(myTestSummary)
                    if report['result'] == False:
                        passed = False
                        result = False
                    else:
                        passed = True
                reportFile.write('          Pass Level  +/-(' + str(report['calObj'].absErrorLimit) + str(report['calObj'].units) + ' + ' + str(report['calObj'].relErrorLimit) + '%) \n')
                reportFile.write('Unit Temperature : ' + str(report['calObj'].unitTemp) + '   5v Temperature : ' + str(report['calObj'].v5Temp) + '   12v Temperature : ' + str(report['calObj'].v12Temp))
                reportFile.write('\n' + report['report'].replace('\r\n', '\n') + '\n\n\n')
                reportFile.write('' + '{0:<35}'.format(title) + '     ' + '{0:>10}'.format('Passed : ') + '  ' + '{0:<5}'.format(str(passed)) + '     ' + '{0:>11}'.format('worst case:') + '  ' + '{0:>11}'.format(report['worst case']))
                reportFile.write('\n\n\n')
                reportFile.flush()

        if action == 'calibrate':
            self.write_calibration()
        self.close_module()
        return [
         result, calHeader]


def bestFit(points):
    try:
        AveX = reduce(lambda sum, point: sum + point[0], points, 0) / len(points)
        AveY = reduce(lambda sum, point: sum + point[1], points, 0) / len(points)
        SumXY = reduce(lambda sum, point: sum + (point[0] - AveX) * (point[1] - AveY), points, 0)
        SumX2 = reduce(lambda sum, point: sum + (point[0] - AveX) * (point[0] - AveX), points, 0)
        Slope = SumXY / SumX2
        Intercept = AveY - Slope * AveX
        return (
         Slope, Intercept)
    except Exception as e:
        try:
            raise Exception(e)
        finally:
            e = None
            del e


def getError(reference_value, calculated_value, abs_error_limit, rel_error_limit):
    error_value = calculated_value - reference_value
    if error_value >= 0:
        error_sign = '+'
    else:
        error_sign = '-'
    error_value = abs(error_value)
    if error_value >= abs_error_limit:
        abs_error_val = abs_error_limit
        rel_error_val = abs((error_value - abs_error_val) / calculated_value * 100)
    else:
        abs_error_val = ceil(error_value)
        rel_error_val = 0
    if abs(rel_error_val) <= rel_error_limit:
        result = True
    else:
        result = False
    return [
     error_value, error_sign, abs_error_val, rel_error_val, result]


if __name__ == '__main__':
    main()