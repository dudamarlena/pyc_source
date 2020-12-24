# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\sboon\AppData\Local\Temp\pip-install-ptdbtr91\quarchpy\quarchpy\connection_specific\connection_QIS.py
# Compiled at: 2020-03-25 05:10:07
# Size of source mod 2**32: 45475 bytes
import socket, re, time, sys, os, datetime, select, threading, math
from quarchpy.user_interface import *

class QisInterface:

    def __init__(self, host='127.0.0.1', port=9722, connectionMessage=True):
        self.host = host
        self.port = port
        self.maxRxBytes = 4096
        self.sock = None
        self.StreamRunSentSemaphore = threading.Semaphore()
        self.sockSemaphore = threading.Semaphore()
        self.stopFlagList = []
        self.listSemaphore = threading.Semaphore()
        self.deviceList = []
        self.deviceDict = {}
        self.dictSemaphore = threading.Semaphore()
        self.connect(connectionMessage=connectionMessage)
        self.stripesEvent = threading.Event()
        self.streamSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.streamSock.connect((self.host, self.port))
        self.streamSock.settimeout(5)
        self.pythonVersion = sys.version[0]
        if self.pythonVersion == '3':
            temp = '>'
            self.cursor = temp.encode()
        else:
            self.cursor = '>'
        try:
            welcomeString = self.streamSock.recv(self.maxRxBytes).rstrip()
        except:
            raise

    def connect(self, connectionMessage=True):
        try:
            self.deviceDictSetup('QIS')
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.host, self.port))
            self.sock.settimeout(5)
            try:
                welcomeString = self.sock.recv(self.maxRxBytes).rstrip()
                welcomeString = 'Connected@' + str(self.host) + ':' + str(self.port) + ' ' + '\n    ' + str(welcomeString)
                self.deviceDict['QIS'][0:3] = [False, 'Connected', welcomeString]
                return welcomeString
            except:
                print('')
                print('No welcome received. Unable to connect to Quarch backend on specified host and port (' + self.host + ':' + str(self.port) + ')')
                print('Is backend running and host accessible?')
                print('')
                self.deviceDict['QIS'][0:3] = [True, 'Disconnected', 'Unable to connect to QIS']
                raise

        except:
            self.deviceDictSetup('QIS')
            if connectionMessage:
                print('')
                print('Unable to connect to Quarch backend on specified host and port (' + self.host + ':' + str(self.port) + ').')
                print('Is backend running and host accessible?')
                print('')
            self.deviceDict['QIS'][0:3] = [
             True, 'Disconnected', 'Unable to connect to QIS']
            raise

    def disconnect(self):
        res = 'Disconnecting from backend'
        try:
            self.sock.shutdown(socket.SHUT_RDWR)
            self.sock.close()
            self.deviceDict['QIS'][0:3] = [False, 'Disconnected', 'Successfully disconnected from QIS']
        except:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            message = 'Unable to end connection. ' + self.host + ':' + str(self.port) + ' \r\n' + str(exc_type) + ' ' + str(fname) + ' ' + str(exc_tb.tb_lineno)
            self.deviceDict['QIS'][0:3] = [True, 'Connected', message]
            raise

        return res

    def getCanStream(self, module):
        streamableDevices = [
         'qtl1824', 'qtl1847', 'qtl1944', 'qtl1995', 'qtl1999']
        for item in streamableDevices:
            if str(item) in module:
                return True

        return False

    def startStream(self, module, fileName, fileMaxMB, streamName, streamAverage, releaseOnData, separator):
        if not self.getCanStream(module):
            print('This device does not support streaming.')
            return
        self.StreamRunSentSemaphore.acquire()
        self.deviceDictSetup('QIS')
        i = self.deviceMulti(module)
        self.stopFlagList[i] = True
        self.stripesEvent.set()
        t1 = threading.Thread(target=(self.startStreamThread), name=module, args=(module, fileName, fileMaxMB, streamName, streamAverage, releaseOnData, separator))
        t1.start()
        while self.stripesEvent.is_set():
            pass

    def stopStream(self, module, blocking=True):
        try:
            i = self.deviceMulti(module)
            self.stopFlagList[i] = False
            if blocking:
                running = True
                while running:
                    threadNameList = []
                    for t1 in threading.enumerate():
                        threadNameList.append(t1.name)

                    if module in threadNameList:
                        time.sleep(0.5)
                    else:
                        running = False

            time.sleep(0.1)
        except:
            print('!!!!!!!!!!!!!!!!!!  stopStream exception !!!!!!!!!!!!!!!!!!')
            raise

    def startStreamThread(self, module, fileName, fileMaxMB, streamName, streamAverage, releaseOnData, separator):
        try:
            stripes = [
             'Empty Header']
            streamRes = self.sendAndReceiveCmd((self.streamSock), 'rec stream', device=module, betweenCommandDelay=0)
            if 'rec stream : OK' in streamRes:
                if releaseOnData == False:
                    self.StreamRunSentSemaphore.release()
                    self.stripesEvent.clear()
                self.deviceDict[module][0:3] = [
                 False, 'Running', 'Stream Running']
            else:
                self.StreamRunSentSemaphore.release()
                self.deviceDict[module][0:3] = [True, 'Stopped', module + " couldn't start because " + streamRes]
                return
                if fileName is not None:
                    averaging = self.streamHeaderAverage(device=module, sock=(self.streamSock))
                    count = 0
                    maxTries = 10
                    while 'Header Not Available' in averaging:
                        averaging = self.streamHeaderAverage(device=module, sock=(self.streamSock))
                        time.sleep(0.1)
                        count += 1
                        if count > maxTries:
                            self.deviceDict[module][0:3] = [
                             True, 'Stopped', 'Header not available']
                            exit()

                    version = self.streamHeaderVersion(device=module, sock=(self.streamSock))
                    sampleRate = 250000
                    stripeRate = sampleRate / float(averaging)
                    with open(fileName, 'w') as (f):
                        timeStampHeader = datetime.datetime.now().strftime('%H:%M:%S:%f %d/%m/%y')
                        formatHeader = self.streamHeaderFormat(device=module, sock=(self.streamSock))
                        f.write(str(streamName) + ', ' + str(version) + ', ' + str(module) + ', ' + str(timeStampHeader) + ', avg=' + str(averaging) + ' samples per stripe, stripeRate=' + str(stripeRate) + ' stripes per second\n')
                        formatHeader = formatHeader.replace(', ', separator)
                        f.write(formatHeader + '\n')
                numStripesPerRead = 4096
                maxFileExceeded = False
                openAttempts = 0
                leftover = 0
                remainingStripes = []
                streamOverrun = False
                if streamAverage != None:
                    streamAverage = self.convertStreamAverage(streamAverage)
                    stripesPerAverage = float(streamAverage) / (float(averaging) * 4e-06)
                isRun = True
                while isRun:
                    try:
                        with open(fileName, 'ab') as (f):
                            i = self.deviceMulti(module)
                            while self.stopFlagList[i]:
                                if not streamOverrun:
                                    streamOverrun, removeChar, newStripes = self.streamGetStripesText(self.streamSock, module, numStripesPerRead)
                                    newStripes = newStripes.replace(b' ', str.encode(separator))
                                    if streamOverrun:
                                        self.deviceDict[module][0:3] = [
                                         True, 'Stopped', 'Device buffer overrun']
                                    if removeChar == -6 and len(newStripes) == 6:
                                        isEmpty = False
                                    else:
                                        isEmpty = True
                                    if isEmpty:
                                        statInfo = os.stat(fileName)
                                        fileMB = statInfo.st_size / 1048576
                                        try:
                                            int(fileMaxMB)
                                        except:
                                            continue

                                        if int(fileMB) < int(fileMaxMB):
                                            if releaseOnData == True:
                                                self.StreamRunSentSemaphore.release()
                                                self.stripesEvent.clear()
                                                releaseOnData = False
                                            elif streamAverage != None:
                                                leftover, remainingStripes = self.averageStripes(leftover, stripesPerAverage, newStripes[:removeChar], f, remainingStripes)
                                            else:
                                                f.write(newStripes[:removeChar])
                                        else:
                                            maxFileExceeded = True
                                            maxFileStatus = self.streamBufferStatus(device=module, sock=(self.streamSock))
                                            f.write('Warning: Max file size exceeded before end of stream.\n')
                                            f.write('Unrecorded stripes in buffer when file full: ' + maxFileStatus + '.')
                                            self.deviceDict[module][0:3] = [True, 'Stopped', 'User defined max filesize reached']
                                            break
                                else:
                                    time.sleep(0.1)
                                    streamStatus = self.streamRunningStatus(device=module, sock=(self.streamSock))
                                    if streamOverrun:
                                        break
                                    elif 'Stopped' in streamStatus:
                                        self.deviceDict[module][0:3] = [
                                         True, 'Stopped', 'User halted stream']
                                        break

                            self.sendAndReceiveCmd((self.streamSock), 'rec stop', device=module, betweenCommandDelay=0)
                            if not streamOverrun:
                                if not maxFileExceeded:
                                    self.deviceDict[module][0:3] = [
                                     False, 'Stopped', 'Stream stopped - emptying buffer']
                            streamOverrun, removeChar, newStripes = maxFileExceeded or self.streamGetStripesText(self.streamSock, module, numStripesPerRead)
                            isEmpty = True
                            if removeChar == -6:
                                if len(newStripes) == 6:
                                    isEmpty = False
                            while isEmpty:
                                statInfo = os.stat(fileName)
                                fileMB = statInfo.st_size / 1048576
                                try:
                                    int(fileMaxMB)
                                except:
                                    continue

                                if int(fileMB) < int(fileMaxMB):
                                    if streamAverage != None:
                                        leftover, remainingStripes = self.averageStripes(leftover, stripesPerAverage, newStripes[:removeChar], f, remainingStripes)
                                    else:
                                        newStripes = newStripes.replace(b' ', str.encode(separator))
                                        f.write(newStripes[:removeChar])
                                else:
                                    if not maxFileExceeded:
                                        maxFileStatus = self.streamBufferStatus(device=module, sock=(self.streamSock))
                                        maxFileExceeded = True
                                        self.deviceDict[module][0:3] = [True, 'Stopped', 'User defined max filesize reached']
                                    break
                                streamOverrun, removeChar, newStripes = self.streamGetStripesText((self.streamSock), module, numStripesPerRead, skipStatusCheck=True)
                                if removeChar == -6 and len(newStripes) == 6:
                                    isEmpty = False

                            if maxFileExceeded:
                                f.write('Warning: Max file size exceeded before end of stream.\n')
                                f.write('Unrecorded stripes in buffer when file full: ' + maxFileStatus + '.')
                                print('Warning: Max file size exceeded. Some data has not been saved to file: ' + maxFileStatus + '.')
                            if streamOverrun:
                                self.deviceDict[module][0:3] = [
                                 True, 'Stopped', 'Device buffer overrun - QIS buffer empty']
                            else:
                                if not maxFileExceeded:
                                    self.deviceDict[module][0:3] = [
                                     False, 'Stopped', 'Stream stopped']
                                time.sleep(0.2)
                            isRun = False
                    except IOError as err:
                        try:
                            time.sleep(0.5)
                            openAttempts += 1
                            if openAttempts > 4:
                                print('\n\n!!!!!!!!!!!!!!!!!!!! Too many IO Errors in QisInterface !!!!!!!!!!!!!!!!!!!!\n\n')
                                raise
                        finally:
                            err = None
                            del err

        except:
            raise

    def sendCmd(self, device='', cmd='$help', sock=None, readUntilCursor=True, betweenCommandDelay=0.0, expectedResponse=True):
        if sock == None:
            sock = self.sock
        if not device == '':
            self.deviceDictSetup(device)
        res = self.sendAndReceiveText(sock, cmd, device, readUntilCursor)
        if betweenCommandDelay > 0:
            time.sleep(betweenCommandDelay)
        if res[-1:] == self.cursor:
            res = res[:-3]
        return res.decode()

    def sendAndReceiveCmd(self, sock=None, cmd='$help', device='', readUntilCursor=True, betweenCommandDelay=0.0):
        if sock == None:
            sock = self.sock
        else:
            if not device == '':
                self.deviceDictSetup(device)
            if self.pythonVersion == '3':
                res = self.sendAndReceiveText(sock, cmd, device, readUntilCursor).decode()
            else:
                res = self.sendAndReceiveText(sock, cmd, device, readUntilCursor)
        if betweenCommandDelay > 0:
            time.sleep(betweenCommandDelay)
        if res[-1:] == '>':
            res = res[:-3]
        return cmd + ' : ' + res

    def sendAndReceiveText(self, sock, sentText='$help', device='', readUntilCursor=True):
        self.sockSemaphore.acquire()
        try:
            try:
                self.sendText(sock, sentText, device)
                if self.pythonVersion == '3':
                    res = bytearray()
                    res.extend(self.rxBytes(sock))
                    if res[0] == self.cursor:
                        print('Only Returned Cursor!!!!!')
                    cba = 'Create Socket Fail'
                    if cba.encode() == res[0]:
                        print(res[0].decode())
                    cba = 'Connection Timeout'
                    if cba.encode() == res[0]:
                        print(res[0].decode())
                    if readUntilCursor:
                        maxReads = 1000
                        count = 1
                        while res[-1:] != self.cursor:
                            res.extend(self.rxBytes(sock))
                            count += 1
                            if count >= maxReads:
                                res = ' Count = Error: max reads exceeded before cursor returned\r\n'
                                print(res)

                    return res
                res = self.rxBytes(sock)
                if res == self.cursor:
                    res = self.rxBytes(sock)
                if 'Create Socket Fail' in res:
                    print(res)
                if 'Connection Timeout' in res:
                    print(res)
                if readUntilCursor:
                    maxReads = 1000
                    count = 1
                    while res[-1:] != self.cursor:
                        res += self.rxBytes(sock)
                        count += 1
                        if count >= maxReads:
                            res = ' Count = Error: max reads exceeded before cursor returned\r\n'
                            print(res)

                return res
            except:
                raise

        finally:
            self.sockSemaphore.release()

    def rxBytes(self, sock):
        maxExceptions = 10
        exceptions = 0
        maxReadRepeats = 50
        readRepeats = 0
        timeout_in_seconds = 10
        while 1:
            try:
                ready = select.select([sock], [], [], timeout_in_seconds)
                if ready[0]:
                    ret = sock.recv(self.maxRxBytes)
                    return ret
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((self.host, self.port))
                sock.settimeout(5)
                try:
                    welcomeString = self.sock.recv(self.maxRxBytes).rstrip()
                    welcomeString = 'Connected@' + self.host + ':' + str(self.port) + ' ' + '\n    ' + welcomeString
                    print('New Welcome:' + welcomeString)
                except:
                    print('tried and failed to get new welcome')
                    raise

                readRepeats = readRepeats + 1
                time.sleep(0.5)
            except:
                raise
                exceptions = exceptions + 1
                time.sleep(0.5)

            if readRepeats >= maxReadRepeats:
                print('Max read repeats exceeded - returning.')
                return 'No data received from QIS'
            if exceptions >= maxExceptions:
                print('Max exceptions exceeded - exiting')
                exit()

    def sendText(self, sock, message='$help', device=''):
        if device != '':
            specialTimeout = '%500000'
            message = device + specialTimeout + ' ' + message
        try:
            if self.pythonVersion == 2:
                sock.sendall(message + '\r\n')
            else:
                convM = message + '\r\n'
                sock.sendall(convM.encode('utf-8'))
            return 'Sent:' + message
        except:
            raise

    def getDeviceList(self, sock=None):
        if sock == None:
            sock = self.sock
        else:
            scanWait = 2
            if self.pythonVersion == '3':
                devString = self.sendAndReceiveText(sock, '$list').decode()
            else:
                devString = self.sendAndReceiveText(sock, '$list')
        devString = devString.replace('>', '')
        devString = devString.replace('\\d+\\) ', '')
        devString = devString.split('\r\n')
        devString = filter(None, devString)
        return devString

    def GetQisModuleSelection--- This code section failed: ---

 L. 529         0  BUILD_LIST_0          0 
                2  STORE_FAST               'deviceList'

 L. 530         4  LOAD_STR                 'Modules'
                6  BUILD_LIST_1          1 
                8  STORE_FAST               'tableHeaders'

 L. 531        10  LOAD_STR                 '1'
               12  STORE_FAST               'foundDevices'

 L. 532        14  LOAD_STR                 '2'
               16  STORE_FAST               'foundDevices2'

 L. 533        18  LOAD_CONST               2
               20  STORE_FAST               'scanWait'

 L. 534        22  LOAD_FAST                'self'
               24  LOAD_ATTR                pythonVersion
               26  LOAD_STR                 '3'
               28  COMPARE_OP               ==
               30  POP_JUMP_IF_FALSE   144  'to 144'

 L. 535        32  LOAD_FAST                'scan'
               34  POP_JUMP_IF_FALSE   124  'to 124'

 L. 536        36  LOAD_FAST                'self'
               38  LOAD_METHOD              sendAndReceiveText
               40  LOAD_FAST                'self'
               42  LOAD_ATTR                sock
               44  LOAD_STR                 '$scan'
               46  CALL_METHOD_2         2  '2 positional arguments'
               48  LOAD_ATTR                decode
               50  STORE_FAST               'devString'

 L. 537        52  LOAD_GLOBAL              time
               54  LOAD_METHOD              sleep
               56  LOAD_FAST                'scanWait'
               58  CALL_METHOD_1         1  '1 positional argument'
               60  POP_TOP          

 L. 538        62  SETUP_LOOP          142  'to 142'
               64  LOAD_FAST                'foundDevices'
               66  LOAD_FAST                'foundDevices2'
               68  COMPARE_OP               not-in
               70  POP_JUMP_IF_FALSE   120  'to 120'

 L. 539        72  LOAD_FAST                'self'
               74  LOAD_METHOD              sendAndReceiveText
               76  LOAD_FAST                'self'
               78  LOAD_ATTR                sock
               80  LOAD_STR                 '$list'
               82  CALL_METHOD_2         2  '2 positional arguments'
               84  LOAD_METHOD              decode
               86  CALL_METHOD_0         0  '0 positional arguments'
               88  STORE_FAST               'foundDevices'

 L. 540        90  LOAD_GLOBAL              time
               92  LOAD_METHOD              sleep
               94  LOAD_FAST                'scanWait'
               96  CALL_METHOD_1         1  '1 positional argument'
               98  POP_TOP          

 L. 541       100  LOAD_FAST                'self'
              102  LOAD_METHOD              sendAndReceiveText
              104  LOAD_FAST                'self'
              106  LOAD_ATTR                sock
              108  LOAD_STR                 '$list'
              110  CALL_METHOD_2         2  '2 positional arguments'
              112  LOAD_METHOD              decode
              114  CALL_METHOD_0         0  '0 positional arguments'
              116  STORE_FAST               'foundDevices2'
              118  JUMP_BACK            64  'to 64'
            120_0  COME_FROM            70  '70'
              120  POP_BLOCK        
              122  JUMP_ABSOLUTE       240  'to 240'
            124_0  COME_FROM            34  '34'

 L. 543       124  LOAD_FAST                'self'
              126  LOAD_METHOD              sendAndReceiveText
              128  LOAD_FAST                'self'
              130  LOAD_ATTR                sock
              132  LOAD_STR                 '$list'
              134  CALL_METHOD_2         2  '2 positional arguments'
              136  LOAD_METHOD              decode
              138  CALL_METHOD_0         0  '0 positional arguments'
              140  STORE_FAST               'foundDevices'
            142_0  COME_FROM_LOOP       62  '62'
              142  JUMP_FORWARD        240  'to 240'
            144_0  COME_FROM            30  '30'

 L. 546       144  LOAD_FAST                'scan'
              146  POP_JUMP_IF_FALSE   226  'to 226'

 L. 547       148  LOAD_FAST                'self'
              150  LOAD_METHOD              sendAndReceiveText
              152  LOAD_FAST                'self'
              154  LOAD_ATTR                sock
              156  LOAD_STR                 '$scan'
              158  CALL_METHOD_2         2  '2 positional arguments'
              160  STORE_FAST               'devString'

 L. 548       162  LOAD_GLOBAL              time
              164  LOAD_METHOD              sleep
              166  LOAD_FAST                'scanWait'
              168  CALL_METHOD_1         1  '1 positional argument'
              170  POP_TOP          

 L. 549       172  SETUP_LOOP          240  'to 240'
              174  LOAD_FAST                'foundDevices'
              176  LOAD_FAST                'foundDevices2'
              178  COMPARE_OP               not-in
              180  POP_JUMP_IF_FALSE   222  'to 222'

 L. 550       182  LOAD_FAST                'self'
              184  LOAD_METHOD              sendAndReceiveText
              186  LOAD_FAST                'self'
              188  LOAD_ATTR                sock
              190  LOAD_STR                 '$list'
              192  CALL_METHOD_2         2  '2 positional arguments'
              194  STORE_FAST               'foundDevices'

 L. 551       196  LOAD_GLOBAL              time
              198  LOAD_METHOD              sleep
              200  LOAD_FAST                'scanWait'
              202  CALL_METHOD_1         1  '1 positional argument'
              204  POP_TOP          

 L. 552       206  LOAD_FAST                'self'
              208  LOAD_METHOD              sendAndReceiveText
              210  LOAD_FAST                'self'
              212  LOAD_ATTR                sock
              214  LOAD_STR                 '$list'
              216  CALL_METHOD_2         2  '2 positional arguments'
              218  STORE_FAST               'foundDevices2'
              220  JUMP_BACK           174  'to 174'
            222_0  COME_FROM           180  '180'
              222  POP_BLOCK        
              224  JUMP_FORWARD        240  'to 240'
            226_0  COME_FROM           146  '146'

 L. 554       226  LOAD_FAST                'self'
              228  LOAD_METHOD              sendAndReceiveText
              230  LOAD_FAST                'self'
              232  LOAD_ATTR                sock
              234  LOAD_STR                 '$list'
              236  CALL_METHOD_2         2  '2 positional arguments'
              238  STORE_FAST               'foundDevices'
            240_0  COME_FROM           224  '224'
            240_1  COME_FROM_LOOP      172  '172'
            240_2  COME_FROM           142  '142'

 L. 556       240  LOAD_STR                 'no devices found'
              242  LOAD_FAST                'foundDevices'
              244  LOAD_METHOD              lower
              246  CALL_METHOD_0         0  '0 positional arguments'
              248  COMPARE_OP               in
          250_252  POP_JUMP_IF_FALSE   286  'to 286'

 L. 557       254  LOAD_STR                 '***No Devices Found***'
              256  BUILD_LIST_1          1 
              258  STORE_FAST               'selectionList'

 L. 558       260  LOAD_GLOBAL              listSelection
              262  LOAD_STR                 'Select a module'
              264  LOAD_STR                 'Select a module'
              266  LOAD_FAST                'selectionList'

 L. 559       268  LOAD_FAST                'additionalOptions'
              270  LOAD_CONST               True
              272  LOAD_FAST                'tableHeaders'
              274  LOAD_CONST               True
              276  LOAD_CONST               ('title', 'message', 'selectionList', 'additionalOptions', 'nice', 'tableHeaders', 'indexReq')
              278  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
              280  STORE_FAST               'myDeviceID'

 L. 560       282  LOAD_FAST                'myDeviceID'
              284  RETURN_VALUE     
            286_0  COME_FROM           250  '250'

 L. 562       286  LOAD_FAST                'foundDevices'
              288  LOAD_METHOD              replace
              290  LOAD_STR                 '>'
              292  LOAD_STR                 ''
              294  CALL_METHOD_2         2  '2 positional arguments'
              296  STORE_FAST               'foundDevices'

 L. 563       298  LOAD_FAST                'foundDevices'
              300  LOAD_METHOD              replace
              302  LOAD_STR                 '\\d+\\) '
              304  LOAD_STR                 ''
              306  CALL_METHOD_2         2  '2 positional arguments'
              308  STORE_FAST               'foundDevices'

 L. 565       310  LOAD_FAST                'foundDevices'
              312  LOAD_METHOD              split
              314  LOAD_STR                 '\r\n'
              316  CALL_METHOD_1         1  '1 positional argument'
              318  STORE_FAST               'foundDevices'

 L. 567       320  LOAD_GLOBAL              list
              322  CALL_FUNCTION_0       0  '0 positional arguments'
              324  STORE_FAST               'tempList'

 L. 568       326  SETUP_LOOP          402  'to 402'
              328  LOAD_FAST                'foundDevices'
              330  GET_ITER         
              332  FOR_ITER            400  'to 400'
              334  STORE_FAST               'item'

 L. 569       336  LOAD_FAST                'item'
              338  LOAD_CONST               None
              340  COMPARE_OP               is
          342_344  POP_JUMP_IF_TRUE    396  'to 396'
              346  LOAD_STR                 'rest'
              348  LOAD_FAST                'item'
              350  LOAD_METHOD              lower
              352  CALL_METHOD_0         0  '0 positional arguments'
              354  COMPARE_OP               in
          356_358  POP_JUMP_IF_TRUE    396  'to 396'
              360  LOAD_FAST                'item'
              362  LOAD_STR                 ''
              364  COMPARE_OP               ==
          366_368  POP_JUMP_IF_FALSE   372  'to 372'

 L. 570       370  CONTINUE            332  'to 332'
            372_0  COME_FROM           366  '366'

 L. 572       372  LOAD_FAST                'tempList'
              374  LOAD_METHOD              append
              376  LOAD_FAST                'item'
              378  LOAD_METHOD              split
              380  LOAD_STR                 ')'
              382  CALL_METHOD_1         1  '1 positional argument'
              384  LOAD_CONST               1
              386  BINARY_SUBSCR    
              388  LOAD_METHOD              strip
              390  CALL_METHOD_0         0  '0 positional arguments'
              392  CALL_METHOD_1         1  '1 positional argument'
              394  POP_TOP          
            396_0  COME_FROM           356  '356'
            396_1  COME_FROM           342  '342'
          396_398  JUMP_BACK           332  'to 332'
              400  POP_BLOCK        
            402_0  COME_FROM_LOOP      326  '326'

 L. 573       402  LOAD_FAST                'tempList'
              404  STORE_FAST               'foundDevices'

 L. 577       406  LOAD_FAST                'favouriteOnly'
          408_410  POP_JUMP_IF_FALSE   422  'to 422'

 L. 578       412  LOAD_FAST                'self'
              414  LOAD_METHOD              sortFavourite
              416  LOAD_FAST                'foundDevices'
              418  CALL_METHOD_1         1  '1 positional argument'
              420  STORE_FAST               'foundDevices'
            422_0  COME_FROM           408  '408'

 L. 580       422  LOAD_GLOBAL              listSelection
              424  LOAD_STR                 'Select a module'
              426  LOAD_STR                 'Select a module'
              428  LOAD_FAST                'foundDevices'

 L. 581       430  LOAD_FAST                'additionalOptions'
              432  LOAD_CONST               True
              434  LOAD_FAST                'tableHeaders'

 L. 582       436  LOAD_CONST               True
              438  LOAD_CONST               ('title', 'message', 'selectionList', 'additionalOptions', 'nice', 'tableHeaders', 'indexReq')
              440  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
              442  STORE_FAST               'myDeviceID'

 L. 584       444  LOAD_FAST                'myDeviceID'
              446  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM_LOOP' instruction at offset 142_0

    def sortFavourite(self, foundDevices):
        index = 0
        sortedFoundDevices = []
        conPref = ['USB', 'TCP', 'SERIAL', 'REST', 'TELNET']
        while len(sortedFoundDevices) != len(foundDevices):
            for device in foundDevices:
                if conPref[index] in device.upper():
                    sortedFoundDevices.append(device)

            index += 1

        foundDevices = sortedFoundDevices
        favConFoundDevices = []
        index = 0
        for device in sortedFoundDevices:
            if favConFoundDevices == [] or device.split('::')[1] not in str(favConFoundDevices):
                favConFoundDevices.append(device)

        foundDevices = favConFoundDevices
        return foundDevices

    def streamRunningStatus(self, device, sock=None):
        try:
            if sock == None:
                sock = self.sock
            else:
                index = 0
                if self.pythonVersion == '3':
                    streamStatus = self.sendAndReceiveText(sock, 'stream?', device).decode()
                else:
                    streamStatus = self.sendAndReceiveText(sock, 'stream?', device)
            streamStatus = streamStatus.split('\r\n')
            streamStatus[index] = re.sub(':', '', streamStatus[index])
            return streamStatus[index]
        except:
            raise

    def streamBufferStatus(self, device, sock=None):
        try:
            if sock == None:
                sock = self.sock
            else:
                index = 1
                if self.pythonVersion == '3':
                    streamStatus = self.sendAndReceiveText(sock, 'stream?', device).decode()
                else:
                    streamStatus = self.sendAndReceiveText(sock, 'stream?', device)
            streamStatus = streamStatus.split('\r\n')
            streamStatus[index] = re.sub('^Stripes Buffered: ', '', streamStatus[index])
            return streamStatus[index]
        except:
            raise

    def streamHeaderAverage(self, device, sock=None):
        try:
            if sock == None:
                sock = self.sock
            else:
                index = 2
                if self.pythonVersion == '3':
                    streamStatus = self.sendAndReceiveText(sock, sentText='stream text header', device=device).decode()
                else:
                    streamStatus = self.sendAndReceiveText(sock, sentText='stream text header', device=device)
            streamStatus = streamStatus.split('\r\n')
            if 'Header Not Available' in streamStatus[0]:
                dummy = streamStatus[0] + '. Check stream has been ran on device.'
                return dummy
            streamStatus[index] = re.sub('^Average: ', '', streamStatus[index])
            avg = streamStatus[index]
            avg = 2 ** int(avg)
            return '{}'.format(avg)
        except:
            print(device + ' Unable to get stream average.' + self.host + ':' + str(self.port))
            raise

    def streamHeaderVersion(self, device, sock=None):
        try:
            if sock == None:
                sock = self.sock
            else:
                index = 0
                if self.pythonVersion == '3':
                    streamStatus = self.sendAndReceiveText(sock, 'stream text header', device).decode()
                else:
                    streamStatus = self.sendAndReceiveText(sock, 'stream text header', device)
                streamStatus = streamStatus.split('\r\n')
                if 'Header Not Available' in streamStatus[0]:
                    str = streamStatus[0] + '. Check stream has been ran on device.'
                    print(str)
                    return str
                    version = re.sub('^Version: ', '', streamStatus[index])
                    if version == '3':
                        version = 'Original PPM'
                elif version == '4':
                    version = 'XLC PPM'
                else:
                    if version == '5':
                        version = 'HD PPM'
                    else:
                        version = 'Unknown stream version'
            return version
        except:
            print(device + ' Unable to get stream version.' + self.host + ':' + str(self.port))
            raise

    def streamHeaderFormat(self, device, sock=None):
        try:
            if sock == None:
                sock = self.sock
            else:
                index = 1
                if self.pythonVersion == '3':
                    streamStatus = self.sendAndReceiveText(sock, 'stream text header', device).decode()
                else:
                    streamStatus = self.sendAndReceiveText(sock, 'stream text header', device)
                streamStatus = streamStatus.split('\r\n')
                if 'Header Not Available' in streamStatus[0]:
                    str = streamStatus[0] + '. Check stream has been ran on device.'
                    print(str)
                    return str
                if self.pythonVersion == '3':
                    outputMode = self.sendAndReceiveText(sock, 'Config Output Mode?', device).decode()
                    powerMode = self.sendAndReceiveText(sock, 'stream mode power?', device).decode()
                else:
                    outputMode = self.sendAndReceiveText(sock, 'Config Output Mode?', device)
                    powerMode = self.sendAndReceiveText(sock, 'stream mode power?', device)
                format = int(re.sub('^Format: ', '', streamStatus[index]))
                b0 = 1
                b1 = 2
                b2 = 4
                b3 = 8
                formatHeader = 'StripeNum, Trig, '
                if format & b3:
                    if '3V3' in outputMode:
                        formatHeader = formatHeader + '3V3_V,'
                    else:
                        formatHeader = formatHeader + '5V_V,'
                if format & b2:
                    if '3V3' in outputMode:
                        formatHeader = formatHeader + ' 3V3_I,'
                    else:
                        formatHeader = formatHeader + ' 5V_I,'
            if format & b1:
                formatHeader = formatHeader + ' 12V_V,'
            if format & b0:
                formatHeader = formatHeader + ' 12V_I'
            if 'Enabled' in powerMode:
                if '3V3' in outputMode:
                    formatHeader = formatHeader + ' 3V3_P'
                else:
                    formatHeader = formatHeader + ' 5V_P'
                if format & b1 or format & b0:
                    formatHeader = formatHeader + ' 12V_P'
            return formatHeader
        except:
            print(device + ' Unable to get stream  format.' + self.host + ':' + '{}'.format(self.port))
            raise

    def streamGetStripesText(self, sock, device, numStripes=4096, skipStatusCheck=False):
        try:
            bufferStatus = False
            if skipStatusCheck == False:
                if self.pythonVersion == '3':
                    streamStatus = self.sendAndReceiveText(sock, 'stream?', device).decode()
                else:
                    streamStatus = self.sendAndReceiveText(sock, 'stream?', device)
            else:
                if not 'Overrun' in streamStatus:
                    if '8388608 of 8388608' in streamStatus:
                        bufferStatus = True
                else:
                    stripes = self.sendAndReceiveText(sock, 'stream text all', device, readUntilCursor=True)
                    if stripes[-1:] != self.cursor:
                        return 'Error no cursor returned.'
                        if self.pythonVersion == '3':
                            endOfFile = 'eof\r\n>'
                            genEndOfFile = endOfFile.encode()
                    else:
                        genEndOfFile = 'eof\r\n>'
                if stripes[-6:] == genEndOfFile:
                    removeChar = -6
                else:
                    removeChar = -1
            return (
             bufferStatus, removeChar, stripes)
        except:
            raise

    def avgStringFromPwr(self, avgPwrTwo):
        if avgPwrTwo == 0:
            return '0'
        else:
            if avgPwrTwo == 1:
                return '2'
            if avgPwrTwo > 1 and avgPwrTwo < 10:
                avg = 2 ** int(avgPwrTwo)
                return '{}'.format(avg)
        if avgPwrTwo == 10:
            return '1k'
        if avgPwrTwo == 11:
            return '2k'
        if avgPwrTwo == 12:
            return '4k'
        if avgPwrTwo == 13:
            return '8k'
        if avgPwrTwo == 14:
            return '16k'
        if avgPwrTwo == 15:
            return '32k'
        return 'Invalid Average Value'

    def averageStripes(self, leftover, streamAverage, newStripes, f, remainingStripes=[]):
        newString = str(newStripes)
        newList = []
        if remainingStripes == []:
            newList = newString.split('\r\n')
        else:
            newList = remainingStripes
            newList.extend(newString.split('\r\n'))
        numElements = newList[0].count(' ') + 1
        streamTotalAverage = leftover + streamAverage
        splitList = [] * numElements
        if len(newList) < streamTotalAverage:
            remainingStripes = newList[:-1]
            return (leftover, remainingStripes)
        runningAverage = [
         0] * (len(newList[0].split(' ')) - 2)
        j = 0
        z = 1
        for i in newList[:-1]:
            splitList = i.split(' ')
            splitNumbers = [int(x) for x in splitList[2:]]
            runningAverage = [sum(x) for x in zip(runningAverage, splitNumbers)]
            if z == math.floor(streamTotalAverage):
                finalAverage = splitList[0:2] + [str(round(x / streamAverage)) for x in runningAverage]
                for counter in xrange(len(finalAverage) - 1):
                    finalAverage[counter] = finalAverage[counter] + ' '

                if self.pythonVersion == '3':
                    finalAverage = finalAverage.encode
                for x in finalAverage:
                    f.write(x)

                f.write('\r\n')
                streamTotalAverage += streamAverage
                j += 1
            z += 1

        remainingStripes = newList[int(math.floor(j * streamAverage + leftover)):-1]
        leftover = (streamTotalAverage - streamAverage) % 1
        return (leftover, remainingStripes)

    def deviceMulti(self, device):
        if device in self.deviceList:
            return self.deviceList.index(device)
        self.listSemaphore.acquire()
        self.deviceList.append(device)
        self.stopFlagList.append(True)
        self.listSemaphore.release()
        return self.deviceList.index(device)

    def deviceDictSetup(self, module):
        if module in self.deviceDict.keys():
            return
        if module == 'QIS':
            self.dictSemaphore.acquire()
            self.deviceDict[module] = [False, 'Disconnected', 'No attempt to connect to QIS yet']
            self.dictSemaphore.release()
        else:
            self.dictSemaphore.acquire()
            self.deviceDict[module] = [False, 'Stopped', "User hasn't started stream"]
            self.dictSemaphore.release()

    def streamInterrupt(self):
        for key in self.deviceDict.keys():
            if self.deviceDict[key][0]:
                return True

        return False

    def interruptList(self):
        streamIssueList = []
        for key in self.deviceDict.keys():
            if self.deviceDict[key][0]:
                streamIssue = [
                 key]
                streamIssue.append(self.deviceDict[key][1])
                streamIssue.append(self.deviceDict[key][2])
                streamIssueList.append(streamIssue)

        return streamIssueList

    def waitStop(self):
        running = 1
        while running != 0:
            threadNameList = []
            for t1 in threading.enumerate():
                threadNameList.append(t1.name)

            running = 0
            for module in self.deviceList:
                if module in threadNameList:
                    running += 1
                    time.sleep(0.5)

            time.sleep(1)

    def convertStreamAverage(self, streamAveraging):
        returnValue = 32000
        if 'k' in streamAveraging:
            returnValue = streamAveraging.replace('k', '000')
        else:
            returnValue = streamAveraging
        return returnValue