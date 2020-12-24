# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\sboon\AppData\Local\Temp\pip-install-ptdbtr91\quarchpy\quarchpy\iometer\iometerFuncs.py
# Compiled at: 2020-03-25 05:10:07
# Size of source mod 2**32: 13373 bytes
"""
This contains useful functions for Iometer automation with Quarch tools

########### VERSION HISTORY ###########

13/08/2018 - Andy Norrie    - First version, based on initial work from Pedro Leao
"""
import time, os, subprocess, threading, multiprocessing as mp
from multiprocessing import Pipe
import csv, datetime, socket, csv, mmap
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

def runIOMeter(*fileName):
    time.sleep(1)
    filepassed = ''
    for value in fileName:
        filepassed = filepassed + value

    info = subprocess.STARTUPINFO()
    info.dwFlags = 1
    info.wShowWindow = 0
    runAsAdminCmd = 'runas'
    proc = subprocess.Popen(('IOmeter.exe /c ' + filepassed + ' /r testfile.csv'), stdout=(subprocess.PIPE), stderr=(subprocess.PIPE), startupinfo=info, shell=True)
    out, error = proc.communicate()


def followResultsFile(theFile):
    while True:
        line = theFile.readline()
        if not line:
            time.sleep(0.1)
            continue
        yield line


def processIometerInstResults(testName, myStream, userCallbacks):
    while os.path.isfile('insttestfile.csv') == False:
        pass

    resultsFile = open('insttestfile.csv', 'rb')
    resultsIterator = followResultsFile(resultsFile)
    driveSpeed = ''
    fileSection = 0
    lineCount = 0
    lineCount2 = 0
    sum_all_threads1 = 0
    sum_all_threads2 = 0
    sum_all_threads3 = 0
    testDescrip = 'Undescribed Test'
    workerCount = 99999
    workerList = []
    resultsMap = {'IOPS':0, 
     'RATE':0, 
     'RESPONSE':0}
    for dataLine in resultsIterator:
        f = StringIO(dataLine.decode('utf-8'))
        lineCount = lineCount + 1
        csvData = list(csv.reader(f))
        if lineCount == 2:
            if csvData[0][1] != '':
                testDescrip = csvData[0][1]
        if fileSection == 0 and csvData[0][0] != "'Time Stamp":
            continue
        else:
            if fileSection == 0:
                fileSection = 1
                continue
        if fileSection == 1:
            timeStamp = csvData[0][0]
            if 'TEST_START' in userCallbacks:
                userCallbacks['TEST_START'](myStream, timeStamp, testDescrip)
            fileSection = 2
            continue
        if fileSection == 2 and csvData[0][0] != 'TimeStamp':
            continue
        else:
            if fileSection == 2:
                fileSection = 3
                continue
        if fileSection == 3:
            lineCount2 += 1
            prevTimeStamp = timeStamp
            timeStamp = csvData[0][0]
            if timeStamp == "'Time Stamp":
                fileSection = 4
                continue
            if workerCount == 99999:
                if workerList.__contains__(csvData[0][2]) == False:
                    workerList.append(csvData[0][2])
                else:
                    workerCount = len(workerList)
                    sum_all_threads2 = sum_all_threads2 * 1000000
                    sum_all_threads3 = sum_all_threads3 / workerCount
                    resultsMap['IOPS'] = sum_all_threads1
                    resultsMap['DATA_RATE'] = sum_all_threads2
                    resultsMap['RESPONSE_TIME'] = sum_all_threads3
                    if 'TEST_RESULT' in userCallbacks:
                        userCallbacks['TEST_RESULT'](myStream, prevTimeStamp, resultsMap)
                    sum_all_threads1 = 0
                    sum_all_threads2 = 0
                    sum_all_threads3 = 0
            dataValue1 = csvData[0][7]
            dataValue2 = csvData[0][13]
            dataValue3 = csvData[0][18]
            sum_all_threads1 += float(dataValue1)
            sum_all_threads2 += float(dataValue2)
            sum_all_threads3 += float(dataValue3)
            if lineCount2 % workerCount == 0:
                sum_all_threads2 = sum_all_threads2 * 1000000
                sum_all_threads3 = sum_all_threads3 / workerCount
                resultsMap['IOPS'] = sum_all_threads1
                resultsMap['DATA_RATE'] = sum_all_threads2
                resultsMap['RESPONSE_TIME'] = sum_all_threads3
                if 'TEST_RESULT' in userCallbacks:
                    userCallbacks['TEST_RESULT'](myStream, prevTimeStamp, resultsMap)
                sum_all_threads1 = 0
                sum_all_threads2 = 0
                sum_all_threads3 = 0
            if fileSection == 4:
                timeStamp = csvData[0][0]
                if 'TEST_END' in userCallbacks:
                    userCallbacks['TEST_END'](myStream, timeStamp, testDescrip)
                resultsFile.close()
                return


def generateIcfFromConf(confPath, driveInfo, managerName=socket.gethostname()):
    configFiles = []
    fileCount = 0
    config_list = []
    for file in os.listdir(confPath):
        if file.endswith('.conf'):
            confFilePath = os.path.join(confPath, file)
            icfFilePath = confFilePath.replace('.conf', '.icf')
            if os.path.exists(icfFilePath):
                os.remove(icfFilePath)
            else:
                openFile = open(confFilePath)
                fileData = openFile.read()
                openFile.close()
                if driveInfo['FW_REV']:
                    newStr = str(driveInfo['DRIVE']) + ': "' + str(driveInfo['NAME']) + ' ' + str(driveInfo['FW_REV']) + '"'
                else:
                    newStr = str(driveInfo['DRIVE']) + ': "' + str(driveInfo['NAME']) + '"'
            oldStr = '[*TARGET*]'
            fileData = fileData.replace(str(oldStr), str(newStr))
            newStr = managerName
            oldStr = '[*MANAGER*]'
            fileData = fileData.replace(str(oldStr), str(newStr))
            openFile = open(icfFilePath, 'a+')
            openFile.write(fileData)
            s = mmap.mmap((openFile.fileno()), 0, access=(mmap.ACCESS_READ))
            pos_start = s.find(str.encode('Assigned access specs'))
            pos_end = s.find(str.encode('End assigned access specs'))
            if pos_start != -1:
                config_list.append(s[pos_start + 21:pos_end - 1])
            openFile.close()
            fileCount = fileCount + 1

    return (
     fileCount, config_list)


def generateIcfFromCsvLineData(csvData, icfFilePath, driveInfo, managerName=socket.gethostname()):
    templateFilePath = os.path.dirname(os.path.abspath(__file__)) + '\\IometerTemplate.dat'
    csvTestName = None
    csvWorkers = None
    csvRequestSize = None
    csvReadPer = None
    csvRandomPer = None
    csvRunTime = None
    accessSpecName = 'quarch-autogenerated-spec'
    accessSpecString = ''
    csvTestName = csvData['TEST_NAME']
    csvWorkers = csvData['WORKER_COUNT']
    csvRequestSize = csvData['REQUEST_SIZE']
    csvReadPer = csvData['READ_PER']
    csvRandomPer = csvData['RANDOM_PER']
    csvRunTime = csvData['RUN_TIME']
    accessSpecString = '\t' + csvRequestSize + ',100,' + csvReadPer + ',' + csvRandomPer + ',0,1,0,0'
    if os.path.exists(icfFilePath):
        os.remove(icfFilePath)
    else:
        openFile = open(templateFilePath)
        fileData = openFile.readlines()
        openFile.close()
        workerData = fileData[51:72]
        workerData = ''.join(workerData)
        fileData = fileData[:51]
        fileData = ''.join(fileData)
        newStr = managerName
        oldStr = '[*MANAGER*]'
        fileData = fileData.replace(str(oldStr), str(newStr))
        newStr = "'Access specification name,default assignment\n\t" + accessSpecName + ",NONE\n'size,% of size,% reads,% random,delay,burst,align,reply\n" + accessSpecString
        oldStr = '[*ACCESS_SPEC_DEFINE*]'
        fileData = fileData.replace(str(oldStr), str(newStr))
        newStr = csvTestName
        oldStr = '[*TEST_NAME*]'
        fileData = fileData.replace(str(oldStr), str(newStr))
        newStr = csvRunTime
        oldStr = '[*TIME_SECS*]'
        fileData = fileData.replace(str(oldStr), str(newStr))
        newStr = csvRunTime
        oldStr = '[*TIME_SECS*]'
        fileData = fileData.replace(str(oldStr), str(newStr))
        if driveInfo['FW_REV']:
            newStr = str(driveInfo['DRIVE']) + ': "' + str(driveInfo['NAME']) + ' ' + str(driveInfo['FW_REV']) + '"'
        else:
            newStr = str(driveInfo['DRIVE']) + ': "' + str(driveInfo['NAME']) + '"'
    oldStr = '[*TARGET_1*]'
    workerData = workerData.replace(str(oldStr), str(newStr))
    oldStr = '[*SPEC_1*]'
    workerData = workerData.replace(str(oldStr), str(accessSpecName))
    for x in range(int(csvWorkers)):
        workerData0 = workerData
        oldStr = '[*WORKER_#*]'
        fileData = fileData + workerData0.replace(str(oldStr), str(x + 1))

    finalString = "'End manager\n'END manager list\nVersion 1.1.0"
    openFile = open(icfFilePath, 'a+')
    openFile.write(fileData + finalString)
    openFile.close()


def readIcfCsvLineData(csvFileName, csvFileLine):
    csvFilePath = os.getcwd() + '\\' + csvFileName
    with open(csvFilePath, 'rt') as (csvFile):
        csvReader = csv.reader(csvFile, delimiter='\t')
        csvReader = list(csvReader)
        headerRow = csvReader[0]
        try:
            dataRow = csvReader[csvFileLine]
        except:
            return (None, False)

    csvDataLine = {'TEST_NAME':None, 
     'WORKER_COUNT':None, 
     'REQUEST_SIZE':None, 
     'READ_PER':None, 
     'RANDOM_PER':None, 
     'RUN_TIME':None}
    csvDataLine.update(dict(zip(['TEST_NAME', 'WORKER_COUNT', 'REQUEST_SIZE', 'READ_PER', 'RANDOM_PER', 'RUN_TIME'], dataRow)))
    return (
     csvDataLine, True)