# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\sboon\AppData\Local\Temp\pip-install-ptdbtr91\quarchpy\quarchpy\disk_test\powerTest.py
# Compiled at: 2020-03-25 05:10:07
# Size of source mod 2**32: 8901 bytes
import os, sys, time, logging
from quarchpy.user_interface import *
from connection_specific.connection_QPS import QpsInterface
import quarchpy.disk_test.dtsGlobals as dtsGlobals
from quarchpy.disk_test import driveTestConfig
from quarchpy.disk_test.driveTestCore import sendLogMessage, executeAndCheckCommand
from quarchpy.device.quarchQPS import quarchStream

def SetupStreamAveraging(quarchDevice, averagingRate):
    quarchDevice.sendCommand('record:averaging ' + str(averagingRate))


def simplePowerMarginingTest(uniqueID, quarchName, driveName, maxDecreasePercent, numberOfIncrements, repeats=1, onTime=15, offTime=10, averagingRate='16k'):
    startTestTime = time.time()
    errorSubCounter = 0
    customSleepEnd = 5
    maxDecreasePercent = float(maxDecreasePercent) / 100
    logging.info('\nStarting test point ' + str(uniqueID))
    counter = 0
    startUID = uniqueID
    repeating = int(repeats) > 1
    if 'TEST_GETDISKSTATUS' not in driveTestConfig.testCallbacks:
        raise ValueError('You have not implemented the required TEST_GETDISKSTATUS callback!')
    else:
        if 'TEST_GETRESOURCE' not in driveTestConfig.testCallbacks:
            raise ValueError('You have not implemented the required TEST_GETRESOURCE callback!')
        sendLogMessage((time.time()), 'testDescription', ('Starting Power Margining test, over ' + str(repeats) + ' repetitions'),
          (os.path.basename(__file__) + ' - ' + sys._getframe().f_code.co_name), uId=uniqueID)
        quarchDevice = driveTestConfig.testCallbacks['TEST_GETRESOURCE'](quarchName)
        if quarchDevice is None:
            raise ValueError('Selected test resource: [' + quarchName + '] not found')
        driveObject = driveTestConfig.testCallbacks['TEST_GETRESOURCE'](driveName)
        if driveObject is None:
            raise ValueError('Selected test resource: [' + driveName + '] not found')
        SetupStreamAveraging(quarchDevice, averagingRate)
        filePath = os.path.dirname(os.path.realpath(__file__))
        fileName = time.strftime('%Y-%m-%d-%H-%M-%S', time.gmtime())
        time.sleep(3)
        myStream = quarchDevice.startStream(filePath + fileName)
        powerSetting = 12000
        currentPower = powerSetting
        minimumPower = int(powerSetting) - int(powerSetting) * int(maxDecreasePercent)
        powerDecrement = float(powerSetting) * float(maxDecreasePercent) / float(numberOfIncrements)
        logging.info(powerDecrement)
        for loop in range(0, int(numberOfIncrements) + 1):
            counter = 0
            if dtsGlobals.continueTest is False:
                printText('Test Aborted, waiting on next test start..')
                myStream.addAnnotation('TEST ABORTED')
                return
            currentPower = int(currentPower) - int(powerDecrement)
            logging.info('current power = ' + str(currentPower))
            if loop == 0:
                currentPower = powerSetting
            uniqueID = startUID + '.' + str(int(loop + 1))
            sendLogMessage((time.time()), 'testDescription', ('Power Margining cycle ' + str(int(loop + 1)) + '; ' + str(currentPower) + 'mV'),
              (os.path.basename(__file__) + ' - ' + sys._getframe().f_code.co_name),
              uId=uniqueID)
            executeAndCheckCommand(quarchDevice, 'run:power down')
            time.sleep(0.1)
            myStream.addAnnotation('Starting Power Margining cycle ' + str(int(loop + 1)) + '\\n' + str(currentPower) + 'mV')
            driveTestConfig.testCallbacks['TEST_NEWSLEEP'](driveObject, 0, offTime)
            counter = counter + 1
            if driveTestConfig.testCallbacks['TEST_GETDISKSTATUS'](uniqueID, driveObject, 0):
                sendLogMessage((time.time()), 'testResult', ('HOT_PLUG: Drive removed within ' + str(offTime) + 'seconds, as expected'),
                  (os.path.basename(__file__) + ' - ' + sys._getframe().f_code.co_name),
                  {'testResult': True}, uId=(uniqueID + '.' + str(counter)))
            else:
                sendLogMessage((time.time()), 'testResult', ('HOT_PLUG: Drive NOT removed as expected after ' + str(offTime) + 'seconds'),
                  (os.path.basename(__file__) + ' - ' + sys._getframe().f_code.co_name),
                  {'testResult': False}, uId=(uniqueID + '.' + str(counter)))
                errorSubCounter += 1
            executeAndCheckCommand(quarchDevice, 'sig:12v:volt ' + str(currentPower))
            executeAndCheckCommand(quarchDevice, 'run:power up')
            driveTestConfig.testCallbacks['TEST_NEWSLEEP'](driveObject, 1, onTime)
            counter = counter + 1
            if driveTestConfig.testCallbacks['TEST_GETDISKSTATUS'](uniqueID, driveObject, 1):
                sendLogMessage((time.time()), 'testResult', ('HOT_PLUG: Drive detected as expected after ' + str(onTime) + 'seconds'),
                  (os.path.basename(__file__) + ' - ' + sys._getframe().f_code.co_name),
                  {'testResult': True}, uId=(uniqueID + '.' + str(counter)))
                elapsedTime = time.time() - startTestTime
                myStream.addAnnotation('Drive Found\\n' + str(round(elapsedTime, 5)) + 's')
            else:
                sendLogMessage((time.time()), 'testResult', ('HOT_PLUG: Drive NOT detected after ' + str(onTime) + 'seconds'), (os.path.basename(__file__) + ' - ' + sys._getframe().f_code.co_name),
                  {'testResult': False}, uId=(uniqueID + '.' + str(counter)))
                errorSubCounter += 1
            time.sleep(customSleepEnd)

        myStream.stopStream()
        uniqueID = startUID + '.' + str(int(numberOfIncrements) + 2)
        sendLogMessage((time.time()), 'testDescription', 'Results of Power Margining test', (os.path.basename(__file__) + ' - ' + sys._getframe().f_code.co_name), uId=uniqueID)
        if errorSubCounter == 0:
            sendLogMessage((time.time()), 'testResult', 'Power Margining test passed all repetitions', (os.path.basename(__file__) + ' - ' + sys._getframe().f_code.co_name),
              {'testResult': True}, uId=(uniqueID + '.1'))
        else:
            sendLogMessage((time.time()), 'testResult', ('Power Margining test failed: ' + str(errorSubCounter) + ' sub-test points'),
              (os.path.basename(__file__) + ' - ' + sys._getframe().f_code.co_name),
              {'testResult': False}, uId=(uniqueID + '.1'))
    elapsedTime = time.time() - startTestTime
    summaryString = 'Total TestTime Elapsed: ' + str(int(elapsedTime)) + 's, Error count = ' + str(errorSubCounter)
    sendLogMessage((time.time()), 'testSummary', summaryString, (os.path.basename(__file__) + ' - ' + sys._getframe().f_code.co_name),
      uId=(uniqueID + '.2'))
    logging.info('Test point end')
    quarchDevice.closeConnection()