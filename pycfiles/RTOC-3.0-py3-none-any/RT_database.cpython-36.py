# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Benutzer\haschtl\Dokumente\GIT\kellerlogger\RTOC\RTLogger\RT_database.py
# Compiled at: 2019-05-13 13:12:30
# Size of source mod 2**32: 41804 bytes
import psycopg2, time, os, json, hashlib, psutil, logging as log
from threading import Thread, Lock
log.basicConfig(level=(log.DEBUG))
logging = log.getLogger(__name__)
try:
    from whaaaaat import style_from_dict, Token, prompt
    style = style_from_dict({Token.Separator: '#6C6C6C', 
     Token.QuestionMark: '#FF9D00 bold', 
     Token.Selected: '#5F819D', 
     Token.Pointer: '#FF9D00 bold', 
     Token.Instruction: '', 
     Token.Answer: '#5F819D bold', 
     Token.Question: ''})
except ImportError:
    logging.error('"whaaaaat" is not installed. Please install with "pip3 install whaaaaat" to use the console')
    prompt = None

DEVICE_TABLE_NAME = 'devices'
SIGNAL_TABLE_NAME = 'signals'
EVENT_TABLE_NAME = 'events'
lock = Lock()

class RT_database:

    def __init__(self, logger=None, localLength=None):
        self.logger = logger
        if logger is not None:
            self.config = logger.config
            self.connect_callbacks()
            logging.info('RT_database connected to RTLogger')
        else:
            logging.info('RT_database not connected to RTLogger')
            self.callback = None
            self.newSignalCallback = None
            self.newEventCallback = None
            self.handleScriptCallback = None
            self.recordingLengthChangedCallback = None
            self.reloadSignalsGUICallback = None
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
        if localLength is not None:
            self.config['postgresql']['localLength'] = localLength
        self._RT_database__signals = []
        self._RT_database__devices = {}
        self._RT_database__signalNames = []
        self._RT_database__signalUnits = []
        self._RT_database__signalIDs = []
        self._RT_database__events = []
        self.newEvents = True
        self.run = False
        self.connection = None
        self.cursor = None
        self.status = 'not connected'
        ok = self.connect()
        if ok:
            dev, sig, ev = self.checkDatabases()
            self.clear(not dev, not sig, not ev)
            ids, names, units = self.updateLocalSignalData()
            self._RT_database__signalIDs = ids
            self._RT_database__signalNames = names
            self._RT_database__signalUnits = units
            self._RT_database__signals = self.updateLocalSignals()
            self._RT_database__events = self.updateLocalEvents()

    def start(self):
        self.run = True
        self.updateOpts = [True, True, True]
        if self.config['postgresql']['service_updateRate'] != 0:
            self.updateT = Thread(target=(self._RT_database__updateT))
            self.updateT.start()
        else:
            logging.warning('Database-service is enabled, but updateRate was set to zero! Will not update database')

    def stop(self):
        self.run = False

    def __updateT(self):
        diff = 1 / self.config['postgresql']['service_updateRate'] + 1
        while self.run:
            if diff < 1 / self.config['postgresql']['service_updateRate']:
                time.sleep(1 / self.config['postgresql']['service_updateRate'] - diff)
            start_time = time.time()
            (self.update)(*self.updateOpts)
            diff = time.time() - start_time

    def connect_callbacks(self):
        self.callback = self.logger.callback
        self.newSignalCallback = self.logger.newSignalCallback
        self.newEventCallback = self.logger.newEventCallback
        self.handleScriptCallback = self.logger.handleScriptCallback
        self.recordingLengthChangedCallback = self.logger.recordingLengthChangedCallback
        self.reloadSignalsGUICallback = self.logger.reloadSignalsGUICallback

    def connect(self):
        try:
            self.connection = psycopg2.connect(user=(self.config['postgresql']['user']),
              password=(self.config['postgresql']['password']),
              host=(self.config['postgresql']['host']),
              port=(self.config['postgresql']['port']),
              database=(self.config['postgresql']['database']))
            self.cursor = self.connection.cursor()
            self.execute_n_fetchall('SELECT version();')
            self.status = 'connected'
            return True
        except (Exception, psycopg2.Error) as error:
            logging.error('Error while connecting to PostgreSQL', error)
            self.status = 'could not connect'
            self.connection = None
            self.cursor = None
            return False

    def createDevicesTable(self):
        create_table_query = 'CREATE TABLE ' + DEVICE_TABLE_NAME + '\n          (ID SERIAL PRIMARY KEY     UNIQUE NOT NULL,\n          NAME          TEXT   UNIQUE NOT NULL,\n          CREATION_DATE REAL   NOT NULL); '
        if self.execute(create_table_query):
            logging.info('Initialized devices table')

    def createSignalsTable(self):
        create_table_query = 'CREATE TABLE ' + SIGNAL_TABLE_NAME + '\n          (ID SERIAL PRIMARY KEY     UNIQUE NOT NULL,\n          DEVICE_ID INT      NOT NULL,\n          NAME      TEXT    NOT NULL,\n          X           NUMERIC[],\n          Y         NUMERIC[],\n          UNIT      TEXT,\n          CREATION_DATE REAL   NOT NULL,\n          CONSTRAINT signal_device_id_fkey FOREIGN KEY (DEVICE_ID)\n              REFERENCES ' + DEVICE_TABLE_NAME + ' (ID) MATCH SIMPLE\n              ON UPDATE NO ACTION ON DELETE NO ACTION\n          ); '
        if self.execute(create_table_query):
            logging.info('Initialized signals table')

    def createEventsTable(self):
        create_table_query = 'CREATE TABLE ' + EVENT_TABLE_NAME + '\n          (ID SERIAL PRIMARY KEY    UNIQUE NOT NULL,\n          DEVICE_ID INT       NOT NULL,\n          SIGNAL_ID INT      NOT NULL,\n          EVENT_ID TEXT      NOT NULL,\n          TEXT   TEXT   NOT NULL,\n          TIME NUMERIC   NOT NULL,\n          VALUE TEXT,\n          PRIORITY INT NOT NULL,\n          CONSTRAINT event_device_id_fkey FOREIGN KEY (DEVICE_ID)\n              REFERENCES ' + DEVICE_TABLE_NAME + ' (ID) MATCH SIMPLE\n              ON UPDATE NO ACTION ON DELETE NO ACTION,\n          CONSTRAINT event_signal_id_fkey FOREIGN KEY (SIGNAL_ID)\n              REFERENCES ' + SIGNAL_TABLE_NAME + ' (ID) MATCH SIMPLE\n              ON UPDATE NO ACTION ON DELETE NO ACTION\n          ); '
        if self.execute(create_table_query):
            logging.info('Initialized events table')

    def checkDatabases(self):
        table = DEVICE_TABLE_NAME
        existtest = "SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = '" + table + "' );"
        dev = self.execute_n_fetchall(existtest)[0]
        table = SIGNAL_TABLE_NAME
        existtest = "SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = '" + table + "' );"
        sig = self.execute_n_fetchall(existtest)[0]
        table = EVENT_TABLE_NAME
        existtest = "SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = '" + table + "' );"
        ev = self.execute_n_fetchall(existtest)[0]
        return (
         dev[0], sig[0], ev[0])

    def execute(self, query):
        if self.execute_n_commit(query):
            logging.info('Table created successfully in PostgreSQL ')

    def execute_n_fetchall(self, query):
        if self.cursor is not None:
            with lock:
                try:
                    self.connection.commit()
                    self.cursor.execute(query)
                    ans = self.cursor.fetchall()
                except (Exception, psycopg2.DatabaseError) as error:
                    if str(error) != 'connection already closed':
                        logging.info('Error while execution+fetch in PostgreSQL table')
                        logging.error(error)
                        logging.error(query)
                    ans = None

            return ans

    def execute_n_commit(self, query):
        if self.cursor is not None:
            with lock:
                try:
                    self.connection.commit()
                    self.cursor.execute(query)
                    self.connection.commit()
                    ans = True
                except (Exception, psycopg2.DatabaseError) as error:
                    if str(error) != 'connection already closed':
                        logging.info('Error while execution+commit in PostgreSQL table')
                        logging.error(error)
                        logging.error(query)
                    ans = False

            return ans

    def update(self, dat, sig, ev):
        if dat:
            ids, names, units = self.updateLocalSignalData()
        else:
            if sig:
                signals = self.updateLocalSignals()
            else:
                if ev:
                    events = self.updateLocalEvents()
                if dat:
                    self._RT_database__signalIDs = ids
                    self._RT_database__signalNames = names
                    self._RT_database__signalUnits = units
                if sig:
                    self._RT_database__signals = signals
            if ev:
                self._RT_database__events = events

    def updateLocalSignals(self):
        t_signals = []
        sigLen = self.config['postgresql']['localLength']
        for id in self._RT_database__signalIDs:
            t_signals.append(self.getSignal(id, sigLen, True))

        return t_signals

    def updateLocalEvents(self):
        numEvents = self.config['postgresql']['localLength']
        if numEvents is None:
            strung = 'select TIME, TEXT, PRIORITY, VALUE, EVENT_ID, DEVICE_ID, SIGNAL_ID, ID  from ' + EVENT_TABLE_NAME
        else:
            strung = 'select TIME, TEXT, PRIORITY, VALUE, EVENT_ID, DEVICE_ID, SIGNAL_ID, ID  from ' + EVENT_TABLE_NAME + ' LIMIT ' + str(numEvents)
        ans = self.execute_n_fetchall(strung)
        if ans is not None:
            if ans != []:
                ans = [list(i) for i in ans]
                for idx, element in enumerate(ans):
                    ans[idx][0] = float(ans[idx][0])
                    ans[idx][5], ans[idx][6] = self.getSignalNames(element[6], True)

        else:
            ans = []
        return ans

    def updateLocalSignalData(self):
        devIds = self.execute_n_fetchall('select ID, NAME from ' + DEVICE_TABLE_NAME)
        if devIds is not None:
            if devIds != []:
                devIds = {i[0]:i[1] for i in devIds}
                self._RT_database__devices = devIds
        else:
            devIds = {}
        sigIds = self.execute_n_fetchall('select ID, NAME, DEVICE_ID, UNIT from ' + SIGNAL_TABLE_NAME)
        if sigIds is not None and sigIds != []:
            _RT_database__signalIDs = [i[0] for i in sigIds]
            _RT_database__signalNames = [[self._RT_database__devices[i[2]], i[1]] for i in sigIds]
            _RT_database__signalUnits = [i[3] for i in sigIds]
            return (
             _RT_database__signalIDs, _RT_database__signalNames, _RT_database__signalUnits)
        else:
            return ([], [], [])

    def devices(self):
        return self._RT_database__devices

    def signals(self, force=False):
        ans = self.execute_n_fetchall('select X, Y from ' + SIGNAL_TABLE_NAME)
        if ans is not None:
            if ans != []:
                ans = [list(i) for i in ans]
                for sig in ans:
                    sig[0] = [float(i) for i in sig[0]]
                    sig[1] = [float(i) for i in sig[1]]

        else:
            ans = []
        return ans

    def events(self, force=False):
        if self.run:
            if not force:
                return self._RT_database__events
        self._RT_database__events = self.updateLocalEvents()
        print(self._RT_database__events)
        return self._RT_database__events

    def signalIDs(self, force=False):
        if self.run:
            if not force:
                return self._RT_database__signalIDs
        else:
            sigID = self.execute_n_fetchall('select ID from ' + SIGNAL_TABLE_NAME)
            if sigID is not None:
                if sigID != []:
                    sigID = [float(i[0]) for i in sigID]
                    self._RT_database__signalIDs = sigID
            sigID = []
        return sigID

    def signalNames(self, force=False):
        if self.run:
            if not force:
                return self._RT_database__signalNames
        devIds = self.execute_n_fetchall('select ID, NAME from ' + DEVICE_TABLE_NAME)
        if devIds is not None:
            if devIds != []:
                devIds = {i[0]:i[1] for i in devIds}
                self._RT_database__devices = devIds
        sigIds = self.execute_n_fetchall('select ID, NAME, DEVICE_ID, UNIT from ' + SIGNAL_TABLE_NAME)
        if sigIds is not None and sigIds != []:
            signalNames = [[self._RT_database__devices[i[2]], i[1]] for i in sigIds]
            self._RT_database__signalNames = signalNames
            return signalNames
        else:
            return []

    def signalUnits(self, force=False):
        return self._RT_database__signalUnits

    def printSignals(self):
        ans = self.execute_n_fetchall("select relname from pg_class where relkind='r' and relname !~ '^(pg_|sql_)';")
        print('Print signals:')
        print(ans)

    def getSignalId(self, devicename, dataname, force=False):
        if self.run and not force:
            if [
             devicename, dataname] in self._RT_database__signalNames:
                idx = self._RT_database__signalNames.index([devicename, dataname])
                if idx != -1:
                    id = self._RT_database__signalIDs[idx]
                else:
                    id = -1
            else:
                id = -1
            return id
        else:
            devID = self.getDeviceID(devicename, True)
            sigID = self.execute_n_fetchall('select ID from ' + SIGNAL_TABLE_NAME + " where NAME = '" + dataname + "' and DEVICE_ID =" + str(devID))
            if sigID is not None:
                if sigID != []:
                    sigID = sigID[0][0]
            else:
                sigID = -1
            return sigID

    def getDeviceID(self, devicename, force=False):
        if force:
            devId = self.execute_n_fetchall('select ID from ' + DEVICE_TABLE_NAME + " where NAME = '" + str(devicename) + "'")
            if devId is not None:
                if devId != []:
                    devId = devId[0][0]
            else:
                devId = -1
            return devId
        else:
            if devicename in self._RT_database__devices.values():
                id = list(self._RT_database__devices)[list(self._RT_database__devices.values()).index(devicename)]
            else:
                id = -1
            return id

    def getDeviceName(self, deviceid):
        if deviceid in self._RT_database__devices.keys():
            return self._RT_database__devices[deviceid]
        else:
            return

    def getSignal(self, id, length=None, force=False):
        if self.run:
            if id in self._RT_database__signalIDs:
                if not force:
                    idx = self._RT_database__signalIDs.index(id)
                    if idx < len(self._RT_database__signals) and idx >= 0:
                        a = list(self._RT_database__signals[idx])
                        return a
                    else:
                        return [[], []]
        else:
            if type(id) == str:
                if len(id.split('.')) == 2:
                    devicename, dataname = id.split('.')
                    id = self.getSignalId(devicename, dataname)
                else:
                    return
                if length is not None:
                    sigLen = self.execute_n_fetchall('select array_upper(X,1) from ' + SIGNAL_TABLE_NAME + ' where ID = ' + str(id) + '')
                    if sigLen is not None and sigLen != []:
                        sigLen = sigLen[0][0]
                        if sigLen == None:
                            return [[], []]
                    else:
                        return [[], []]
                    if length > sigLen:
                        length = sigLen
                    lower = sigLen - length + 1
                    upper = sigLen
                    lenstr = '[' + str(lower) + ':' + str(upper) + ']'
                    ans = self.execute_n_fetchall('select X' + lenstr + ',Y' + lenstr + ' from ' + SIGNAL_TABLE_NAME + ' where ID = ' + str(id) + '')
                else:
                    ans = self.execute_n_fetchall('select X,Y from ' + SIGNAL_TABLE_NAME + ' where ID = ' + str(id) + '')
            elif ans != [] and ans is not None:
                ans = ans[0]
                ans = [list(i) for i in ans]
                ans[0] = [float(i) for i in ans[0]]
                ans[1] = [float(i) for i in ans[1]]
            else:
                ans = [[], []]
            return ans

    def getSignalUnits(self, ids):
        if type(ids) != list:
            ids = [
             ids]
        ans = []
        for id in ids:
            if type(id) == str:
                if len(id.split('.')) == 2:
                    devicename, dataname = id.split('.')
                    id = self.getSignalId(devicename, dataname)
                else:
                    return
            ans2 = self.execute_n_fetchall('select UNIT from ' + SIGNAL_TABLE_NAME + ' where ID = ' + str(id) + '')
            ans += ans2[0]

        if len(ans) == 1:
            ans = ans[0]
        return ans

    def deviceExists(self, devicename):
        existtest = 'SELECT EXISTS (select ID from ' + DEVICE_TABLE_NAME + " where NAME = '" + str(devicename) + "');"
        sig = self.execute_n_fetchall(existtest)
        if sig is not None:
            if sig != []:
                sig = bool(sig[0][0])
        else:
            sig = False
        return sig

    def signalExists(self, signalname, devicename):
        name = 'select ID from ' + DEVICE_TABLE_NAME + " where NAME = '" + str(devicename) + "'"
        ans = self.execute_n_fetchall(name)
        if ans is None or ans == []:
            return False
        else:
            devID = ans[0][0]
            existtest = 'SELECT EXISTS (select ID from ' + SIGNAL_TABLE_NAME + " where NAME = '" + str(signalname) + "' and DEVICE_ID = " + str(devID) + ');'
            sig = self.execute_n_fetchall(existtest)
            if sig:
                sig = bool(sig[0][0])
            else:
                sig = False
            return sig

    def getSignalNames(self, ids, force=False):
        if not self.run or force:
            id, names, units = self.updateLocalSignalData()
            self._RT_database__signalIDs = id
            self._RT_database__signalNames = names
            self._RT_database__signalUnits = units
        else:
            if type(ids) != list:
                ids = [
                 ids]
            ans = []
            for id in ids:
                idx = self._RT_database__signalIDs.index(id)
                if idx != -1:
                    name = self._RT_database__signalNames[idx]
                    ans.append(name)
                else:
                    ans.append(['Not', 'found'])

            if len(ans) == 1:
                ans = ans[0]
        return ans

    def getSignalSize(self):
        obj_Disk = psutil.disk_usage('/')
        total = round(obj_Disk.total / 1073741824.0, 3)
        used = round(obj_Disk.used / 1073741824.0, 3)
        return (
         used, total)

    def getEvents(self, signal_id):
        sql = 'select TIME, TEXT, PRIORITY, VALUE, ID from ' + EVENT_TABLE_NAME + ' where SIGNAL_ID = ' + str(signal_id) + ';'
        ans = self.execute_n_fetchall(sql)
        if ans != [] and ans is not None:
            events_sorted = [[], [], [], [], []]
            for i in ans:
                for idx, j in enumerate(list(i)):
                    events_sorted[idx].append(j)

            return events_sorted
        else:
            ans = [[], [], [], [], []]
            return ans

    def getLatest(self, force=False):
        ans = {}
        ans['latest'] = {}
        for dev in self.signalNames(force):
            sig = self.getSignal(self.getSignalId(dev[0], dev[1], force), 1, force)
            if sig is not None and sig != [] and len(sig[0]) > 0:
                ans['latest']['.'.join(dev)] = [
                 sig[0][(-1)], sig[1][(-1)]]

        return ans

    def getEventList(self, force=False):
        ans = {}
        ans['events'] = {}
        if self.run:
            if not force:
                for ev in self._RT_database__events:
                    signame = ev[5] + '.' + ev[6]
                    if signame not in ans['events'].keys():
                        ans['events'][signame] = []
                    ans['events'][signame].append([float(ev[0]), ev[1], ev[2], ev[3], ev[4]])

        else:
            for name in self.signalNames():
                sig = self.getEvents(self.getSignalId(name[0], name[1]))
                if sig != [[], [], [], [], []]:
                    ans['events']['.'.join(name)] = []
                    if len(sig[0]) > 0:
                        for idx, s in enumerate(sig[0]):
                            ans['events']['.'.join(name)].append([
                             float(sig[0][idx]), sig[1][idx], sig[2][idx], sig[3][idx], sig[4][idx]])

        return ans

    def renameSignal(self, id, signame):
        sql = '\nUPDATE ' + SIGNAL_TABLE_NAME + " SET NAME = '" + str(signame) + "' WHERE ID =" + str(id) + ';'
        self.execute_n_commit(sql)

    def clear(self, dev=True, sig=True, ev=True):
        d, s, e = self.checkDatabases()
        if dev is True:
            ev = True
        if self.cursor is not None:
            with lock:
                if e is True:
                    if ev is True:
                        self.cursor.execute('DROP TABLE ' + EVENT_TABLE_NAME + ' CASCADE;')
                        logging.info('Deleting events table')
                    if s is True:
                        if sig is True:
                            self.cursor.execute('DROP TABLE ' + SIGNAL_TABLE_NAME + ' CASCADE;')
                            logging.info('Deleting signals table')
                else:
                    if d is True:
                        if dev is True:
                            self.cursor.execute('DROP TABLE ' + DEVICE_TABLE_NAME + ' CASCADE;')
                            logging.info('Deleting devices table')
                self.connection.commit()
            if dev is True:
                self.createDevicesTable()
            if sig is True:
                self.createSignalsTable()
                self._RT_database__signalNames = []
                self._RT_database__signalUnits = []
                self._RT_database__signalIDs = []
                self._RT_database__devices = {}
            if ev is True:
                self.createEventsTable()
                self._RT_database__events = []

    def clearSignals(self, newLength=None):
        print('clearSignals')
        self.clear(dev=False, sig=True, ev=False)

    def removeSignal(self, id):
        ans = self.execute('DELETE FROM ' + SIGNAL_TABLE_NAME + ' WHERE id = ' + str(id) + ';')
        print('removeSignal')
        if ans is False:
            return -1
        else:
            return id

    def addNewData(self, dataY, dataunit, devicename, dataname, dataX=None, createCallback=True, wait=False):
        if dataX is None:
            dataX = time.time()
        else:
            newSignal = False
            sql = ''
            dev = self.deviceExists(devicename)
            if dev is False:
                self.createDevice(devicename)
                sigID = self.createSignal(dataname, devicename, dataX, dataY, dataunit)
                newSignal = True
            else:
                sig = self.signalExists(dataname, devicename)
                if sig is False:
                    sigID = self.createSignal(dataname, devicename, dataX, dataY, dataunit)
                    newSignal = True
                else:
                    sigID = self.getSignalId(devicename, dataname, True)
            sql = 'UPDATE ' + SIGNAL_TABLE_NAME + ' SET X = array_append(X, ' + str(dataX) + '::NUMERIC) WHERE ID =' + str(sigID) + ';'
            sql += '\nUPDATE ' + SIGNAL_TABLE_NAME + ' SET Y = array_append(Y,' + str(dataY) + '::NUMERIC) WHERE ID =' + str(sigID) + ';'
            sql += '\nUPDATE ' + SIGNAL_TABLE_NAME + " SET UNIT = '" + str(dataunit) + "' WHERE ID =" + str(sigID) + ';'
            if not wait:
                self.execute_n_commit(sql)
            if sigID in self._RT_database__signalIDs:
                print('adding to local')
                idx = self._RT_database__signalIDs.index(sigID)
                if idx < len(self._RT_database__signals):
                    self._RT_database__signals[idx][0].append(dataX)
                    self._RT_database__signals[idx][1].append(dataY)
            if newSignal:
                if self.newSignalCallback:
                    self.newSignalCallback(sigID, devicename, dataname, dataunit)
            if self.handleScriptCallback:
                self.handleScriptCallback(devicename, dataname)
            if self.callback:
                if createCallback:
                    self.callback(devicename, dataname)
            if self.config['global']['globalEventsActivated']:
                if self.logger is not None:
                    self.logger.performGlobalEvents(dataY, dataunit, devicename, dataname, dataX)
        return sql

    def createSignal(self, signalname, devicename, x=None, y=None, unit=None):
        dev_id = self.getDeviceID(devicename, True)
        if dev_id != -1:
            logging.info('Creating new signal:' + str(devicename) + '.' + str(signalname))
            timestamp = time.time()
            if x is None:
                x = ''
                y = ''
            else:
                x = ''
                y = ''
            sql = 'INSERT INTO ' + SIGNAL_TABLE_NAME + "(NAME, DEVICE_ID, CREATION_DATE, X, Y, UNIT)\n                    VALUES\n                     ('" + str(signalname) + "'," + str(dev_id) + ',' + str(timestamp) + ',ARRAY[' + str(x) + ']::real[],ARRAY[' + str(y) + "]::real[],'" + str(unit) + "');"
            self.execute_n_commit(sql)
            name = 'select ID from ' + SIGNAL_TABLE_NAME + " where NAME = '" + str(signalname) + "' and DEVICE_ID = " + str(dev_id)
            sigID = self.execute_n_fetchall(name)
            if sigID != [] and sigID is not None:
                sigID = sigID[0][0]
                ids, names, units = self.updateLocalSignalData()
                self._RT_database__signalIDs = ids
                self._RT_database__signalNames = names
                self._RT_database__signalUnits = units
                self._RT_database__signals = self.updateLocalSignals()
            return sigID
        else:
            logging.error('Could not create signal! Device ' + str(devicename) + ' does not exist!')
            return -1

    def createEvent(self, x, strung, devicename, dataname, priority, value, eventid):
        logging.info('Creating new event:' + str(devicename) + '.' + str(dataname))
        devID = self.getDeviceID(devicename, True)
        sigID = self.getSignalId(devicename, dataname, True)
        sql = 'INSERT INTO ' + EVENT_TABLE_NAME + '(TIME, TEXT, DEVICE_ID, SIGNAL_ID, PRIORITY, VALUE, EVENT_ID)\n                VALUES\n                 (' + str(x) + ",'" + str(strung) + "'," + str(devID) + ',' + str(sigID) + ',' + str(priority) + ",'" + str(value) + "','" + str(eventid) + "');"
        self.execute_n_commit(sql)
        name = 'select ID from ' + EVENT_TABLE_NAME + " where EVENT_ID = '" + str(eventid) + "' and DEVICE_ID = " + str(devID) + ' and TIME = ' + str(x)
        evID = self.execute_n_fetchall(name)
        if evID is not None:
            if evID != []:
                evID = evID[0][0]
        else:
            evID = -1
        print(evID)
        return evID

    def createDevice(self, devicename):
        logging.info('Creating new device: ' + str(devicename))
        timestamp = time.time()
        sql = 'INSERT INTO ' + DEVICE_TABLE_NAME + "(NAME, CREATION_DATE)\n                VALUES\n                 ('" + str(devicename) + "'," + str(timestamp) + ');'
        self.execute_n_commit(sql)

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
                sql = ''
                for idx, data in enumerate(datasY):
                    sql += self.addNewData(datasY[idx], units[idx], devicename, datanames[idx], datasX[idx], createCallback, True)

                self.execute_n_commit(sql)
        if type(datasY) == str:
            self.addNewEvent(datasY)

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
                if not self.deviceExists(devicename):
                    self.createDevice(devicename)
                else:
                    if not self.signalExists(dataname, devicename):
                        sigID = self.createSignal(dataname, devicename)
                        self.plotNewData(x, y, dataunit, devicename, dataname, createCallback, hold, autoResize)
                        if self.newSignalCallback:
                            self.newSignalCallback(sigID, devicename, dataname, dataunit)
                    else:
                        self.plotNewData(x, y, dataunit, devicename, dataname, createCallback, hold, autoResize)
            else:
                logging.error('Plotting aborted. len(x)!=len(y)')

    def plotNewData(self, x, y, dataunit, devicename, dataname, createCallback=False, hold='off', autoResize=False):
        sigID = self.getSignalId(devicename, dataname, True)
        if autoResize:
            logging.warning('autoResize is DEPRECATED for postgresql')
        else:
            if hold == 'on':
                sql = 'UPDATE ' + SIGNAL_TABLE_NAME + ' SET X = array_cat(X, ' + str(x) + ') WHERE ID =' + str(sigID) + ';'
                sql += '\nUPDATE ' + SIGNAL_TABLE_NAME + ' SET Y = array_cat(Y,' + str(y) + ') WHERE ID =' + str(sigID) + ';'
                sql += '\nUPDATE ' + SIGNAL_TABLE_NAME + " SET UNIT = '" + str(dataunit) + "' WHERE ID =" + str(sigID) + ';'
            else:
                if hold == 'mergeX':
                    logging.error('mergeX is NOT IMPLEMENTED YET for postgresql')
                else:
                    if hold == 'mergeY':
                        logging.error('mergeY is NOT IMPLEMENTED YET for postgresql')
                    else:
                        sql = 'UPDATE ' + SIGNAL_TABLE_NAME + ' SET X = ARRAY' + str(x) + ' WHERE ID =' + str(sigID) + ';'
                        sql += '\nUPDATE ' + SIGNAL_TABLE_NAME + ' SET Y = ARRAY' + str(y) + ' WHERE ID =' + str(sigID) + ';'
                        sql += '\nUPDATE ' + SIGNAL_TABLE_NAME + " SET UNIT = '" + str(dataunit) + "' WHERE ID =" + str(sigID) + ';'
        self.execute_n_commit(sql)
        if self.handleScriptCallback:
            self.handleScriptCallback(devicename, dataname)
        if self.callback:
            if createCallback:
                self.callback(devicename, dataname)

    def addData(self, data=0, *args, **kwargs):
        logging.error('addData is DEPRECATED since postgresql database')

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
        callback = False
        if not self.deviceExists(devicename):
            self.createDevice(devicename)
        if not self.signalExists(dataname, devicename):
            self.createSignal(dataname, devicename)
            callback = True
        id = self.getSignalId(devicename, dataname, True)
        if x is None:
            x = time.time()
        evID = self.createEvent(x, strung, devicename, dataname, priority, value, id)
        if self.newEventCallback:
            self.newEventCallback(x, strung, devicename, dataname, priority, value, id, evID)
        if self.newSignalCallback:
            if callback:
                if devicename != 'RTOC':
                    self.newSignalCallback(id, devicename, dataname, '')
        if self.config['telegram']['active']:
            if self.logger is not None:
                if self.logger.telegramBot is not None:
                    self.logger.telegramBot.sendEvent(strung, devicename, dataname, priority)
        if self.config['global']['globalActionsActivated']:
            self.logger.performGlobalActions(id, value)

    def close(self):
        self.run = False
        if self.connection:
            self.cursor.close()
            self.connection.close()
            logging.info('PostgreSQL connection is closed')
            self.status = 'not connected'

    def getSignalDict(self):
        print('getSignalDict')
        return {'Generator': {'square': [1000, 0]}}

    def resizeSignals(self, newLength=None):
        if newLength is not None:
            if self.logger is not None:
                self.logger.config['global']['recordLength'] = newLength


def run(logger=None):
    database = RT_database(logger)
    try:
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        if logger is not None:
            logger.stop()
        database.close()


def mainmenu():
    mainmenu = [
     {'type':'list', 
      'name':'mainmenu', 
      'message':'Mainmenu', 
      'choices':[
       'Devices',
       'Signals',
       'Events',
       'Create event/signalClear signals',
       'Clear events',
       'Clear all devices',
       'test',
       'Quit']}]
    main = prompt(mainmenu, style=style)
    return main['mainmenu']


def main():
    database = RT_database()
    ans = ''
    try:
        try:
            while not ans == 'Quit':
                ans = mainmenu()
                if ans == 'Clear signals':
                    database.clear(False, True, False)
                elif ans == 'Clear events':
                    database.clear(False, False, True)
                elif ans == 'Clear all devices':
                    database.clear(True, True, True)
                elif ans == 'Devices':
                    print('Devices:')
                    print(database.devices())
                elif ans == 'Signals':
                    print('Signals:')
                    print(database.signals())
                elif ans == 'test':
                    database.addDataCallback(5, snames='Haus', dname='Baut', unit='hoch')
                    database.addDataCallback(5, snames='Haus', dname='Baut2', unit='hoch')
                    database.addDataCallback(5, snames='Haus2', dname='Baut', unit='hoch')
                    database.addDataCallback(5, snames='Haus3', dname='Baut3', unit='hoch')

        except KeyboardInterrupt:
            logging.info('Terminated by user')

    finally:
        database.close()


if __name__ == '__main__':
    run()