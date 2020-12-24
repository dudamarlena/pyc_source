# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\sboon\AppData\Local\Temp\pip-install-ptdbtr91\quarchpy\quarchpy\calibration\HDPowerModule.py
# Compiled at: 2020-03-25 05:10:07
# Size of source mod 2**32: 62710 bytes
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
from quarchpy.calibration.calibrationConfig import *
from quarchpy.user_interface import *
from quarchpy.user_interface import logSimpleResult
from quarchpy.device.device import *
from quarchpy.device.scanDevices import userSelectDevice

class HDPowerModule(PowerModule):
    V5_VOLT_OFFSET_ADDR = '0xF002'
    V5_VOLT_MULTIPLIER_ADDR = '0xF003'
    V5_LOW_OFFSET_ADDR = '0xF004'
    V5_LOW_MULTIPLIER_ADDR = '0xF005'
    V5_LEAKAGE_MULTIPLIER_ADDR = '0xF006'
    V5_HIGH_OFFSET_ADDR = '0xF007'
    V5_HIGH_MULTIPLIER_ADDR = '0xF008'
    V12_VOLT_OFFSET_ADDR = '0xF009'
    V12_VOLT_MULTIPLIER_ADDR = '0xF00A'
    V12_LOW_OFFSET_ADDR = '0xF00B'
    V12_LOW_MULTIPLIER_ADDR = '0xF00C'
    V12_LEAKAGE_MULTIPLIER_ADDR = '0xF00D'
    V12_HIGH_OFFSET_ADDR = '0xF00E'
    V12_HIGH_MULTIPLIER_ADDR = '0xF00F'
    V5_OUTPUT_OFFSET_ADDR = '0xF010'
    V12_OUTPUT_OFFSET_ADDR = '0xF011'
    switchbox = None

    def specific_requirements(self):
        if 'switchbox' in calibrationResources.keys():
            self.switchbox = calibrationResources['switchbox']
        self.switchbox = self.getSwitchbox()
        calibrationResources['switchbox'] = self.switchbox
        if 'runtimecheckskipped' not in calibrationResources.keys():
            self.wait_for_up_time(desired_up_time=600)

    def open_module(self):
        self.dut.sendCommand('write 0xf000 0xaa55')
        self.dut.sendCommand('write 0xf000 0x55aa')

    def getSwitchbox(self):
        if self.switchbox is None:
            while True:
                switchboxAddress = userSelectDevice(scanFilterStr=['QTL2294'], message='Select a calibration switchbox.', nice=True, target_conn='rest')
                if switchboxAddress == 'quit':
                    printText('User Quit Program')
                    sys.exit(0)
                try:
                    self.switchbox = quarchDevice(switchboxAddress)
                    break
                except:
                    printText('Unable to communicate with selected device!')
                    printText('')
                    switchboxAddress = None

        return self.switchbox

    def wait_for_up_time(self, desired_up_time=600):
        calibrationResources['runtimecheckskipped'] = False
        try:
            current_up_time = int(self.dut.sendCommand('conf:runtimes?').lower().replace('s', ''))
            success = True
            wait_time = desired_up_time - current_up_time
        except:
            success = False
            current_up_time = 0
            wait_time = desired_up_time

        if current_up_time < desired_up_time:
            if calibrationResources['user_mode'] == 'console':
                skip_uptime_wait = listSelection(title='Up Time', message=('Has the Module been on for more than ' + str(desired_up_time) + ' seconds?'),
                  selectionList=[
                 'Yes', 'No'],
                  tableHeaders=['Options'],
                  nice=True)
            else:
                skip_uptime_wait = listSelection(title='Up Time', message=('Has the Module been on for more than ' + str(desired_up_time) + ' seconds?'),
                  selectionList='Yes=Yes,No=No',
                  tableHeaders=['Options'])
            if skip_uptime_wait.lower() == 'no':
                printText('Waiting ' + str(wait_time) + ' seconds')
                startTime = time.time()
                currentTime = time.time()
                while currentTime - startTime < wait_time:
                    progressBar(int(currentTime - startTime), wait_time - 1)
                    currentTime = time.time()

                printText('Wait Complete')
            else:
                printText('Wait for runtime to reach ' + str(desired_up_time) + 's skipped')
                calibrationResources['runtimecheckskipped'] = True

    def clear_calibration(self):
        self.dut.sendCommand('write 0xf000 0xaa55')
        self.dut.sendCommand('write 0xf000 0x55aa')
        self.dut.sendAndVerifyCommand('write ' + HDPowerModule.V12_OUTPUT_OFFSET_ADDR + ' 0x0000')
        self.dut.sendAndVerifyCommand('write ' + HDPowerModule.V12_VOLT_OFFSET_ADDR + ' 0x0000')
        self.dut.sendAndVerifyCommand('write ' + HDPowerModule.V12_VOLT_MULTIPLIER_ADDR + ' 0x0000')
        self.dut.sendAndVerifyCommand('write ' + HDPowerModule.V12_LOW_OFFSET_ADDR + ' 0x0000')
        self.dut.sendAndVerifyCommand('write ' + HDPowerModule.V12_LOW_MULTIPLIER_ADDR + ' 0x0000')
        self.dut.sendAndVerifyCommand('write ' + HDPowerModule.V12_HIGH_OFFSET_ADDR + ' 0x0000')
        self.dut.sendAndVerifyCommand('write ' + HDPowerModule.V12_HIGH_MULTIPLIER_ADDR + ' 0x0000')
        self.dut.sendAndVerifyCommand('write ' + HDPowerModule.V12_LEAKAGE_MULTIPLIER_ADDR + ' 0x0000')
        self.dut.sendAndVerifyCommand('write ' + HDPowerModule.V5_OUTPUT_OFFSET_ADDR + ' 0x0000')
        self.dut.sendAndVerifyCommand('write ' + HDPowerModule.V5_VOLT_OFFSET_ADDR + ' 0x0000')
        self.dut.sendAndVerifyCommand('write ' + HDPowerModule.V5_VOLT_MULTIPLIER_ADDR + ' 0x0000')
        self.dut.sendAndVerifyCommand('write ' + HDPowerModule.V5_LOW_OFFSET_ADDR + ' 0x0000')
        self.dut.sendAndVerifyCommand('write ' + HDPowerModule.V5_LOW_MULTIPLIER_ADDR + ' 0x0000')
        self.dut.sendAndVerifyCommand('write ' + HDPowerModule.V5_HIGH_OFFSET_ADDR + ' 0x0000')
        self.dut.sendAndVerifyCommand('write ' + HDPowerModule.V5_HIGH_MULTIPLIER_ADDR + ' 0x0000')
        self.dut.sendAndVerifyCommand('write ' + HDPowerModule.V5_LEAKAGE_MULTIPLIER_ADDR + ' 0x0000')
        self.dut.sendAndVerifyCommand('write 0xf012 0xaa55')

    def close_module(self):
        printText('')
        printText('resetting the device...')
        printText('')
        self.dut.resetDevice(40)
        response = self.dut.sendCommand('*idn?')

    class HDCalibration(Calibration):

        def __init__(self):
            super().__init__()

        def init_cal(self, voltage):
            mode = self.powerModule.dut.sendCommand('conf:out:mode?')
            while mode != '5V':
                self.powerModule.dut.sendAndVerifyCommand('conf:out:mode 5v')
                sleep(4)
                mode = self.powerModule.dut.sendCommand('conf:out:mode?')

            self.powerModule.dut.sendAndVerifyCommand('power up')
            self.powerModule.dut.sendAndVerifyCommand('CONFig:OUTput:12v:PULLdown OFF')
            self.powerModule.dut.sendAndVerifyCommand('CONFig:OUTput:5v:PULLdown OFF')
            if self.powerModule.dut.sendCommand('rec:ave?').find('32k') != 0:
                self.powerModule.dut.sendAndVerifyCommand('rec:ave 32k')
            else:
                self.powerModule.dut.sendCommand('write 0xf000 0xaa55')
                self.powerModule.dut.sendCommand('write 0xf000 0x55aa')
                if voltage.upper() == '12V':
                    self.powerModule.switchbox.sendAndVerifyCommand('connect 12v')
                else:
                    if voltage.upper() == '5V':
                        self.powerModule.switchbox.sendAndVerifyCommand('connect 5v')
                    else:
                        raise ValueError('Invalid voltage specified')
                if voltage.upper() == '12V':
                    lower_limit = 11
                    upper_limit = 13
                    self.powerModule.dut.sendAndVerifyCommand('sig:12v:volt 12000')
                else:
                    if voltage.upper() == '5V':
                        lower_limit = 4
                        upper_limit = 6
                        self.powerModule.dut.sendAndVerifyCommand('sig:5v:volt 5000')
                    else:
                        raise ValueError('Invalid voltage specified')
            result = self.powerModule.load.measureNoLoadVoltage()
            while not result < lower_limit:
                if result > upper_limit:
                    if voltage.upper() == '12V':
                        lower_limit = 11
                        upper_limit = 13
                        self.powerModule.dut.sendAndVerifyCommand('sig:12v:volt 12000')
                    else:
                        if voltage.upper() == '5V':
                            lower_limit = 4
                            upper_limit = 6
                            self.powerModule.dut.sendAndVerifyCommand('sig:5v:volt 5000')
                        else:
                            enclosure = self.powerModule.dut.sendCommand('*enclosure?')
                            if enclosure.__contains__('1995'):
                                port = self.powerModule.dut.sendCommand('*POSITION?')
                                showDialog(title='Check load connection', message=('\x07Please connect the calibration switch box to ' + enclosure + ' Port: ' + port))
                            else:
                                showDialog(title='Check load connection', message=('\x07Please connect the calibration switch box to ' + enclosure))
                            self.powerModule.dut.sendAndVerifyCommand('run pow up')
                            if voltage.upper() == '12V':
                                self.powerModule.switchbox.sendAndVerifyCommand('connect 12v')
                            else:
                                if voltage.upper() == '5V':
                                    self.powerModule.switchbox.sendAndVerifyCommand('connect 5v')
                                else:
                                    raise ValueError('Invalid voltage specified')
                        printText('Verifying Connection...')
                        result = self.powerModule.load.measureNoLoadVoltage()
                    if result < lower_limit or result > upper_limit:
                        printText('Connection is NOT correct, check cabling\n')
                else:
                    printText('Connection is correct\n')

            self.unitTemp = self.powerModule.dut.sendCommand('meas:temp unit?')
            self.v5Temp = self.powerModule.dut.sendCommand('meas:temp 5v?')
            self.v12Temp = self.powerModule.dut.sendCommand('meas:temp 12v?')

        def set_12v_volt(self, value):
            self.powerModule.dut.sendAndVerifyCommand('sig:12v:volt ' + str(value))
            sleep(0.2)

        def get_12v_volt(self):
            response = returnMeasurement(self.powerModule.dut, 'sig:12v:volt?')
            return int(response[0])

        def meas_12v_volt(self):
            response = returnMeasurement(self.powerModule.dut, 'meas:volt:12v?')
            return int(response[0])

        def meas_12v_cur(self):
            response = returnMeasurement(self.powerModule.dut, 'meas:cur 12v?')
            return float(response[0]) * 1000

        def set_5v_volt(self, value):
            self.powerModule.dut.sendAndVerifyCommand('sig:5v:volt ' + str(value))
            sleep(0.2)

        def get_5v_volt(self):
            response = returnMeasurement(self.powerModule.dut, 'sig:5v:volt?')
            return int(response[0])

        def meas_5v_volt(self):
            response = returnMeasurement(self.powerModule.dut, 'meas:volt:5v?')
            return int(response[0])

        def meas_5v_cur(self):
            response = returnMeasurement(self.powerModule.dut, 'meas:cur 5v?')
            return float(response[0]) * 1000

        def finish_cal(self):
            self.powerModule.load.setReferenceCurrent(0)
            self.powerModule.load.disable()
            self.powerModule.dut.sendAndVerifyCommand('power down')
            self.powerModule.dut.sendAndVerifyCommand('sig:12v:volt 5000')
            self.powerModule.dut.sendAndVerifyCommand('sig:12v:volt 12000')
            self.powerModule.dut.sendAndVerifyCommand('write 0xf001 0x0100')

        def report(self, action, data):
            report = []
            if action == 'calibrate':
                tableHeaders = [
                 'Reference ' + self.units, 'Raw Value ' + self.units, 'Result ' + self.units, 'Error ' + self.units, '+/-(Abs Error,% Error)', 'Pass']
            else:
                if action == 'verify':
                    tableHeaders = [
                     'Reference ' + self.units, 'Result ' + self.units, 'Error ' + self.units, '+/-(Abs Error,% Error)', 'Pass']
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
                        report.append(['{:.3f}'.format(reference), '{:.1f}'.format(ppmValue), '{:.1f}'.format(calibratedValue), '{:.3f}'.format(actError), errorSign + '(' + str(absError) + str(self.units) + ',' + str('{:.3f}'.format(relError)) + '%)', passfail(result)])
                    elif action == 'verify':
                        report.append(['{:.3f}'.format(reference), '{:.1f}'.format(ppmValue), '{:.3f}'.format(actError), errorSign + '(' + str(absError) + str(self.units) + ',' + str('{:.3f}'.format(relError)) + '%)', passfail(result)])

            report = displayTable(tableHeaders=tableHeaders, tableData=report, printToConsole=False, indexReq=False, align='r')
            if action == 'calibrate':
                report += '\nCalculated Multiplier: ' + str(self.multiplier.originalValue()) + ', Calculated Offset: ' + str(self.offset.originalValue())
                report += '\nStored Multiplier: ' + str(self.multiplier.storedValue()) + ', Stored Offset: ' + str(self.offset.storedValue())
                report += '\nMultiplier Register: ' + self.multiplier.hexString(4) + ', Offset Register: ' + self.offset.hexString(4)
            return {'result':overallResult,  'worst case':worstCase,  'report':report,  'calObj':self}

    class HD12VOffsetCalibration(HDCalibration):

        def __init__(self, powerModule):
            self.powerModule = powerModule
            self.absErrorLimit = 120
            self.relErrorLimit = 0
            self.test_min = 10800
            self.test_max = 13200
            self.test_steps = 20
            self.units = 'mV'
            self.scaling = 3.538305666
            self.multiplier_signed = False
            self.multiplier_int_width = 16
            self.multiplier_frac_width = 16
            self.offset_signed = False
            self.offset_int_width = 13
            self.offset_frac_width = 0

        def init(self):
            super().init_cal('12v')
            self.powerModule.dut.sendAndVerifyCommand('write ' + HDPowerModule.V12_OUTPUT_OFFSET_ADDR + ' 0x0000')

        def setRef(self, value):
            super().set_12v_volt(value)

        def readRef(self):
            return load_meas_volt(self.powerModule.load) - 11998

        def readVal(self):
            return (int(self.powerModule.dut.sendCommand('read 0x0006'), 16) - 3391) * self.scaling

        def setCoefficients(self):
            result = self.powerModule.dut.sendAndVerifyCommand('write 0xf011 ' + self.offset.hexString(4))
            logSimpleResult('Set 12v output offset', result)

        def finish(self):
            super().finish_cal()

        def report(self, data):
            return super().report('calibrate', data)

        def readCoefficients(self):
            coefficients = {}
            coefficients['offset'] = self.powerModule.dut.sendCommand('read ' + HDPowerModule.V12_OUTPUT_OFFSET_ADDR)
            return coefficients

        def writeCoefficients(self, coefficients):
            self.powerModule.dut.sendAndVerifyCommand('write ' + HDPowerModule.V12_OUTPUT_OFFSET_ADDR + ' ' + coefficients['offset'])

    class HD12VVoltageCalibration(HDCalibration):

        def __init__(self, powerModule):
            self.powerModule = powerModule
            self.absErrorLimit = 1
            self.relErrorLimit = 1
            self.test_min = 40
            self.test_max = 14400
            self.test_steps = 20
            self.units = 'mV'
            self.scaling = 2
            self.multiplier_signed = False
            self.multiplier_int_width = 1
            self.multiplier_frac_width = 16
            self.offset_signed = True
            self.offset_int_width = 10
            self.offset_frac_width = 6

        def init(self):
            super().init_cal('12v')
            self.powerModule.dut.sendCommand('write 0xf000 0xaa55')
            self.powerModule.dut.sendCommand('write 0xf000 0x55aa')
            self.powerModule.dut.sendAndVerifyCommand('write ' + HDPowerModule.V12_VOLT_MULTIPLIER_ADDR + ' 0x0000')
            self.powerModule.dut.sendAndVerifyCommand('write ' + HDPowerModule.V12_VOLT_OFFSET_ADDR + ' 0x0000')
            self.powerModule.dut.sendAndVerifyCommand('sig:12v:volt 0')
            sleep(1)

        def setRef(self, value):
            super().set_12v_volt(value)

        def readRef(self):
            return load_meas_volt(self.powerModule.load)

        def readVal(self):
            return super().meas_12v_volt()

        def setCoefficients(self):
            result1 = self.powerModule.dut.sendAndVerifyCommand('write ' + HDPowerModule.V12_VOLT_MULTIPLIER_ADDR + ' ' + self.multiplier.hexString(4))
            result2 = self.powerModule.dut.sendAndVerifyCommand('write ' + HDPowerModule.V12_VOLT_OFFSET_ADDR + ' ' + self.offset.hexString(4))
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
            coefficients['multiplier'] = self.powerModule.dut.sendCommand('read ' + HDPowerModule.V12_VOLT_MULTIPLIER_ADDR)
            coefficients['offset'] = self.powerModule.dut.sendCommand('read ' + HDPowerModule.V12_VOLT_OFFSET_ADDR)
            return coefficients

        def writeCoefficients(self, coefficients):
            self.powerModule.dut.sendAndVerifyCommand('write ' + HDPowerModule.V12_VOLT_MULTIPLIER_ADDR + ' ' + coefficients['multiplier'])
            self.powerModule.dut.sendAndVerifyCommand('write ' + HDPowerModule.V12_VOLT_OFFSET_ADDR + ' ' + coefficients['offset'])

    class HD12VLowCurrentCalibration(HDCalibration):

        def __init__(self, powerModule):
            self.powerModule = powerModule
            self.absErrorLimit = 2
            self.relErrorLimit = 2
            self.test_min = 10
            self.test_max = 1000
            self.test_steps = 20
            self.units = 'uA'
            self.scaling = 16
            self.multiplier_signed = False
            self.multiplier_int_width = 1
            self.multiplier_frac_width = 16
            self.offset_signed = True
            self.offset_int_width = 10
            self.offset_frac_width = 6

        def init(self):
            super().init_cal('12v')
            self.powerModule.dut.sendAndVerifyCommand('write 0xf001 0x0101')
            self.powerModule.dut.sendAndVerifyCommand('write ' + HDPowerModule.V12_LOW_MULTIPLIER_ADDR + ' 0x0000')
            self.powerModule.dut.sendAndVerifyCommand('write ' + HDPowerModule.V12_LOW_OFFSET_ADDR + ' 0x0000')

        def setRef(self, value):
            load_set_cur(self.powerModule.load, value)

        def readRef(self):
            return load_meas_cur(self.powerModule.load)

        def readVal(self):
            return super().meas_12v_cur()

        def setCoefficients(self):
            result1 = self.powerModule.dut.sendAndVerifyCommand('write ' + HDPowerModule.V12_LOW_MULTIPLIER_ADDR + ' ' + self.multiplier.hexString(4))
            result2 = self.powerModule.dut.sendAndVerifyCommand('write ' + HDPowerModule.V12_LOW_OFFSET_ADDR + ' ' + self.offset.hexString(4))
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
            coefficients['multiplier'] = self.powerModule.dut.sendCommand('read ' + HDPowerModule.V12_LOW_MULTIPLIER_ADDR)
            coefficients['offset'] = self.powerModule.dut.sendCommand('read ' + HDPowerModule.V12_LOW_OFFSET_ADDR)
            return coefficients

        def writeCoefficients(self, coefficients):
            self.powerModule.dut.sendAndVerifyCommand('write ' + HDPowerModule.V12_LOW_MULTIPLIER_ADDR + ' ' + coefficients['multiplier'])
            self.powerModule.dut.sendAndVerifyCommand('write ' + HDPowerModule.V12_LOW_OFFSET_ADDR + ' ' + coefficients['offset'])

    class HD12VHighCurrentCalibration(HDCalibration):

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

        def init(self):
            super().init_cal('12v')
            self.powerModule.dut.sendAndVerifyCommand('write 0xf001 0x0102')
            self.powerModule.dut.sendAndVerifyCommand('write ' + HDPowerModule.V12_HIGH_MULTIPLIER_ADDR + ' 0x0000')
            self.powerModule.dut.sendAndVerifyCommand('write ' + HDPowerModule.V12_HIGH_OFFSET_ADDR + ' 0x0000')

        def setRef(self, value):
            load_set_cur(self.powerModule.load, value)

        def readRef(self):
            return load_meas_cur(self.powerModule.load)

        def readVal(self):
            return super().meas_12v_cur()

        def setCoefficients(self):
            result1 = self.powerModule.dut.sendAndVerifyCommand('write ' + HDPowerModule.V12_HIGH_MULTIPLIER_ADDR + ' ' + self.multiplier.hexString(4))
            result2 = self.powerModule.dut.sendAndVerifyCommand('write ' + HDPowerModule.V12_HIGH_OFFSET_ADDR + ' ' + self.offset.hexString(4))
            if result1 and result2:
                result = True
            else:
                result = False
            logSimpleResult('Set 12v high current', result)

        def finish(self):
            super().finish_cal()

        def report(self, data):
            return super().report('calibrate', data)

        def readCoefficients(self):
            coefficients = {}
            coefficients['multiplier'] = self.powerModule.dut.sendCommand('read ' + HDPowerModule.V12_HIGH_MULTIPLIER_ADDR)
            coefficients['offset'] = self.powerModule.dut.sendCommand('read ' + HDPowerModule.V12_HIGH_OFFSET_ADDR)
            return coefficients

        def writeCoefficients(self, coefficients):
            self.powerModule.dut.sendAndVerifyCommand('write ' + HDPowerModule.V12_HIGH_MULTIPLIER_ADDR + ' ' + coefficients['multiplier'])
            self.powerModule.dut.sendAndVerifyCommand('write ' + HDPowerModule.V12_HIGH_OFFSET_ADDR + ' ' + coefficients['offset'])

    class HD12VLeakageCalibration(HDCalibration):

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

        def init(self):
            super().init_cal('12v')
            self.powerModule.dut.sendAndVerifyCommand('write 0xf001 0x0101')
            self.powerModule.dut.sendAndVerifyCommand('write ' + HDPowerModule.V12_LEAKAGE_MULTIPLIER_ADDR + ' 0x0000')
            self.powerModule.load.setReferenceCurrent(0.005)
            super().set_12v_volt(self.test_min)
            sleep(1)

        def setRef(self, value):
            super().set_12v_volt(value)

        def readRef(self):
            return 5000 - float(returnMeasurement(self.powerModule.dut, 'meas:cur 12v?')[0]) * 1000

        def readVal(self):
            return 3391 - int(self.powerModule.dut.sendCommand('read 0x0006'), 16)

        def setCoefficients(self):
            result = self.powerModule.dut.sendAndVerifyCommand('write ' + HDPowerModule.V12_LEAKAGE_MULTIPLIER_ADDR + ' ' + self.multiplier.hexString(4))
            logSimpleResult('Set 12v leakage to device', result)

        def finish(self):
            super().finish_cal()

        def report(self, data):
            return super().report('calibrate', data)

        def readCoefficients(self):
            coefficients = {}
            coefficients['multiplier'] = self.powerModule.dut.sendCommand('read ' + HDPowerModule.V12_LEAKAGE_MULTIPLIER_ADDR)
            return coefficients

        def writeCoefficients(self, coefficents):
            self.powerModule.dut.sendAndVerifyCommand('write ' + HDPowerModule.V12_LEAKAGE_MULTIPLIER_ADDR + ' ' + coefficents['multiplier'])

    class HD5VOffsetCalibration(HDCalibration):

        def __init__(self, powerModule):
            self.powerModule = powerModule
            self.absErrorLimit = 50
            self.relErrorLimit = 0
            self.test_min = 4500
            self.test_max = 5500
            self.test_steps = 20
            self.units = 'mV'
            self.scaling = 3.538305666
            self.multiplier_signed = False
            self.multiplier_int_width = 16
            self.multiplier_frac_width = 16
            self.offset_signed = True
            self.offset_int_width = 13
            self.offset_frac_width = 0

        def init(self):
            super().init_cal('5v')
            self.powerModule.dut.sendAndVerifyCommand('write ' + HDPowerModule.V5_OUTPUT_OFFSET_ADDR + ' 0x0000')

        def setRef(self, value):
            super().set_5v_volt(value)

        def readRef(self):
            return load_meas_volt(self.powerModule.load) - 5000

        def readVal(self):
            return (int(self.powerModule.dut.sendCommand('read 0x0005'), 16) - 1413) * self.scaling

        def setCoefficients(self):
            result = self.powerModule.dut.sendAndVerifyCommand('write 0xf010 ' + self.offset.hexString(4))
            logSimpleResult('Set 5v output offset', result)

        def finish(self):
            super().finish_cal()

        def report(self, data):
            return super().report('calibrate', data)

        def readCoefficients(self):
            coefficients = {}
            coefficients['offset'] = self.powerModule.dut.sendCommand('read ' + HDPowerModule.V5_OUTPUT_OFFSET_ADDR)
            return coefficients

        def writeCoefficients(self, coefficients):
            self.powerModule.dut.sendAndVerifyCommand('write ' + HDPowerModule.V5_OUTPUT_OFFSET_ADDR + ' ' + coefficients['offset'])

    class HD5VVoltageCalibration(HDCalibration):

        def __init__(self, powerModule):
            self.powerModule = powerModule
            self.absErrorLimit = 1
            self.relErrorLimit = 1
            self.test_min = 40
            self.test_max = 6000
            self.test_steps = 20
            self.units = 'mV'
            self.scaling = 2
            self.multiplier_signed = False
            self.multiplier_int_width = 1
            self.multiplier_frac_width = 16
            self.offset_signed = True
            self.offset_int_width = 10
            self.offset_frac_width = 6

        def init(self):
            super().init_cal('5v')
            self.powerModule.dut.sendAndVerifyCommand('write ' + HDPowerModule.V5_VOLT_MULTIPLIER_ADDR + ' 0x0000')
            self.powerModule.dut.sendAndVerifyCommand('write ' + HDPowerModule.V5_VOLT_OFFSET_ADDR + ' 0x0000')
            self.powerModule.dut.sendAndVerifyCommand('sig:5v:volt 0')
            sleep(1)

        def setRef(self, value):
            super().set_5v_volt(value)

        def readRef(self):
            return load_meas_volt(self.powerModule.load)

        def readVal(self):
            return super().meas_5v_volt()

        def setCoefficients(self):
            result1 = self.powerModule.dut.sendAndVerifyCommand('write ' + HDPowerModule.V5_VOLT_MULTIPLIER_ADDR + ' ' + self.multiplier.hexString(4))
            result2 = self.powerModule.dut.sendAndVerifyCommand('write ' + HDPowerModule.V5_VOLT_OFFSET_ADDR + ' ' + self.offset.hexString(4))
            if result1 and result2:
                result = True
            else:
                result = False
            logSimpleResult('Set 5v voltage', result)

        def finish(self):
            super().finish_cal()

        def report(self, data):
            return super().report('calibrate', data)

        def readCoefficients(self):
            coefficients = {}
            coefficients['multiplier'] = self.powerModule.dut.sendCommand('read ' + HDPowerModule.V5_VOLT_MULTIPLIER_ADDR)
            coefficients['offset'] = self.powerModule.dut.sendCommand('read ' + HDPowerModule.V5_VOLT_OFFSET_ADDR)
            return coefficients

        def writeCoefficients(self, coefficients):
            self.powerModule.dut.sendAndVerifyCommand('write ' + HDPowerModule.V5_VOLT_MULTIPLIER_ADDR + ' ' + coefficients['multiplier'])
            self.powerModule.dut.sendAndVerifyCommand('write ' + HDPowerModule.V5_VOLT_OFFSET_ADDR + ' ' + coefficients['offset'])

    class HD5VLowCurrentCalibration(HDCalibration):

        def __init__(self, powerModule):
            self.powerModule = powerModule
            self.absErrorLimit = 2
            self.relErrorLimit = 2
            self.test_min = 10
            self.test_max = 1000
            self.test_steps = 20
            self.units = 'uA'
            self.scaling = 16
            self.multiplier_signed = False
            self.multiplier_int_width = 1
            self.multiplier_frac_width = 16
            self.offset_signed = True
            self.offset_int_width = 10
            self.offset_frac_width = 6

        def init(self):
            super().init_cal('5v')
            self.powerModule.dut.sendAndVerifyCommand('write 0xf001 0x0101')
            self.powerModule.dut.sendAndVerifyCommand('write ' + HDPowerModule.V5_LOW_MULTIPLIER_ADDR + ' 0x0000')
            self.powerModule.dut.sendAndVerifyCommand('write ' + HDPowerModule.V5_LOW_OFFSET_ADDR + ' 0x0000')

        def setRef(self, value):
            load_set_cur(self.powerModule.load, value)

        def readRef(self):
            return load_meas_cur(self.powerModule.load)

        def readVal(self):
            return super().meas_5v_cur()

        def setCoefficients(self):
            result1 = self.powerModule.dut.sendAndVerifyCommand('write ' + HDPowerModule.V5_LOW_MULTIPLIER_ADDR + ' ' + self.multiplier.hexString(4))
            result2 = self.powerModule.dut.sendAndVerifyCommand('write ' + HDPowerModule.V5_LOW_OFFSET_ADDR + ' ' + self.offset.hexString(4))
            if result1 and result2:
                result = True
            else:
                result = False
            logSimpleResult('Set 5v low current', result)

        def finish(self):
            super().finish_cal()

        def report(self, data):
            return super().report('calibrate', data)

        def readCoefficients(self):
            coefficients = {}
            coefficients['multiplier'] = self.powerModule.dut.sendCommand('read ' + HDPowerModule.V5_LOW_MULTIPLIER_ADDR)
            coefficients['offset'] = self.powerModule.dut.sendCommand('read ' + HDPowerModule.V5_LOW_OFFSET_ADDR)
            return coefficients

        def writeCoefficients(self, coefficients):
            self.powerModule.dut.sendAndVerifyCommand('write ' + HDPowerModule.V5_LOW_MULTIPLIER_ADDR + ' ' + coefficients['multiplier'])
            self.powerModule.dut.sendAndVerifyCommand('write ' + HDPowerModule.V5_LOW_OFFSET_ADDR + ' ' + coefficients['offset'])

    class HD5VHighCurrentCalibration(HDCalibration):

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

        def init(self):
            super().init_cal('5v')
            self.powerModule.dut.sendAndVerifyCommand('write 0xf001 0x0102')
            self.powerModule.dut.sendAndVerifyCommand('write ' + HDPowerModule.V5_HIGH_MULTIPLIER_ADDR + ' 0x0000')
            self.powerModule.dut.sendAndVerifyCommand('write ' + HDPowerModule.V5_HIGH_OFFSET_ADDR + ' 0x0000')

        def setRef(self, value):
            load_set_cur(self.powerModule.load, value)

        def readRef(self):
            return load_meas_cur(self.powerModule.load)

        def readVal(self):
            return super().meas_5v_cur()

        def setCoefficients(self):
            result1 = self.powerModule.dut.sendAndVerifyCommand('write ' + HDPowerModule.V5_HIGH_MULTIPLIER_ADDR + ' ' + self.multiplier.hexString(4))
            result2 = self.powerModule.dut.sendAndVerifyCommand('write ' + HDPowerModule.V5_HIGH_OFFSET_ADDR + ' ' + self.offset.hexString(4))
            if result1 and result2:
                result = True
            else:
                result = False
            logSimpleResult('Set 5v high current', result)

        def finish(self):
            super().finish_cal()

        def report(self, data):
            return super().report('calibrate', data)

        def readCoefficients(self):
            coefficients = {}
            coefficients['multiplier'] = self.powerModule.dut.sendCommand('read ' + HDPowerModule.V5_HIGH_MULTIPLIER_ADDR)
            coefficients['offset'] = self.powerModule.dut.sendCommand('read ' + HDPowerModule.V5_HIGH_OFFSET_ADDR)
            return coefficients

        def writeCoefficients(self, coefficients):
            self.powerModule.dut.sendAndVerifyCommand('write ' + HDPowerModule.V5_HIGH_MULTIPLIER_ADDR + ' ' + coefficients['multiplier'])
            self.powerModule.dut.sendAndVerifyCommand('write ' + HDPowerModule.V5_HIGH_OFFSET_ADDR + ' ' + coefficients['offset'])

    class HD5VLeakageCalibration(HDCalibration):

        def __init__(self, powerModule):
            self.powerModule = powerModule
            self.absErrorLimit = 50
            self.relErrorLimit = 0
            self.test_min = 1000
            self.test_max = 6000
            self.test_steps = 20
            self.units = 'uA'
            self.scaling = 1
            self.multiplier_signed = False
            self.multiplier_int_width = 1
            self.multiplier_frac_width = 16
            self.offset_signed = True
            self.offset_int_width = 16
            self.offset_frac_width = 16

        def init(self):
            super().init_cal('5v')
            self.powerModule.dut.sendAndVerifyCommand('write 0xf001 0x0101')
            self.powerModule.dut.sendAndVerifyCommand('write ' + HDPowerModule.V5_LEAKAGE_MULTIPLIER_ADDR + ' 0x0000')
            self.powerModule.load.setReferenceCurrent(0.005)
            super().set_5v_volt(self.test_min)
            sleep(1)

        def setRef(self, value):
            super().set_5v_volt(value)

        def readRef(self):
            return 5000 - float(returnMeasurement(self.powerModule.dut, 'meas:cur 5v?')[0]) * 1000

        def readVal(self):
            return 3391 - int(self.powerModule.dut.sendCommand('read 0x0005'), 16)

        def setCoefficients(self):
            result = self.powerModule.dut.sendAndVerifyCommand('write ' + HDPowerModule.V5_LEAKAGE_MULTIPLIER_ADDR + ' ' + self.multiplier.hexString(4))
            logSimpleResult('Set 5v leakage', result)

        def finish(self):
            super().finish_cal()

        def report(self, data):
            return super().report('calibrate', data)

        def readCoefficients(self):
            coefficients = {}
            coefficients['multiplier'] = self.powerModule.dut.sendCommand('read ' + HDPowerModule.V5_LEAKAGE_MULTIPLIER_ADDR)
            return coefficients

        def writeCoefficients(self, coefficients):
            self.powerModule.dut.sendAndVerifyCommand('write ' + HDPowerModule.V5_LEAKAGE_MULTIPLIER_ADDR + ' ' + coefficients['multiplier'])

    class HD12VOffsetVerification(HDCalibration):

        def __init__(self, powerModule):
            self.powerModule = powerModule
            self.absErrorLimit = 0
            self.relErrorLimit = 1
            self.test_min = 10800
            self.test_max = 13200
            self.test_steps = 20
            self.units = 'mV'

        def init(self):
            super().init_cal('12V')

        def setRef(self, value):
            super().set_12v_volt(value)

        def readRef(self):
            return super().get_12v_volt()

        def readVal(self):
            return load_meas_volt(self.powerModule.load)

        def finish(self):
            super().finish_cal()

        def report(self, data):
            return super().report('verify', data)

    class HD12VVoltageVerification(HDCalibration):

        def __init__(self, powerModule):
            self.powerModule = powerModule
            self.absErrorLimit = 1
            self.relErrorLimit = 1
            self.test_min = 40
            self.test_max = 14400
            self.test_steps = 20
            self.units = 'mV'

        def init(self):
            super().init_cal('12V')

        def setRef(self, value):
            super().set_12v_volt(value)

        def readRef(self):
            return load_meas_volt(self.powerModule.load)

        def readVal(self):
            return super().meas_12v_volt()

        def finish(self):
            super().finish_cal()

        def report(self, data):
            return super().report('verify', data)

    class HD12VLowCurrentVerification(HDCalibration):

        def __init__(self, powerModule):
            self.powerModule = powerModule
            self.absErrorLimit = 2
            self.relErrorLimit = 2
            self.test_min = 100
            self.test_max = 1000
            self.test_steps = 20
            self.units = 'uA'

        def init(self):
            super().init_cal('12V')

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

    class HD12VHighCurrentVerification(HDCalibration):

        def __init__(self, powerModule):
            self.powerModule = powerModule
            self.absErrorLimit = 2000
            self.relErrorLimit = 1
            self.test_min = 1000
            self.test_max = 4000000
            self.test_steps = 20
            self.units = 'uA'

        def init(self):
            super().init_cal('12v')

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

    class HD12VLeakageVerification(HDCalibration):

        def __init__(self, powerModule):
            self.powerModule = powerModule
            self.absErrorLimit = 0
            self.relErrorLimit = 1
            self.test_min = 1000
            self.test_max = 14400
            self.test_steps = 20
            self.units = 'uA'

        def init(self):
            super().init_cal('12v')
            self.powerModule.load.setReferenceCurrent(0.005)
            super().set_12v_volt(self.test_min)
            sleep(1)

        def setRef(self, value):
            super().set_12v_volt(value)

        def readRef(self):
            return load_meas_cur(self.powerModule.load)

        def readVal(self):
            return super().meas_12v_cur()

        def finish(self):
            super().finish_cal()

        def report(self, data):
            return super().report('verify', data)

    class HD5VOffsetVerification(HDCalibration):

        def __init__(self, powerModule):
            self.powerModule = powerModule
            self.absErrorLimit = 0
            self.relErrorLimit = 1
            self.test_min = 4500
            self.test_max = 5500
            self.test_steps = 20
            self.units = 'mV'

        def init(self):
            super().init_cal('5v')

        def setRef(self, value):
            super().set_5v_volt(value)

        def readRef(self):
            return super().get_5v_volt()

        def readVal(self):
            return load_meas_volt(self.powerModule.load)

        def finish(self):
            super().finish_cal()

        def report(self, data):
            return super().report('verify', data)

    class HD5VVoltageVerification(HDCalibration):

        def __init__(self, powerModule):
            self.powerModule = powerModule
            self.absErrorLimit = 1
            self.relErrorLimit = 1
            self.test_min = 40
            self.test_max = 6000
            self.test_steps = 20
            self.units = 'mV'

        def init(self):
            super().init_cal('5v')

        def setRef(self, value):
            super().set_5v_volt(value)

        def readRef(self):
            return load_meas_volt(self.powerModule.load)

        def readVal(self):
            return super().meas_5v_volt()

        def finish(self):
            super().finish_cal()

        def report(self, data):
            return super().report('verify', data)

    class HD5VLowCurrentVerification(HDCalibration):

        def __init__(self, powerModule):
            self.powerModule = powerModule
            self.absErrorLimit = 2
            self.relErrorLimit = 2
            self.test_min = 100
            self.test_max = 1000
            self.test_steps = 20
            self.units = 'uA'

        def init(self):
            super().init_cal('5v')

        def setRef(self, value):
            load_set_cur(self.powerModule.load, value)

        def readRef(self):
            return load_meas_cur(self.powerModule.load)

        def readVal(self):
            return super().meas_5v_cur()

        def finish(self):
            super().finish_cal()

        def report(self, data):
            return super().report('verify', data)

    class HD5VHighCurrentVerification(HDCalibration):

        def __init__(self, powerModule):
            self.powerModule = powerModule
            self.absErrorLimit = 2000
            self.relErrorLimit = 1
            self.test_min = 1000
            self.test_max = 4000000
            self.test_steps = 20
            self.units = 'uA'

        def init(self):
            super().init_cal('5v')

        def setRef(self, value):
            load_set_cur(self.powerModule.load, value)

        def readRef(self):
            return load_meas_cur(self.powerModule.load)

        def readVal(self):
            return super().meas_5v_cur()

        def finish(self):
            super().finish_cal()

        def report(self, data):
            return super().report('verify', data)

    class HD5VLeakageVerification(HDCalibration):

        def __init__(self, powerModule):
            self.powerModule = powerModule
            self.absErrorLimit = 50
            self.relErrorLimit = 0
            self.test_min = 1000
            self.test_max = 6000
            self.test_steps = 20
            self.units = 'uA'

        def init(self):
            super().init_cal('5v')
            self.powerModule.load.setReferenceCurrent(0.005)
            super().set_5v_volt(self.test_min)
            sleep(1)

        def setRef(self, value):
            super().set_5v_volt(value)

        def readRef(self):
            return load_meas_cur(self.powerModule.load)

        def readVal(self):
            return super().meas_5v_cur()

        def finish(self):
            super().finish_cal()

        def report(self, data):
            return super().report('verify', data)

    def __init__(self, dut):
        self.name = 'HD Programmable Power Module'
        self.dut = dut
        self.calibrations = {}
        self.calibrations['12V'] = {'Output Offset':self.HD12VOffsetCalibration(self), 
         'Voltage':self.HD12VVoltageCalibration(self), 
         'Low Current':self.HD12VLowCurrentCalibration(self), 
         'High Current':self.HD12VHighCurrentCalibration(self), 
         'Leakage':self.HD12VLeakageCalibration(self)}
        self.calibrations['5V'] = {'Output Offset':self.HD5VOffsetCalibration(self), 
         'Voltage':self.HD5VVoltageCalibration(self), 
         'Low Current':self.HD5VLowCurrentCalibration(self), 
         'High Current':self.HD5VHighCurrentCalibration(self), 
         'Leakage':self.HD5VLeakageCalibration(self)}
        self.verifications = {}
        self.verifications['12V'] = {'Output Offset':self.HD12VOffsetVerification(self), 
         'Voltage':self.HD12VVoltageVerification(self), 
         'Low Current':self.HD12VLowCurrentVerification(self), 
         'High Current':self.HD12VHighCurrentVerification(self), 
         'Leakage':self.HD12VLeakageVerification(self)}
        self.verifications['5V'] = {'Output Offset':self.HD5VOffsetVerification(self), 
         'Voltage':self.HD5VVoltageVerification(self), 
         'Low Current':self.HD5VLowCurrentVerification(self), 
         'High Current':self.HD5VHighCurrentVerification(self), 
         'Leakage':self.HD5VLeakageVerification(self)}


if __name__ == '__main__':
    main()