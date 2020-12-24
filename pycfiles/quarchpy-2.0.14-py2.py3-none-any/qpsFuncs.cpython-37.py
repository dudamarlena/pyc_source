# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\sboon\AppData\Local\Temp\pip-install-ptdbtr91\quarchpy\quarchpy\qps\qpsFuncs.py
# Compiled at: 2020-03-25 05:10:07
# Size of source mod 2**32: 5022 bytes
import os, sys, datetime, time, platform
from quarchpy.qis import isQisRunning, startLocalQis
from quarchpy.connection_specific.connection_QIS import QisInterface
from quarchpy.connection_specific.connection_QPS import QpsInterface
from quarchpy.user_interface import *
import subprocess, logging

def isQpsRunning(host='127.0.0.1', port=9822):
    answer = '0'
    try:
        myQps = QpsInterface(host, port)
        answer = myQps.sendCmdVerbose(cmd='$list')
    except:
        pass

    if answer is None or answer == '':
        logging.debug('QPS did not return expected output from $list')
        logging.debug('$list: ' + str(answer))
        return False
    if answer[0] == '1' or 'no device' in str(answer).lower() or 'no module' in str(answer).lower():
        return True
    logging.debug('QPS did not return expected output from $list')
    logging.debug('$list: ' + str(answer))
    return False


def startLocalQps(keepQisRunning=True, args=None):
    if keepQisRunning:
        if not isQisRunning():
            startLocalQis()
    else:
        QpsPath = os.path.dirname(os.path.abspath(__file__))
        QpsPath, junk = os.path.split(QpsPath)
        QpsPath = os.path.join(QpsPath, 'connection_specific', 'QPS', 'qps.jar')
        current_direc = os.getcwd()
        os.chdir(os.path.dirname(QpsPath))
        command = '-jar "' + QpsPath + '"'
        currentOs = platform.system()
        if currentOs in 'Windows':
            command = 'start /high /b javaw -Djava.awt.headless=true ' + command
            os.system(command)
        else:
            if currentOs in 'Linux':
                if sys.version_info[0] < 3:
                    os.popen2('java ' + command + ' 2>&1')
                else:
                    os.popen('java ' + command + ' 2>&1')
            else:
                command = 'start /high /b javaw -Djava.awt.headless=true ' + command
                os.system(command)
    while not isQpsRunning():
        time.sleep(0.1)

    os.chdir(current_direc)


def closeQps(host='127.0.0.1', port=9822):
    myQps = QpsInterface(host, port)
    myQps.sendCmdVerbose('$shutdown')
    del myQps


def GetQpsModuleSelection(QpsConnection, favouriteOnly=True, additionalOptions=[], scan=True):
    tableHeaders = ['Module']
    devList = QpsConnection.getDeviceList(scan=scan)
    if 'no device' in devList[0].lower() or 'no module' in devList[0].lower():
        favouriteOnly = False
    devList = [x for x in devList if 'rest' not in x]
    message = 'Select a quarch module'
    if favouriteOnly:
        index = 0
        sortedDevList = []
        conPref = ['USB', 'TCP', 'SERIAL', 'REST', 'TELNET']
        while len(sortedDevList) != len(devList):
            for device in devList:
                if conPref[index] in device.upper():
                    sortedDevList.append(device)

            index += 1

        devList = sortedDevList
        favConDevList = []
        index = 0
        for device in sortedDevList:
            if favConDevList == [] or device.split('::')[1] not in str(favConDevList):
                favConDevList.append(device)

        devList = favConDevList
    myDeviceID = listSelection(title=message, message=message, selectionList=devList, additionalOptions=additionalOptions, nice=True, tableHeaders=tableHeaders, indexReq=True)
    return myDeviceID


def legacyAdjustTime(timestamp):
    return timestamp


def toQpsTimeStamp(timestamp):
    if type(timestamp) is datetime:
        newTime = time.mktime(timestamp.timetuple())
        return int(newTime * 1000)
    if type(timestamp) is float or type(timestamp) is int:
        return int(timestamp)
    try:
        timestamp = float(timestamp)
        return int(timestamp)
    except:
        newTime = time.mktime(datetime.datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S:%f').timetuple())
        return int(newTime * 1000)