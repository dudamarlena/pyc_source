# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Benutzer\haschtl\Dokumente\GIT\kellerlogger\RTOC\RTLogger\DeviceFunctions.py
# Compiled at: 2020-01-06 16:35:38
# Size of source mod 2**32: 20220 bytes
import os, traceback, importlib, sys, json
from . import loggerlib
from . import plugins
import logging as log, inspect
log.basicConfig(level=(log.INFO))
logging = log.getLogger(__name__)

class DeviceFunctions:
    __doc__ = '\n    This class contains all plugin-specific functions of RTLogger\n    '

    def getDeviceList(self):
        userpath = self.config['global']['documentfolder']
        userpath = os.path.expanduser(userpath)
        if not os.path.exists(userpath):
            os.mkdir(userpath)
        if not os.path.exists(userpath + '/devices'):
            os.mkdir(userpath + '/devices')
        sys.path.insert(0, userpath)
        import devices
        self.devicenames = {}
        self.pluginStatus = {}
        self.pluginInfos = {}
        for _, name, _ in loggerlib.iter_namespace(plugins):
            namesplit = name.split('.')
            devname = namesplit[(-1)].replace('.', 'Dot').replace(':', 'DDot')
            if devname not in ('LoggerPlugin', ):
                self.devicenames[devname] = name
                self.pluginStatus[devname] = False
                self.pluginInfos[devname] = None

        subfolders = [f.name for f in os.scandir(list(devices.__path__)[0]) if f.is_dir()]
        for folder in subfolders:
            if folder not in ('', '__pycache__', '.git', '.vscode'):
                a = __import__(devices.__name__ + '.' + folder)
                for filename in os.listdir(list(devices.__path__)[0] + '/' + folder):
                    if filename.endswith('.py'):
                        file = ''
                        with open((list(devices.__path__)[0] + '/' + folder + '/' + filename), mode='r') as (f):
                            file = f.readlines()
                        if 'class Plugin(' in ''.join(file):
                            name = devices.__name__ + '.' + folder + '.' + filename.replace('.py', '')
                            devname = filename.replace('.py', '').replace('.', 'Dot').replace(':', 'DDot')
                            if devname not in ('LoggerPlugin', ):
                                self.devicenames[devname] = name
                                self.pluginStatus[devname] = False
                                self.pluginInfos[devname] = None

    def startPlugin(self, name, remote=True):
        """
        This function starts a plugin.

        Args:
            name (str): This is the name of the plugin you want to start.
            remote (bool): If true, this function trigger a callback to update GUI

        Returns:
            bool: True, if sucessfully started

            error (str): Error message, if errors occured
        """
        try:
            if name in self.devicenames.keys():
                fullname = self.devicenames[name]
                self.pluginObjects[name] = importlib.import_module(fullname).Plugin(logger=self)
                self.analysePlugin(name)
                self.pluginStatus[name] = True
                logging.info('PLUGIN: ' + name + ' connected\n')
                if self.startDeviceCallback:
                    if remote:
                        self.startDeviceCallback(name)
                if self.websocketDevice_callback:
                    self.websocketDevice_callback(name)
                return (True, '')
            else:
                logging.warning("PLUGIN not found: '" + str(name) + "'\n")
                return (False, "PLUGIN not found: '" + str(name) + "'\n")
        except Exception:
            tb = traceback.format_exc()
            self.pluginStatus[name] = tb
            logging.debug(tb)
            logging.warning("PLUGIN FAILURE\nCould not load Plugin '" + str(name) + "'\n")
            if self.websocketDevice_callback:
                self.websocketDevice_callback(name, False)
            return (
             False, tb)

    def getPlugin(self, name):
        """
        This function returns an object of the 'Plugin' class of given plugin-name.

        Args:
            name (str): This is the name of the plugin you want to get.

        Returns:
            bool: False, if the object did not exist

            object: Object of plugin-class of given plugin
        """
        try:
            if name in self.pluginObjects.keys():
                return self.pluginObjects[name]
            else:
                logging.warning('Plugin ' + name + ' not found or started')
                return False
        except Exception:
            tb = traceback.format_exc()
            logging.debug(tb)
            logging.warning("PLUGIN FAILURE\nCould not get Plugin '" + str(name) + "'\n")
            return False

    def setPluginSamplerate(self, name, samplerate):
        """
        Sets the samplerate of a given plugin. This will ONLY work, if the plugin uses the integrated PerpetualTimer.

        Args:
            name (str): This is the name of the plugin you want to start.
            samplerate (float): The desired samplerate in Hz.

        Returns:
            bool: True, if sucessfully set
        """
        if name in self.pluginObjects.keys():
            try:
                self.pluginObjects[name].samplerate = samplerate
                if self.websocketDevice_callback:
                    self.websocketDevice_callback(name)
                return True
            except Exception:
                tb = traceback.format_exc()
                logging.debug(tb)
                return False

        else:
            return False

    def setAllSamplerates(self, samplerate):
        """
        Sets the samplerate of a all plugin. This will ONLY work, if the plugins use the integrated PerpetualTimer.

        Args:
            samplerate (float): The desired samplerate in Hz.
        """
        for plugin in self.pluginObjects.keys():
            self.setPluginSamplerate(plugin, samplerate)

        if self.websocketDevice_callback:
            self.websocketDevice_callback('all')

    def getPluginSamplerate(self, name):
        """
        Returns the samplerate of a given plugin.

        Args:
            name (str): This is the name of the plugin.

        Returns:
            samplerate (float): The actual samplerate in Hz.
        """
        if name in self.pluginObjects.keys():
            try:
                return self.pluginObjects[name].samplerate
            except Exception:
                tb = traceback.format_exc()
                logging.debug(tb)
                return 0

        else:
            return 0

    def getPluginParameter(self, name, parameter, *args):
        r"""
        This function is used to get and also set parameters from a given plugin.

        You can **get** multiple parameters at once. To get a parameter, use the following parameter mapping:

        Args:
            name (str): This is the name of the plugin.
            parameter (str): If == 'get', this call is understood as a get-request
            args (\*str): Can be multiple names of plugin-parameters

        You can **set** a single parameter. To set a parameter, use the following parameter mapping:

        Args:
            name (str): This is the name of the plugin.
            parameter (str): The parameter-name you want to change.
            args (any): Desired value of the parameter.

        Returns:
            parameter (any): The value of the requested/setted parameter(s).

            False, if any error occured, while trying to get/set parameter
        """
        try:
            if parameter == 'get':
                if type(parameter) == str:
                    if type(args[0]) == list:
                        rets = []
                        for param in args[0]:
                            exec('self.ret=self.pluginObjects[name].' + str(param))
                            rets.append(self.ret)

                        self.ret = rets
                        return self.ret
                    if type(args[0]) == str:
                        exec('self.ret=self.pluginObjects[name].' + str(args[0]))
                        return self.ret
            else:
                if name in self.pluginObjects.keys():
                    if type(args[0]) == str:
                        strung = "'" + args[0] + "'"
                    else:
                        strung = str(args[0])
                    exec('self.pluginObjects["' + name + '"].' + parameter + ' = ' + strung)
                    exec('self.ret = self.pluginObjects[name]._devicename')
                    dname = self.ret
                    if self.isPersistentVariable(parameter, dname):
                        self.pluginObjects[name].savePersistentVariable(parameter, args[0], dname)
                    else:
                        logging.info('Parameter {} from device {} is not persistant'.format(parameter, name))
                    if self.websocketDevice_callback:
                        self.websocketDevice_callback(name)
                    return self.ret
                else:
                    logging.warning('Plugin ' + name + ' not found or started')
                    return False
        except Exception:
            tb = traceback.format_exc()
            logging.error(tb)
            logging.warning("PLUGIN FAILURE\nCould not get/set/call Plugin parameter/function'" + str(name) + "'\n")
            return False

    def callPluginFunction(self, name, function, *args, **kwargs):
        r"""
        This function is used to call a function from a given plugin.

        You can **get** multiple parameters at once. To get a parameter, use the following parameter mapping:

        Args:
            name (str): This is the name of the plugin.
            function (str): The function-name, you want to call
            args (\*any): Parameters transmitted to the function
            kwargs (\*any): Keyworded parameters transmitted to the function

        Returns:
            bool: True, if call was successfull

            parameter (any): The value of the requested/setted parameter(s).
        """
        try:
            if name in self.pluginObjects.keys() and type(function) == str:
                exec('self.func = self.pluginObjects["' + name + '"].' + function)
                ans = (self.func)(*args, **kwargs)
                if self.websocketDevice_callback:
                    self.websocketDevice_callback(name)
                return (True, ans)
            else:
                logging.warning('Plugin ' + name + ' not found or started')
                return (False, 'Plugin ' + name + ' not found or started')
        except Exception:
            tb = traceback.format_exc()
            logging.error(tb)
            logging.warning("PLUGIN FAILURE\nCould not get/set/call Plugin parameter/function'" + str(name) + "'\n")
            return (False, tb)

    def stopPlugin(self, name, remote=True):
        """
        This function stops a plugin.

        Args:
            name (str): This is the name of the plugin you want to stop.
            remote (bool): If true, this function trigger a callback to update GUI

        Returns:
            bool: True, if sucessfully stopped
        """
        try:
            if name in self.pluginObjects.keys():
                self.pluginStatus[name] = False
                self.pluginObjects[name].close()
                logging.info('PLUGIN: ' + name + ' disconnected\n')
            else:
                if self.stopDeviceCallback:
                    if remote:
                        self.stopDeviceCallback(name)
                if self.websocketDevice_callback:
                    self.websocketDevice_callback(name, False)
            return True
        except Exception:
            tb = traceback.format_exc()
            logging.info(tb)
            logging.warning("PLUGIN FAILURE\nCould not stop Plugin '" + str(name) + "'\n")
            return False

    def analysePlugins(self):
        for name in self.pluginObjects.keys():
            self.analysePlugin(name)

    def getPluginLog(self, name):
        if name in self.pluginObjects.keys():
            log = self.pluginObjects[name]._log
            return list(log)
        else:
            return

    def getPluginDict(self):
        """
        Returns a dictonary containing all plugin information, which is used in Websocket-requests

        Returns:
            dict: {'functions':[], 'parameters':[], 'status':bool}
        """
        dict = {}
        for name in self.devicenames.keys():
            dict[name] = self.getPluginInfo(name)

        return dict

    def getPluginInfo(self, devicename):
        dict = {}
        dict['functions'] = []
        dict['parameters'] = []
        dict['status'] = False
        hiddenFuncs = ['savePersistentVariable', 'loadPersistentVariable', 'loadGUI', 'updateT', 'stream', 'plot', 'event', 'close', 'cancel', 'start', 'setSamplerate', 'setDeviceName', 'setPerpetualTimer', 'setInterval', 'getDir', 'telegram_send_message', 'telegram_send_photo', 'telegram_send_document', 'telegram_send_plot']
        hiddenParams = ['run', 'smallGUI', 'widget', 'samplerate', 'lockPerpetialTimer', 'logger', 'rtoc', 'gen_start']
        for fun in self.pluginFunctions.keys():
            if fun.startswith(devicename + '.') and fun not in [devicename + '.' + i for i in hiddenFuncs]:
                dict['functions'].append(fun.replace(devicename + '.', ''))

        for fun in self.pluginParameters.keys():
            if fun.startswith(devicename + '.') and fun not in [devicename + '.' + i for i in hiddenParams]:
                value = self.getPluginParameter(devicename, 'get', fun.replace(devicename + '.', ''))
                if type(value) not in [str, int, float, list, bool] or value != None:
                    value = 'Unknown datatype'
                dict['parameters'].append([fun.replace(devicename + '.', ''), value])

        if devicename in self.pluginStatus.keys():
            dict['status'] = self.pluginStatus[devicename]
        else:
            dict['status'] = 'Error'
        return dict

    def analysePlugin(self, name):
        """
        Collects all necessary information about a specific plugin (function names and parameter names) and stores them in parameter 'pluginFunctions' and 'pluginParameters'

        """
        object = self.pluginObjects[name]
        all = dir(object)
        self.pluginInfos[name] = object.__doc__
        for element in all:
            if str(element)[0] != '_':
                if callable(getattr(object, element)):
                    origFunName = "self.pluginObjects['" + name + "']." + getattr(object, element).__name__
                    argCount = getattr(object, element).__code__.co_argcount - 1
                    varnames = getattr(object, element).__code__.co_varnames
                    argNames = varnames[1:argCount + 1]
                    docs = getattr(object, element).__doc__
                    defaults = getattr(object, element).__defaults__
                    sig = inspect.signature(getattr(object, element))
                    self.pluginFunctions[name + '.' + element] = [origFunName, argNames, argCount, varnames, defaults, docs, str(sig)]
                else:
                    origParName = "self.pluginObjects['" + name + "']." + str(element)
                    self.pluginParameters[name + '.' + element] = origParName
            else:
                if str(element).startswith('__doc_') and str(element).endswith('__'):
                    param = element[6:-2]
                    self.pluginParameterDocstrings[name + '.' + param] = str(getattr(object, element))

    def initPersistentVariables(self):
        configpath = self.config['global']['documentfolder'] + '/persistentVariables.json'
        if os.path.exists(configpath):
            try:
                with open(configpath, encoding='UTF-8') as (jsonfile):
                    self.persistentVariables = json.load(jsonfile, encoding='UTF-8')
            except:
                logging.error('Persistent variables are damaged! Cannot load')

        else:
            logging.warning('No persistent variables found.')

    def loadPersistentVariable(self, parname: str, fallback, dname: str):
        if dname not in self.persistentVariables.keys():
            return fallback
        else:
            if parname not in self.persistentVariables[dname].keys():
                return fallback
            return self.persistentVariables[dname][parname]

    def initPersistentVariable(self, parname: str, fallback, dname: str):
        if self.isPersistentVariable(parname, dname):
            return self.loadPersistentVariable(parname, None, dname)
        else:
            if dname not in self.persistentVariables.keys():
                self.persistentVariables[dname] = {}
            if parname not in self.persistentVariables[dname].keys():
                self.persistentVariables[dname][parname] = fallback
                return fallback
            return self.persistentVariables[dname][parname]

    def isPersistentVariable(self, parname: str, dname: str):
        if dname not in self.persistentVariables.keys():
            return False
        else:
            if parname not in self.persistentVariables[dname].keys():
                return False
            return True

    def savePersistentVariable(self, parname: str, value, dname: str):
        if dname not in self.persistentVariables.keys():
            self.persistentVariables[dname] = {}
        self.persistentVariables[dname][parname] = value
        with open((self.config['global']['documentfolder'] + '/persistentVariables.json'), 'w', encoding='utf-8') as (fp):
            json.dump((self.persistentVariables), fp, sort_keys=False, indent=4, separators=(',',
                                                                                             ': '))
        return True