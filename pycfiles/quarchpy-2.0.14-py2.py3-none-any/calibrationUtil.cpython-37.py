# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\sboon\AppData\Local\Temp\pip-install-ptdbtr91\quarchpy\quarchpy\calibration\calibrationUtil.py
# Compiled at: 2020-03-25 05:10:07
# Size of source mod 2**32: 14231 bytes
"""
This example runs the calibration process for a HD PPM
It products a calibrated PPM and a calibration file for later use

########### VERSION HISTORY ###########

05/04/2019 - Andy Norrie     - First Version

########### INSTRUCTIONS ###########

1- Connect the PPM on LAN and power up
2- Connect the Keithley 2460 until on LAN, power up and check its IP address
3- Connect the calibration switch unit to the output ports of the PPM and Keithley

####################################
"""
from time import sleep, time
import datetime, logging, os, sys
from quarchpy.device import *
from quarchpy.calibration.keithley_2460_control import *
from quarchpy.calibration.calibration_classes import *
from quarchpy.calibration.HDPowerModule import *
from quarchpy.calibration.QTL2347 import *
from quarchpy.calibration.calibrationConfig import *
from quarchpy.user_interface import *

def runCalibration(instrAddress=None, calPath=None, ppmAddress=None, logLevel='warning', calAction=None, userMode='testcenter', extra_args=None):
    try:
        printText('********************************************************')
        printText('          Quarch Technology Calibration System')
        printText('             (C) 2019, All rights reserved')
        printText('                          V' + quarchpy.calibration.calCodeVersion)
        printText('********************************************************')
        printText('')
        calPath = get_check_valid_calPath(calPath)
        setup_logging(logLevel)
        calHeader = CalibrationHeaderInformation()
        calibrationResources['CalHeader'] = calHeader
        calibrationResources['user_mode'] = userMode
        while 1:
            if calAction != None and 'select' in calAction or ppmAddress == None:
                calAction, ppmAddress = select_module(calAction, ppmAddress)
            while True:
                try:
                    printText('Selected Module: ' + ppmAddress)
                    myPpmDevice = quarchDevice(ppmAddress)
                    break
                except:
                    printText('Failed to connect to ' + str(ppmAddress))
                    calAction, ppmAddress = select_module(calAction, ppmAddress)

            serialNumber = myPpmDevice.sendCommand('*SERIAL?')
            success = False
            if '1944' in serialNumber:
                dut = HDPowerModule(myPpmDevice)
                success = True
            else:
                if '2312' in serialNumber:
                    fixtureId = myPpmDevice.sendCommand('read 0xA401')
                    if '2347' in fixtureId:
                        dut = QTL2347(myPpmDevice)
                        success = True
                else:
                    if success == False:
                        raise ValueError('ERROR - Serial number not recogised as a valid power module')
                    populateCalHeader_HdPpm(calHeader, dut.dut, calAction)
                    populateCalHeader_System(calHeader)
                    storeDeviceInfo(serial=(calHeader.quarchEnclosureSerial), idn=(calHeader.idnStr))
                    if 'QTL1995' in calHeader.quarchEnclosureSerial.upper():
                        calFilename = calHeader.quarchEnclosureSerial + '-' + calHeader.quarchEnclosurePosition
                    else:
                        calFilename = calHeader.quarchEnclosureSerial
                calHeader.result = True
                if calAction == None:
                    calAction = show_action_menu(calAction)
                if calAction == 'quit':
                    if userMode == 'testcenter':
                        return calHeader
                        sys.exit(0)
                    else:
                        pass
            if not 'calibrate' in calAction:
                if 'verify' in calAction:
                    while True:
                        if instrAddress == None:
                            instrAddress = userSelectCalInstrument(scanFilterStr='Keithley 2460', nice=True)
                        try:
                            myCalInstrument = keithley2460(instrAddress)
                            myCalInstrument.openConnection()
                            populateCalHeader_Keithley(calHeader, myCalInstrument)
                            break
                        except:
                            printText('Unable to communicate with selected instrument!')
                            printText('')
                            instrAddress = None

                    calHeader, myCalInstrument, report = cal_or_ver(calAction, calFilename, calHeader, calPath, dut, myCalInstrument)
                myPpmDevice.closeConnection()
                if 'calibrate' in calAction:
                    if report:
                        calAction = 'verify'
                    else:
                        printText('Not verifying this module because calibration failed')
                        calAction = 'quit'
                elif userMode == 'testcenter':
                    calAction = 'quit'
                else:
                    if 'select' in calAction:
                        continue
                    calAction = None

    except Exception as thisException:
        try:
            try:
                myCalInstrument.setLoadCurrent(0)
                myCalInstrument.closeConnection()
            except:
                pass

            logging.error(thisException)
            raise thisException
        finally:
            thisException = None
            del thisException


def select_module(calAction, ppmAddress):
    ppmAddress = userSelectDevice(scanFilterStr=['QTL1999', 'QTL1995', 'QTL1944', 'QTL2312'], nice=True, message='Select device for calibration')
    if ppmAddress.lower() == 'quit':
        printText('User Quit Program')
        sys.exit(0)
    if calAction != None:
        if 'select' in calAction:
            calAction = None
    return (
     calAction, ppmAddress)


def setup_logging(logLevel):
    numeric_level = getattr(logging, logLevel.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % loglevel)
    logging.basicConfig(level=numeric_level)


def get_check_valid_calPath(calPath):
    inputOK = False
    while inputOK is False:
        if calPath is None:
            calPath = os.path.expanduser('~')
            calPath = requestDialog('Enter Report Path', ('Enter the desired save path for the calibration report. Leave blank to defaut to [' + calPath + '] :'),
              desiredType='path',
              defaultUserInput=(os.path.expanduser('~')))
        if os.path.isdir(calPath) == False:
            printText('Supplied calibration path is invalid: ' + calPath)
            inputOK = False
            calPath = None
        else:
            inputOK = True

    return calPath


def cal_or_ver(calAction, calFilename, calHeader, calPath, dut, myCalInstrument):
    calHeader.calibrationType = calAction
    dut.specific_requirements()
    fileName = calPath + '\\' + calFilename + '_' + datetime.datetime.now().strftime('%d-%m-%y_%H-%M-' + calAction + '.txt')
    printText('')
    printText('Report file: ' + fileName)
    reportFile = open(fileName, 'a+')
    reportFile.write(calHeader.toReportText())
    if getCalibrationResource('runtimecheckskipped') is True:
        tempString = 'Module temperature not guaranteed to be stable.'
    else:
        if getCalibrationResource('runtimecheckskipped') is False:
            tempString = 'Module temperature is stable.'
    reportFile.write(tempString)
    if 'calibrate' in calAction:
        retTupple = dut.calibrate(myCalInstrument, reportFile, calHeader)
        title = 'Calibration '
    else:
        if 'verify' in calAction:
            retTupple = dut.verify(myCalInstrument, reportFile, calHeader)
            title = 'Verification '
        else:
            report = retTupple[0]
            calHeader = retTupple[1]
            formatFinalReport(reportFile)
            if report is True:
                result = 'Passed'
            else:
                result = 'Failed'
            calHeader.result = False
        printText('\n====================\n' + title + result + '\n====================')
        printText('More information at : ' + fileName + '\n\n')
        reportFile.write('\n====================\n' + title + result + '\n====================')
        myCalInstrument.closeConnection()
        reportFile.close()
        return (calHeader, myCalInstrument, report)


def show_action_menu(calAction):
    actionList = []
    actionList.append(['Calibrate', 'Calibrate the power module'])
    actionList.append(['Verify', 'Verify existing calibration on the power module'])
    actionList.append(['Select', 'Select a different power module'])
    actionList.append(['Quit', 'Quit'])
    calAction = listSelection('Select an action', 'Please select an action to perform', actionList, nice=True, tableHeaders=['Option', 'Description'], indexReq=True)
    return calAction[1].lower()


def getCalibrationResource(resourceName):
    try:
        return calibrationResources[resourceName]
    except Exception as e:
        try:
            printText('Failed to get calibration resource : ' + str(resourceName))
            printText('Exception : ' + str(e))
            return
        finally:
            e = None
            del e


def formatFinalReport(reportFile):
    with open(reportFile.name, 'r+') as (f):
        lines = f.readlines()
        f.seek(0)
        overview = []
        for line in lines:
            if not line.__contains__('worst case:'):
                f.write(line)
            else:
                overview.append(line)

        for i in overview:
            f.write(i)


def getFailuresFromReport(reportFile):
    with open(reportFile.name, 'r+') as (f):
        lines = f.readlines()
        f.seek(0)
        listOfFailures = []
        for line in lines:
            if line.__contains__('worst case:') and line.__contains__('False'):
                listOfFailures.append(line)

    listOfFailures = ''.join(listOfFailures)
    return listOfFailures


def main(argstring):
    import argparse
    parser = argparse.ArgumentParser(description='Calibration utility parameters')
    parser.add_argument('-a', '--action', help='Calibration action to perform', choices=['calibrate', 'verify'], type=(str.lower))
    parser.add_argument('-m', '--module', help='IP Address or netBIOS name of power module to calibrate', type=(str.lower))
    parser.add_argument('-i', '--instr', help='IP Address or netBIOS name of calibration instrument', type=(str.lower))
    parser.add_argument('-p', '--path', help='Path to store calibration logs', type=(str.lower))
    parser.add_argument('-l', '--logging', help=(argparse.SUPPRESS), choices=['warning', 'error', 'debug'], type=(str.lower), default='warning')
    parser.add_argument('-u', '--userMode', help=(argparse.SUPPRESS), choices=['console', 'testcenter'], type=(str.lower), default='console')
    args, extra_args = parser.parse_known_args(argstring)
    thisInterface = User_interface(args.userMode)
    runCalibration(instrAddress=(args.instr), calPath=(args.path), ppmAddress=(args.module), logLevel=(args.logging), calAction=(args.action), userMode=(args.userMode), extra_args=extra_args)


if __name__ == '__main__':
    main(sys.argv[1:])