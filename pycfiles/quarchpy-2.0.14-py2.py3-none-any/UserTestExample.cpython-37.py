# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\sboon\AppData\Local\Temp\pip-install-ptdbtr91\quarchpy\quarchpy\disk_test\UserTestExample.py
# Compiled at: 2020-03-25 05:10:07
# Size of source mod 2**32: 3382 bytes
"""
This example demonstrates the use of Quarch Drive Test Suite functions to create a set of tests

- Tests can be run directly, or parsed from a CSV file
- Test callbacks can be overridden by the user and modified to add additional functionality

########### VERSION HISTORY ###########

20/09/2018 - Andy Norrie                - First Version

########### INSTRUCTIONS ###########

1- Run the script and follow the instructions on screen

####################################
"""
from quarchpy.disk_test import driveTestCore
from quarchpy.disk_test import driveTestConfig
from quarchpy.disk_test import hotPlugTest
from quarchpy.device import scanDevices
from quarchpy.user_interface import *

def main():
    """
    Setup the callback functions used by the tests, for logging and checking drive function
    This currently uses the standard provided functions, can cab be altered by the user
    """
    driveTestConfig.testCallbacks = {'TEST_LOG':driveTestCore.notifyTestLogEventXml, 
     'TEST_GETDISKSTATUS':driveTestCore.DiskStatusCheck, 
     'UTILS_VISUALSLEEP':driveTestCore.visualSleep, 
     'TEST_GETRESOURCE':driveTestCore.getTestResource, 
     'TEST_SETRESOURCE':driveTestCore.setTestResource}
    printText('\n################################################################################')
    printText('\n                           QUARCH TECHNOLOGY                        \n\n  ')
    printText('Automated Drive/Host test suite.   ')
    printText('\n################################################################################\n')
    driveTestCore.ActivateRemoteServer()


def ExampleTests():
    printText(scanDevices('all', scanInArray=True))
    driveTestCore.specifyQuarchModule('USB:QTL1743-03-392', 'quarchModule1')
    quarchDevice = driveTestConfig.testCallbacks['TEST_GETRESOURCE']('quarchModule1')
    hotPlugTest.executeAndCheckCommand(quarchDevice, 'sig:all:sour 1')
    hotPlugTest.executeAndCheckCommand(quarchDevice, 'sig:all:sour 2')
    hotPlugTest.executeAndCheckCommand(quarchDevice, 'sig:all:sour 3')
    hotPlugTest.executeAndCheckCommand(quarchDevice, 'conf:def state')
    hotPlugTest.executeAndCheckCommand(quarchDevice, 'sig:all:sour 4')


if __name__ == '__main__':
    main()