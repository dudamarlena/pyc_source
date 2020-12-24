# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Benutzer\haschtl\Dokumente\GIT\kellerlogger\RTOC\RTLogger\RT_datalocal.py
# Compiled at: 2019-05-13 12:25:14
# Size of source mod 2**32: 24003 bytes
import time
from collections import deque
import sys, logging as log, hashlib
log.basicConfig(level=(log.INFO))
logging = log.getLogger(__name__)
try:
    from PyQt5.QtCore import QCoreApplication
    translate = QCoreApplication.translate
except ImportError:

    def translate(id, text):
        return text


try:
    from .telegramBot import telegramBot
except ImportError:
    logging.warning('Telegram for python not installed. Please install with "pip3 install python-telegram-bot"')
    telegramBot = None

class RT_datalocal:

    def __init__(self, logger=None):
        self.logger = logger
        self.status = 'connected'
        self._signals = []
        self._signalNames = []
        self._signalUnits = []
        self._signalIDs = []
        self._events = []
        self.callback = None
        self.newSignalCallback = None
        self.newEventCallback = None
        self.handleScriptCallback = None
        self.recordingLengthChangedCallback = None

    def connect_callbacks(self):
        self.callback = self.logger.callback
        self.newSignalCallback = self.logger.newSignalCallback
        self.newEventCallback = self.logger.newEventCallback
        self.handleScriptCallback = self.logger.handleScriptCallback
        self.recordingLengthChangedCallback = self.logger.recordingLengthChangedCallback

    def clear(self, dev=True, sig=True, ev=True):
        if dev == True or sig == True:
            self._signals = []
            self._signalNames = []
            self._signalUnits = []
            self._signalIDs = []
            self.clearSignals()
        if ev == True:
            self._events = []

    def devices(self):
        return self._RT_datalocal__devicenames

    def getNewID(self):
        newID = 0
        while newID in self._signalIDs or newID == 0:
            newID += 1

        return newID

    def events(self):
        sorted_events = []
        if len(self._events) > 0:
            for idx, sig in enumerate(self._events):
                signame, devname = self.signalNames()[idx]
                if len(sig) > 0:
                    for idx, ev in enumerate(sig[0]):
                        event = [
                         sig[0][idx], sig[1][idx], sig[2][idx],
                         sig[3][idx], sig[4][idx], signame, devname, sig[5][idx]]
                        sorted_events.append(event)

        return sorted_events

    def signals(self):
        return self._signals

    def signalNames(self):
        return self._signalNames

    def signalIDs(self):
        return self._signalIDs

    def signalUnits(self):
        print(self._signalUnits)
        return self._signalUnits

    def clearSignals(self, newLength=None):
        if newLength is None:
            newLength = self.logger.config['global']['recordLength']
        else:
            self.logger.config['global']['recordLength'] = newLength
        self._signals = [[deque([], newLength), deque([], newLength)] for _ in range(len(self._signalNames))]
        self._signalUnits = ['' for _ in range(len(self._signalNames))]
        self._events = [[deque([], newLength), deque([], newLength), deque([], newLength), deque([], newLength), deque([], newLength), deque([], newLength)] for _ in range(len(self._signalNames))]

    def resizeSignals(self, newLength=None):
        if newLength is None:
            newLength = self.logger.config['global']['recordLength']
        else:
            self.logger.config['global']['recordLength'] = newLength
        self._signals = [[deque(list(self._signals[idx][0]), newLength), deque(list(self._signals[idx][1]), newLength)] for idx in range(len(self._signalNames))]
        self._events = [[deque(list(self._events[idx][0]), newLength), deque(list(self._events[idx][1]), newLength), deque(list(self._events[idx][2]), newLength), deque(list(self._events[idx][3]), newLength), deque(list(self._events[idx][4]), newLength), deque(list(self._events[idx][5]), newLength)] for idx in range(len(self._signalNames))]

    def removeSignal(self, id):
        idx = self._signalIDs.index(id)
        if idx != -1:
            self._signalNames.pop(idx)
            self._signalIDs.pop(idx)
            self._signals.pop(idx)
            self._signalUnits.pop(idx)
        return idx

    def __addNewSignal(self, dataY, dataunit, devicename, dataname, dataX=None, createCallback=True):
        if dataY is not None:
            logging.info('LOGGER: Adding signal: ' + devicename + ', ' + dataname)
            newLength = self.logger.config['global']['recordLength']
            self._signalNames += [[devicename, dataname]]
            newID = self.getNewID()
            self._signalIDs.append(newID)
            self._signals += [[deque([], newLength), deque([], newLength)]]
            self._events += [
             [deque([], newLength), deque([], newLength),
              deque([], newLength), deque([], newLength), deque([], newLength), deque([], newLength)]]
            self._signalUnits += ['']
            if self.newSignalCallback:
                self.newSignalCallback(newID, devicename, dataname, dataunit)
            self.addNewData(float(dataY), dataunit, devicename, dataname, dataX, createCallback)

    def addNewData(self, dataY, dataunit, devicename, dataname, dataX=None, createCallback=True):
        if dataY is not None:
            self._RT_datalocal__latestSignal = [
             devicename, dataname]
            idx = self._signalNames.index([devicename, dataname])
            if len(self._signals[idx][1]) + 1 >= self.logger.config['global']['recordLength']:
                if self.logger.config['backup']['autoIfFull']:
                    self.logger.backupJSON()
            if dataX is None:
                self._signals[idx][0].append(time.time())
            else:
                self._signals[idx][0].append(dataX)
            self._signals[idx][1].append(float(dataY))
            self._signalUnits[idx] = dataunit
            if self.handleScriptCallback:
                self.handleScriptCallback(devicename, dataname)
            if self.callback:
                if createCallback:
                    self.callback(devicename, dataname)
            if self.logger.config['global']['globalEventsActivated']:
                self.logger.performGlobalEvents(dataY, dataunit, devicename, dataname, dataX)

    def __plotNewSignal(self, x, y, dataunit, devicename, dataname, createCallback=False, autoResize=False):
        logging.info('LOGGER: Adding signalplot: ' + devicename + ', ' + dataname)
        newLength = self.logger.config['global']['recordLength']
        self._signalNames += [[devicename, dataname]]
        self._events += [
         [deque([], newLength), deque([], newLength),
          deque([], newLength), deque([], newLength), deque([], newLength), deque([], newLength)]]
        self._signalIDs.append(self.getNewID())
        self._signals += [[deque([], newLength), deque([], newLength)]]
        self._signalUnits += ['']
        if autoResize and len(y) > self.logger.config['global']['recordLength']:
            self.resizeSignals(len(y))
            logging.warning('Your recording length was updated due to plotting a bigger signal')
            if self.recordingLengthChangedCallback:
                self.recordingLengthChangedCallback(devicename, dataname, len(y))
        self.plotNewData(x, y, dataunit, devicename, dataname, createCallback, 'off', autoResize)
        if self.newSignalCallback:
            self.newSignalCallback(self._signalIDs[(-1)], devicename, dataname, dataunit)

    def plotNewData(self, x, y, dataunit, devicename, dataname, createCallback=False, hold='off', autoResize=False):
        self._RT_datalocal__latestSignal = [
         devicename, dataname]
        idx = self._signalNames.index([devicename, dataname])
        if autoResize:
            newsize = None
            if hold == 'on':
                if len(y) + len(self._signals[idx][1]) > self.logger.config['global']['recordLength']:
                    newsize = len(y) + len(self._signals[idx][1])
            else:
                if len(y) > self.logger.config['global']['recordLength']:
                    newsize = len(y)
                if newsize:
                    self.resizeSignals(newsize)
                    logging.warning('Your recording length was updated due to plotting a bigger signal')
                    if self.recordingLengthChangedCallback:
                        self.recordingLengthChangedCallback(devicename, dataname, newsize)
        else:
            if hold == 'on':
                self._signals[idx][0] += x
                self._signals[idx][1] += y
            else:
                if hold == 'mergeX':
                    for val_idx, value in enumerate(x):
                        if value not in self._signals[idx][0]:
                            if autoResize:
                                if len(self._signals[idx][0]) >= self.logger.config['global']['recordLength']:
                                    self.resizeSignals(len(self._signals[idx][0]) + 50)
                            self._signals[idx][0].append(x[val_idx])
                            self._signals[idx][1].append(y[val_idx])

                else:
                    if hold == 'mergeY':
                        for val_idx, value in enumerate(y):
                            if value not in self._signals[idx][1]:
                                if autoResize:
                                    if len(self._signals[idx][0]) >= self.logger.config['global']['recordLength']:
                                        self.resizeSignals(len(self._signals[idx][0]) + 50)
                                self._signals[idx][0].append(x[val_idx])
                                self._signals[idx][1].append(y[val_idx])

                    else:
                        self._signals[idx][0].clear()
                        self._signals[idx][1].clear()
                        self._signals[idx][0] = deque(x, self.logger.config['global']['recordLength'])
                        self._signals[idx][1] = deque(y, self.logger.config['global']['recordLength'])
                if type(dataunit) == str:
                    self._signalUnits[idx] = dataunit
                else:
                    if type(dataunit) == list:
                        self._signalUnits[idx] = dataunit[(-1)]
                    else:
                        logging.warning('no unit specified')
                        self._signalUnits[idx] = ''
        if self.handleScriptCallback:
            self.handleScriptCallback(devicename, dataname)
        if self.callback:
            if createCallback:
                self.callback(devicename, dataname)

    def printSignals(self):
        for idx, signal in enumerate(self._signals):
            logging.info('Device: ' + self._signalNames[idx][0] + ', Signal: ' + self._signalNames[idx][1])
            logging.info('Timebase:')
            for data in self._signals[idx][0]:
                sys.stdout.write(str(round(data, 1)) + '\t')

            logging.info('\nData:')
            for data in self._signals[idx][1]:
                sys.stdout.write(str(round(data, 1)) + '\t\t')

            logging.info('\nUnit: ')
            sys.stdout.write(str(self._signalUnits[idx]) + '\t\t')
            logging.info('')

    def getSignalId(self, devicename, dataname):
        curridx = -1
        for idx, value in enumerate(self._signalNames):
            if value[0] == devicename:
                if value[1] == dataname:
                    curridx = idx
                    break

        if curridx != -1:
            return self._signalIDs[curridx]
        else:
            return -1

    def addDataCallback(self, *args, **kwargs):
        datasY = kwargs.get('y', [])
        datanames = kwargs.get('snames', [''])
        devicename = kwargs.get('dname', 'noDevice')
        units = kwargs.get('unit', '')
        datasX = kwargs.get('x', [None])
        createCallback = kwargs.get('c', True)
        for idx, arg in enumerate(args):
            if idx == 0:
                datasY = arg
            else:
                if idx == 1:
                    datanames = arg
                else:
                    if idx == 2:
                        devicename = arg
                    if idx == 3:
                        units = arg
                if idx == 4:
                    datasX = arg
            if idx == 5:
                createCallback = arg

        if type(units) == str:
            units = [
             units]
        if type(datanames) == str:
            datanames = [
             datanames]
        if type(datasY) == float or type(datasY) == int:
            datasY = [
             datasY]
        if type(datasX) == float or type(datasX) == int:
            datasX = [
             datasX]
        if type(datasY) == list:
            if type(datanames) == list:
                if datasX == [None]:
                    datasX = [
                     None] * len(datasY)
                else:
                    if units == [''] or units is None or type(units) == str:
                        units = [
                         ''] * len(datasY)
                    if len(units) < len(datasY):
                        units += [''] * (len(datasY) - len(units))
                    elif len(units) > len(datasY):
                        units = units[0:len(datasY)]
                if len(datanames) < len(datasY):
                    datanames += ['Unnamed'] * (len(datasY) - len(datanames))
                for idx, data in enumerate(datasY):
                    if [
                     devicename, datanames[idx]] in self._signalNames:
                        self.addNewData(datasY[idx], units[idx], devicename, datanames[idx], datasX[idx], createCallback)
                    else:
                        self._RT_datalocal__addNewSignal(datasY[idx], units[idx], devicename, datanames[idx], datasX[idx], createCallback)

        if type(datasY) == str:
            self.addNewEvent(datasY)

    def addData(self, data=0, *args, **kwargs):
        dataname = kwargs.get('sname', 'noName')
        devicename = kwargs.get('dname', 'noDevice')
        dataunit = kwargs.get('unit', '')
        createCallback = kwargs.get('c', False)
        for idx, arg in enumerate(args):
            if idx == 0:
                dataname = arg
            else:
                if idx == 1:
                    devicename = arg
                if idx == 2:
                    dataunit = arg
            if idx == 3:
                createCallback = arg

        if type(data) == list:
            if len(data) == 2:
                if [
                 devicename, dataname] in self._signalNames:
                    self.addNewData(float(data[1]), dataunit, devicename, dataname, float(data[0]), createCallback)
                else:
                    self._RT_datalocal__addNewSignal(float(data[1]), dataunit, devicename, dataname, float(data[0]), createCallback)
            else:
                logging.error('Wrong data size')
        elif type(data) == int or type(data) == float:
            if [
             devicename, dataname] in self._signalNames:
                self.addNewData(data, dataunit, devicename, dataname, None, createCallback)
            else:
                self._RT_datalocal__addNewSignal(data, dataunit, devicename, dataname, None, createCallback)

    def plot(self, x=[], y=[], *args, **kwargs):
        dataname = kwargs.get('sname', 'noName')
        devicename = kwargs.get('dname', 'noDevice')
        dataunit = kwargs.get('unit', '')
        hold = kwargs.get('hold', 'off')
        autoResize = kwargs.get('autoResize', False)
        createCallback = kwargs.get('c', False)
        for idx, arg in enumerate(args):
            if idx == 0:
                dataname = arg
            else:
                if idx == 1:
                    devicename = arg
                if idx == 2:
                    dataunit = arg
            if idx == 3:
                createCallback = arg

        if y == []:
            y = x
            x = list(range(len(x)))
        else:
            if len(x) == len(y):
                if [
                 devicename, dataname] in self._signalNames:
                    self.plotNewData(x, y, dataunit, devicename, dataname, createCallback, hold, autoResize)
                else:
                    self._RT_datalocal__plotNewSignal(x, y, dataunit, devicename, dataname, createCallback, autoResize)
            else:
                logging.error('Plotting aborted. len(x)!=len(y)')

    def getSignal(self, id, sigLen=None):
        if id in self._signalIDs:
            idx = self._signalIDs.index(id)
            return self._signals[idx]
        else:
            return [[], []]

    def getSignalUnits(self, id):
        if id in self._signalIDs:
            idx = self._signalIDs.index(id)
            return str(self._signalUnits[idx])
        else:
            return ''

    def getSignalNames(self, id):
        if id in self._signalIDs:
            idx = self._signalIDs.index(id)
            return self._signalNames[idx]
        else:
            return [
             [
              ''], ['']]

    def getSignalSize(self):
        maxsize = len(self._signals) * (2 * (self.logger.config['global']['recordLength'] * 8 + 64) + 16)
        outerlayer = sys.getsizeof(self._signals)
        innerlayer = 0
        for sig in self._signals:
            innerlayer += sys.getsizeof(sig)
            innerlayer += sys.getsizeof(sig[0]) * 2
            innerlayer += sys.getsizeof(list(sig[0])) * 2

        size = outerlayer + innerlayer
        return (size, maxsize)

    def getLatest(self, force=None):
        ans = {}
        ans['latest'] = {}
        for dev in self.signalNames():
            sig = self.getSignal(self.getSignalId(dev[0], dev[1]))
            if len(sig[0]) > 0:
                ans['latest']['.'.join(dev)] = [
                 sig[0][(-1)], sig[1][(-1)]]

        return ans

    def addNewEvent(self, *args, **kwargs):
        strung = kwargs.get('text', '')
        dataname = kwargs.get('sname', 'noName')
        devicename = kwargs.get('dname', 'noDevice')
        value = kwargs.get('value', None)
        id = kwargs.get('id', hashlib.sha1(strung.encode()).hexdigest())
        x = kwargs.get('x', None)
        priority = kwargs.get('priority', 0)
        for idx, arg in enumerate(args):
            if idx == 0:
                strung = arg
            else:
                if idx == 1:
                    dataname = arg
                if idx == 2:
                    devicename = arg
                if idx == 3:
                    x = arg
            if idx == 4:
                priority = arg

        logging.info('New Event: ' + str(devicename) + '.' + str(dataname) + ': ' + str(strung) + ' (ID: ' + str(id) + ', Value: ' + str(value))
        if priority not in (0, 1, 2):
            priority = 0
        else:
            callback = False
            if [devicename, dataname] not in self._signalNames:
                self._signalNames += [[devicename, dataname]]
                newLength = self.logger.config['global']['recordLength']
                self._signals += [[deque([], newLength), deque([], newLength)]]
                newID = self.getNewID()
                self._signalIDs.append(newID)
                self._events += [
                 [deque([], newLength),
                  deque([], newLength), deque([], newLength), deque([], newLength), deque([], newLength)]]
                self._signalUnits += ['']
                callback = True
            idx = self._signalNames.index([devicename, dataname])
            if x is None:
                self._events[idx][0].append(time.time())
                x = time.time()
            else:
                self._events[idx][0].append(float(x))
        self._events[idx][1].append(strung)
        self._events[idx][2].append(priority)
        self._events[idx][3].append(value)
        self._events[idx][4].append(id)
        self._events[idx][5].append(idx * len(self._events[idx][0]))
        if self.newEventCallback:
            self.newEventCallback(x, strung, devicename, dataname, priority, value, id, idx)
        if self.newSignalCallback:
            if callback:
                if devicename != 'RTOC':
                    self.newSignalCallback(newID, devicename, dataname, '')
        if self.logger.config['telegram']['active']:
            if telegramBot is not None:
                if self.logger is not None:
                    if self.logger.telegramBot is not None:
                        self.logger.telegramBot.sendEvent(strung, devicename, dataname, priority)
        if self.logger.config['global']['globalActionsActivated']:
            self.logger.performGlobalActions(id, value)

    def getEvents(self, id):
        if id in self._signalIDs:
            idx = self._signalIDs.index(id)
            return self._events[idx]
        else:
            return []

    def getEventList(self):
        return self._events

    def renameSignal(self, id, signame):
        idx = self._signalIDs.index(id)
        if idx != -1:
            self._signalNames[idx][1] = signame

    def close(self):
        pass

    def start(self):
        pass

    def stop(self):
        pass