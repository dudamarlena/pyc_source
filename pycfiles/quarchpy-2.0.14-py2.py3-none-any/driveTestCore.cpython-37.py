# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\sboon\AppData\Local\Temp\pip-install-ptdbtr91\quarchpy\quarchpy\disk_test\driveTestCore.py
# Compiled at: 2020-03-25 05:10:07
# Size of source mod 2**32: 39603 bytes
"""
This file contains the core functions for the drive test suite.
Functions are placed here for the core setup functions called during the init stage of a test (or CSV parsed test set)

########### VERSION HISTORY ###########

03/01/2019 - Andy Norrie        - First Version

########### INSTRUCTIONS ###########

N/A

####################################
"""
from __future__ import print_function
import sys, os, multiprocessing, logging, pkg_resources, importlib
from datetime import datetime
import traceback
import xml.etree.ElementTree as cElementTree
from quarchpy.user_interface import *
from quarchpy.device.scanDevices import *
from quarchpy.device import quarchQPS, quarchDevice
from quarchpy.connection_specific.connection_QPS import QpsInterface
from quarchpy.qps.qpsFuncs import isQpsRunning
import quarchpy.disk_test.testLine as testLine
from quarchpy.disk_test import driveTestConfig
import quarchpy.disk_test.dtsGlobals as dtsGlobals
from quarchpy.disk_test.dtsComms import DTSCommms
from quarchpy.disk_test.hostInformation import HostInformation
try:
    import zeroconf
    from zeroconf import ServiceInfo, Zeroconf
    zeroConfAvail = True
except:
    logging.warning("Please install zeroconf using 'pip install zeroconf'")
    zeroConfAvail = False

myHostInfo = HostInformation()
comms = DTSCommms()
ignoredChoices = ['choiceResponse::rescan']

def printToBackend(text=''):
    printText(text=text, terminalWidth=80, fillLine=True)


def printProgressBar(iteration, total):
    iteration = float(iteration)
    total = float(total)
    progressBar(iteration, total, fullWidth=80)


def sendLogMessage(logTime, messageType, messageText, messageSource, messageData=None, uId=''):
    if 'TEST_LOG' in driveTestConfig.testCallbacks:
        driveTestConfig.testCallbacks['TEST_LOG'](uId, logTime, messageType, messageText, messageSource, messageData)


def executeAndCheckCommand(myDevice, command):
    result = myDevice.sendCommand(command)
    sendLogMessage((time.time()), 'debug', ('Quarch Command: ' + command + ' - Response: ' + result), (os.path.basename(__file__) + ' - ' + sys._getframe().f_code.co_name),
      {'debugLevel':1, 
     'textDetails':'Executing command on module'},
      uId='')
    if result == 'OK':
        return True
    sendLogMessage((time.time()), 'error', 'Failed to execute Torridon command', (os.path.basename(__file__) + ' - ' + sys._getframe().f_code.co_name),
      uId='')
    return False


def storeResourceString(resourceName, resourceValue):
    driveTestConfig.testResources[resourceName] = resourceValue


def isUserAdmin():
    if os.name == 'nt':
        import ctypes
        try:
            return ctypes.windll.shell32.IsUserAnAdmin() == 1
        except:
            traceback.print_exc()
            return False

    else:
        if os.name == 'posix':
            return os.getuid() == 0
        raise RuntimeError('Unsupported operating system for this module: %s' % (os.name,))


def specifyQuarchModule(moduleName, interFaceType='PY', powerOnDevice=True):
    connection = None
    if 'PY' in interFaceType:
        connection = chooseQuarchModule(moduleName)
    else:
        if 'QPS' in interFaceType:
            connection = chooseQuarchModuleQPS(moduleName)
        elif connection is None:
            printText('No item selected, test aborted. Waiting for new test start..\n')
            return 0
            strPos = connection.find('<')
            if strPos != -1:
                logging.debug(connection + ' : ' + moduleName)
                arrayConnection = connection[0:strPos]
                arrayPosition = connection[strPos + 1:]
                arrayPosition = arrayPosition.strip(' >')
                try:
                    myQuarchDevice = quarchDevice(arrayConnection)
                except Exception as e:
                    try:
                        connection = None
                        comms.sendMsgToGUI(toSend='stopTest')
                        printText('Could not establish connection to root device. Test aborted')
                        return 0
                    finally:
                        e = None
                        del e

                myArray = quarchArray(myQuarchDevice)
                mySubDevice = myArray.getSubDevice(arrayPosition)
                moduleResponse = mySubDevice.sendCommand('*TST?')
                if moduleResponse != 'OK':
                    notifyTestLogEvent(time.time(), 'error', 'Quarch module not ready', os.path.basename(__file__) + ' - ' + sys._getframe().f_code.co_name, {'textDetails': 'Module responded: ' + moduleResponse})
            else:
                driveTestConfig.testResources[moduleName] = mySubDevice
        else:
            if 'QPS' in interFaceType:
                connection, outputModeValue = connection.split('=')
                myQuarchDevice = quarchDevice(connection, ConType=('QPS:' + dtsGlobals.GUI_TCP_IP + ':9822'))
                myQpsDevice = quarchQPS(myQuarchDevice)
                myQpsDevice.openConnection()
                driveTestConfig.testResources[moduleName] = myQpsDevice
                if powerOnDevice:
                    powerOnDrive(myQpsDevice, outputMode=outputModeValue)
            else:
                myQuarchDevice = None
                try:
                    myQuarchDevice = quarchDevice(connection)
                except Exception as e:
                    try:
                        connection = None
                        comms.sendMsgToGUI(toSend='stopTest')
                        printText('Error while connecting to specified device, test aborted')
                        return 0
                    finally:
                        e = None
                        del e

                moduleResponse = myQuarchDevice.sendCommand('*TST?')
                if moduleResponse is None or moduleResponse == '':
                    notifyTestLogEvent(time.time(), 'error', 'Quarch module did not respond', os.path.basename(__file__) + ' - ' + sys._getframe().f_code.co_name)
                    return
                if moduleResponse != 'OK':
                    notifyTestLogEvent(time.time(), 'warning', 'Quarch module did not pass self test', os.path.basename(__file__) + ' - ' + sys._getframe().f_code.co_name, {'textDetails': 'Module responded: ' + moduleResponse})
                driveTestConfig.testResources[moduleName] = myQuarchDevice
        if powerOnDevice:
            powerOnDrive(myQuarchDevice)


def powerOnDrive(myQuarchDevice, outputMode=None):
    if outputMode is not None:
        myQuarchDevice.sendCommand('conf:out:mode ' + outputMode)
        myQuarchDevice.sendCommand('conf out 12v pull on')
    myQuarchDevice.sendCommand('sig 12v volt 12000')
    powerStatus = myQuarchDevice.sendCommand('run pow?')
    counter = 0
    while 'on' not in str(powerStatus).lower() and counter < 50:
        if 'plugged' in str(powerStatus).lower():
            return
        myQuarchDevice.sendCommand('run:pow up')
        time.sleep(0.2)
        counter += 1
        powerStatus = myQuarchDevice.sendCommand('run:pow?')


def chooseQuarchModuleQPS(moduleName, myQps=None):
    dir = os.path.dirname(os.path.realpath(__file__))
    if not isQpsRunning(dtsGlobals.GUI_TCP_IP):
        comms.sendMsgToGUI('QuarchDTS::StartQPS::' + str(dir), None)
    else:
        dtsGlobals.choiceResponse = None
        while True:
            try:
                send_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                send_sock.connect((dtsGlobals.GUI_TCP_IP, 9822))
                send_sock.close()
                break
            except socket.error:
                time.sleep(1)

        myQps = QpsInterface(host=(dtsGlobals.GUI_TCP_IP))
        status = myQps.sendCmdVerbose('$qis status')
        while 'Not Connected' in status:
            status = myQps.sendCmdVerbose('$qis status')
            time.sleep(0.2)

        time.sleep(3)
        qpsDeviceList = myQps.getDeviceList()
        comms.sendMsgToGUI('QuarchDTS::header<QPS>::Choose a Quarch module to connect to', None)
        content = ' '
        content = content.join(qpsDeviceList)
        if 'No Devices Found' in content:
            printText('No Quarch modules currently detected', fillLine=True, terminalWidth=80)
        else:
            for quarchModule in qpsDeviceList:
                if 'rest' in quarchModule:
                    continue
                connectionWithoutConType = quarchModule[quarchModule.rindex(':') + 1:]
                comms.newNotifyChoiceOption('qpsmodule', quarchModule.replace('::', ':'), connectionWithoutConType)

    comms.sendMsgToGUI('QuarchDTS::end-of-data', None)
    while dtsGlobals.choiceResponse is None and dtsGlobals.continueTest is True:
        time.sleep(0.25)

    choice = bytes.decode(dtsGlobals.choiceResponse)
    selection = choice.replace('\r\n', '').split('::', 2)
    if 'rescan' not in selection:
        logging.debug('Response from module selection was : ' + choice)
    if 'choice-abort' in choice:
        return
    if 'rescan' in choice:
        return chooseQuarchModuleQPS(moduleName, myQps)
    selection[1] = selection[1].replace(':', '::')
    logging.debug('Selection1 is now ' + selection[1])
    myQps.sendCmdVerbose('selection[1] conf:def:state')
    outMode = myQps.sendCmdVerbose(selection[1] + ' conf:out:mode?')
    logging.debug('Out mode for selection was ' + outMode)
    if 'DISABLED' in outMode:
        comms.sendMsgToGUI('QuarchDTS::header::Choose a Quarch module to connect to', None)
        selection[1] = selection[1].replace('::', ':')
        connectionWithoutConType = selection[1][selection[1].rindex(':') + 1:]
        comms.newNotifyChoiceOption('qpsmodule', (selection[1].replace('::', ':')), connectionWithoutConType, outputMode=outMode)
        time.sleep(0.5)
        comms.sendMsgToGUI('QuarchDTS::end-of-data::true', None)
        while dtsGlobals.choiceResponse is None and dtsGlobals.continueTest is True:
            time.sleep(0.25)

        choice = bytes.decode(dtsGlobals.choiceResponse)
        if 'choice-abort' in choice:
            return
        if 'rescan' in choice:
            return chooseQuarchModuleQPS(moduleName, myQps)
        outModeSelection = str(dtsGlobals.choiceResponse).split('::')
        outMode = outModeSelection[2]
        logging.debug(outMode)
        if '5V' in outMode:
            outMode = '5V'
        if '3v3' in outMode:
            outMode = '3v3'
    myQps.client.close()
    selection[1] = selection[1].replace('::', ':')
    selection = selection[1]
    retVal = selection.strip() + '=' + outMode
    return retVal


def chooseQuarchModule(moduleName, ipAddressLookup=None):
    dtsGlobals.choiceResponse = None
    scanDictionary = scanDevices(favouriteOnly=False, ipAddressLookup=ipAddressLookup)
    ipAddressLookup = None
    comms.sendMsgToGUI('QuarchDTS::header<PY>::Choose a Quarch module to connect to', None)
    for connection in scanDictionary:
        comms.newNotifyChoiceOption('module', connection, scanDictionary[connection])

    if not scanDictionary:
        printText('No Quarch modules currently detected')
    comms.sendMsgToGUI('QuarchDTS::end-of-data', None)
    while dtsGlobals.choiceResponse is None and dtsGlobals.continueTest is True:
        time.sleep(0.25)

    choice = bytes.decode(dtsGlobals.choiceResponse)
    selection = choice.split('::')
    selection = selection[1]
    selection = selection.replace(':', '::')
    if 'rescan' not in selection:
        logging.debug('Response from module selection was : ' + choice)
    if 'choice-abort' in selection:
        return
    if 'rescan' in selection:
        if '==' in selection:
            ipAddressLookup = selection[selection.index('==') + 2:]
        return chooseQuarchModule(moduleName, ipAddressLookup)
    return selection.strip()


def executeCsvTestFile(testCallbacks, filePath, delimitor='\t'):
    with open(filePath, 'r') as (scriptFile):
        for fileLine in scriptFile:
            if fileLine.find('#') == 0:
                continue
            elif fileLine.find('Config') == 0:
                lineSections = fileLine.split(delimitor)
                moduleName = lineSections[1]
                testName = lineSections[2]
                funcParams = ''
                for x in range(3, len(lineSections)):
                    if len(lineSections[x].strip()) > 0:
                        funcParams = funcParams + lineSections[x].strip() + ','

                funcParams = funcParams.strip(',')
                parsedArgs = dict((e.split('=') for e in funcParams.split(',')))
                modulePointer = sys.modules[moduleName]
                (getattr(modulePointer, testName))(**parsedArgs)
            elif fileLine.find('Test') == 0:
                lineSections = fileLine.split(delimitor)
                moduleName = lineSections[1]
                testName = lineSections[2]
                funcParams = ''
                for x in range(3, len(lineSections)):
                    if len(lineSections[x].strip()) > 0:
                        funcParams = funcParams + lineSections[x].strip() + ','

                funcParams = funcParams.strip(',')
                parsedArgs = dict((e.split('=') for e in funcParams.split(',')))
                modulePointer = sys.modules[moduleName]
                (getattr(modulePointer, testName))(**parsedArgs)
            elif fileLine.find('Skip') == 0:
                continue
            elif len(fileLine.strip()) == 0:
                continue
            else:
                lineSections = fileLine.split(delimitor)
                driveTestConfig.testCallbacks['TEST_LOG'](time.time(), 'error', 'Unknown test line type: ' + lineSections[0], os.path.basename(__file__) + ' - ' + sys._getframe().f_code.co_name)


def specifyDriveById(driveId, driveName):
    driveTestConfig.testResources[driveName] = driveId


def getTestResource(resourceName):
    if resourceName in driveTestConfig.testResources:
        return driveTestConfig.testResources[resourceName]
    notifyTestLogEvent(time.time(), 'error', 'Unknown resource item requested:' + resourceName, os.path.basename(__file__) + ' - ' + sys._getframe().f_code.co_name, {'textDetails': 'The given resource name was not found'})
    return


def setTestResource(resourceName, resourceValue):
    driveTestConfig.testResources[resourceName] = resourceValue


def resetTestResources():
    if driveTestConfig.testResources:
        driveTestConfig.testResources.clear()
    dtsGlobals.continueTest = True
    dtsGlobals.validVersion = True
    dtsGlobals.choiceResponse = None


def checkDriveState(driveObject, deviceState, waitTime):
    start = time.time()
    loop = 0
    end = time.time() - start
    toFind = ''
    while end < float(waitTime):
        end = time.time() - start
        if driveTestConfig.testCallbacks['TEST_GETDISKSTATUS']('', driveObject, deviceState, checkLanes=False):
            return
        time.sleep(0.1)
        loop += 1
        if loop == 5:
            loop = 0
            comms.sendMsgToGUI('testing>')


def visualSleep(delayTime):
    for x in range(0, int(delayTime)):
        time.sleep(1)
        if x % 1 == 0:
            comms.sendMsgToGUI('testing>')


logFilePath = os.path.join(os.getcwd(), 'LogFile' + str(datetime.now()).replace(':', '_') + '.txt')

def notifyTestLogEvent(timeStamp, logType, logText, logSource, logDetails=None):
    logString = datetime.utcfromtimestamp(timeStamp).strftime('%Y-%m-%d %H:%M:%S') + '\t' + logType + '\t' + logText + '\t' + logSource
    if logDetails != None:
        for k, v in logDetails.items():
            logString = logString + '\t' + k + '=' + str(v)

    if not (driveTestConfig.logDebugMessagesInFile == False and logType == 'debug'):
        with open(logFilePath, 'a') as (logFile):
            logFile.write(logString + '\n')


def DiskStatusCheck(uniqueID, driveId, expectedState, checkLanes=True):
    if 'PCIE' in str(driveId).upper():
        if driveId.index('PCIE:') == 0:
            mappingMode = getTestResource('pcieMappingMode')
            if mappingMode == None:
                mappingMode = False
            pcieAddress = driveId[5:]
            driveState = myHostInfo.isDevicePresent(pcieAddress, mappingMode, 'pcie')
            if expectedState:
                if driveState:
                    if checkLanes:
                        return myHostInfo.verifyDriveStats(uniqueID, pcieAddress, mappingMode)
                    return True
                return False
            else:
                if driveState == False:
                    return True
                return False
                return driveState
    if 'SAS' in str(driveId).upper():
        if driveId.index('SAS:') == 0:
            mappingMode = getTestResource('pcieMappingMode')
            if mappingMode == None:
                mappingMode = False
            sasDriveName = driveId[4:]
            driveState = myHostInfo.isDevicePresent(sasDriveName, mappingMode, 'sas')
            if expectedState:
                if driveState:
                    return True
                return False
            else:
                if driveState == False:
                    return True
                return False
                return driveState
    notifyTestLogEvent(time.time(), 'error', 'Unknown drive type: ' + driveId, os.path.basename(__file__) + ' - ' + sys._getframe().f_code.co_name, {'textDetails': 'Unable to check status of the drive'})
    return False


def notifyTestLogEventXml(uniqueId, timeStamp, logType, logText, logSource, logDetails=None):
    if uniqueId == '' or uniqueId is None:
        uniqueId = ' '
    xmlObject = cElementTree.Element('object')
    cElementTree.SubElement(xmlObject, 'uniqueID').text = uniqueId
    cElementTree.SubElement(xmlObject, 'timestamp').text = datetime.utcfromtimestamp(timeStamp).strftime('%Y-%m-%d %H:%M:%S')
    cElementTree.SubElement(xmlObject, 'logType').text = logType
    cElementTree.SubElement(xmlObject, 'text').text = logText
    cElementTree.SubElement(xmlObject, 'messageSource').text = logSource
    if logDetails != None:
        xmlDetails = cElementTree.SubElement(xmlObject, 'logDetails')
        for k, v in logDetails.items():
            xmlEntry = cElementTree.SubElement(xmlDetails, 'entry')
            cElementTree.SubElement(xmlEntry, 'key').text = str(k)
            cElementTree.SubElement(xmlEntry, 'value').text = str(v)

    xmlstr = str(cElementTree.tostring(xmlObject), 'UTF-8').replace('\n', '')
    comms.sendMsgToGUI(xmlstr)


def getLocalIpAddress(first=True):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        try:
            s.connect(('10.255.255.255', 1))
            IP = s.getsockname()[0]
            if IP == '127.0.0.1':
                if first is True:
                    s.close()
                    getLocalIpAddress(first=False)
        except:
            IP = None

    finally:
        s.close()

    return IP


def attemptRestart(conn, sock, reason=None):
    if reason is None:
        printText('Java connection closed, attempting to recover ')
    else:
        printText(reason)
    conn.close()
    sock.close()
    resetTestResources()
    ActivateRemoteServer(localHost=False)


def ActivateRemoteServer(portNumber=9742, localHost=False):
    driveTestConfig.testCallbacks = {'TEST_LOG':notifyTestLogEventXml, 
     'TEST_GETDISKSTATUS':DiskStatusCheck, 
     'UTILS_VISUALSLEEP':visualSleep, 
     'TEST_GETRESOURCE':getTestResource, 
     'TEST_SETRESOURCE':setTestResource, 
     'TEST_NEWSLEEP':checkDriveState}
    TCP_PORT = portNumber
    portNumber = 1024
    BUFFER_SIZE = 4096
    mDnsInfo = None
    conn = None
    serverName = None
    if serverName is None:
        try:
            serverName = socket.gethostname()
        except:
            serverName = 'no-name-server'

    try:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.bind(('', TCP_PORT))
            sock.listen(1)
            printText('----Remote Server Activated----')
            TCP_IP = '127.0.0.1'
            if not localHost:
                TCP_IP = '{address}'.format(address=('127.0.0.1' if getLocalIpAddress() is None else getLocalIpAddress()))
            else:
                printText('\tServer IP: ' + str(TCP_IP))
                if zeroConfAvail:
                    try:
                        mDnsIp = TCP_IP
                        mDnsDesc = {'version':'1.0',  'server-name':serverName}
                        mDnsInfo = ServiceInfo('_http._tcp.local.', 'quarchCS._http._tcp.local.', socket.inet_aton(mDnsIp), TCP_PORT, 0, 0, mDnsDesc)
                        zeroConf = Zeroconf()
                        zeroConf.register_service(mDnsInfo)
                        printText('----mDNS Registered----')
                        printText('\tServer Name: ' + serverName)
                    except:
                        printText('mDNS error, Service not registered')

                else:
                    zeroConf = None
            conn, addr = sock.accept()
            printText('----Remote Server connection opened from: ' + str(addr))
            item = str(addr).split("'")
            dtsGlobals.GUI_TCP_IP = item[1]
            if not checkCompatibility(comms):
                return
            continueScript = True
            try:
                while continueScript:
                    data = conn.recv(BUFFER_SIZE)
                    data = data or data.replace(str.encode('\r\n'), b'')
                    commandParser(conn, sock, data)

            except KeyboardInterrupt:
                printText('---Remote server shutdown request, user CTRL-C received')

        except ConnectionResetError:
            attemptRestart(conn, sock)
        except Exception as ex:
            try:
                printText('----Remote server process exited with an exception')
                printText(ex)
            finally:
                ex = None
                del ex

    finally:
        if conn is not None:
            conn.close()
        sock.close()
        printText('----Remote server shutdown complete')


def commandParser(conn, sock, data):
    if len(data) == 0:
        attemptRestart(conn, sock)
    elif 'Alive?' in bytes.decode(data):
        toSend = str.encode('ok >')
        conn.sendall(toSend + b'\n')
        return
        if 'disconnect' in bytes.decode(data):
            toSend = str.encode('ok >')
            conn.sendall(toSend + b'\n')
            attemptRestart(conn, sock, 'User Closed GUI. Server Restart.')
    else:
        try:
            myobj = testLine()
            xmlRoot = cElementTree.fromstring(bytes.decode(data))
            myobj.initFromXml(xmlRoot)
            if myobj.moduleName == 'driveTestCore':
                modulePointer = sys.modules[__name__]
            else:
                if myobj.moduleName == 'hostInformation':
                    modulePointer = myHostInfo
                else:
                    modulePointer = importlib.import_module('.' + myobj.moduleName, 'quarchpy.disk_test')
            (getattr(modulePointer, myobj.testName))(**myobj.paramList)
            finishedString = 'ok >'
            conn.sendall(str.encode(finishedString) + b'\n')
        except ValueError as err:
            try:
                traceback.print_tb(err.__traceback__)
                printText('ERROR - Bad remote command format')
            finally:
                err = None
                del err

        except AttributeError as e:
            try:
                printText('Hit an attribute error, restarting')
                printText(e)
                printText(AttributeError)
                attemptRestart(conn, sock)
            finally:
                e = None
                del e

        except ConnectionRefusedError as err:
            try:
                printText('Could not send response to Java, aborting')
                attemptRestart(conn, sock)
            finally:
                err = None
                del err

        except Exception as e:
            try:
                printText(e)
                printText('ERROR - Unexpected failure in command parser')
                raise
            finally:
                e = None
                del e


def checkCompatibility(comms):
    comms.sendMsgToGUI('QuarchPy Version: ' + pkg_resources.get_distribution('quarchpy').version)
    if not dtsGlobals.validVersion:
        printText(pkg_resources.get_distribution('quarchpy').version)
        printText('Quarchpy version too low for this QCS version. Please upgrade Quarchpy.')
        return False
    if not dtsGlobals.QCSVersionValid:
        printText('QCS version too low for this Quarchpy version. Please upgrade QCS.')
        return False
    printText('Compatible QCS and quarchpy')
    return True


def setUpLogging(logLevel):
    levels = {'CRITICAL':50, 
     'ERROR':40, 
     'WARNING':30, 
     'INFO':20, 
     'DEBUG':10}
    logging.basicConfig(level=(levels.get(str(logLevel).upper())))


def main(argstring):
    import argparse
    parser = argparse.ArgumentParser(description='QCS parameters')
    parser.add_argument('-l', '--logLevel', help='Logging level sets the base level of what is output. Defaults to warning and above',
      choices=[
     'debug', 'info', 'warning'],
      default='warning',
      type=(str.lower))
    args = parser.parse_args(argstring)
    setUpLogging(args.logLevel)
    printText('\n################################################################################')
    printText('                                   Welcome to                                 ')
    printText("                               Quarch Technology's                            ")
    printText('                             Quarch Compliance Suite                          ')
    printText('                            Quarchpy Version : ' + pkg_resources.get_distribution('quarchpy').version)
    printText('################################################################################\n')
    if isUserAdmin() is False:
        printText('Quarch Compliance Suite must be run from an elevated command prompt.')
        printText('Please restart with administrator privileges')
        sys.exit()
    ActivateRemoteServer()


if __name__ == '__main__':
    main(sys.argv[1:])