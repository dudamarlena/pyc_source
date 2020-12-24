# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\sboon\AppData\Local\Temp\pip-install-ptdbtr91\quarchpy\quarchpy\disk_test\hotPlugTest.py
# Compiled at: 2020-03-25 05:10:07
# Size of source mod 2**32: 26564 bytes
import datetime, time, os, sys, logging
import quarchpy.disk_test.dtsGlobals as dtsGlobals
from quarchpy.disk_test import driveTestConfig
from quarchpy.disk_test.driveTestCore import sendLogMessage, executeAndCheckCommand
from quarchpy.user_interface import *

def visualSleep(delayTime):
    if 'UTILS_VISUALSLEEP' in driveTestConfig.testCallbacks:
        driveTestConfig.testCallbacks['UTILS_VISUALSLEEP'](delayTime)
    else:
        time.sleep(delayTime)


def stringTimeToInt(timeStr, outputUnit):
    multToNano = 0
    nanoTime = 0
    timeStr = timeStr.upper()
    if 'MS' in timeStr:
        multToNano = 1000000
        timeStr = timeStr[:-2]
        nanoTime = int(timeStr) * multToNano
    else:
        if 'US' in timeStr:
            multToNano = 1000
            timeStr = timeStr[:-2]
            nanoTime = int(timeStr) * multToNano
        else:
            if 'NS' in timeStr:
                multToNano = 1
                timeStr = timeStr[:-2]
                nanoTime = int(timeStr) * multToNano
            else:
                if 'S' in timeStr:
                    multToNano = 1000000000
                    timeStr = timeStr[:-1]
                    nanoTime = int(timeStr) * multToNano
                else:
                    raise ValueError('Invalid input time unit specified')
    outputUnit = outputUnit.upper()
    if outputUnit == 'MS':
        return nanoTime / 1000000
    if outputUnit == 'US':
        return nanoTime / 1000
    if outputUnit == 'NS':
        return nanoTime
    if outputUnit == 'S':
        return nanoTime / 1000000000
    raise ValueError('Invalid output time unit specified')
    return nanoTime


def setupSimpleHotplug(myDevice, delayTime, stepCount):
    commandSuccess = True
    delayTime = int(delayTime)
    stepCount = int(stepCount)
    if int(delayTime) < 0:
        raise ValueError('delaytime must be positive')
    if stepCount < 2 or stepCount > 6:
        raise ValueError('stepCount must be between 1 and 6')
    for steps in range(1, 6):
        if steps <= stepCount:
            nextDelay = (steps - 1) * delayTime
        if executeAndCheckCommand(myDevice, 'source:' + str(steps) + ':delay ' + str(nextDelay)) == False:
            commandSuccess = False

    return commandSuccess


def setupSourceBounce(myDevice, sourceNumber, bouncePattern):
    commandSuccess = True
    bounceParams = bouncePattern.split('|')
    if bounceParams[0] == 'Simple':
        if executeAndCheckCommand(myDevice, 'source:' + str(sourceNumber) + ':delay ' + bounceParams[1]) == False:
            commandSuccess = False
        if executeAndCheckCommand(myDevice, 'source:' + str(sourceNumber) + ':bounce:length ' + bounceParams[2]) == False:
            commandSuccess = False
        if executeAndCheckCommand(myDevice, 'source:' + str(sourceNumber) + ':bounce:period ' + bounceParams[3]) == False:
            commandSuccess = False
        if executeAndCheckCommand(myDevice, 'source:' + str(sourceNumber) + ':bounce:duty ' + bounceParams[4].strip('%')) == False:
            commandSuccess = False
    else:
        raise ValueError('Requested bounce type not recognised')
    return commandSuccess


def setupSignalsToSource(myDevice, signalList, sourceNumber):
    commandSuccess = True
    for nextSignal in signalList:
        if executeAndCheckCommand(myDevice, 'signal:' + nextSignal + ':source ' + str(sourceNumber)) == False:
            commandSuccess = False

    return commandSuccess


def clearSourceBounce(myDevice, sourceNumber):
    commandSuccess = True
    if executeAndCheckCommand(myDevice, 'source:' + str(sourceNumber) + ':bounce:clear') == False:
        commandSuccess = False
    return commandSuccess


def unhIolHotPlugSimpleSweep(quarchName, driveName, startTime, endTime, stepCount, repeats=1, onTime=10, offTime=5):
    errorCounter = 0
    errorSubCounter = 0
    counter = 0
    if 'TEST_GETDISKSTATUS' not in driveTestConfig.testCallbacks:
        raise ValueError('You have not implemented the required TEST_GETDISKSTATUS callback!')
    else:
        if 'TEST_GETRESOURCE' not in driveTestConfig.testCallbacks:
            raise ValueError('You have not implemented the required TEST_GETRESOURCE callback!')
        sendLogMessage(time.time(), 'testDescription', 'Starting Hotplug sweep test: ' + startTime + '-' + endTime + ' on device: ' + driveName, os.path.basename(__file__) + ' - ' + sys._getframe().f_code.co_name)
        quarchDevice = driveTestConfig.testCallbacks['TEST_GETRESOURCE'](quarchName)
        driveObject = driveTestConfig.testCallbacks['TEST_GETRESOURCE'](driveName)
        startMilli = stringTimeToInt(startTime, 'mS')
        endMilli = stringTimeToInt(endTime, 'mS')
        sweepStep = (endMilli - startMilli) / int(stepCount)
        if endMilli < startMilli:
            raise ValueError('Start time must be less than or equal to the end time for the sweep')
        if endMilli > 1270:
            raise ValueError('End time is out of range (1270mS limit)')
        if stepCount <= 0:
            raise ValueError('Step time must be a positive integer')
        testTimes = list()
        for s in range(0, int(stepCount) - 1):
            testTimes.append(startMilli + s * sweepStep)

        testTimes.append(endMilli)
        executeAndCheckCommand(quarchDevice, 'conf:def:state')
        visualSleep(onTime)
        for nextTime in testTimes:
            errorSubCounter = 0
            sendLogMessage(time.time(), 'testDescription', 'Starting Hotplug sweep sub-point: ' + str(nextTime) + 'mS on device: ' + driveName, os.path.basename(__file__) + ' - ' + sys._getframe().f_code.co_name)
            setupSimpleHotplug(quarchDevice, nextTime, 6)
            if driveTestConfig.testCallbacks['TEST_GETDISKSTATUS'](driveObject, 1):
                sendLogMessage(time.time(), 'testResult', 'HOT_PLUG: Drive detected as expected after ' + str(onTime) + 'seconds', os.path.basename(__file__) + ' - ' + sys._getframe().f_code.co_name, {'testResult': True})
            else:
                sendLogMessage(time.time(), 'testResult', 'HOT_PLUG: Drive NOT detected as expected after ' + str(onTime) + 'seconds', os.path.basename(__file__) + ' - ' + sys._getframe().f_code.co_name, {'testResult': False})
                errorSubCounter += 1
            for loop in range(0, repeats):
                executeAndCheckCommand(quarchDevice, 'run:power down')
                visualSleep(offTime)
                if driveTestConfig.testCallbacks['TEST_GETDISKSTATUS'](driveObject, 0):
                    sendLogMessage(time.time(), 'testResult', 'HOT_PLUG: Drive removed within ' + str(offTime) + 'seconds, as expected', os.path.basename(__file__) + ' - ' + sys._getframe().f_code.co_name, {'testResult': True})
                else:
                    sendLogMessage(time.time(), 'testResult', 'HOT_PLUG: Drive NOT removed after ' + str(offTime) + 'seconds', os.path.basename(__file__) + ' - ' + sys._getframe().f_code.co_name, {'testResult': False})
                    errorSubCounter += 1
                executeAndCheckCommand(quarchDevice, 'run:power up')
                visualSleep(onTime)
                if driveTestConfig.testCallbacks['TEST_GETDISKSTATUS'](driveObject, 1):
                    sendLogMessage(time.time(), 'testResult', 'HOT_PLUG: Drive detected as expected after ' + str(onTime) + 'seconds', os.path.basename(__file__) + ' - ' + sys._getframe().f_code.co_name, {'testResult': True})
                else:
                    sendLogMessage(time.time(), 'testResult', 'HOT_PLUG: Drive NOT detected after ' + str(onTime) + 'seconds', os.path.basename(__file__) + ' - ' + sys._getframe().f_code.co_name, {'testResult': False})
                    errorSubCounter += 1

            errorCounter += errorSubCounter
            if errorSubCounter == 0:
                sendLogMessage(time.time(), 'testResult', 'Hotplug sweep test passed all repetitions at: ' + str(nextTime), os.path.basename(__file__) + ' - ' + sys._getframe().f_code.co_name, {'testResult': True})
            else:
                sendLogMessage(time.time(), 'testResult', 'Hotplug sweep test failed: ' + str(errorSubCounter) + ' repetitions at: ' + str(nextTime), os.path.basename(__file__) + ' - ' + sys._getframe().f_code.co_name, {'testResult': False})

        if errorCounter == 0:
            sendLogMessage(time.time(), 'testResult', 'Hotplug sweep test passed all tests', os.path.basename(__file__) + ' - ' + sys._getframe().f_code.co_name, {'testResult': True})
        else:
            sendLogMessage(time.time(), 'testResult', 'Hotplug sweep test failed: ' + str(errorCounter) + ' repetitions in total', os.path.basename(__file__) + ' - ' + sys._getframe().f_code.co_name, {'testResult': False})


def simpleHotPlugTest(uniqueID, quarchName, driveName, insertTime, repeats=1, onTime=10, offTime=5):
    startTestTime = time.time()
    errorSubCounter = 0
    logging.info('\nStarting test point ' + str(uniqueID))
    startUID = uniqueID
    if 'TEST_GETDISKSTATUS' not in driveTestConfig.testCallbacks:
        raise ValueError('You have not implemented the required TEST_GETDISKSTATUS callback!')
    else:
        if 'TEST_GETRESOURCE' not in driveTestConfig.testCallbacks:
            raise ValueError('You have not implemented the required TEST_GETRESOURCE callback!')
        sendLogMessage((time.time()), 'testDescription', ('Starting Hotplug test at: ' + str(insertTime) + 'mS on device: ' + driveName + ', over ' + str(repeats) + ' repetitions'), (os.path.basename(__file__) + ' - ' + sys._getframe().f_code.co_name), uId=uniqueID)
        quarchDevice = driveTestConfig.testCallbacks['TEST_GETRESOURCE'](quarchName)
        if quarchDevice is None:
            raise ValueError('Selected test resource: [' + quarchName + '] not found')
        driveObject = driveTestConfig.testCallbacks['TEST_GETRESOURCE'](driveName)
        if driveObject is None:
            raise ValueError('Selected test resource: [' + driveName + '] not found')
        sendLogMessage((time.time()), 'testDescription', 'Setting up module for hotplug test', (os.path.basename(__file__) + ' - ' + sys._getframe().f_code.co_name), uId=(uniqueID + '.0'))
        executeAndCheckCommand(quarchDevice, 'conf:def:state')
        setupSimpleHotplug(quarchDevice, insertTime, 6)
        visualSleep(onTime)
        for loop in range(0, int(repeats)):
            logging.info('Hotplug Cycle ' + str(int(loop + 1)))
            if dtsGlobals.continueTest is False:
                printText('Test Aborted, waiting on next test start..')
                return
                uniqueID = startUID + '.' + str(int(loop + 1))
                sendLogMessage((time.time()), 'testDescription', ('Hotplug Cycle ' + str(int(loop + 1))), (os.path.basename(__file__) + ' - ' + sys._getframe().f_code.co_name), uId=uniqueID)
                counter = 0
                executeAndCheckCommand(quarchDevice, 'run:power down')
                driveTestConfig.testCallbacks['TEST_NEWSLEEP'](driveObject, 0, offTime)
                counter = counter + 1
                if driveTestConfig.testCallbacks['TEST_GETDISKSTATUS'](uniqueID, driveObject, 0):
                    sendLogMessage((time.time()), 'testResult', ('HOT_PLUG: Drive removed within ' + str(offTime) + 'seconds, as expected'), (os.path.basename(__file__) + ' - ' + sys._getframe().f_code.co_name), {'testResult': True}, uId=(uniqueID + '.' + str(counter)))
                else:
                    sendLogMessage((time.time()), 'testResult', ('HOT_PLUG: Drive NOT removed as expected after ' + str(offTime) + 'seconds'), (os.path.basename(__file__) + ' - ' + sys._getframe().f_code.co_name), {'testResult': False}, uId=(uniqueID + '.' + str(counter)))
                    errorSubCounter += 1
                executeAndCheckCommand(quarchDevice, 'run:power up')
                driveTestConfig.testCallbacks['TEST_NEWSLEEP'](driveObject, 1, onTime)
                counter = counter + 1
                if driveTestConfig.testCallbacks['TEST_GETDISKSTATUS'](uniqueID, driveObject, 1):
                    sendLogMessage((time.time()), 'testResult', ('HOT_PLUG: Drive detected as expected after ' + str(onTime) + 'seconds'), (os.path.basename(__file__) + ' - ' + sys._getframe().f_code.co_name), {'testResult': True}, uId=(uniqueID + '.' + str(counter)))
            else:
                sendLogMessage((time.time()), 'testResult', ('HOT_PLUG: Drive NOT detected after ' + str(onTime) + 'seconds'), (os.path.basename(__file__) + ' - ' + sys._getframe().f_code.co_name), {'testResult': False}, uId=(uniqueID + '.' + str(counter)))
                errorSubCounter += 1

        uniqueID = startUID + '.' + str(int(repeats) + 1)
        sendLogMessage((time.time()), 'testDescription', 'Results of hotplug test', (os.path.basename(__file__) + ' - ' + sys._getframe().f_code.co_name), uId=uniqueID)
        if errorSubCounter == 0:
            sendLogMessage((time.time()), 'testResult', 'Hotplug test passed all repetitions', (os.path.basename(__file__) + ' - ' + sys._getframe().f_code.co_name), {'testResult': True}, uId=(uniqueID + '.1'))
        else:
            sendLogMessage((time.time()), 'testResult', ('Hotplug sweep test failed: ' + str(errorSubCounter) + ' sub-test points'), (os.path.basename(__file__) + ' - ' + sys._getframe().f_code.co_name), {'testResult': False}, uId=(uniqueID + '.1'))
    elapsedTime = time.time() - startTestTime
    summaryString = 'Total TestTime Elapsed: ' + str(int(elapsedTime)) + 's, Error count = ' + str(errorSubCounter)
    sendLogMessage((time.time()), 'testSummary', summaryString, (os.path.basename(__file__) + ' - ' + sys._getframe().f_code.co_name), uId=(uniqueID + '.2'))
    logging.info('Test point end')


def simpleHotPlugBounceTest(uniqueID, quarchName, driveName, insertTime, bouncePattern, bounceSignals, repeats=1, onTime=15, offTime=10, bounceOnPlug=True, bounceOnPull=False):
    startTestTime = time.time()
    startUID = uniqueID
    errorSubCounter = 0
    signalList = bounceSignals.split('|')
    bounceParams = bouncePattern.split('|')
    logging.info('\nStarting test point ' + str(uniqueID))
    if 'TEST_GETDISKSTATUS' not in driveTestConfig.testCallbacks:
        raise ValueError('You have not implemented the required TEST_GETDISKSTATUS callback!')
    else:
        if 'TEST_GETRESOURCE' not in driveTestConfig.testCallbacks:
            raise ValueError('You have not implemented the required TEST_GETRESOURCE callback!')
        else:
            sendLogMessage((time.time()), 'testDescription', ('Starting ' + str(insertTime) + ' mS staged Hotplug with ' + str(bounceParams[1]) + ' bounce on source: 4, over ' + str(repeats) + ' repetitions'), (os.path.basename(__file__) + ' - ' + sys._getframe().f_code.co_name), uId=uniqueID)
            quarchDevice = driveTestConfig.testCallbacks['TEST_GETRESOURCE'](quarchName)
            driveObject = driveTestConfig.testCallbacks['TEST_GETRESOURCE'](driveName)
            sendLogMessage((time.time()), 'testDescription', 'Setting up module for Bounce test', (os.path.basename(__file__) + ' - ' + sys._getframe().f_code.co_name), uId=(uniqueID + '.0'))
            executeAndCheckCommand(quarchDevice, 'conf:def:state')
            setupSimpleHotplug(quarchDevice, insertTime, 6)
            setupSignalsToSource(quarchDevice, signalList, 4)
            if bounceOnPull:
                setupSourceBounce(quarchDevice, 4, bouncePattern)
            else:
                clearSourceBounce(quarchDevice, 4)
        visualSleep(onTime)
        for loop in range(0, int(repeats)):
            if dtsGlobals.continueTest is False:
                printText('Test Aborted, waiting on next test start..')
                return
                uniqueID = startUID + '.' + str(int(loop + 1))
                sendLogMessage((time.time()), 'testDescription', ('Bounce test Cycle ' + str(int(loop + 1))), (os.path.basename(__file__) + ' - ' + sys._getframe().f_code.co_name),
                  uId=uniqueID)
                if bounceOnPull:
                    setupSourceBounce(quarchDevice, 4, bouncePattern)
                else:
                    clearSourceBounce(quarchDevice, 4)
                counter = 0
                executeAndCheckCommand(quarchDevice, 'run:power down')
                driveTestConfig.testCallbacks['TEST_NEWSLEEP'](driveObject, 0, offTime)
                counter = counter + 1
                if driveTestConfig.testCallbacks['TEST_GETDISKSTATUS'](uniqueID, driveObject, 0):
                    sendLogMessage((time.time()), 'testResult', ('HOT_PLUG: Drive removed within ' + str(offTime) + 'seconds, as expected'), (os.path.basename(__file__) + ' - ' + sys._getframe().f_code.co_name), {'testResult': True}, uId=(uniqueID + '.' + str(counter)))
                else:
                    sendLogMessage((time.time()), 'testResult', ('HOT_PLUG: Drive NOT removed as expected after ' + str(offTime) + 'seconds'), (os.path.basename(__file__) + ' - ' + sys._getframe().f_code.co_name), {'testResult': False}, uId=(uniqueID + '.' + str(counter)))
                    errorSubCounter += 1
                if bounceOnPlug:
                    setupSourceBounce(quarchDevice, 4, bouncePattern)
                else:
                    clearSourceBounce(quarchDevice, 4)
                executeAndCheckCommand(quarchDevice, 'run:power up')
                driveTestConfig.testCallbacks['TEST_NEWSLEEP'](driveObject, 1, onTime)
                counter = counter + 1
                if driveTestConfig.testCallbacks['TEST_GETDISKSTATUS'](uniqueID, driveObject, 1):
                    sendLogMessage((time.time()), 'testResult', ('HOT_PLUG: Drive detected as expected after ' + str(onTime) + 'seconds'), (os.path.basename(__file__) + ' - ' + sys._getframe().f_code.co_name), {'testResult': True}, uId=(uniqueID + '.' + str(counter)))
            else:
                sendLogMessage((time.time()), 'testResult', ('HOT_PLUG: Drive NOT detected after ' + str(onTime) + 'seconds'), (os.path.basename(__file__) + ' - ' + sys._getframe().f_code.co_name), {'testResult': False}, uId=(uniqueID + '.' + str(counter)))
                errorSubCounter += 1

        uniqueID = startUID + '.' + str(int(repeats) + 1)
        sendLogMessage((time.time()), 'testDescription', 'Results of hotplug test', (os.path.basename(__file__) + ' - ' + sys._getframe().f_code.co_name),
          uId=uniqueID)
        if errorSubCounter == 0:
            sendLogMessage((time.time()), 'testResult', 'Bounce test passed all repetitions', (os.path.basename(__file__) + ' - ' + sys._getframe().f_code.co_name), {'testResult': True}, uId=(uniqueID + '.1'))
        else:
            sendLogMessage((time.time()), 'testResult', ('Bounce sweep test failed: ' + str(errorSubCounter) + ' sub-test points'), (os.path.basename(__file__) + ' - ' + sys._getframe().f_code.co_name), {'testResult': False}, uId=(uniqueID + '.1'))
    elapsedTime = time.time() - startTestTime
    summaryString = 'TestTime Elapsed: ' + str(int(elapsedTime)) + ', Error count = ' + str(errorSubCounter)
    counter = counter + 1
    sendLogMessage((time.time()), 'testSummary', summaryString, (os.path.basename(__file__) + ' - ' + sys._getframe().f_code.co_name), uId=(uniqueID + '.' + str(counter)))
    logging.info('Test point end')