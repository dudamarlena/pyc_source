# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Benutzer\haschtl\Dokumente\GIT\kellerlogger\RTOC\RTLogger\RT_data.py
# Compiled at: 2020-01-06 12:31:52
# Size of source mod 2**32: 95552 bytes
import time
from collections import deque
import sys, logging as log, hashlib
from threading import Timer, Lock
import os, traceback, csv, numpy as np, json, psutil, copy, gzip
try:
    import psycopg2
except Exception:
    print('WARNING: psycopg2 is not installed, database disabled')
    psycopg2 = None

from PyQt5.QtCore import QTimer
try:
    import xlsxwriter
except ImportError:
    xlsxwriter = None

log.basicConfig(level=(log.INFO))
logging = log.getLogger(__name__)
DEVICE_TABLE_NAME = 'devices'
SIGNAL_TABLE_NAME = 'signals'
EVENT_TABLE_NAME = 'events'
lock = Lock()
localLock = Lock()
localEventLock = Lock()

class _perpetualTimer:

    def __init__(self, t, hFunction, useqtimer=False):
        self._t = t
        self._useqtimer = useqtimer
        self._hFunction = hFunction
        if QTimer is not None:
            if self._useqtimer:
                self._thread = QTimer()
                self._thread.timeout.connect(self._handle_function)
                self._thread.setInterval(self._t * 1000)
                self._thread.setSingleShot(True)
        else:
            self._thread = Timer(self._t, self._handle_function)

    def _handle_function(self):
        try:
            self._hFunction()
        except Exception as error:
            logging.info(traceback.format_exc())
            logging.info(error)
            logging.info('Backup failed')

        if QTimer is not None:
            if self._useqtimer:
                self._thread = QTimer()
                self._thread.timeout.connect(self._handle_function)
                self._thread.setInterval(self._t * 1000)
                self._thread.setSingleShot(True)
        else:
            self._thread = Timer(self._t, self._handle_function)
        self._thread.start()

    def start(self):
        self._thread.start()

    def cancel(self):
        if QTimer is not None:
            if self._useqtimer:
                self._thread.stop()
        else:
            self._thread.cancel()


class RT_data:
    __doc__ = '\n    This class manages all devices, signals and events.\n\n    It also manages the postgresql integration.\n    '

    def __init__(self, logger=None):
        self.logger = logger
        self._devices = {}
        self._signals = {}
        self._events = {}
        self.status = 'not connected'
        self._callback = None
        self._newSignalCallback = None
        self._newSignalWebsocketCallback = None
        self._newEventCallback = None
        self._handleScriptCallback = None
        self._recordingLengthChangedCallback = None
        self.websocketEvent_callback = None
        self.websocketSignal_callback = None
        self._startTime = time.time()
        if logger is not None:
            self.config = logger.config
        else:
            userpath = os.path.expanduser('~/.RTOC')
            if os.path.exists(userpath + '/config.json'):
                try:
                    with open((userpath + '/config.json'), encoding='UTF-8') as (jsonfile):
                        self.config = json.load(jsonfile, encoding='UTF-8')
                except Exception as error:
                    logging.error('Error in Config-file: ' + userpath + '/config.json')
                    print(error)
                    return False

            else:
                logging.error('Could not find config file')
                return False
            self._backupThread = None
            self._connection = None
            self._cursor = None
            if self.logger is None:
                self.isGUI = False
                self.webserver = True
                ok = self._connect()
                dev, sig, ev = self._checkDatabases()
                self.clear(not dev, not sig, not ev, True)
                self.pullFromDatabase()
                self.start()
            else:
                self.isGUI = self.logger.isGUI
                self.webserver = False
                if self.logger.forceLocal or self.logger.config['postgresql']['active']:
                    ok = self._connect()
                    if ok:
                        if self.logger.config['backup']['loadOnOpen']:
                            dev, sig, ev = self._checkDatabases()
                            self.clear(not dev, not sig, not ev, True)
                            self.pullFromDatabase()
                    if ok:
                        dev, sig, ev = self._checkDatabases()
                        self.clear(not dev, not sig, not ev, True)
                        self.pullFromDatabase(True, True, True, False)
                    else:
                        logging.error('Checking database failed!')
                    if self.logger.config['backup']['active']:
                        self.start()
                elif self.logger.config['backup']['active']:
                    logging.warning('File backup is not implemented')

    def connect_callbacks(self):
        """
        This function is used to connect the callbacks for the GUI
        """
        self._callback = self.logger.callback
        self._newSignalCallback = self.logger.newSignalCallback
        self._newEventCallback = self.logger.newEventCallback
        self._handleScriptCallback = self.logger.handleScriptCallback
        self._recordingLengthChangedCallback = self.logger.recordingLengthChangedCallback

    def clear(self, dev=True, sig=True, ev=True, database=False):
        """
        Clears data from local/database. You can decide, if you want to delete all devices, all signals or just all events.

        Args:
            dev (bool): If True, everything will be deleted.
            sig (bool): If True, all signals and events will be deleted.
            ev (bool): If True, all events will be deleted.
            database (bool): If True, also data from database will be deleted.
        """
        with localLock:
            if dev is True or sig is True:
                self._signals = {}
                self._devices = {}
            if ev is True:
                self._events = {}
        if database:
            d, s, e = self._checkDatabases()
            if self._cursor is not None:
                with lock:
                    if e is True:
                        if ev is True:
                            self._cursor.execute('DROP TABLE ' + EVENT_TABLE_NAME + ' CASCADE;')
                            logging.info('Deleting events table')
                        if s is True:
                            if sig is True:
                                self._cursor.execute('DROP TABLE ' + SIGNAL_TABLE_NAME + ' CASCADE;')
                                logging.info('Deleting signals table')
                    else:
                        if d is True:
                            if dev is True:
                                self._cursor.execute('DROP TABLE ' + DEVICE_TABLE_NAME + ' CASCADE;')
                                logging.info('Deleting devices table')
                                self._connection.commit()
                if dev is True:
                    self._createDevicesTable()
                if sig is True:
                    self._createSignalsTable()
                if ev is True:
                    self._createEventsTable()

    def devices(self):
        """
        Returns all devices

        Returns:
            dict: {'devID': dname, ...}
        """
        return self._devices

    def getNewSignalID(self):
        """
        Returns an unused signalID

        Returns:
            sigID (int)
        """
        newID = 0
        while newID in self._signals.keys() or newID == 0:
            newID += 1

        return newID

    def getNewEventID(self):
        """
        Returns an unused eventID

        Returns:
            evID (int)
        """
        newID = 0
        while newID in self._events.keys() or newID == 0:
            newID += 1

        return newID

    def getNewDeviceID(self):
        """
        Returns an unused deviceID

        Returns:
            devID (int)
        """
        newID = 0
        while newID in self._devices.keys() or newID == 0:
            newID += 1

        return newID

    def resizeSignals(self, newLength=None):
        """
        Resizes the local maximum length of signals. If newLength is shorter than a signal, old measurements will be lost.

        This does not affect the database

        Args:
            newLength (int)
        """
        if newLength is None:
            newLength = self.config['global']['recordLength']
        else:
            self.config['global']['recordLength'] = newLength
        for sigID in self._signals.keys():
            s = self._signals[sigID]
            self._signals[sigID] = [s[0], s[1],
             deque(list(s[2]), newLength), deque(list(s[3]), newLength), s[4]]

    def getDeviceID(self, devicename):
        """
        Returns the devID for a given devicename. Returns -1, if device could not be found

        Args:
            devicename (str)

        Returns:
            devID (int)
        """
        for d in self._devices.items():
            if d[1] == devicename:
                return d[0]

        return -1

    def getDeviceName(self, devID):
        """
        Returns the devicename for a given devID. Returns None, if devID could not be found

        Args:
            devID (int)

        Returns:
            devicename (str)
        """
        if devID in self._devices.keys():
            return self._devices[devID]
        else:
            return

    def getSignalID(self, devicename, signalname, database=False):
        """
        Returns the sigID for a given devicename and signalname. Returns -1, if device or signal could not be found

        Args:
            devicename (str)
            signalname (str)
            database (bool): If True, also the database will be searched for signal

        Returns:
            sigID (int)
        """
        if database:
            return self._SQLgetSignalID(devicename, signalname)
        else:
            devID = self.getDeviceID(devicename)
            if devID == -1:
                return -1
            for s in self._signals.items():
                if s[1][0] == devID:
                    if s[1][1] == signalname:
                        return s[0]

            return -1

    def getSignalName(self, sigID):
        """
        Returns the signalname for a given sigID. Returns None, if sigID could not be found

        Args:
            sigID (int)

        Returns:
            name (list): [devicename, signalname]
        """
        if sigID in self._signals.keys():
            s = self._signals[sigID]
            devName = self.getDeviceName(s[0])
            sigName = s[1]
            return [
             devName, sigName]
        else:
            return

    def getSignalUnit(self, sigID):
        """
        Returns the unit for a given sigID. Returns "", if sigID could not be found

        Args:
            sigID (int)

        Returns:
            unit (str)
        """
        if sigID in self._signals.keys():
            s = self._signals[sigID]
            unit = s[4]
            return unit
        else:
            return ''

    def getEventName(self, evID):
        """
        Returns the signalname for a given evID. Returns None, if evID could not be found

        Args:
            evID (int)

        Returns:
            name (list): [devicename, signalname]
        """
        if evID in self._events.keys():
            e = self._events[evID]
            sigName = self.getSignalName(e[1])
            return sigName
        else:
            return

    def _createSignal(self, signalname, devicename, x=None, y=None, unit=None):
        dev_id = self.getDeviceID(devicename)
        if dev_id == -1:
            dev_id = self._createDevice(devicename)
        else:
            sigID = self.getNewSignalID()
            sigLen = self.config['global']['recordLength']
            if y is None or type(y) != list:
                x = deque([], sigLen)
                y = deque([], sigLen)
            else:
                x = deque(x, sigLen)
            y = deque(y, sigLen)
        signal = [
         dev_id, signalname, x, y, unit]
        self._signals[sigID] = signal
        if self._newSignalCallback:
            self._newSignalCallback(sigID, devicename, signalname, unit)
        if self._newSignalWebsocketCallback:
            self._newSignalWebsocketCallback(x, y, unit, devicename, signalname, sigID)
        return sigID

    def _createDevice(self, devicename, devID=None):
        if devicename not in self._devices.values():
            if devID is None or type(devID) != int:
                devID = self.getNewDeviceID()
            else:
                if type(devID) is int:
                    if devID in self._devices[devID]:
                        devID = self.getNewDeviceID()
            self._devices[devID] = devicename
            return True
        else:
            return False

    def _addNewData(self, y, dataunit, devicename, signalname, x=None, createCallback=True):
        if y is not None:
            with localLock:
                if devicename == None or type(devicename) != str:
                    devicename = 'noDevice'
                else:
                    if signalname == None or type(signalname) != str:
                        signalname = 'noSignal'
                    elif x is None:
                        x = time.time()
                    else:
                        devID = self.getDeviceID(devicename)
                        if devID == -1:
                            devID = self._createDevice(devicename)
                        sigID = self.getSignalID(devicename, signalname)
                        if sigID == -1:
                            sigID = self._createSignal(signalname, devicename, x=None, y=None, unit=None)
                        if len(self._signals[sigID][2]) + 1 >= self.config['global']['recordLength'] and self.config['backup']['autoIfFull']:
                            logging.info('Backing up signals, because local variable full.')
                            self._RT_data__updateT()
                            if self.logger:
                                self.logger.clearCB()
                            else:
                                self.clear()
                            if self.config['postgresql']['active']:
                                dev, sig, ev = self._checkDatabases()
                                self.clear(not dev, not sig, not ev)
                                self.pullFromDatabase(True, True, True, False)
                    if sigID not in self._signals.keys():
                        logging.error('Cannot add data. SignalID is unknown!')
                        return
                self._signals[sigID][2].append(float(x))
                self._signals[sigID][3].append(float(y))
                self._signals[sigID][4] = dataunit
            if self._handleScriptCallback:
                self._handleScriptCallback(devicename, signalname)
            if self._callback:
                if createCallback:
                    self._callback(devicename, signalname)
            if self.websocketSignal_callback:
                self.websocketSignal_callback(x, y, dataunit, devicename, signalname, sigID)
            if self.config['global']['globalEventsActivated']:
                if self.logger is not None:
                    self.logger.performGlobalEvents(y, dataunit, devicename, signalname, x)

    def _plotNewData(self, x, y, dataunit, devicename, signalname, createCallback=False, hold='off', autoResize=False):
        if y is not None and x is not None:
            with localLock:
                if devicename == None or type(devicename) != str:
                    devicename = 'noDevice'
                elif signalname == None or type(signalname) != str:
                    signalname = 'noSignal'
                else:
                    devID = self.getDeviceID(devicename)
                    if devID == -1:
                        devID = self._createDevice(devicename)
                    sigID = self.getSignalID(devicename, signalname)
                    if sigID == -1:
                        sigID = self._createSignal(signalname, devicename, x=None, y=None, unit=None)
                    if autoResize:
                        newsize = None
                        if hold == 'on':
                            if len(y) + len(self._signals[sigID][3]) > self.config['global']['recordLength']:
                                newsize = len(y) + len(self._signals[sigID][3])
                        else:
                            if len(y) > self.config['global']['recordLength']:
                                newsize = len(y)
                            if newsize:
                                self.resizeSignals(newsize)
                                logging.warning('Your recording length was updated due to plotting a bigger signal')
                                if self._recordingLengthChangedCallback:
                                    self._recordingLengthChangedCallback(devicename, signalname, newsize)
                    if hold == 'on':
                        self._signals[sigID][2] += x
                        self._signals[sigID][3] += y
                    else:
                        if hold == 'mergeX':
                            for val_idx, value in enumerate(x):
                                if value not in self._signals[sigID][2]:
                                    if autoResize:
                                        if len(self._signals[sigID][3]) >= self.config['global']['recordLength']:
                                            self.resizeSignals(len(self._signals[sigID][3]) + 50)
                                    self._signals[sigID][2].append(x[val_idx])
                                    self._signals[sigID][3].append(y[val_idx])

                        else:
                            if hold == 'mergeY':
                                for val_idx, value in enumerate(y):
                                    if value not in self._signals[sigID][2]:
                                        if autoResize:
                                            if len(self._signals[sigID][3]) >= self.config['global']['recordLength']:
                                                self.resizeSignals(len(self._signals[sigID][3]) + 50)
                                        self._signals[sigID][2].append(x[val_idx])
                                        self._signals[sigID][3].append(y[val_idx])

                            else:
                                self._signals[sigID][2] = deque(x, self.config['global']['recordLength'])
                                self._signals[sigID][3] = deque(y, self.config['global']['recordLength'])
                    if type(dataunit) == str:
                        self._signals[sigID][4] = dataunit
                    elif type(dataunit) == list:
                        self._signals[sigID][4] = dataunit[(-1)]
            if self._handleScriptCallback:
                self._handleScriptCallback(devicename, signalname)
            if self._callback:
                if createCallback:
                    self._callback(devicename, signalname)

    def printSignals(self):
        """
        Logs all signals to terminal.
        """
        for sigID in self._signals.keys():
            logging.info('Device: ' + self.getDeviceName(self._signals[sigID][0]) + ', Signal: ' + self._signals[sigID][1])
            logging.info('Timebase:')
            for data in self._signals[sigID][2]:
                sys.stdout.write(str(round(data, 1)) + '\t')

            logging.info('\nData:')
            for data in self._signals[sigID][3]:
                sys.stdout.write(str(round(data, 1)) + '\t\t')

            logging.info('\nUnit: ')
            sys.stdout.write(str(self._signals[sigID][4]) + '\t\t')
            logging.info('')

    def addData(self, *args, **kwargs):
        """
        This function calls :meth:`.addDataCallback` with parameter 'callback'=True.
        """
        kwargs['c'] = True
        (self.addDataCallback)(*args, **kwargs)

    def addDataCallback(self, y=[], snames=[], dname='noDevice', unit=[], x=[], c=True):
        """
        Adds new data to multiple signals and automatically creates new devices and signals if they do not exist.

        Args:
            y (list): List of multiple y-values for multiple signals
            snames (list): List of signalnames for y-values
            dname (str): devicename for each signal
            unit (list): List of units for y-values
            x (list): x-values for each y-value. If not set, each x-value is time.time()
            c (bool): If True, callback for GUI is called
        """
        if type(unit) == str:
            unit = [
             unit]
        elif type(snames) == str:
            snames = [
             snames]
        else:
            if type(y) == float or type(y) == int:
                y = [
                 y]
            if type(x) == float or type(x) == int:
                x = [
                 x]
            if type(y) == list and type(snames) == list:
                if x == [] or x == None:
                    x = [
                     time.time()] * len(y)
                if unit == [] or unit is None or type(unit) == str:
                    unit = [
                     ''] * len(y)
                else:
                    if len(unit) < len(y):
                        unit += [''] * (len(y) - len(unit))
                    else:
                        if len(unit) > len(y):
                            unit = unit[0:len(y)]
                if len(snames) < len(y):
                    snames += ['Unnamed'] * (len(y) - len(snames))
                for idx, data in enumerate(y):
                    self._addNewData(y[idx], unit[idx], dname, snames[idx], x[idx], c)

            elif type(y) == str:
                self.addNewEvent(y)

    def plot(self, x=[], y=[], sname='noName', dname='noDevice', unit='', c=False, hold='off', autoResize=False, sigID=None):
        """
        Adds/merges/replaces new data to one signals and automatically creates new devices and signals if they do not exist.

        Args:
            x (list): List of x-values
            y (list): List of y-values
            sname (str): signalname for signal
            dname (str): devicename for signal
            unit (str): unit for signal
            c (bool): If True, callback for GUI is called
            hold ('off','on','mergeX' or 'mergeY'): Defines how data is added to signal. 'off' will replace existing data. 'on' will append new data to existing data. 'mergeX' will only add xy-pairs with unique x-values. 'mergeY' will only add xy-pairs with unique y-values.
            autoResize (bool): If True, recordLength will automatically be adjusted, if new signal is too long
        """
        if y == []:
            y = x
            x = list(range(len(x)))
        else:
            if sigID is not None:
                names = self.getSignalName(sigID)
                dname = names[0]
                sname = names[1]
            if len(x) == len(y):
                self._plotNewData(x, y, unit, dname, sname, c, hold, autoResize)
            else:
                logging.error('Plotting aborted. len(x)!=len(y)')

    def getSignalSize(self):
        """
        Returns information about storage of signals.

        If using postgreSQL database:

        Returns:
            used (float): Used disk-space in GB

            total (float): Maximum disk-space in GB

            parts (list): [devicesize, signalsize, eventsize]

        If **not** using postgreSQL database:

        Returns:
            used (float): Used disk-space in Bytes

            total (float): Disk-space used, if local storage full (in Bytes)

            None
        """
        if self.config['postgresql']['active']:
            dbname = self.config['postgresql']['database']
            q = "select pg_size_pretty( pg_database_size('{dbname}'));".format(dbname=dbname)
            row0 = self._execute_n_fetchall(q)
            dbname = DEVICE_TABLE_NAME
            q = "select pg_size_pretty( pg_total_relation_size('{dbname}'));".format(dbname=dbname)
            row1 = self._execute_n_fetchall(q)
            dbname = SIGNAL_TABLE_NAME
            q = "select  pg_size_pretty( pg_total_relation_size('{dbname}'));".format(dbname=dbname)
            row2 = self._execute_n_fetchall(q)
            dbname = EVENT_TABLE_NAME
            q = "select  pg_size_pretty( pg_total_relation_size('{dbname}'));".format(dbname=dbname)
            row3 = self._execute_n_fetchall(q)
            obj_Disk = psutil.disk_usage('/')
            total = round(obj_Disk.total / 1073741824.0, 3)
            used = round(obj_Disk.used / 1073741824.0, 3)
            free = round(obj_Disk.free / 1073741824.0, 3)
            return (
             used, total, [row0[0][0], row1[0][0], row2[0][0], row3[0][0]])
        else:
            maxsize = len(self._signals) * (2 * (self.config['global']['recordLength'] * 8 + 64) + 16)
            outerlayer = sys.getsizeof(self._signals)
            innerlayer = 0
            for sig in self._signals.values():
                innerlayer += sys.getsizeof(sig)
                innerlayer += sys.getsizeof(list(sig[2])) * 2

            size = outerlayer + innerlayer
            return (size, maxsize, None)

    def getLatest(self, force=None):
        """
        Returns a dictonary with latest xy-pairs for each signal.

        Args:
            force (bool): Unused

        Returns:
            dict: {'dname.sname':[x,y,unit],...}
        """
        ans = {}
        for sigID in self._signals.keys():
            dev = self.getSignalName(sigID)
            if len(self._signals[sigID][2]) > 0:
                ans['.'.join(dev)] = [
                 self._signals[sigID][2][(-1)], self._signals[sigID][3][(-1)], self._signals[sigID][4], sigID, self._signals[sigID][2][0], self._signals[sigID][2][(-1)]]

        return ans

    def addNewEvent(self, text='', sname='noName', dname='noDevice', x=None, priority=0, id=None, value=None):
        """
        Adds a new event.

        Args:
            text (str): Text displayed in event.
            sname (str): Allocated signalname for event.
            dname (str): Allocated devicename for event.
            x (float): x-value for event.
            priority (0,1,2): Priority of signal (0=Information, 1=Warning, 2=Error)
            id (str): Event-ID to trigger actions
            value (any): Unused
        """
        if dname == None or type(dname) != str:
            dname = 'noDevice'
        elif sname == None or type(sname) != str:
            sname = 'noSignal'
        else:
            if id is None:
                id = hashlib.sha1((sname + dname + text).encode()).hexdigest()
            elif priority not in (0, 1, 2):
                priority = 0
            else:
                logging.info('New Event: ' + str(dname) + '.' + str(sname) + ': ' + str(text) + ' (ID: ' + str(id) + ', Value: ' + str(value))
                devID = self.getDeviceID(dname)
                if devID == -1:
                    self._createDevice(dname)
                    devID = self.getDeviceID(dname)
                sigID = self.getSignalID(dname, sname)
                if sigID == -1:
                    self._createSignal(sname, dname, x=None, y=None, unit=None)
                    sigID = self.getSignalID(dname, sname)
                if x is None:
                    x = time.time()
                with localEventLock:
                    eventID = self.getNewEventID()
                    event = [devID, sigID, eventID, text, x, value, priority, id]
                    self._events[eventID] = event
                if self._newEventCallback:
                    self._newEventCallback(x, text, dname, sname, priority, value, id, eventID)
                if self.websocketEvent_callback:
                    self.websocketEvent_callback(x, text, dname, sname, priority, value, id, eventID)
                if self.config['telegram']['active']:
                    if self.logger is not None:
                        if self.logger.telegramBot is not None:
                            self.logger.telegramBot.sendEvent(text, dname, sname, priority)
            if self.config['global']['globalActionsActivated']:
                if self.logger is not None:
                    self.logger.performGlobalActions(id, value)

    def getEvents(self, sigID):
        """
        Returns all events of a given sigID

        Args:
            sigID (int)

        Returns:
            list: List of events
        """
        events = []
        for ev in self._events.items():
            if ev[1][1] == sigID:
                events.append(ev[1])

        return events

    def renameSignal(self, sigID, signame):
        """
        Renames a signal with given sigID. **Will not rename signals in database!**

        Args:
            sigID (int)
            signame (str): New signalname for signal with given sigID.

        Returns:
            bool: True, if successfully renamed, False, if not.
        """
        if sigID in self._signals.keys():
            self._signals[sigID][1] = signame
            return True
        else:
            return False

    def events(self, beauty=False, latest=None):
        """
        Returns all locally stored events.

        Args:
            beauty (bool): If True, dict will contain names instead of ids

        Returns:
            dict: {EVENT_ID: [DEVICE_ID,SIGNAL_ID,EVENT_ID,TEXT,TIME,VALUE,PRIORITY, ID],...}
        """
        if beauty:
            ev = {}
            with localEventLock:
                for idx, evID in enumerate(self._events.keys()):
                    name = self.getEventName(evID)
                    old = self._events[evID]
                    ev[evID] = [name[0], name[1], *old[2:]]
                    if type(latest) == int:
                        if idx >= latest:
                            break

            return ev
        else:
            return dict(self._events)

    def signals(self):
        """
        Returns all locally stored signals.

        Returns:
            dict: {SIGNAL_ID: [DEVICE_ID, NAME, X,Y, UNIT],...}
        """
        return self._signals

    def signalNames(self, units=[], devices=[]):
        """
        Returns all signalNames with given units and devices. Returns all signalNames, if units == [] and devices == [].

        Args:
            units (list)
            devices (list)

        Returns:
            list: [[dname,sname],...]
        """
        names = []
        for sigID in self._signals.keys():
            signame = self._signals[sigID][1]
            devID = self._signals[sigID][0]
            unit = self._signals[sigID][4]
            devname = self.getDeviceName(devID)
            if (units == [] or unit in units) and (devices == [] or devname in devices):
                names.append([devname, signame])

        return names

    def deviceNames(self):
        """
        Returns all deviceNames.

        Returns:
            list: [dname,...]
        """
        return list(self._devices.values())

    def _connect(self):
        if psycopg2 is None:
            self.status = 'psycopg2 not installed'
            self._connection = None
            self._cursor = None
            return False
        try:
            self._connection = psycopg2.connect(user=(self.config['postgresql']['user']),
              password=(self.config['postgresql']['password']),
              host=(self.config['postgresql']['host']),
              port=(self.config['postgresql']['port']),
              database=(self.config['postgresql']['database']))
            self._cursor = self._connection.cursor()
            self._execute_n_fetchall('SELECT version();')
            self.status = 'connected'
            return True
        except (Exception, psycopg2.Error) as error:
            logging.error('Error while connecting to PostgreSQL', error)
            self.status = 'could not connect'
            self._connection = None
            self._cursor = None
            return False

    def _checkDatabases(self):
        table = DEVICE_TABLE_NAME
        existtest = "SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = '" + table + "' );"
        dev = self._execute_n_fetchall(existtest)[0]
        table = SIGNAL_TABLE_NAME
        existtest = "SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = '" + table + "' );"
        sig = self._execute_n_fetchall(existtest)[0]
        table = EVENT_TABLE_NAME
        existtest = "SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = '" + table + "' );"
        ev = self._execute_n_fetchall(existtest)[0]
        return (
         dev[0], sig[0], ev[0])

    def pullFromDatabase(self, dev=True, sig=True, ev=True, getData=True):
        """
        Writes all devices,signals and/or events from database to local.

        Args:
            dev (bool): If True, devices will be pulled.
            sig (bool): If True, devices and signals will be pulled.
            ev (bool): If True, devices, signals and events will be pulled.
            getData (bool): If True, all signaldata will be pulled. If False, only empty signals will be pulled.
        """
        if self.status == 'connected':
            self._startTime = self._SQLgetStartTime()
            if dev or sig or ev:
                devIds = self._execute_n_fetchall('select ID, NAME from ' + DEVICE_TABLE_NAME)
                if devIds is not None:
                    if devIds != []:
                        devIds = {i[0]:i[1] for i in devIds}
                        self._devices = devIds
                if sig or ev:
                    if getData:
                        signals = self._execute_n_fetchall('select ID, DEVICE_ID, NAME, X, Y, UNIT from ' + SIGNAL_TABLE_NAME)
                    else:
                        signals = self._execute_n_fetchall('select ID, DEVICE_ID, NAME, UNIT from ' + SIGNAL_TABLE_NAME)
                    if signals is not None and signals != []:
                        signals = {signal[0]:list(signal)[1:] for signal in signals}
                        if self.logger is not None:
                            maxLength = self.logger.config['global']['recordLength']
                        else:
                            maxLength = 500000
                        if getData:
                            for sigID in signals.keys():
                                signals[sigID][2] = [float(i) for i in signals[sigID][2][0:maxLength]]
                                signals[sigID][3] = [float(i) for i in signals[sigID][3][0:maxLength]]
                                signals[sigID][2] = deque(signals[sigID][2], maxLength)
                                signals[sigID][3] = deque(signals[sigID][3], maxLength)
                                signals[sigID][4] = signals[sigID][4]

                        else:
                            for sigID in signals.keys():
                                devID = signals[sigID][0]
                                name = signals[sigID][1]
                                unit = signals[sigID][2]
                                x = deque([], maxLength)
                                y = deque([], maxLength)
                                signals[sigID] = [devID, name, x, y, unit]

                        self._signals = signals
                    else:
                        signals = {}
                    if ev:
                        numEvents = self.config['global']['recordLength']
                        if numEvents is None:
                            strung = 'select DEVICE_ID, SIGNAL_ID, EVENT_ID, TEXT, TIME, VALUE,PRIORITY, ID  from ' + EVENT_TABLE_NAME
                        else:
                            strung = 'select DEVICE_ID, SIGNAL_ID, EVENT_ID, TEXT, TIME, VALUE,PRIORITY, ID  from ' + EVENT_TABLE_NAME + ' LIMIT ' + str(numEvents)
                        events = self._execute_n_fetchall(strung)
                        if events is not None:
                            if events != []:
                                events = {i[7]:list(i) for i in events}
                                for evID in events.keys():
                                    events[evID][4] = float(events[evID][4])

                                self._events = events
                        else:
                            events = []

    def pushToDatabase(self):
        """
        Writes all new devices,signals and/or events from local to database.
        """
        latest = {}
        for sigID in self._signals.keys():
            sig = self._getSQLSignal(sigID, 1)
            if sig is not None and len(sig[2]) > 0:
                latest[sigID] = [
                 sig[2][(-1)], sig[3][(-1)]]

        with localLock:
            localData = dict(self._signals)
            newData = {}
            newSignals = {}
            for sigID in localData.keys():
                signal = localData[sigID]
                if sigID in latest.keys():
                    for idx, x in enumerate(signal[2]):
                        if x > latest[sigID][0]:
                            newData[sigID] = [
                             -1, '', [], [], '']
                            newData[sigID][0] = localData[sigID][0]
                            newData[sigID][1] = localData[sigID][1]
                            newData[sigID][4] = localData[sigID][4]
                            newData[sigID][2] = list(localData[sigID][2])[int(idx):]
                            newData[sigID][3] = list(localData[sigID][3])[int(idx):]
                            break

                else:
                    newSignals[sigID] = localData[sigID]

        if self.logger.config['backup']['resample'] != 0:
            for sigID in newData.keys():
                newData[sigID][2], newData[sigID][3] = resample(newData[sigID][2], newData[sigID][3], self.logger.config['backup']['resample'])

            for sigID in newSignals.keys():
                newSignals[sigID][2], newSignals[sigID][3] = resample(newSignals[sigID][2], newSignals[sigID][3], self.logger.config['backup']['resample'])

        else:
            if newData == {}:
                if newSignals == {}:
                    logging.info('Signal-Backup is already up to date.')
            else:
                for sigID in newData.keys():
                    x = newData[sigID][2]
                    y = newData[sigID][3]
                    self._appendSQLSignal(sigID, x, y)

                for sigID in newSignals.keys():
                    self._addSQLSignal(sigID, newSignals[sigID])

            newEvents = {}
            storedEventIDs = self._getSQLEventIDs()
            for evID in self._events.keys():
                if evID not in storedEventIDs:
                    newEvents[evID] = self._events[evID]

            if newEvents == {}:
                logging.info('Event-Backup is up to date')
            else:
                logging.info('Adding new events to database')
                for evID in newEvents.keys():
                    (self._SQLcreateEvent)(*newEvents[evID])

    def _createDevicesTable(self):
        create_table_query = 'CREATE TABLE ' + DEVICE_TABLE_NAME + '\n          (ID SERIAL PRIMARY KEY     UNIQUE NOT NULL,\n          NAME          TEXT   UNIQUE NOT NULL,\n          CREATION_DATE REAL   NOT NULL); '
        print('here')
        if self._execute(create_table_query):
            logging.info('Initialized devices table')
        print('there')

    def _createSignalsTable(self):
        create_table_query = 'CREATE TABLE ' + SIGNAL_TABLE_NAME + '\n          (ID SERIAL PRIMARY KEY     UNIQUE NOT NULL,\n          DEVICE_ID INT      NOT NULL,\n          NAME      TEXT    NOT NULL,\n          X           NUMERIC[],\n          Y         NUMERIC[],\n          UNIT      TEXT,\n          CREATION_DATE REAL   NOT NULL,\n          CONSTRAINT signal_device_id_fkey FOREIGN KEY (DEVICE_ID)\n              REFERENCES ' + DEVICE_TABLE_NAME + ' (ID) MATCH SIMPLE\n              ON UPDATE NO ACTION ON DELETE NO ACTION\n          ); '
        if self._execute(create_table_query):
            logging.info('Initialized signals table')

    def _createEventsTable(self):
        create_table_query = 'CREATE TABLE ' + EVENT_TABLE_NAME + '\n          (ID SERIAL PRIMARY KEY    UNIQUE NOT NULL,\n          DEVICE_ID INT       NOT NULL,\n          SIGNAL_ID INT      NOT NULL,\n          EVENT_ID TEXT      NOT NULL,\n          TEXT   TEXT   NOT NULL,\n          TIME NUMERIC   NOT NULL,\n          VALUE TEXT,\n          PRIORITY INT NOT NULL,\n          CONSTRAINT event_device_id_fkey FOREIGN KEY (DEVICE_ID)\n              REFERENCES ' + DEVICE_TABLE_NAME + ' (ID) MATCH SIMPLE\n              ON UPDATE NO ACTION ON DELETE NO ACTION,\n          CONSTRAINT event_signal_id_fkey FOREIGN KEY (SIGNAL_ID)\n              REFERENCES ' + SIGNAL_TABLE_NAME + ' (ID) MATCH SIMPLE\n              ON UPDATE NO ACTION ON DELETE NO ACTION\n          ); '
        if self._execute(create_table_query):
            logging.info('Initialized events table')

    def _execute(self, query):
        ok = self._execute_n_commit(query)
        if ok:
            logging.info('Table created successfully in PostgreSQL ')

    def _execute_n_fetchall(self, query):
        if self._cursor is not None:
            with lock:
                try:
                    starttime = time.time()
                    self._connection.commit()
                    self._cursor.execute(query)
                    ans = self._cursor.fetchall()
                    delta = time.time() - starttime
                except (Exception, psycopg2.DatabaseError) as error:
                    if str(error) != 'connection already closed':
                        logging.info('Error while execution+fetch in PostgreSQL table')
                        logging.error(error)
                        logging.error(query)
                    ans = None

            return ans

    def _execute_n_commit(self, query):
        if self._cursor is not None:
            return self._commit(query)
        else:
            return False

    def _commit(self, query):
        with lock:
            try:
                starttime = time.time()
                self._connection.commit()
                self._cursor.execute(query)
                self._connection.commit()
                delta = time.time() - starttime
                delta = time.time() - starttime
                ans = True
            except (Exception, psycopg2.DatabaseError) as error:
                if str(error) != 'connection already closed':
                    logging.info('Error while execution+commit in PostgreSQL table')
                    logging.error(error)
                    logging.error(query)
                    logging.error(traceback.format_exc())
                ans = False

    def _getSQLSignalUnit(self, sigID):
        ans = self._execute_n_fetchall('select UNIT from ' + SIGNAL_TABLE_NAME + ' where ID = ' + str(sigID) + '')
        if ans != []:
            if ans is not None:
                ans = ans[0][0]
        else:
            ans = None
        return ans

    def _appendSQLSignal(self, sigID, x, y):
        sql = 'UPDATE ' + SIGNAL_TABLE_NAME + ' SET X = array_cat(X, ARRAY' + str(list(x)) + '::NUMERIC[]) WHERE ID =' + str(sigID) + ';'
        sql += '\nUPDATE ' + SIGNAL_TABLE_NAME + ' SET Y = array_cat(Y,ARRAY' + str(list(y)) + '::NUMERIC[]) WHERE ID =' + str(sigID) + ';'
        self._execute_n_commit(sql)

    def _addSQLSignal(self, sigID, signal):
        devicename = self.getDeviceName(signal[0])
        x = list(signal[2])
        y = list(signal[3])
        unit = signal[4]
        signalname = signal[1]
        dev = self._SQLdeviceExists(devicename)
        if dev is False:
            self._SQLcreateDevice(signal[0], devicename)
        if not self._SQLsignalExists(signalname, devicename):
            sigID = self._SQLcreateSignal(sigID, signalname, devicename, x, y, unit)
        sql = 'UPDATE ' + SIGNAL_TABLE_NAME + ' SET X = ARRAY' + str(x) + '::NUMERIC[] WHERE ID =' + str(sigID) + ';'
        sql += '\nUPDATE ' + SIGNAL_TABLE_NAME + ' SET Y = ARRAY' + str(y) + '::NUMERIC[] WHERE ID =' + str(sigID) + ';'
        sql += '\nUPDATE ' + SIGNAL_TABLE_NAME + " SET UNIT = '" + str(unit) + "' WHERE ID =" + str(sigID) + ';'
        self._execute_n_commit(sql)

    def _SQLdeviceExists(self, devicename):
        existtest = 'SELECT EXISTS (select ID from ' + DEVICE_TABLE_NAME + " where NAME = '" + str(devicename) + "');"
        sig = self._execute_n_fetchall(existtest)
        if sig is not None:
            if sig != []:
                sig = bool(sig[0][0])
        else:
            sig = False
        return sig

    def _SQLsignalExists(self, signalname, devicename):
        if self._SQLdeviceExists(devicename):
            devID = self._SQLgetDeviceID(devicename)
        else:
            return False
        existtest = 'SELECT EXISTS (select ID from ' + SIGNAL_TABLE_NAME + " where NAME = '" + str(signalname) + "' and DEVICE_ID = " + str(devID) + ');'
        sig = self._execute_n_fetchall(existtest)
        if sig is not None:
            if sig != []:
                sig = bool(sig[0][0])
        else:
            sig = False
        return sig

    def _SQLcreateDevice(self, devID, devicename):
        timestamp = time.time()
        if devicename != None:
            sql = 'INSERT INTO ' + DEVICE_TABLE_NAME + '(ID, NAME, CREATION_DATE)\n                    VALUES\n                     (' + str(devID) + ",'" + str(devicename) + "'," + str(timestamp) + ');'
            self._execute_n_commit(sql)
        else:
            logging.error('Cannot create devicename=None')

    def _SQLcreateSignal(self, sigID, signalname, devicename, x='', y='', unit=''):
        devID = self._SQLgetDeviceID(devicename)
        if devID == -1:
            self._SQLcreateDevice(devID, devicename)
            devID = self._SQLgetDeviceID(devicename)
        if devID != -1:
            logging.info('Creating new signal:' + str(devicename) + '.' + str(signalname))
            timestamp = time.time()
            if x is None:
                x = ''
                y = ''
            else:
                x = ''
                y = ''
            sql = 'INSERT INTO ' + SIGNAL_TABLE_NAME + '(ID, NAME, DEVICE_ID, CREATION_DATE, X, Y, UNIT)\n                    VALUES\n                     (' + str(sigID) + ",'" + str(signalname) + "'," + str(devID) + ',' + str(timestamp) + ',ARRAY[' + str(x) + ']::real[],ARRAY[' + str(y) + "]::real[],'" + str(unit) + "');"
            self._execute_n_commit(sql)
            name = 'select ID from ' + SIGNAL_TABLE_NAME + " where NAME = '" + str(signalname) + "' and DEVICE_ID = " + str(devID)
            sigID = self._execute_n_fetchall(name)
            if sigID != []:
                if sigID is not None:
                    sigID = sigID[0][0]
            return sigID
        else:
            logging.error('SQL: Could not create Signal')
            return -1

    def _SQLcreateEvent(self, devID, sigID, evID, strung, x, value, priority, eventid):
        devicename, signalname = self.getEventName(evID)
        logging.info('Creating new event:' + str(devicename) + '.' + str(signalname))
        check_devID = self._SQLgetDeviceID(devicename)
        if check_devID == -1:
            self._SQLcreateDevice(devID, devicename)
            devID = self._SQLgetDeviceID(devicename)
        if not self._SQLsignalExists(signalname, devicename):
            sigID = self._SQLcreateSignal(sigID, devicename, signalname)
        if devID != -1 and sigID != -1:
            sql = 'INSERT INTO ' + EVENT_TABLE_NAME + '(ID, TIME, TEXT, DEVICE_ID, SIGNAL_ID, PRIORITY, VALUE, EVENT_ID)\n                    VALUES\n                     (' + str(evID) + ',' + str(x) + ",'" + str(strung) + "'," + str(devID) + ',' + str(sigID) + ',' + str(priority) + ",'" + str(value) + "','" + str(eventid) + "');"
            self._execute_n_commit(sql)
            name = 'select ID from ' + EVENT_TABLE_NAME + " where EVENT_ID = '" + str(eventid) + "' and DEVICE_ID = " + str(devID) + ' and TIME = ' + str(x)
            evID = self._execute_n_fetchall(name)
            if evID is not None:
                if evID != []:
                    evID = evID[0][0]
            else:
                evID = -1
            return evID
        else:
            print('Could not create device')
            return -1

    def _SQLgetDeviceID(self, devicename):
        devId = self._execute_n_fetchall('select ID from ' + DEVICE_TABLE_NAME + " where NAME = '" + str(devicename) + "'")
        if devId is not None:
            if devId != []:
                devId = devId[0][0]
        else:
            devId = -1
        return devId

    def _SQLgetSignalID(self, devicename, signalname):
        devID = self.getDeviceID(devicename)
        sigID = self._execute_n_fetchall('select ID from ' + SIGNAL_TABLE_NAME + " where NAME = '" + signalname + "' and DEVICE_ID =" + str(devID))
        if sigID is not None:
            if sigID != []:
                sigID = sigID[0][0]
        else:
            sigID = -1
        return sigID

    def _SQLgetStartTime(self):
        t = self._execute_n_fetchall('select CREATION_DATE from ' + DEVICE_TABLE_NAME)
        if t is not None:
            if t != []:
                t = [float(i[0]) for i in t]
                t = min(t)
        else:
            t = time.time()
        return t

    def _getSQLEventIDs(self):
        numEvents = None
        if numEvents is None:
            strung = 'select ID from ' + EVENT_TABLE_NAME
        else:
            strung = 'select ID from ' + EVENT_TABLE_NAME + ' LIMIT ' + str(numEvents)
        ans = self._execute_n_fetchall(strung)
        if ans is not None:
            if ans != []:
                ans = [int(i[0]) for i in ans]
        else:
            ans = []
        return ans

    def _getSQLDeviceIDs(self):
        numEvents = None
        if numEvents is None:
            strung = 'select ID from ' + DEVICE_TABLE_NAME
        else:
            strung = 'select ID from ' + DEVICE_TABLE_NAME + ' LIMIT ' + str(numEvents)
        ans = self._execute_n_fetchall(strung)
        if ans is not None:
            if ans != []:
                pass
        else:
            ans = []
        return ans

    def _getSQLSignalIDs(self):
        numEvents = None
        if numEvents is None:
            strung = 'select ID from ' + SIGNAL_TABLE_NAME
        else:
            strung = 'select ID from ' + SIGNAL_TABLE_NAME + ' LIMIT ' + str(numEvents)
        ans = self._execute_n_fetchall(strung)
        if ans is not None:
            if ans != []:
                pass
        else:
            ans = []
        return ans

    def _SQLplot(self, x=[], y=[], sname='noName', dname='noDevice', unit='', c=False, hold='off', autoResize=False, sigID=None):
        if y == []:
            y = x
            x = list(range(len(x)))
        else:
            if sigID is not None:
                names = self.getSignalName(sigID)
                dname = names[0]
                sname = names[1]
            if len(x) == len(y):
                if not self._SQLdeviceExists(dname):
                    self._SQLcreateDevice(dname)
                if not self._SQLsignalExists(sname, dname):
                    sigID = self._SQLcreateSignal(sname, dname)
                    self._SQLplotNewData(x, y, unit, dname, sname, c, hold, autoResize)
                else:
                    self._SQLplotNewData(x, y, unit, dname, sname, c, hold, autoResize)
            else:
                logging.error('Plotting aborted. len(x)!=len(y)')

    def _SQLplotNewData(self, x, y, dataunit, devicename, signalname, createCallback=False, hold='off', autoResize=False):
        sigID = self._SQLgetSignalID(devicename, signalname)
        if autoResize:
            logging.warning('autoResize is DEPRECATED for postgresql')
        else:
            if hold == 'on':
                sql = 'UPDATE ' + SIGNAL_TABLE_NAME + ' SET X = array_cat(X, ' + str(x) + '::NUMERIC[]) WHERE ID =' + str(sigID) + ';'
                sql += '\nUPDATE ' + SIGNAL_TABLE_NAME + ' SET Y = array_cat(Y,' + str(y) + '::NUMERIC[]) WHERE ID =' + str(sigID) + ';'
                sql += '\nUPDATE ' + SIGNAL_TABLE_NAME + " SET UNIT = '" + str(dataunit) + "' WHERE ID =" + str(sigID) + ';'
            else:
                if hold == 'mergeX':
                    logging.error('mergeX is NOT IMPLEMENTED YET for postgresql')
                else:
                    if hold == 'mergeY':
                        logging.error('mergeY is NOT IMPLEMENTED YET for postgresql')
                    else:
                        sql = 'UPDATE ' + SIGNAL_TABLE_NAME + ' SET X = ARRAY' + str(list(x)) + '::NUMERIC[] WHERE ID =' + str(sigID) + ';'
                        sql += '\nUPDATE ' + SIGNAL_TABLE_NAME + ' SET Y = ARRAY' + str(list(y)) + '::NUMERIC[] WHERE ID =' + str(sigID) + ';'
                        sql += '\nUPDATE ' + SIGNAL_TABLE_NAME + " SET UNIT = '" + str(dataunit) + "' WHERE ID =" + str(sigID) + ';'
        self._execute_n_commit(sql)
        print(devicename + '.' + signalname + ' has been changed')

    def _SQLExportCSV(self, filenamepart):
        filenames = []
        for table in [DEVICE_TABLE_NAME, SIGNAL_TABLE_NAME, EVENT_TABLE_NAME]:
            filename = filenamepart + '_' + table + '.gz'
            with gzip.open(filename, 'wb') as (gzip_file):
                self._cursor.copy_to(gzip_file, table, sep='|')
            filenames.append(filename)

        return filenames

    def start(self):
        """
        Starts the repeated backup-thread.
        """
        if self.config['postgresql']['active'] or self.config['backup']['active']:
            if self.config['backup']['intervall'] > 0:
                self._backupThread = _perpetualTimer(self.config['backup']['intervall'], self._RT_data__updateT, self.isGUI)
                self._backupThread.start()
                logging.info('Backup-Thread started')
            else:
                logging.warning('Database-service is enabled, but backup intervall was set to zero! Will not update database')

    def __updateT(self):
        if self.config['postgresql']['active']:
            if not self.webserver:
                self.pushToDatabase()
            if self.webserver:
                self.pullFromDatabase(dev=True, sig=True, ev=True)
            else:
                if self.logger is not None:
                    if not self.config['postgresql']['onlyPush']:
                        self.pullFromDatabase(dev=True, sig=True, ev=True)
            if self.logger:
                if self.config['backup']['clear']:
                    if self.config['backup']['active']:
                        self.logger.clearCB()
                        logging.info('Local data cleared after backup')
        else:
            self.backupJSON(self.config['backup']['path'])
            logging.info('Backup saved in path: ' + self.config['backup']['path'])
        if self.logger:
            self.logger.clearCB()

    def createLocalBackupNow(self):
        self.backupJSON(self.config['backup']['path'])
        logging.info('Backup saved in path: ' + self.config['backup']['path'])

    def stop(self):
        """
        Stops the repeated backup-thread.
        """
        if self._backupThread:
            self._backupThread.cancel()

    def close(self):
        """
        This function is called, if RTOC is beeing closed.
        """
        if self.config['backup']['autoOnClose']:
            if self.config['backup']['active']:
                self._RT_data__updateT()
        if self._backupThread:
            self._backupThread.cancel()

    def setBackupIntervall(self, intervall):
        """
        Sets a backup-Interval and automatically restarts backup-thread.

        Args:
            intervall (float): Backup-interval in seconds
        """
        if self._backupThread:
            self._backupThread.cancel()
        else:
            if not self.config['postgresql']['active']:
                if intervall > 0 and self.config['backup']['active']:
                    self.config['backup']['intervall'] = intervall
                    self._backupThread = _perpetualTimer(self.config['backup']['intervall'], self._RT_data__updateT, self.logger.isGUI)
                    self._backupThread.start()
                    return True
                else:
                    return False
            else:
                return False

    def getStoredBackupList(self):
        """
        Returns a list with all backup-files (only if not using postgreSQL for backup)

        Returns:
            list: ['path/to/backup1.json',...]
        """
        if os.path.isdir(self.config['backup']['path']):
            list = os.listdir(self.config['backup']['path'])
            jsonlist = []
            for i in list:
                if i.endswith('.json'):
                    jsonlist.append(i)

            return jsonlist
        else:
            return []

    def exportSignal(self, filename, signal):
        """
        Exports a single signal to csv-file.

        Args:
            filename (str): Filename (without '.csv')
            signal (SIGNAL): The signal to be stored.
        """
        with open(filename, 'w', newline='') as (myfile):
            wr = csv.writer(myfile, quoting=(csv.QUOTE_NONE), delimiter=' ', quotechar='|')
            wr.writerow(list(signal[2]))
            wr.writerow(list(signal[3]))

    def exportXLSX(self, filename):
        """
        Export all signals to Excel-file

        Args:
            filename (str)
        """
        if xlsxwriter is not None:
            workbook = xlsxwriter.Workbook(filename)
            worksheet = workbook.add_worksheet()
            row = -1
            col = -1
            jsonfile = {}
            jsonfile['maxLength'] = self.config['global']['recordLength']
            for key in jsonfile.keys():
                col = 0
                row += 1
                worksheet.write(row, col, key)
                if type(jsonfile[key]) == list:
                    for item in jsonfile[key]:
                        col += 1
                        if np.isnan(item):
                            data = -1
                        worksheet.write(row, col, item)

                else:
                    if np.isnan(jsonfile[key]):
                        jsonfile[key] = -1
                    worksheet.write(row, col + 1, jsonfile[key])

            worksheet2 = workbook.add_worksheet()
            row = 0
            col = -1
            for signalname in self.signalNames():
                col += 1
                worksheet2.write(row, col, '.'.join(signalname) + ' X')
                col += 1
                worksheet2.write(row, col, '.'.join(signalname) + ' Y')
                col += 1
                worksheet2.write(row, col, 'Einheit')

            row += 1
            col = -1
            for sigID in self._signals.keys():
                signal = self._signals[sigID]
                for xy in [signal[2], signal[3]]:
                    col += 1
                    row = 1
                    for data in xy:
                        if np.isnan(data):
                            data = -1
                        worksheet2.write(row, col, data)
                        row += 1

                col += 1
                row = 1
                worksheet2.write(row, col, str(signal[4]))
                row += 1

            workbook.close()
        else:
            logging.error('XLSXWriter not installed! Please install with "pip3 install xlsxwriter"')

    def generateSessionJSON(self):
        """
        Generates a json-file of all data to export

        """
        jsonfile = {}
        jsonfile['maxLength'] = self.config['global']['recordLength']
        t_signals = {}
        signals = dict(self._signals)
        for sigID in signals.keys():
            s = signals[sigID]
            t_signals[sigID] = [s[0], s[1], list(s[2]), list(s[3]), s[4]]

        jsonfile['signals'] = t_signals
        jsonfile['events'] = dict(self._events)
        jsonfile['devices'] = dict(self._devices)
        return jsonfile

    def backupJSON(self, filename=None, overwrite=False):
        """
        Backup session to JSON-file

        Args:
            filename (str): Filename of backup
            overwrite (bool): If True, existing file will be overwritten.
        """
        if self.config['backup']['active']:
            if filename is None:
                filename = self.config['backup']['path']
            else:
                if filename != '':
                    self.exportJSON(filename, overwrite)
                else:
                    logging.warning('Cannot create backup in root folder. Aborted')

    def exportJSON(self, filename, overwrite=False):
        """
        Save session to JSON-file

        Args:
            filename (str): Filename of backup
            overwrite (bool): If True, existing file will be overwritten.
        """
        jsonfile = self.generateSessionJSON()
        if os.path.isdir(filename):
            filename = os.path.join(filename, time.strftime('RTOC_%d_%m_%Hh%Mm%Ss') + '.json')
        if overwrite or not os.path.exists(filename):
            with open(filename, 'w') as (fp):
                json.dump(jsonfile, fp, sort_keys=False, indent=4, separators=(',',
                                                                               ': '))
            return True
        raise NotImplemented
        try:
            return True
        except Exception:
            logging.debug(traceback.format_exc())
            logging.error('Could not export data!')
            return False

    def restoreJSON(self, filename=None, clear=False):
        """
        Load session from JSON-file

        Args:
            filename (str): Filename of backup
            clear (bool): If True, existing data will be cleared
        """
        if filename is None:
            filename = self.config['global']['documentfolder'] + '/restore.json'
        else:
            if os.path.exists(filename):
                try:
                    with open(filename) as (f):
                        data = json.load(f)
                    if clear:
                        self.clear()
                        holde = 'off'
                    else:
                        holde = 'mergeX'
                    for devID in data['devices'].keys():
                        devicename = data['devices'][devID]
                        self._createDevice(devicename, devID=devID)

                    for sigID in data['signals'].keys():
                        signal = data['signals'][sigID]
                        devname = self.getDeviceName(signal[0])
                        self.plot((signal[2]), (signal[3]), (signal[1]),
                          devname, (signal[4]), False, hold=holde, autoResize=True)

                    for evID in data['events'].keys():
                        event = data['events'][evID]
                        name = self.getSignalName(event[1])
                        self.addNewEvent(text=(event[3]),
                          sname=(name[1]),
                          dname=(name[0]),
                          x=(event[4]),
                          priority=(event[6]),
                          value=(event[5]),
                          id=(event[7]))

                    return True
                except Exception:
                    logging.error(traceback.format_exc())
                    logging.error('Could not import data')
                    return False

            else:
                return False

    def exportCSV(self, filename, database=False):
        """
        Save all signals to CSV-file

        Args:
            filename (str): Filename of backup
            database (bool): If True, signals from database will also be stored.
        """
        if database:
            return self._SQLExportCSV(filename)
        else:
            textfile = ''
            with open((filename + '.csv'), 'w', newline='') as (myfile):
                wr = csv.writer(myfile, quoting=(csv.QUOTE_NONE), delimiter=' ', quotechar='|')
                for sigID in self.signals().keys():
                    signal = self.signals()[sigID]
                    wr.writerow(list(signal[2]))
                    wr.writerow(list(signal[3]))
                    signame = '.'.join(self.getSignalName(sigID))
                    textfile = textfile + signame + ' X\n' + signame + ' Y\n'

            with open(filename + '.txt', 'w') as (myfile):
                myfile.write(textfile)
            return [
             filename + '.csv', filename + '.txt']

    def signalsToCSV(self, sigIDs, filename, xmin=None, xmax=None, database=False):
        """
        Save selected signals to CSV-file

        Args:
            sigIDs (list): List of signalIDs to be stored.
            filename (str): Filename of backup
            xmin (float): minimum x-value of signals to be stored
            xmax (float): maximum x-value of signals to be stored
            database (bool): If True, signals from database will also be stored.
        """
        textfile = ''
        with open((filename + '.csv'), 'w', newline='') as (myfile):
            wr = csv.writer(myfile, quoting=(csv.QUOTE_NONE), delimiter=' ', quotechar='|')
            for sigID in self.signals().keys():
                if sigID in sigIDs:
                    signal = self.signals()[sigID]
                    signal = self.getSignal(sigID, xmin, xmax, database)
                    wr.writerow(list(signal[2]))
                    wr.writerow(list(signal[3]))
                    signame = '.'.join(self.getSignalName(sigID))
                    textfile = textfile + signame + ' X\n' + signame + ' Y\n'

        with open(filename + '.txt', 'w') as (myfile):
            myfile.write(textfile)

    def getGlobalXmin(self, database=True, fast=False):
        """
        Returns the minimum timestamp of all data

        Args:
            database (bool): If True, the minimum timestamp will be searched in database (slow)
            fast (bool): If True, the stored value will be returned, which is much faster, but not as accurate.

        Returns:
            float
        """
        if fast:
            return self._startTime
        else:
            if self.logger.config['postgresql']['active']:
                if database:
                    ans = self._execute_n_fetchall('select X[1] from ' + SIGNAL_TABLE_NAME)
                    if ans != []:
                        if ans is not None:
                            for idx, i in enumerate(ans):
                                if i[0] != None:
                                    ans[idx] = float(i[0])
                                else:
                                    ans[idx] = time.time()

                            for idx, a in enumerate(ans):
                                if a < 10000:
                                    ans[idx] = time.time()

                            ans = min(ans)
                    ans = time.time()
            else:
                ans = time.time()
            try:
                with localLock:
                    xdata = list(self._signals.values())
                    x_local = column(xdata, 2)
                    x_local = [x for l in list(x_local) for x in l]
                    if list(x_local) != []:
                        ans = min(min(list(x_local)), ans)
            except Exception:
                logging.warning('Could not get local xmin, because _signals are in use')

            return ans

    def getGlobalXmax(self, database=True, fast=False):
        """
        Returns the maximum timestamp of all data

        Args:
            database (bool): If True, the maximum timestamp will be searched in database (slow)
            fast (bool): If True, time.time() will be returned, which is much faster, but not accurate.

        Returns:
            float
        """
        if fast:
            return time.time()
        else:
            if self.logger.config['postgresql']['active']:
                if database:
                    ans = self._execute_n_fetchall('select X[array_upper(X,1)] from ' + SIGNAL_TABLE_NAME)
                    if ans != []:
                        if ans is not None:
                            for idx, i in enumerate(ans):
                                if i[0] != None:
                                    ans[idx] = float(i[0])
                                else:
                                    ans[idx] = 0

                            ans = max(ans)
                    ans = time.time()
            else:
                ans = time.time()
            try:
                with localLock:
                    xdata = list(self._signals.values())
                    x_local = column(xdata, 2)
                    x_local = [x for l in list(x_local) for x in l]
                    if list(x_local) != []:
                        ans = max(max(list(x_local)), ans)
            except Exception:
                logging.warning('Could not get local xmax, because _signals are in use')

            return ans

    def getSignalInfo(self, sigID, database=True):
        """
        Returns the minimum, maximum timestamp and signalLength of a given signal

        Args:
            sigID (int)
            database (bool): If True, the signal will be loaded from database to calculate info.

        Returns:
            xmin (float)

            xmax (float)

            sigLen (float)
        """
        xmin = time.time()
        xmax = xmin
        sigLen = 0
        if self.logger.config['postgresql']['active']:
            if database:
                xmin = self._execute_n_fetchall('select X[1] from ' + SIGNAL_TABLE_NAME + ' where ID = ' + str(sigID))
                if xmin != []:
                    if xmin is not None:
                        xmin = xmin[0][0]
                    else:
                        xmin = time.time()
                else:
                    xmax = self._execute_n_fetchall('select X[array_upper(X,1)] from ' + SIGNAL_TABLE_NAME + ' where ID = ' + str(sigID))
                    if xmax != []:
                        if xmax is not None:
                            xmax = xmax[0][0]
                    xmax = time.time() + 100
                sigLen = self._execute_n_fetchall('select array_upper(X,1) from ' + SIGNAL_TABLE_NAME + ' where ID = ' + str(sigID) + '')
                if sigLen is not None and sigLen != []:
                    sigLen = sigLen[0][0]
                    if sigLen == None:
                        sigLen = 0
                else:
                    sigLen = 0
        signal = self.getSignal(sigID)
        if signal is not None:
            if len(signal[2]) > 0:
                xminLocal = min(signal[2])
                xmaxLocal = max(signal[2])
                sigLenLocal = len(list(signal[2]))
                xmin = min([xminLocal, xmin])
                xmax = max([xmaxLocal, xmax])
                sigLen = max([sigLenLocal, sigLen])
        if xmin is None or xmax is None or sigLen is None:
            return (0, 0, 0)
        else:
            return (
             float(xmin), float(xmax), int(sigLen))

    def removeSignal(self, sigID, xmin=None, xmax=None, database=False):
        """
        Removes data from a given signal in between xmin and xmax. If the range from xmin to xmax is bigger than the signal-range, the whole signal will be removed.

        Args:
            sigID (int)
            xmin (float): Minimum timestamp of data to be deleted.
            xmax (float): Maximum timestamp of data to be deleted.
            database (bool): If True, the signal will be removed from database.
        """
        logging.info('Deleting signal {}'.format(sigID))
        if xmin == None or xmax == None:
            if sigID in self._signals.keys():
                self._signals.pop(sigID)
            else:
                if not database:
                    return False
                self.removeEvents(sigID, None, None, database)
                if database:
                    ans = self._execute_n_commit('DELETE from ' + SIGNAL_TABLE_NAME + ' where ID = ' + str(sigID))
        else:
            self.removeEvents(sigID, xmin, xmax, database)
            if sigID in self._signals.keys():
                signal = copy.deepcopy(self._signals[sigID])
                idxmin = 0
                idxmax = len(list(signal[2]))
                for idx, x in enumerate(signal[2]):
                    if x > xmin:
                        idxmin = idx
                        break

                for idx, x in enumerate(signal[2]):
                    if x > xmax:
                        idxmax = idx
                        break

                if idxmin == 0:
                    if idxmax == len(signal[2]):
                        self.removeSignal(sigID, None, None, database)
                        return
                signal[2] = list(signal[2])[0:idxmin] + list(signal[2])[idxmax:]
                signal[3] = list(signal[3])[0:idxmin] + list(signal[3])[idxmax:]
                signal[2] = deque(signal[2], self.config['global']['recordLength'])
                signal[3] = deque(signal[3], self.config['global']['recordLength'])
                self._signals[sigID] = signal
            else:
                if not database:
                    return False
        if database:
            signal = list(self.getSignal(sigID, xmin, xmax, database))
            if signal != None:
                if signal != []:
                    idxmin = 0
                    idxmax = len(list(signal[2]))
                    for idx, x in enumerate(signal[2]):
                        if x > xmin:
                            idxmin = idx
                            break

                    for idx, x in enumerate(signal[2]):
                        if x > xmax:
                            idxmax = idx
                            break

                    if idxmin == 0:
                        if idxmax == len(signal[2]):
                            self.removeSignal(sigID, None, None, database)
                            return
                    signal[2] = list(signal[2])[0:idxmin] + list(signal[2])[idxmax:]
                    signal[3] = list(signal[3])[0:idxmin] + list(signal[3])[idxmax:]
                    name = self.getSignalName(sigID)
                    print('Editing ' + '.'.join(name) + ' from database. New length: ' + str(len(signal[2])))
                    self._SQLplotNewData(signal[2], signal[3], signal[4], name[0], name[1])

    def removeEvent(self, evID, database=False):
        """
        Removes a single event with given evID.

        Args:
            evID (int)
            database (bool): If True, the event will be removed from database.
        """
        if evID in self._events.keys():
            self._events.pop(evID)
            return database or True
        else:
            if not database:
                return False
            if database is True:
                ans = self._execute_n_commit('DELETE from ' + EVENT_TABLE_NAME + ' where ID = ' + str(evID) + '')
            print('event has been deleted')
            return ans

    def removeEvents(self, sigID, xmin=None, xmax=None, database=True):
        """
        Removes events from a given signal in between xmin and xmax.

        Args:
            sigID (int)
            xmin (float): Minimum timestamp of data to be deleted.
            xmax (float): Maximum timestamp of data to be deleted.
            database (bool): If True, the signal will be removed from database.
        """
        if xmin == None:
            xmin = 0
        else:
            if xmax == None:
                xmax = time.time() * 2
            del_eventIDs = []
            for evID in self._events.keys():
                event = self._events[evID]
                if event[1] == sigID and event[4] < xmax and event[4] > xmin:
                    del_eventIDs.append(evID)

            for evID in del_eventIDs:
                self._events.pop(evID)

            if database is True:
                ans = self._execute_n_commit('DELETE from ' + EVENT_TABLE_NAME + ' where SIGNAL_ID = ' + str(sigID) + ' and TIME >' + str(xmin) + ' and TIME < ' + str(xmax))
                logging.info(ans)
                logging.info('Events from Signal: {} have been deleted. Database: {}'.format(sigID, database))

    def getSignal(self, sigID, xmin=None, xmax=None, database=False, maxN=None, returnID=True):
        """
        Returns signal with given sigID in between xmin and xmax.

        Args:
            sigID (int)
            xmin (float): Minimum timestamp of data to be returned.
            xmax (float): Maximum timestamp of data to be returned.
            database (bool): If True, the signal will be returned from database.
            maxN (int): Signal will be filtered, that the signal-length has a maximum of n
        """
        if xmax == None:
            xmax = float(time.time()) * 2
        elif xmin == None:
            xmin = -xmax
        else:
            signal = None
            if self.logger.config['postgresql']['active']:
                if database:
                    signal = self._getSQLSignal(sigID, None, xmin=xmin, xmax=xmax, maxN=maxN)
                    if signal == None:
                        logging.warning('Could not find {} in database'.format(sigID))
                        database = False
            if sigID in self._signals:
                signal_local = list(self._signals[sigID])
                if signal is None:
                    signal = signal_local
                else:
                    overlapping = False
                if len(list(signal_local[2])) > 0:
                    for idx, x in enumerate(signal[2]):
                        if signal_local[2][0] < x:
                            overlapping = True
                            signal[2] = signal[2][:idx] + list(signal_local[2])
                            signal[3] = signal[3][:idx] + list(signal_local[3])
                            break

                    if not overlapping:
                        for idx, x in enumerate(signal_local[2]):
                            if x > signal[2][(-1)]:
                                signal[2] += list(signal_local[2])[idx:]
                                signal[3] += list(signal_local[3])[idx:]
                                break

        if signal is not None:
            if len(signal[2]) == 0:
                return
            else:
                xMin = min(signal[2])
                xMax = max(signal[2])
                for idx, x in enumerate(signal[2]):
                    if x > xmin:
                        signal[2] = list(signal[2])[idx:]
                        signal[3] = list(signal[3])[idx:]
                        break

                for idx, x in enumerate(signal[2]):
                    if x > xmax:
                        signal[2] = list(signal[2])[0:idx - 1]
                        signal[3] = list(signal[3])[0:idx - 1]
                        break

                if maxN != None and type(maxN) == int or type(maxN) == float:
                    maxN = int(maxN)
                    if len(signal[2]) > maxN:
                        overRatio = int(len(signal[2]) / maxN)
                        newX = []
                        newY = []
                        for idx, i in enumerate(signal[2]):
                            if idx % overRatio == 0:
                                newX.append(signal[2][idx])
                                newY.append(signal[3][idx])

                        signal[2] = newX
                        signal[3] = newY
                if returnID:
                    signal = [
                     *signal, sigID, xMin, xMax]
            return signal
        else:
            return

    def getSignal_byName(self, devicename, signalname, xmin=None, xmax=None, database=False, maxN=None):
        """
        Returns signal with given devicename and signalname in between xmin and xmax.

        Args:
            devicename (str)
            signalname (str)
            xmin (float): Minimum timestamp of data to be returned.
            xmax (float): Maximum timestamp of data to be returned.
            database (bool): If True, the signal will be returned from database.
            maxN (int): Signal will be filtered, that the signal-length has a maximum of n
        """
        devID = self.getDeviceID(devicename)
        if devID == -1:
            return
        else:
            sigID = self.getSignalID(devicename, signalname)
            if sigID == -1:
                return
            return self.getSignal(sigID, xmin=xmin, xmax=xmax, database=database, maxN=maxN)

    def _getSQLSignal(self, id, length=None, xmin=None, xmax=None, maxN=None):
        if maxN != None or xmin != None or xmax != None:
            logging.warning('!!! Reading of database is not optimized for specific timerange and maxN !!!')
        else:
            if type(id) == str:
                if len(id.split('.')) == 2:
                    devicename, signalname = id.split('.')
                    id = self.getSignalId(devicename, signalname)
                else:
                    return
            else:
                if length is not None:
                    sigLen = self._execute_n_fetchall('select array_upper(X,1) from ' + SIGNAL_TABLE_NAME + ' where ID = ' + str(id) + '')
                    if sigLen is not None and sigLen != []:
                        sigLen = sigLen[0][0]
                        if sigLen == None:
                            return
                    else:
                        return
                    if length > sigLen:
                        length = sigLen
                    lower = sigLen - length + 1
                    upper = sigLen
                    lenstr = '[' + str(lower) + ':' + str(upper) + ']'
                    ans = self._execute_n_fetchall('select X' + lenstr + ',Y' + lenstr + ' from ' + SIGNAL_TABLE_NAME + ' where ID = ' + str(id))
                else:
                    ans = self._execute_n_fetchall('select X,Y from ' + SIGNAL_TABLE_NAME + ' where ID = ' + str(id))
            if ans != [] and ans is not None:
                ans = ans[0]
                ans = [list(i) for i in ans]
                ans[0] = [float(i) for i in ans[0]]
                ans[1] = [float(i) for i in ans[1]]
            else:
                return
        ans2 = self._execute_n_fetchall('select DEVICE_ID, NAME, UNIT from ' + SIGNAL_TABLE_NAME + ' where ID = ' + str(id))[0]
        return [ans2[0], ans2[1], ans[0], ans[1], ans2[2]]

    def getUniqueEvents(self, database=False):
        """
        Returns a dictonary with all unique events.

        Args:
            database (bool): Loads events from database
        """
        unique = {}
        for evID in self._events.keys():
            event = self._events[evID]
            if event[2] not in unique.keys():
                unique[event[2]] = event

        if self.logger.config['postgresql']['active']:
            if database:
                strung = 'select DEVICE_ID, SIGNAL_ID, EVENT_ID, TEXT, TIME, VALUE,PRIORITY, ID  from ' + EVENT_TABLE_NAME
                base_events = self._execute_n_fetchall(strung)
                if base_events is not None:
                    if base_events != []:
                        base_events = {i[7]:list(i) for i in base_events}
                        for evID in base_events.keys():
                            base_events[evID][4] = float(base_events[evID][4])
                            if base_events[evID][2] not in unique.keys():
                                unique[base_events[evID][2]] = base_events[evID]

        return unique

    def getUniqueUnits(self, database=False):
        """
        Returns a list with all unique units.

        Args:
            database (bool): Loads units from database
        """
        unique = []
        for sigID in self._signals.keys():
            if self._signals[sigID][4] not in unique and self._signals[sigID][4] != '':
                unique.append(self._signals[sigID][4])

        if self.logger.config['postgresql']['active']:
            if database:
                strung = 'select UNIT from ' + SIGNAL_TABLE_NAME
                units = self._execute_n_fetchall(strung)
                if units is not None:
                    if units != []:
                        units = [i[0] for i in units]
                        for unit in units:
                            if unit not in unique and unit != '':
                                unique.append(unit)

        return unique

    def resampleDatabase(self, samplerate):
        """
        Will resample all signals in database with given samplerate

        Args:
            samplerate (float): Desired samplerate for signals

        Returns:
            bool: True, if successfull, False, if nothing to resample
        """
        signals = self._execute_n_fetchall('select ID, X, Y from ' + SIGNAL_TABLE_NAME)
        if signals is not None and signals != []:
            signals = {signal[0]:list(signal)[1:] for signal in signals}
            for sigID in signals.keys():
                signals[sigID][0] = [float(i) for i in signals[sigID][0]]
                signals[sigID][1] = [float(i) for i in signals[sigID][1]]
                s = signals[sigID]
                if len(s[0]) > 2:
                    xrange = s[0][(-1)] - s[0][0]
                    n = samplerate * float(xrange)
                    if len(s[0]) == len(s[1]):
                        x = np.linspace(float(s[0][0]), float(s[0][(-1)]), n)
                        y = np.interp(x, s[0], s[1])
                        self._SQLplot(x=x, y=y, sigID=sigID)

            self.clear()
            return True
        else:
            return False


def saveUserInput(self, strung):
    """
    UNUSED
    """
    strung.replace('.', '_')
    strung.replace(':', '_')
    strung.replace(';', '_')
    strung.replace(',', '_')
    return strung


def column(matrix, i):
    """
    Returns eevery i-th element in array [[i1,...],[i2,...]...]
    """
    ans = []
    for row in list(matrix):
        if (type(row) == list or type(row) == deque) and i < len(list(row)):
            ans.append(row[i])

    return ans


def resample(x, y, samplerate):
    if len(x) == len(y) and len(x) > 0:
        xtime = x[(-1)] - x[0]
        n = samplerate * xtime
        x2 = np.linspace(x[0], x[(-1)], n)
        y = np.interp(x2, x, y)
        return (
         list(x2), list(y))
    else:
        return (
         x, y)