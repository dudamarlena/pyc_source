# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Benutzer\haschtl\Dokumente\GIT\kellerlogger\RTOC\RTLogger\RTWebsocketServer.py
# Compiled at: 2020-01-06 17:26:23
# Size of source mod 2**32: 38865 bytes
import os, traceback, json
from threading import Thread
import time, base64, psutil, ssl
from . import RTWebsocket
from .websocket_server import WebsocketServer
try:
    from PyQt5.QtCore import QCoreApplication
    translate = QCoreApplication.translate
except ImportError:

    def translate(id, text):
        return text


def _(text):
    return translate('web', text)


import logging as log
log.basicConfig(level=(log.INFO))
logging = log.getLogger(__name__)
HOST_WHITELIST = [
 '127.0.0.1', 'localhost']

class RTWebsocketServer(WebsocketServer):
    __doc__ = '\n    This class contains all Websocket-specific functions of RTLogger\n    '

    def __init__(self, parent, port=5050, host='0.0.0.0', password=None):
        print('Starting websocket server at {}:{}'.format(host, port))
        self.setPassword(password)
        sslopts = {}
        if parent.config['websocket']['ssl']:
            cert = parent.config['global']['documentfolder'] + '/' + parent.config['websocket']['certfile']
            key = parent.config['global']['documentfolder'] + '/' + parent.config['websocket']['keyfile']
            if os.path.exists(cert):
                if os.path.exists(key):
                    sslopts = dict(cert=cert, key=key)
                    logging.info('Using SSL Connection')
            logging.info('SSL cert or key not defined')
            logging.error('Run "openssl req -x509 -newkey rsa:4096 -keyout key.pem -out certificate.pem -days 365 -nodes" and add the pathes of the cert and key file in the .RTOC/config.json')
        else:
            logging.warning('You should consider using SSL-encryption')
        (WebsocketServer.__init__)(self, port, host, loglevel=log.INFO, **sslopts)
        print('Started websocket server at {}:{}'.format(host, port))
        self.logger = parent
        self.set_fn_new_client(self.clientConnected)
        self.set_fn_client_left(self.clientDisconnected)
        self.set_fn_message_received(self.received_message)
        self.sids = {}
        self.run = False
        self.connectCallbacks()
        self.start()

    def setPassword(self, password):
        if password is not None:
            self._RTWebsocketServer__password = RTWebsocket.hashPassword(password)
            self._RTWebsocketServer__password_full = RTWebsocket.hashPassword(password, True)
        else:
            self._RTWebsocketServer__password = None
            self._RTWebsocketServer__password_full = None
            logging.warning('Websocket is enabled without encryption!')

    def connectCallbacks(self):
        self.logger.database.websocketEvent_callback = self.newEventCallback
        self.logger.database.websocketSignal_callback = self.newSignalDataCallback
        self.logger.database._newSignalWebsocketCallback = self.newSignalCallback
        self.logger.websocketDevice_callback = self.deviceChangedCallback

    def start(self):
        self.run = True
        self.runner = Thread(target=(self.run_forever))
        self.runner.start()

    def stop(self):
        self.run = False
        self.server_close()
        self.sids = {}

    def send_json_to_all(self, jsondata, but=[]):
        try:
            for id in self.sids.keys():
                client = self.sids[id]['client']
                if client['id'] not in but:
                    self.send_json(client, jsondata)

        except (TypeError, ValueError):
            print(traceback.format_exc())
            raise Exception('You can only send JSON-serializable data')

    def send_json(self, client, jsondata, quietAuth=False):
        try:
            self.createNewClient(client)
            if self._RTWebsocketServer__password == None or self.sids[client['id']]['authorized']:
                if client['address'][0] not in self.logger.config['websocket']['host_whitelist']:
                    msg = RTWebsocket.send(jsondata, self._RTWebsocketServer__password)
                else:
                    logging.warning('This client is local and communicates not encrypted: {}'.format(client['address']))
                    msg = json.dumps(jsondata)
                self.send_message(client, msg)
            else:
                if not quietAuth:
                    if client['address'][0] not in self.logger.config['websocket']['host_whitelist']:
                        msg = RTWebsocket.send({'authorized': False}, self._RTWebsocketServer__password)
                    else:
                        msg = json.dumps({'authorized': False})
                    self.send_message(client, msg)
                else:
                    logging.warning('I will somehow not send this to the client.... sorry.')
        except (TypeError, ValueError):
            print(traceback.format_exc())
            raise Exception('You can only send JSON-serializable data')

    def clientConnected(self, client, server):
        print('New client connected and was given id %d' % client['id'])
        self.createNewClient(client)
        self.send_json_to_all({'client': 'newconnected'}, but=[client['id']])

    def createNewClient(self, client):
        if client['id'] not in self.sids.keys():
            self.resetClient(client)

    def resetClient(self, client):
        self.sids[client['id']] = {'connected':True,  'signalSubscriptions':[],  'deviceSubscriptions':[],  'eventLevel':0,  'client':client,  'authorized':False}

    def authorizeClient(self, client, password):
        print('Client {} wants authorization'.format(client['id']))
        if client['id'] in self.sids.keys():
            if self._RTWebsocketServer__password == None:
                self.sids[client['id']]['authorized'] = True
                self.send_json(client, {'authorized': True})
                print('Authorized, because no password is provided')
            else:
                if client['address'][0] in self.logger.config['websocket']['host_whitelist']:
                    self.sids[client['id']]['authorized'] = True
                    self.send_json(client, {'authorized': True})
                    print('Authorized, because client is in host whitelist')
                else:
                    if password.encode('utf-8') == self._RTWebsocketServer__password_full:
                        self.sids[client['id']]['authorized'] = True
                        self.send_json(client, {'authorized': True})
                        print('Authorized, because provided password is correct')
                    else:
                        self.sids[client['id']]['authorized'] = False
                        self.send_json(client, {'authorized': False})
                        print('Not Authorized, wrong password')
        else:
            print("Client not found. This shouldn't happen")

    def clientDisconnected(self, client, server):
        if client is not None:
            if client['id'] in self.sids.keys():
                print('Client(%d) disconnected' % client['id'])
                self.sids.pop(client['id'])

    def received_message(self, client, server, message):
        ans = {'error': False}
        try:
            if client['address'][0] not in self.logger.config['websocket']['host_whitelist']:
                msg = RTWebsocket.recv(message, self._RTWebsocketServer__password)
            else:
                msg = json.loads(message)
            self.createNewClient(client)
            if type(msg) == dict and msg != {}:
                if 'authorize' in msg.keys():
                    self.authorizeClient(client, msg['authorize'])
                else:
                    if self._RTWebsocketServer__password == None or self.sids[client['id']]['authorized']:
                        if 'y' in msg.keys():
                            plot = msg.get('plot', False)
                            y = msg.get('y', [])
                            sname = msg.get('sname', [''])
                            dname = msg.get('dname', 'noDevice')
                            unit = msg.get('unit', [''])
                            x = msg.get('x', None)
                            if dname is None:
                                dname = 'noDevice'
                            if plot:
                                self.logger.database.plot(x, y, sname, dname, unit)
                            else:
                                self.logger.database.addDataCallback(y, sname, dname, unit, x, True)
                            ans['sent'] = True
                        else:
                            if 'getSignalList' in msg.keys():
                                ans['signalList'] = self.logger.getSignalList()
                            else:
                                if 'getPluginList' in msg.keys():
                                    ans['pluginList'] = self.getPluginDict()
                                else:
                                    if 'event' in msg.keys():
                                        (self.logger.database.addNewEvent)(*msg['event'])
                                    else:
                                        if 'subscribe' in msg.keys():
                                            (self.subscribe)(client['id'], *msg['subscribe'])
                                        else:
                                            if 'unsubscribe' in msg.keys():
                                                (self.unsubscribe)(client['id'], *msg['unsubscribe'])
                                            else:
                                                if 'subscribeAll' in msg.keys():
                                                    self.subscribeAll(client['id'], msg['subscribeAll'])
                                                else:
                                                    if 'unsubscribeAll' in msg.keys():
                                                        self.unsubscribeAll(client['id'], msg['unsubscribeAll'])
                                                    else:
                                                        if 'getEventList' in msg.keys():
                                                            ans['events'] = self.logger.getEventList(latest=(msg['getEventList']))
                                                        if 'getEvent' in msg.keys():
                                                            ans['events'] = self.logger.getEvent(msg['getEvent'])
                                                    if 'getSignal' in msg.keys():
                                                        ans['signals'] = self.getSignal(msg['getSignal'])
                                                if 'getLatest' in msg.keys():
                                                    ans['latest'] = self.logger.getLatest(msg['getLatest'])
                                            if 'getSession' in msg.keys():
                                                ans['session'] = self.logger.database.generateSessionJSON(scripts=None)
                                        if 'remove' in msg.keys():
                                            ans['remove'] = (self.remove)(*msg['remove'])
                                    if 'plugin' in msg.keys():
                                        ans['plugin'] = self.handlewebsocketPlugins(msg['plugin'])
                                if 'logger' in msg.keys():
                                    ans['logger'] = self.handlewebsocketLogger(msg['logger'])
                            if 'userAction' in msg.keys():
                                ans['userAction'] = self.executeUserAction(msg['userAction'])
                        if 'automation' in msg.keys():
                            ans['automation'] = self.handleAutomation(msg['automation'])
                    else:
                        self.send_json(client, {'authorized': False})
                        return
            else:
                ans['error'] = True
            self.send_json(client, ans)
        except KeyboardInterrupt:
            logging.info('websocket Server stopped by user input.')
            self.stop()
        except Exception:
            tb = traceback.format_exc()
            logging.debug(tb)
            print(tb)
            logging.warning('Error in websocket-Connection')
            self.send_json(client, {'error': True})

    def createwebsocketSignal(self, dname, sname, xmin=None, xmax=None, database=False, maxN=None):
        """
        Returns signal for :meth:`.getSignal`, which is used in websocket-requests

        Args:
            dname (str): Devicename of signal
            sname (str): Signalname

        Returns:
            list: [x, y, unit, sigID, xMin, xMax]
        """
        sig = self.logger.database.getSignal_byName(dname,
          sname, xmin=xmin, xmax=xmax, database=database, maxN=maxN)
        ans = [list(sig[2]), list(sig[3]), sig[4], sig[5], sig[6], sig[7]]
        return ans

    def handlewebsocketPlugins(self, pluginDicts):
        """
        Calls plugin function, returns plugin parameter or sets plugin parameter, depending on pluginDicts. (used in websocket-requests)

        Args:
            pluginDicts (dict): {'pluginName':{'start':True/False}} to start/stop plugin

            pluginDicts (dict): {'pluginName':{'parameter':'get'}} to get a parameter

            pluginDicts (dict): {'pluginName':{'parameter': value}} to set a parameter

            pluginDicts (dict): {'pluginName':{'function': params}} to call a function

        Returns:
            dict
        """
        if type(pluginDicts) == dict:
            for plugin in pluginDicts.keys():
                if type(pluginDicts[plugin]) == dict:
                    for call in pluginDicts[plugin].keys():
                        if call == 'start' and type(pluginDicts[plugin][call]) == bool:
                            if pluginDicts[plugin][call]:
                                pluginDicts[plugin][call] = self.logger.startPlugin(plugin,
                                  remote=True)
                            else:
                                pluginDicts[plugin][call] = self.logger.stopPlugin(plugin)
                        elif call == 'autostart' and type(pluginDicts[plugin][call]) == bool:
                            if pluginDicts[plugin][call]:
                                pluginDicts[plugin][call] = self.logger.addAutorunPlugin(plugin)
                            else:
                                pluginDicts[plugin][call] = self.logger.removeAutorunPlugin(plugin)
                        else:
                            if '()' in call:
                                pluginDicts[plugin][call] = (self.logger.callPluginFunction)(plugin, call.replace('()', ''), *pluginDicts[plugin][call])
                            else:
                                pluginDicts[plugin][call] = self.logger.getPluginParameter(plugin, call, pluginDicts[plugin][call])

        return pluginDicts

    def handleAutomation(self, autoDict):
        ans = {}
        if 'setAction' in autoDict.keys():
            print('Setting action ' + str(autoDict['setAction']))
            name = autoDict['setAction']['name']
            listenID = autoDict['setAction']['listenID']
            script = autoDict['setAction']['script']
            parameters = autoDict['setAction']['parameters']
            active = autoDict['setAction']['active']
            self.logger.editGlobalAction(name, listenID, script, parameters, active)
            self.logger.saveGlobalActions()
        if 'setEvent' in autoDict.keys():
            print('Setting event ' + str(autoDict['setEvent']))
            name = autoDict['setEvent']['name']
            cond = autoDict['setEvent']['cond']
            text = autoDict['setEvent']['text']
            priority = autoDict['setEvent']['priority']
            retur = autoDict['setEvent']['retur']
            id = autoDict['setEvent']['id']
            trigger = autoDict['setEvent']['trigger']
            sname = autoDict['setEvent']['sname']
            dname = autoDict['setEvent']['dname']
            active = autoDict['setEvent']['active']
            self.logger.editGlobalEvent(name, cond, text, priority, retur, id, trigger, sname, dname, active)
            self.logger.saveGlobalEvents()
        if 'testAction' in autoDict.keys():
            print('Testing action ' + str(autoDict['testAction']))
            ok, ans2 = self.logger.triggerGlobalAction(autoDict['testAction'])
            ans['testAction'] = {'ok':ok,  'value':ans2}
        if 'testEvent' in autoDict.keys():
            print('Testing event ' + str(autoDict['testEvent']))
            ok, ans2 = self.logger.triggerGlobalEvent(autoDict['testEvent'])
            ans['testEvent'] = {'ok':ok,  'value':ans2}
        if 'removeAction' in autoDict.keys():
            print('Removing action ' + str(autoDict['removeAction']))
            ans['removeAction'] = self.logger.removeGlobalAction(autoDict['removeAction'])
        if 'removeEvent' in autoDict.keys():
            print('Removing event ' + str(autoDict['removeEvent']))
            ans['removeEvent'] = self.logger.removeGlobalEvent(autoDict['removeEvent'])
        if 'active' in autoDict.keys():
            if 'events' in autoDict['active'].keys():
                self.logger.config['global']['globalEventsActivated'] = autoDict['active']['events']
            if 'actions' in autoDict['active'].keys():
                self.logger.config['global']['globalActionsActivated'] = autoDict['active']['actions']
            self.logger.save_config()
        if 'reset' in autoDict.keys():
            self.logger.resetGlobalEventState()
        ans['events'] = self.logger.globalEvents
        ans['actions'] = self.logger.globalActions
        ans['active'] = {'events':self.logger.config['global']['globalEventsActivated'],  'actions':self.logger.config['global']['globalActionsActivated']}
        return ans

    def handlewebsocketLogger(self, loggerDict):
        """
        Calls some RTOC-functions, depending on loggerDict. (used in websocket-requests)

        Args:
            loggerDict (dict): {'clear':'all'/['dname.sname',...]} to clear all data or to clear signals specified in list

            loggerDict (dict): {'resize': int} to resize the local recordingLength

            loggerDict (dict): {'export':['dname.sname',...]} to export a signal

            loggerDict (dict): {'info':None} to get informations about RTOC

            loggerDict (dict): {'reboot':None} to reboot RTOC-server

        Returns:
            dict
        """
        if type(loggerDict) == dict:
            for call in loggerDict.keys():
                if call == 'clear':
                    if loggerDict[call] == 'all':
                        self.logger.clear()
                    else:
                        if loggerDict[call] == 'events':
                            self.logger.database.clear(False, False, True, database=True)
                        elif type(loggerDict[call]) == list:
                            for idx, sig in enumerate(loggerDict[call]):
                                id = (self.logger.database.getSignalID)(*sig.split('.'))
                                if id != -1:
                                    loggerDict[call][idx] = self.logger.database.removeSignal(id)
                                else:
                                    loggerDict[call][idx] = False

                else:
                    if call == 'resize':
                        if type(loggerDict[call]) == int:
                            self.logger.database.resizeSignals(loggerDict[call])
                            loggerDict[call] = True
                    else:
                        if call == 'export':
                            if type(loggerDict[call]) == list and len(loggerDict[call]) <= 2:
                                (self.logger.exportData)(*loggerDict[call])
                                loggerDict[call] = True
                        else:
                            if call == 'info':
                                loggerDict[call] = {}
                                loggerDict[call]['signals'] = len(self.logger.database.signals())
                                loggerDict[call]['starttime'] = self.logger.starttime
                                size, maxsize, databaseSize = self.logger.database.getSignalSize()
                                loggerDict[call]['signal_memory'] = size
                                loggerDict[call]['signal_memory_limit'] = maxsize
                                reduced_config = self.logger.config.reduced()
                                reduced_config['memory'] = {}
                                obj_Disk = psutil.disk_usage('/')
                                reduced_config['memory']['total'] = str(round(obj_Disk.total / 1073741824.0, 3))
                                reduced_config['memory']['used'] = str(round(obj_Disk.used / 1073741824.0, 3))
                                reduced_config['memory']['free'] = str(round(obj_Disk.free / 1073741824.0, 3))
                                reduced_config['memory']['freeL'] = maxsize - size
                                reduced_config['memory']['usedL'] = size
                                reduced_config['memory']['totalL'] = maxsize
                                loggerDict[call]['config'] = reduced_config
                                loggerDict[call]['userActions'] = list(self.logger.userActions.keys())
                            else:
                                if call == 'reboot':
                                    self.logger.database.database.exportJSON(self.logger.config['global']['documentfolder'] + '/restore.json', None, True)
                                    self.logger.save_config()
                                    os.system('sudo reboot')
                                else:
                                    if call == 'backup':
                                        if type(loggerDict[call]) == dict:
                                            for key in loggerDict[call].keys():
                                                if key == 'now':
                                                    self.logger.database.createLocalBackupNow()
                                                else:
                                                    if key == 'resample':
                                                        if type(loggerDict[call][key]) in [int, float]:
                                                            self.logger.config['backup']['resample'] = loggerDict[call][key]
                                                            self.logger.save_config()
                                                        else:
                                                            if key == 'interval':
                                                                if type(loggerDict[call][key]) in [int, float]:
                                                                    self.logger.config['backup']['interval'] = loggerDict[call][key]
                                                                    self.logger.save_config()
                                                            else:
                                                                if key == 'active':
                                                                    if type(loggerDict[call][key]) in [bool]:
                                                                        self.logger.config['backup']['active'] = loggerDict[call][key]
                                                                        self.logger.save_config()
                                                                elif key in ('loadOnOpen',
                                                                             'autoOnClose',
                                                                             'autoIfFull',
                                                                             'clear'):
                                                                    if type(loggerDict[call][key]) == bool:
                                                                        self.logger.config['backup'][key] = loggerDict[call][key]
                                                                        self.logger.save_config()

                                    else:
                                        if call == 'postgresql':
                                            if type(loggerDict[call]) == dict:
                                                for key in loggerDict[call].keys():
                                                    if key == 'active' and type(loggerDict[call][key]) in [bool]:
                                                        self.logger.config['postgresql']['active'] = loggerDict[call][key]
                                                        self.logger.save_config()

                                        else:
                                            if call == 'tcp':
                                                if type(loggerDict[call]) == dict:
                                                    for key in loggerDict[call].keys():
                                                        if key == 'port':
                                                            if type(loggerDict[call][key]) in [int, float]:
                                                                self.logger.config['tcp']['port'] = loggerDict[call][key]
                                                                self.logger.save_config()
                                                            if key == 'active' and type(loggerDict[call][key]) in [bool]:
                                                                self.logger.config['tcp']['active'] = loggerDict[call][key]
                                                                self.logger.save_config()

                                            else:
                                                if call == 'telegram':
                                                    if type(loggerDict[call]) == dict:
                                                        for key in loggerDict[call].keys():
                                                            if key == 'enablactiveed' and type(loggerDict[call][key]) in [bool]:
                                                                self.logger.config['telegram']['active'] = loggerDict[call][key]
                                                                self.logger.save_config()

                                                else:
                                                    if call == 'global':
                                                        if type(loggerDict[call]) == dict:
                                                            for key in loggerDict[call].keys():
                                                                if key == 'samplerate' and type(loggerDict[call][key]) in [int, float]:
                                                                    self.logger.setAllSamplerates(loggerDict[call][key])

        return loggerDict

    def getSignalList(self):
        """
        Returns signallist, which is used in websocket-requests

        Returns:
            :py:meth:`.RT_data.signalNames`
        """
        signalNames = self.logger.database.signalNames()
        if ['RTOC', ''] in signalNames:
            signalNames.pop(signalNames.index(['RTOC', '']))
        return signalNames

    def getPluginDict(self):
        """
        Returns a dictonary containing all plugin information, which is used in websocket-requests

        Returns:
            dict: {'functions':[], 'parameters':[], 'status':bool}
        """
        dict = {}
        for name in self.logger.devicenames.keys():
            dict[name] = {}
            dict[name]['functions'] = []
            dict[name]['parameters'] = []
            dict[name]['status'] = False
            hiddenFuncs = ['savePersistentVariable', 'info', 'error', 'warning', 'debug', 'loadPersistentVariable', 'loadGUI', 'updateT', 'stream', 'plot', 'event', 'close', 'cancel', 'start',
             'setPerpetualTimer', 'createPerpetualTimer', 'initPerpetualTimer', 'initPersistentVariable', 'createPersistentVariable', 'setDeviceName', 'setSamplerate', 'setInterval', 'getDir', 'telegram_send_message', 'telegram_send_photo', 'telegram_send_document', 'telegram_send_plot']
            hiddenParams = ['run', 'smallGUI', 'widget',
             'lockPerpetialTimer', 'logger', 'rtoc']
            if name in self.logger.autorunPlugins:
                dict[name]['autorun'] = True
            else:
                dict[name]['autorun'] = False
            dict[name]['info'] = self.logger.pluginInfos[name]
            for fun in self.logger.pluginFunctions.keys():
                if fun.startswith(name + '.') and fun not in [name + '.' + i for i in hiddenFuncs]:
                    dict[name]['functions'].append([fun.replace(name + '.', ''),
                     self.logger.pluginFunctions[fun][1], self.logger.pluginFunctions[fun][2], self.logger.pluginFunctions[fun][3], self.logger.pluginFunctions[fun][4], self.logger.pluginFunctions[fun][5], self.logger.pluginFunctions[fun][6]])

            for fun in list(self.logger.pluginParameters.keys()):
                if fun.startswith(name + '.'):
                    if fun not in [name + '.' + i for i in hiddenParams]:
                        value = self.logger.getPluginParameter(name, 'get', fun.replace(name + '.', ''))
                        if type(value) not in [str, int, float, list, bool]:
                            value = 'Unknown datatype'
                        docs = None
                        if fun in self.logger.pluginParameterDocstrings.keys():
                            docs = self.logger.pluginParameterDocstrings[fun]
                    dict[name]['parameters'].append([
                     fun.replace(name + '.', ''), value, docs])

            for fun in self.logger.pluginStatus.keys():
                if name == fun:
                    dict[name]['status'] = self.logger.pluginStatus[fun]

            dict[name]['log'] = self.logger.getPluginLog(name)

        return dict

    def getEventList(self):
        """
        Returns eventlist, which is used in websocket-requests

        Returns:
            :py:meth:`.RT_data.events`
        """
        return self.logger.database.events(beauty=True)

    def getEvent(self, nameList):
        """
        Returns events for given signalnames, which is used in websocket-requests

        Args:
            nameList (list): List of device.signalnames

        Returns:
            list: [:py:meth:`.RT_data.getEvents`,...]
        """
        ans = {}
        for device in nameList:
            dev = device.split('.')
            sig = self.logger.database.getEvents(self.logger.database.getSignalID(dev[0], dev[1]))
            if sig != [[], [], [], [], []]:
                ans[device] = []
                if len(sig[0]) > 0:
                    for idx, s in enumerate(sig[0]):
                        ans[device].append([
                         sig[0][idx], sig[1][idx], sig[2][idx], sig[3][idx], sig[4][idx]])

        return ans

    def getSignal(self, sigList):
        """
        Returns signal for given signalnames, which is used in websocket-requests

        Args:
            sigList (list): List of device.signalnames

            sigList (str): If sigList== 'all', all signals are returned

        Returns:
            dict: {'signalname': :meth:`.createwebsocketSignal`,...}
        """
        ans = {}
        if type(sigList) == list:
            for device in sigList:
                if type(device) == str:
                    ans[device] = (self.createwebsocketSignal)(*device.split('.'))

        else:
            if type(sigList) == dict:
                kwargs = {'dname':None,  'sname':None, 
                 'xmin':None, 
                 'xmax':None, 
                 'database':True, 
                 'maxN':None}
                for s in kwargs.keys():
                    if s in sigList.keys():
                        kwargs[s] = sigList[s]

                if kwargs['dname'] is None or kwargs['sname'] is None:
                    return False
                device = kwargs['dname'] + '.' + kwargs['sname']
                ans[device] = self.createwebsocketSignal((kwargs['dname']),
                  (kwargs['sname']), xmin=(kwargs['xmin']), xmax=(kwargs['xmax']), database=(kwargs['database']), maxN=(kwargs['maxN']))
            else:
                if sigList == 'all':
                    for dev in self.logger.database.signalNames():
                        ans[device] = (self.createwebsocketSignal)(*dev)

        return ans

    def executeUserAction(self, action):
        actionDict = {}
        actionDict['name'] = action
        actionDict['success'] = False
        actionDict['type'] = 'text'
        actionDict['data'] = ''
        ok, ans = self.logger.executeUserAction(action)
        if ok and len(ans) == 2:
            try:
                text = translate('RTOC', 'Action has been executed')
                if ans[0] == 'picture':
                    with open(ans[1], 'rb') as (imageFile):
                        image = str(base64.b64encode(imageFile.read()), 'utf-8')
                    actionDict['data'] = image
                    actionDict['success'] = True
                    actionDict['type'] = 'picture'
                else:
                    if ans[0] == 'document':
                        with open(ans[1], 'rb') as (imageFile):
                            file = str(base64.b64encode(imageFile.read()), 'utf-8')
                        actionDict['data'] = file
                        actionDict['success'] = True
                        actionDict['type'] = 'document'
                    else:
                        if ans[0] == 'text':
                            actionDict['data'] = ans[1]
                            actionDict['success'] = True
            except:
                text = translate('RTOC', 'Action is incorrect')
                actionDict['data'] = text

        else:
            text = translate('RTOC', 'Action is incorrect')
            actionDict['data'] = text
        return actionDict

    def remove(self, signalIDs=[], eventIDs=[]):
        """
        Removes latest xy-pairs for given signalnames, which is used in websocket-requests
        or events

        Args:
            signalIDs (list): List of signalIDs
            eventIDs (list): List of eventIDs

        """
        evCounter = 0
        for eventID in eventIDs:
            ans = self.logger.database.removeEvent(eventID, database=True)
            if ans:
                evCounter += 1

        sigCounter = 0
        for signalID in signalIDs:
            ans = self.logger.database.removeSignal(signalID, database=True)
            if ans:
                sigCounter += 1

        return (
         sigCounter, evCounter)

    def setEventSubscription(self, sid, priority):
        if sid in self.sids.keys():
            self.sids[sid]['eventLevel'] = priority
        else:
            logging.warning('Client {} not connected. Cannot set eventLevel'.format(sid))

    def subscribe(self, sid, element, id):
        if element not in ('device', 'signal'):
            return False
        else:
            if sid in self.sids.keys():
                if id not in self.sids[sid][(element + 'Subscriptions')]:
                    self.sids[sid][(element + 'Subscriptions')].append(id)
                    logging.info('Client {} Added {} to subscription'.format(sid, id))
                    return True
            else:
                logging.warning('Client {} not connected. Cannot add {}-subscription'.format(sid, element))
            return False

    def unsubscribe(self, sid, element, id):
        if element not in ('device', 'signal'):
            return False
        else:
            if sid in self.sids.keys():
                if id in self.sids[sid][(element + 'Subscriptions')]:
                    self.sids[sid][(element + 'Subscriptions')].remove(id)
                    return True
            else:
                logging.warning('Client {} not connected. Cannot remove {}-subscription'.format(sid, element))
            return False

    def subscribeAll(self, sid, element):
        if element not in ('device', 'signal'):
            return
        else:
            if sid in self.sids.keys():
                if element == 'signal':
                    self.sids[sid]['signalSubscriptions'] = self.logger.database.signals().keys()
                elif element == 'device':
                    self.sids[sid]['deviceSubscriptions'] = self.logger.database.devices().keys()
            else:
                logging.warning('Client {} not connected. Cannot add subscriptions'.format(sid))

    def unsubscribeAll(self, sid, element):
        if element not in ('device', 'signal'):
            return
        else:
            if sid in self.sids.keys():
                self.sids[sid][element + 'Subscriptions'] = []
            else:
                logging.warning('Client {} not connected. Cannot remove {} subscriptions'.format(sid, element))

    def newSignalCallback(self, x, y, dataunit, devicename, signalname, signalId):
        for sid in list(self.sids.keys()):
            try:
                self.send_json((self.sids[sid]['client']), {'signal': {'x':list(x), 
                            'y':list(y),  'unit':dataunit,  'dname':devicename,  'sname':signalname,  'id':signalId}},
                  quietAuth=True)
            except Exception as e:
                logging.error(e)

    def newSignalDataCallback(self, x, y, dataunit, devicename, signalname, signalId):
        for sid in list(self.sids.keys()):
            try:
                if devicename + '.' + signalname in self.sids[sid]['signalSubscriptions']:
                    self.send_json((self.sids[sid]['client']), {'signal': {'x':[
                                 x], 
                                'y':[y],  'unit':dataunit,  'dname':devicename,  'sname':signalname,  'id':signalId}},
                      quietAuth=True)
            except Exception as e:
                logging.error(e)

    def newEventCallback(self, x, text, dname, sname, priority, value, id, eventID):
        for sid in list(self.sids.keys()):
            try:
                if priority >= self.sids[sid]['eventLevel']:
                    self.send_json((self.sids[sid]['client']), {'event': {'x':x, 
                               'text':text,  'dname':dname,  'sname':sname,  'priority':priority,  'value':value,  'id':id,  'eventId':eventID}},
                      quietAuth=True)
            except Exception as e:
                logging.error(e)

    def deviceChangedCallback(self, device, reload=True):
        if reload:
            self.logger.analysePlugin(device)
        info = self.getPluginDict()
        for sid in list(self.sids.keys()):
            try:
                self.send_json((self.sids[sid]['client']), {'pluginList': info},
                  quietAuth=True)
            except Exception as e:
                logging.error(e)