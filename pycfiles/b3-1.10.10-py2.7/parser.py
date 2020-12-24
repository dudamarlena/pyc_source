# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\b3\parser.py
# Compiled at: 2016-03-08 18:42:09
__author__ = 'ThorN, Courgette, xlr8or, Bakes, Ozon, Fenix'
__version__ = '1.43.6'
import os, sys, re, time, thread, datetime, dateutil.tz, Queue, imp, atexit, socket, glob, b3, b3.config, b3.storage, b3.events, b3.output, b3.game, b3.cron, b3.parsers.q3a.rcon, b3.timezones
from ConfigParser import NoOptionError
from collections import OrderedDict
from b3 import __version__ as currentVersion
from b3.clients import Clients
from b3.clients import Group
from b3.decorators import Memoize
from b3.exceptions import MissingRequirement
from b3.functions import getModule
from b3.functions import vars2printf
from b3.functions import main_is_frozen
from b3.functions import splitDSN
from b3.functions import right_cut
from b3.functions import topological_sort
from b3.plugin import PluginData
from b3.update import B3version
from textwrap import TextWrapper
from traceback import extract_tb
try:
    from xml.etree import cElementTree as ElementTree
except ImportError:
    from xml.etree import ElementTree

class Parser(object):
    OutputClass = b3.parsers.q3a.rcon.Rcon
    _commands = {}
    _cron = None
    _events = {}
    _eventNames = {}
    _eventsStats_cronTab = None
    _handlers = {}
    _lineTime = None
    _lineFormat = re.compile('^([a-z ]+): (.*?)', re.IGNORECASE)
    _line_color_prefix = ''
    _line_length = 80
    _messages = {}
    _message_delay = 0
    _paused = False
    _pauseNotice = False
    _plugins = OrderedDict()
    _port = 0
    _publicIp = ''
    _rconIp = ''
    _rconPort = None
    _rconPassword = ''
    _reColor = re.compile('\\^[0-9a-z]')
    _timeStart = None
    _use_color_codes = True
    autorestart = False
    clients = None
    config = None
    delay = 0.33
    delay2 = 0.02
    encoding = 'latin-1'
    game = None
    gameName = None
    log = None
    logTime = 0
    name = 'b3'
    output = None
    privateMsg = False
    queue = None
    rconTest = False
    remoteLog = False
    screen = None
    storage = None
    type = None
    working = True
    wrapper = None
    deadPrefix = '[DEAD]^7'
    msgPrefix = ''
    pmPrefix = '^8[pm]^7'
    prefix = '^2%s:^3'
    _messages_default = {'kicked_by': '$clientname^7 was kicked by $adminname^7 $reason', 
       'kicked': '$clientname^7 was kicked $reason', 
       'banned_by': '$clientname^7 was banned by $adminname^7 $reason', 
       'banned': '$clientname^7 was banned $reason', 
       'temp_banned_by': '$clientname^7 was temp banned by $adminname^7 for $banduration^7 $reason', 
       'temp_banned': '$clientname^7 was temp banned for $banduration^7 $reason', 
       'unbanned_by': '$clientname^7 was un-banned by $adminname^7 $reason', 
       'unbanned': '$clientname^7 was un-banned $reason'}
    _frostBiteGameNames = [
     'bfbc2', 'moh', 'bf3', 'bf4']
    exiting = thread.allocate_lock()
    exitcode = None

    def __new__(cls, *args, **kwargs):
        cls.__read = cls.__read_input
        if sys.platform == 'darwin':
            cls.__read = cls.___read_input_darwin
        return object.__new__(cls)

    def __init__(self, conf, options):
        """
        Object contructor.
        :param conf: The B3 configuration file
        :param options: command line options
        """
        self._timeStart = self.time()
        self.autorestart = options.autorestart
        if not self.loadConfig(conf):
            print 'CRITICAL ERROR : COULD NOT LOAD CONFIG'
            raise SystemExit(220)
        if self.config.has_option('server', 'encoding'):
            self.encoding = self.config.get('server', 'encoding')
        logfile = self.config.getpath('b3', 'logfile')
        log2console = self.config.has_option('devmode', 'log2console') and self.config.getboolean('devmode', 'log2console')
        logfile = b3.getWritableFilePath(logfile, True)
        try:
            logsize = b3.functions.getBytes(self.config.get('b3', 'logsize'))
        except (TypeError, NoOptionError):
            logsize = b3.functions.getBytes('10MB')

        self.log = b3.output.getInstance(logfile, self.config.getint('b3', 'log_level'), logsize, log2console)
        self.screen = sys.stdout
        self.screen.write('Activating log   : %s\n' % b3.getShortPath(os.path.abspath(b3.getAbsolutePath(logfile, True))))
        self.screen.flush()
        sys.stdout = b3.output.STDOutLogger(self.log)
        sys.stderr = b3.output.STDErrLogger(self.log)
        if self.gameName in 'bf3':
            self._publicIp = ''
            if self.config.has_option('server', 'public_ip'):
                self._publicIp = self.config.get('server', 'public_ip')
            self._port = ''
            if self.config.has_option('server', 'port'):
                self._port = self.config.getint('server', 'port')
        else:
            self._publicIp = self.config.get('server', 'public_ip')
            self._port = self.config.getint('server', 'port')
        self._rconPort = self._port
        self._rconIp = self._publicIp
        if self.config.has_option('server', 'rcon_ip'):
            self._rconIp = self.config.get('server', 'rcon_ip')
        if self.config.has_option('server', 'rcon_port'):
            self._rconPort = self.config.getint('server', 'rcon_port')
        if self.config.has_option('server', 'rcon_password'):
            self._rconPassword = self.config.get('server', 'rcon_password')
        if self._publicIp and self._publicIp[0:1] in ('~', '/'):
            f = file(b3.getAbsolutePath(self._publicIp, decode=True))
            self._publicIp = f.read().strip()
            f.close()
        if self._rconIp[0:1] in ('~', '/'):
            f = file(b3.getAbsolutePath(self._rconIp, decode=True))
            self._rconIp = f.read().strip()
            f.close()
        try:
            self._rconIp = socket.gethostbyname(self._rconIp)
        except socket.gaierror:
            pass

        self.bot('%s', b3.getB3versionString())
        self.bot('Python: %s', sys.version.replace('\n', ''))
        self.bot('Default encoding: %s', sys.getdefaultencoding())
        self.bot('Starting %s v%s for server %s:%s (autorestart = %s)', self.__class__.__name__, getattr(getModule(self.__module__), '__version__', ' Unknown'), self._rconIp, self._port, 'ON' if self.autorestart else 'OFF')
        self.Events = b3.events.eventManager
        self._eventsStats = b3.events.EventsStats(self)
        self.bot('--------------------------------------------')
        bot_name = self.config.get('b3', 'bot_name')
        if bot_name:
            self.name = bot_name
        bot_prefix = self.config.get('b3', 'bot_prefix')
        if bot_prefix:
            self.prefix = bot_prefix
        else:
            self.prefix = ''
        self.msgPrefix = self.prefix
        if self.config.has_option('server', 'delay'):
            delay = self.config.getfloat('server', 'delay')
            if self.delay > 0:
                self.delay = delay
        if self.config.has_option('server', 'lines_per_second'):
            delay2 = self.config.getfloat('server', 'lines_per_second')
            if delay2 > 0:
                self.delay2 = 1 / delay2
        try:
            dsn = self.config.get('b3', 'database')
            self.storage = b3.storage.getStorage(dsn=dsn, dsnDict=splitDSN(dsn), console=self)
        except (AttributeError, ImportError) as e:
            self.critical('Could not setup storage module: %s', e)

        self.storage.connect()
        if self.config.has_option('server', 'game_log'):
            game_log = self.config.get('server', 'game_log')
            if game_log[0:6] == 'ftp://' or game_log[0:7] == 'sftp://' or game_log[0:7] == 'http://':
                self.remoteLog = True
                self.bot('Working in remote-log mode: %s', game_log)
                if self.config.has_option('server', 'local_game_log'):
                    f = self.config.getpath('server', 'local_game_log')
                else:
                    logext = str(self._rconIp.replace('.', '_'))
                    logext = 'games_mp_' + logext + '_' + str(self._port) + '.log'
                    f = os.path.normpath(os.path.expanduser(logext))
                f = b3.getWritableFilePath(f, True)
                if self.config.has_option('server', 'log_append'):
                    if not (self.config.getboolean('server', 'log_append') and os.path.isfile(f)):
                        self.screen.write('Creating gamelog : %s\n' % b3.getShortPath(os.path.abspath(f)))
                        ftptempfile = open(f, 'w')
                        ftptempfile.close()
                    else:
                        self.screen.write('Append to gamelog: %s\n' % b3.getShortPath(os.path.abspath(f)))
                else:
                    self.screen.write('Creating gamelog : %s\n' % b3.getShortPath(os.path.abspath(f)))
                    ftptempfile = open(f, 'w')
                    ftptempfile.close()
            else:
                self.bot('Game log is: %s', game_log)
                f = self.config.getpath('server', 'game_log')
            self.bot('Starting bot reading file: %s', os.path.abspath(f))
            self.screen.write('Using gamelog    : %s\n' % b3.getShortPath(os.path.abspath(f)))
            if os.path.isfile(f):
                self.input = file(f, 'r')
                if self.config.has_option('server', 'seek'):
                    seek = self.config.getboolean('server', 'seek')
                    if seek:
                        self.input.seek(0, os.SEEK_END)
                else:
                    self.input.seek(0, os.SEEK_END)
            else:
                self.screen.write('>>> Cannot read file: %s\n' % os.path.abspath(f))
                self.screen.flush()
                self.critical('Cannot read file: %s', os.path.abspath(f))
        try:
            self.output = self.OutputClass(self, (self._rconIp, self._rconPort), self._rconPassword)
        except Exception as err:
            self.screen.write('>>> Cannot setup RCON: %s\n' % err)
            self.screen.flush()
            self.critical('Cannot setup RCON: %s' % err, exc_info=err)

        if self.config.has_option('server', 'rcon_timeout'):
            custom_socket_timeout = self.config.getfloat('server', 'rcon_timeout')
            self.output.socket_timeout = custom_socket_timeout
            self.bot('Setting rcon socket timeout to: %0.3f sec', custom_socket_timeout)
        if self.config.has_option('server', 'max_line_length'):
            self._line_length = self.config.getint('server', 'max_line_length')
            self.bot('Setting line_length to: %s', self._line_length)
        if self.config.has_option('server', 'line_color_prefix'):
            self._line_color_prefix = self.config.get('server', 'line_color_prefix')
            self.bot('Setting line_color_prefix to: "%s"', self._line_color_prefix)
        if self.rconTest:
            res = self.output.write('status')
            self.output.flush()
            self.screen.write('Testing RCON     : ')
            self.screen.flush()
            badRconReplies = ['Bad rconpassword.', 'Invalid password.']
            if res in badRconReplies:
                self.screen.write('>>> Oops: Bad RCON password\n>>> Hint: This will lead to errors and render B3 without any power to interact!\n')
                self.screen.flush()
                time.sleep(2)
            elif res == '':
                self.screen.write('>>> Oops: No response\n>>> Could be something wrong with the rcon connection to the server!\n>>> Hint 1: The server is not running or it is changing maps.\n>>> Hint 2: Check your server-ip and port.\n')
                self.screen.flush()
                time.sleep(2)
            else:
                self.screen.write('OK\n')
        self.loadEvents()
        self.screen.write('Loading events   : %s events loaded\n' % len(self._events))
        self.clients = Clients(self)
        self.loadPlugins()
        self.loadArbPlugins()
        self.game = b3.game.Game(self, self.gameName)
        try:
            queuesize = self.config.getint('b3', 'event_queue_size')
        except NoOptionError:
            queuesize = 50
        except ValueError as err:
            queuesize = 50
            self.warning(err)

        self.debug('Creating the event queue with size %s', queuesize)
        self.queue = Queue.Queue(queuesize)
        atexit.register(self.shutdown)

    def getAbsolutePath(self, path, decode=False):
        """
        Return an absolute path name and expand the user prefix (~)
        :param path: the relative path we want to expand
        """
        return b3.getAbsolutePath(path, decode=decode)

    def _dumpEventsStats(self):
        """
        Dump event statistics into the B3 log file.
        """
        self._eventsStats.dumpStats()

    def start(self):
        """
        Start B3
        """
        self.bot('Starting parser..')
        self.startup()
        self.say('%s ^2[ONLINE]' % b3.version)
        self.call_plugins_onLoadConfig()
        self.bot('Starting plugins')
        self.startPlugins()
        self._eventsStats_cronTab = b3.cron.CronTab(self._dumpEventsStats)
        self.cron.add(self._eventsStats_cronTab)
        self.bot('All plugins started')
        self.pluginsStarted()
        self.bot('Starting event dispatching thread')
        thread.start_new_thread(self.handleEvents, ())
        self.bot('Start reading game events')
        self.run()

    def die(self):
        """
        Stop B3 with the die exit status (222)
        """
        self.shutdown()
        self.finalize()
        time.sleep(5)
        self.exitcode = 222

    def restart(self):
        """
        Stop B3 with the restart exit status (221)
        """
        self.shutdown()
        time.sleep(5)
        self.bot('Restarting...')
        self.exitcode = 221

    def upTime(self):
        """
        Amount of time B3 has been running
        """
        return self.time() - self._timeStart

    def loadConfig(self, conf):
        """
        Set the config file to load
        """
        if not conf:
            return False
        self.config = conf
        return True

    def saveConfig(self):
        """
        Save configration changes
        """
        self.bot('Saving config: %s', self.config.fileName)
        return self.config.save()

    def startup(self):
        """
        Called after the parser is created before run(). Overwrite this
        for anything you need to initialize you parser with.
        """
        pass

    def pluginsStarted(self):
        """
        Called after the parser loaded and started all plugins. 
        Overwrite this in parsers to take actions once plugins are ready
        """
        pass

    def pause(self):
        """
        Pause B3 log parsing
        """
        self.bot('PAUSING')
        self._paused = True

    def unpause(self):
        """
        Unpause B3 log parsing
        """
        self._paused = False
        self._pauseNotice = False
        self.input.seek(0, os.SEEK_END)

    def loadEvents(self):
        """
        Load events from event manager
        """
        self._events = self.Events.events

    def createEvent(self, key, name=None):
        """
        Create a new event
        """
        self.Events.createEvent(key, name)
        self._events = self.Events.events
        return self._events[key]

    def getEventID(self, key):
        """
        Get the numeric ID of an event key
        """
        return self.Events.getId(key)

    def getEvent(self, key, data=None, client=None, target=None):
        """
        Return a new Event object for an event name
        """
        return b3.events.Event(self.Events.getId(key), data, client, target)

    def getEventName(self, key):
        """
        Get the name of an event by its key
        """
        return self.Events.getName(key)

    def getEventKey(self, event_id):
        """
        Get the key of a given event ID
        """
        return self.Events.getKey(event_id)

    def getPlugin(self, plugin):
        """
        Get a reference to a loaded plugin
        """
        try:
            return self._plugins[plugin]
        except KeyError:
            return

        return

    def reloadConfigs(self):
        """
        Reload all config files
        """
        self.config.load(self.config.fileName)
        for k in self._plugins:
            self.bot('Reload configuration file for plugin %s', k)
            self._plugins[k].loadConfig()

        self.updateDocumentation()

    def loadPlugins(self):
        """
        Load plugins specified in the config
        """
        self.screen.write('Loading plugins  : ')
        self.screen.flush()
        extplugins_dir = self.config.get_external_plugins_dir()
        self.bot('Loading plugins (external plugin directory: %s)' % extplugins_dir)

        def _get_plugin_config(p_name, p_clazz, p_config_path=None):
            """
            Helper that load and return a configuration file for the given Plugin
            :param p_name: The plugin name
            :param p_clazz: The class implementing the plugin
            :param p_config_path: The plugin configuration file path
            """

            def _search_config_file(match):
                """
                Helper that returns a list of configuration files.
                :param match: The plugin name
                """
                search = '%s%s*%s*' % (b3.getAbsolutePath('@conf\\', decode=True), os.path.sep, match)
                self.debug('Searching for configuration file(s) matching: %s' % search)
                collection = glob.glob(search)
                if len(collection) > 0:
                    return collection
                search = '%s%s*%s*' % (os.path.join(b3.getAbsolutePath(extplugins_dir, decode=True), match, 'conf'), os.path.sep, match)
                self.debug('Searching for configuration file(s) matching: %s' % search)
                collection = glob.glob(search)
                return collection

            if p_config_path is None:
                if not p_clazz.requiresConfigFile:
                    self.debug('No configuration file specified for plugin %s: is not required either' % p_name)
                    return
                self.warning('No configuration file specified for plugin %s: searching a valid configuration file...' % p_name)
                search_path = _search_config_file(p_name)
                if len(search_path) == 0:
                    raise b3.config.ConfigFileNotFound('could not find any configuration file for plugin %s' % p_name)
                if len(search_path) > 1:
                    self.warning('Multiple configuration files found for plugin %s: %s', p_name, (', ').join(search_path))
                self.warning('Using %s as configuration file for plugin %s', search_path[0], p_name)
                self.bot('Loading configuration file %s for plugin %s', search_path[0], p_name)
                return b3.config.load(search_path[0])
            else:
                p_config_absolute_path = b3.getAbsolutePath(p_config_path, decode=True)
                if os.path.exists(p_config_absolute_path):
                    self.bot('Loading configuration file %s for plugin %s', p_config_absolute_path, p_name)
                    return b3.config.load(p_config_absolute_path)
                self.warning('Could not find specified configuration file %s for plugin %s', p_config_absolute_path, p_name)
                if p_clazz.requiresConfigFile:
                    raise b3.config.ConfigFileNotFound('plugin %s cannot be loaded without a configuration file' % p_name)
                self.warning('Not loading a configuration file for plugin %s: plugin %s can work also without a configuration file', p_name, p_name)
                self.info('NOTE: plugin %s may behave differently from what expected since no user configuration file has been loaded', p_name)
                return
                return

        plugin_list = []
        plugin_required = []
        sorted_plugin_list = []
        plugins = OrderedDict()
        for p in self.config.get_plugins():
            if p['name'] in [ plugins[i].name for i in plugins if plugins[i].name == p['name'] ]:
                self.warning('Plugin %s already loaded: avoid multiple entries of the same plugin', p['name'])
                continue
            try:
                mod = self.pluginImport(p['name'], p['path'])
                clz = getattr(mod, '%sPlugin' % p['name'].title())
                cfg = _get_plugin_config(p['name'], clz, p['conf'])
                plugins[p['name']] = PluginData(name=p['name'], module=mod, clazz=clz, conf=cfg, disabled=p['disabled'])
            except Exception as err:
                self.error('Could not load plugin %s' % p['name'], exc_info=err)

        if 'admin' not in plugins:
            self.critical('Plugin admin is essential and MUST be loaded! Cannot continue without admin plugin')

        def _get_plugin_data(p_data):
            """
            Return a list of PluginData of plugins needed by the current one
            :param p_data: A PluginData containing plugin information
            :return: list[PluginData] a list of PluginData of plugins needed by the current one
            """
            if p_data.clazz:
                if p_data.clazz.requiresVersion and B3version(p_data.clazz.requiresVersion) > B3version(currentVersion):
                    raise MissingRequirement('plugin %s requires B3 version %s (you have version %s) : please update your B3 if you want to run this plugin' % (
                     p_data.name, p_data.clazz.requiresVersion, currentVersion))
                if p_data.clazz.requiresParsers and self.gameName not in p_data.clazz.requiresParsers:
                    raise MissingRequirement('plugin %s is not compatible with %s parser : supported games are : %s' % (
                     p_data.name, self.gameName, (', ').join(p_data.clazz.requiresParsers)))
                if p_data.clazz.requiresStorage and self.storage.protocol not in p_data.clazz.requiresStorage:
                    raise MissingRequirement('plugin %s is not compatible with the storage protocol being used (%s) : supported protocols are : %s' % (
                     p_data.name, self.storage.protocol,
                     (', ').join(p_data.clazz.requiresStorage)))
                if p_data.clazz.requiresPlugins:
                    collection = [p_data]
                    for r in p_data.clazz.requiresPlugins:
                        if r not in plugins and r not in plugin_required:
                            try:
                                self.debug('Plugin %s has unmet dependency : %s : trying to load plugin %s...' % (p_data.name, r, r))
                                collection += _get_plugin_data(PluginData(name=r))
                                self.debug('Plugin %s dependency satisfied: %s' % (p_data.name, r))
                            except Exception as ex:
                                raise MissingRequirement('missing required plugin: %s : %s' % (r, extract_tb(sys.exc_info()[2])), ex)

                    return collection
            if p_data.name not in plugins and p_data.name not in plugin_required:
                self.debug('Looking for plugin %s module and configuration file...' % p_data.name)
                p_data.module = self.pluginImport(p_data.name)
                p_data.clazz = getattr(p_data.module, '%sPlugin' % p_data.name.title())
                p_data.conf = _get_plugin_config(p_data.name, p_data.clazz)
                plugin_required.append(p_data.name)
            return [p_data]

        for plugin_name, plugin_data in plugins.items():
            try:
                plugin_list += _get_plugin_data(plugin_data)
            except MissingRequirement as err:
                self.error('Could not load plugin %s' % plugin_name, exc_info=err)

        plugin_dict = {x.name:x for x in plugin_list}
        plugin_data = plugin_dict.pop('admin')
        plugin_list.remove(plugin_data)
        sorted_plugin_list.append(plugin_data)
        self.bot('Sorting plugins according to their dependency tree...')
        sorted_list = [ y for y in topological_sort([ (x.name, set(x.clazz.requiresPlugins + [ z for z in x.clazz.loadAfterPlugins if z in plugin_dict ])) for x in plugin_list
                                                    ])
                      ]
        for plugin_name in sorted_list:
            sorted_plugin_list.append(plugin_dict[plugin_name])

        for plugin_data in sorted_plugin_list:
            if plugin_data.disabled:
                if plugin_data.name == 'admin':
                    plugin_data.enabled = True
                elif plugin_data.clazz.requiresPlugins:
                    for req in plugin_data.clazz.requiresPlugins:
                        plugin_dict = {x.name:x for x in sorted_plugin_list}
                        if req in plugin_dict and plugin_dict[req].enabled:
                            plugin_data.enabled = True

        self.bot('Ready to create plugin instances: %s' % (', ').join([ x.name for x in sorted_plugin_list ]))
        plugin_num = 1
        self._plugins = OrderedDict()
        for plugin_data in sorted_plugin_list:
            plugin_conf_path = '--' if plugin_data.conf is None else plugin_data.conf.fileName
            try:
                try:
                    self.bot('Loading plugin #%s : %s [%s]', plugin_num, plugin_data.name, plugin_conf_path)
                    self._plugins[plugin_data.name] = plugin_data.clazz(self, plugin_data.conf)
                except Exception as err:
                    self.error('Could not load plugin %s' % plugin_data.name, exc_info=err)
                    self.screen.write('x')
                else:
                    if plugin_data.disabled:
                        self.info('Disabling plugin %s' % plugin_data.name)
                        self._plugins[plugin_data.name].disable()
                    plugin_num += 1
                    version = getattr(plugin_data.module, '__version__', 'Unknown Version')
                    author = getattr(plugin_data.module, '__author__', 'Unknown Author')
                    self.bot('Plugin %s (%s - %s) loaded', plugin_data.name, version, author)
                    self.screen.write('.')

            finally:
                self.screen.flush()

        return

    def call_plugins_onLoadConfig(self):
        """
        For each loaded plugin, call the onLoadConfig hook.
        """
        for plugin_name in self._plugins:
            p = self._plugins[plugin_name]
            p.onLoadConfig()

    def loadArbPlugins(self):
        """
        Load must have plugins.
        """
        _mandatory_plugins = [
         'ftpytail', 'sftpytail', 'httpytail']

        def _load_plugin(console, plugin_name):
            """
            Helper which takes care of loading a single plugin.
            :param console: The current console instance
            :param plugin_name: The name of the plugin to load
            """
            try:
                try:
                    console.bot('Loading plugin : %s', plugin_name)
                    plugin_module = console.pluginImport(plugin_name)
                    console._plugins[plugin_name] = getattr(plugin_module, '%sPlugin' % plugin_name.title())(console)
                    version = getattr(plugin_module, '__version__', 'Unknown Version')
                    author = getattr(plugin_module, '__author__', 'Unknown Author')
                except Exception as e:
                    console.screen.write('x')
                    if plugin_name in _mandatory_plugins:
                        console.screen.write('\n')
                        console.screen.write('>>> CRITICAL: missing mandatory plugin: %s\n' % plugin_name)
                        console.critical('Could not start B3 without %s plugin' % plugin_name, exc_info=e)
                    else:
                        console.error('Could not load plugin %s' % plugin_name, exc_info=e)
                else:
                    console.screen.write('.')
                    console.bot('Plugin %s (%s - %s) loaded', plugin_name, version, author)

            finally:
                console.screen.flush()

        if 'publist' not in self._plugins:
            _load_plugin(self, 'publist')
        if self.config.has_option('server', 'game_log'):
            game_log = self.config.get('server', 'game_log')
            remote_log_plugin = None
            if game_log.startswith('ftp://'):
                remote_log_plugin = 'ftpytail'
            elif game_log.startswith('sftp://'):
                remote_log_plugin = 'sftpytail'
            elif game_log.startswith('http://'):
                remote_log_plugin = 'httpytail'
            if remote_log_plugin and remote_log_plugin not in self._plugins:
                _load_plugin(self, remote_log_plugin)
        self.screen.write(' (%s)\n' % len(self._plugins.keys()))
        self.screen.flush()
        return

    def pluginImport(self, name, path=None):
        """
        Import a single plugin.
        :param name: The plugin name
        """
        if path is not None:
            self.info('Loading plugin from specified path: %s', path)
            fp, pathname, description = imp.find_module(name, [path])
            try:
                return imp.load_module(name, fp, pathname, description)
            finally:
                if fp:
                    fp.close()

        fp = None
        try:
            try:
                fp, pathname, description = imp.find_module(name, [os.path.join(b3.getB3Path(True), 'plugins')])
                return imp.load_module(name, fp, pathname, description)
            except ImportError as m:
                self.verbose('%s is not a built-in plugin (%s)' % (name.title(), m))
                self.verbose('Trying external plugin directory : %s', self.config.get_external_plugins_dir())
                fp, pathname, description = imp.find_module(name, [self.config.get_external_plugins_dir()])
                return imp.load_module(name, fp, pathname, description)

        finally:
            if fp:
                fp.close()

        return

    def startPlugins(self):
        """
        Start all loaded plugins.
        """
        self.screen.write('Starting plugins : ')
        self.screen.flush()

        def start_plugin(console, p_name):
            """
            Helper which handles the startup of a single plugin
            :param console: the console instance
            :param p_name: the plugin name
            """
            p = console._plugins[p_name]
            p.onStartup()
            p.start()

        plugin_num = 1
        for plugin_name in self._plugins:
            try:
                try:
                    self.bot('Starting plugin #%s : %s' % (plugin_num, plugin_name))
                    start_plugin(self, plugin_name)
                except Exception as err:
                    self.error('Could not start plugin %s' % plugin_name, exc_info=err)
                    self.screen.write('x')
                else:
                    self.screen.write('.')
                    plugin_num += 1

            finally:
                self.screen.flush()

        self.screen.write(' (%s)\n' % str(plugin_num - 1))

    def disablePlugins(self):
        """
        Disable all plugins except for 'admin', 'publist', 'ftpytail', 'sftpytail', 'httpytail', 'cod7http'
        """
        for k in self._plugins:
            if k not in ('admin', 'publist', 'ftpytail', 'sftpytail', 'httpytail',
                         'cod7http'):
                p = self._plugins[k]
                self.bot('Disabling plugin: %s', k)
                p.disable()

    def enablePlugins(self):
        """
        Enable all plugins except for 'admin', 'publist', 'ftpytail', 'sftpytail', 'httpytail', 'cod7http'
        """
        for k in self._plugins:
            if k not in ('admin', 'publist', 'ftpytail', 'sftpytail', 'httpytail',
                         'cod7http'):
                p = self._plugins[k]
                self.bot('Enabling plugin: %s', k)
                p.enable()

    def getMessage(self, msg, *args):
        """
        Return a message from the config file
        """
        try:
            msg = self._messages[msg]
        except KeyError:
            try:
                msg = self._messages[msg] = self.config.getTextTemplate('messages', msg)
            except Exception as err:
                self.warning("Falling back on default message for '%s': %s" % (msg, err))
                msg = vars2printf(self._messages_default.get(msg, '')).strip()

        if len(args):
            if type(args[0]) == dict:
                return msg % args[0]
            else:
                return msg % args

        else:
            return msg

    @staticmethod
    def getMessageVariables(*args, **kwargs):
        """
        Dynamically generate a dictionary of fields available for messages in config file.
        """
        variables = {}
        for obj in args:
            if obj is None:
                continue
            if type(obj).__name__ in ('str', 'unicode'):
                if obj not in variables:
                    variables[obj] = obj
            else:
                for attr in vars(obj):
                    pattern = re.compile('[\\W_]+')
                    cleanattr = pattern.sub('', attr)
                    variables[cleanattr] = getattr(obj, attr)

        for key, obj in kwargs.iteritems():
            if obj is None:
                continue
            if type(obj).__name__ in ('str', 'unicode'):
                if key not in variables:
                    variables[key] = obj
            else:
                for attr in vars(obj):
                    pattern = re.compile('[\\W_]+')
                    cleanattr = pattern.sub('', attr)
                    currkey = ('').join([key, cleanattr])
                    variables[currkey] = getattr(obj, attr)

        return variables

    def getCommand(self, cmd, **kwargs):
        """
        Return a reference to a loaded command
        """
        try:
            cmd = self._commands[cmd]
        except KeyError:
            return

        return cmd % kwargs

    @Memoize
    def getGroup(self, data):
        """
        Return a valid Group from storage.
        <data> can be either a group keyword or a group level.
        Raises KeyError if group is not found.
        """
        if type(data) is int or isinstance(data, basestring) and data.isdigit():
            g = Group(level=data)
        else:
            g = Group(keyword=data)
        return self.storage.getGroup(g)

    def getGroupLevel(self, data):
        """
        Return a valid Group level.
        <data> can be either a group keyword or a group level.
        Raises KeyError if group is not found.
        """
        group = self.getGroup(data)
        return group.level

    def getTzOffsetFromName(self, tz_name=None):
        """
        Returns the timezone offset given its name.
        :param tz_name: The timezone name
        :return: tuple
        """
        if tz_name:
            if tz_name not in b3.timezones.timezones:
                self.warning('Unknown timezone name [%s]: falling back to auto-detection mode. Valid timezone codes can be found on http://wiki.bigbrotherbot.net/doku.php/usage:available_timezones' % tz_name)
            else:
                self.info('Using timezone: %s : %s' % (tz_name, b3.timezones.timezones[tz_name]))
                return (b3.timezones.timezones[tz_name], tz_name)
        self.debug('Auto detecting timezone information...')
        tz_local = dateutil.tz.tzlocal()
        tz_info = (tz_local.utcoffset(datetime.datetime.now(tz_local)).total_seconds() / 3600,
         tz_local.tzname(datetime.datetime.now(tz_local)))
        self.info('Using timezone: %s : %s' % (tz_info[1], tz_info[0]))
        return tz_info

    def formatTime(self, gmttime, tz_name=None):
        """
        Return a time string formatted to local time in the b3 config time_format
        :param gmttime: The current GMT time
        :param tz_name: The timezone name to be used for time formatting
        """
        if tz_name:
            tz_name = str(tz_name).strip().upper()
            try:
                tz_offset = float(tz_name) * 3600
            except ValueError:
                tz_offset, tz_name = self.getTzOffsetFromName(tz_name)

        else:
            tz_name = None
            if self.config.has_option('b3', 'time_zone'):
                tz_name = self.config.get('b3', 'time_zone').strip().upper()
                tz_name = tz_name if tz_name and tz_name != 'AUTO' else None
            tz_offset, tz_name = self.getTzOffsetFromName(tz_name)
        time_format = self.config.get('b3', 'time_format').replace('%Z', tz_name).replace('%z', tz_name)
        self.debug('Formatting time with timezone [%s], tzOffset : %s' % (tz_name, tz_offset))
        return time.strftime(time_format, time.gmtime(gmttime + int(tz_offset * 3600)))

    def run(self):
        """
        Main worker thread for B3
        """
        self.screen.write("Startup complete : B3 is running! Let's get to work!\n\n")
        self.screen.write('If you run into problems check your B3 log file for more information\n')
        self.screen.flush()
        self.updateDocumentation()
        log_time_start = None
        log_time_last = 0
        while self.working:
            if self._paused:
                if not self._pauseNotice:
                    self.bot('PAUSED - not parsing any lines: B3 will be out of sync')
                    self._pauseNotice = True
            else:
                lines = self.read()
                if lines:
                    for line in lines:
                        line = str(line).strip()
                        if line and self._lineTime is not None:
                            m = self._lineTime.match(line)
                            if m:
                                log_time_current = int(m.group('minutes')) * 60 + int(m.group('seconds'))
                                if log_time_start and log_time_current - log_time_start < log_time_last:
                                    log_time_start = log_time_current
                                    log_time_last = 0
                                    self.debug('log time reset %d' % log_time_current)
                                elif not log_time_start:
                                    log_time_start = log_time_current
                                log_time_current -= log_time_start
                                self.logTime += log_time_current - log_time_last
                                log_time_last = log_time_current
                            self.console(line)
                            try:
                                self.parseLine(line)
                            except SystemExit:
                                raise
                            except Exception as msg:
                                self.error('Could not parse line %s: %s', msg, extract_tb(sys.exc_info()[2]))

                            time.sleep(self.delay2)

            time.sleep(self.delay)

        self.bot('Stop reading')
        with self.exiting:
            self.input.close()
            self.output.close()
            if self.exitcode:
                sys.exit(self.exitcode)
        return

    def parseLine(self, line):
        """
        Parse a single line from the log file
        """
        m = re.match(self._lineFormat, line)
        if m:
            self.queueEvent(b3.events.Event(self.getEventID('EVT_UNKNOWN'), m.group(2)[:1]))

    def registerHandler(self, event_name, event_handler):
        """
        Register an event handler.
        """
        self.debug('%s: register event <%s>', event_handler.__class__.__name__, self.getEventName(event_name))
        if event_name not in self._handlers:
            self._handlers[event_name] = []
        if event_handler not in self._handlers[event_name]:
            self._handlers[event_name].append(event_handler)

    def unregisterHandler(self, event_handler):
        """
        Unregister an event handler.
        """
        for event_name in self._handlers:
            if event_handler in self._handlers[event_name]:
                self.debug('%s: unregister event <%s>', event_handler.__class__.__name__, self.getEventName(event_name))
                self._handlers[event_name].remove(event_handler)

    def queueEvent(self, event, expire=10):
        """
        QueEvents.gevent for processing.
        """
        if not hasattr(event, 'type'):
            return False
        if event.type in self._handlers:
            self.verbose('Queueing event %s : %s', self.getEventName(event.type), event.data)
            try:
                time.sleep(0.001)
                self.queue.put((self.time(), self.time() + expire, event), True, 2)
                return True
            except Queue.Full:
                self.error('**** Event queue was full (%s)', self.queue.qsize())
                return False

        return False

    def handleEvents(self):
        """
        Event handler thread.
        """
        while self.working:
            added, expire, event = self.queue.get(True)
            if event.type == self.getEventID('EVT_EXIT') or event.type == self.getEventID('EVT_STOP'):
                self.working = False
            event_name = self.getEventName(event.type)
            self._eventsStats.add_event_wait((self.time() - added) * 1000)
            if self.time() >= expire:
                self.error('**** Event sat in queue too long: %s %s', event_name, self.time() - expire)
            else:
                nomore = False
                for hfunc in self._handlers[event.type]:
                    if not hfunc.isEnabled():
                        continue
                    elif nomore:
                        break
                    self.verbose('Parsing event: %s: %s', event_name, hfunc.__class__.__name__)
                    timer_plugin_begin = time.clock()
                    try:
                        try:
                            hfunc.parseEvent(event)
                            time.sleep(0.001)
                        except b3.events.VetoEvent:
                            self.bot('Event %s vetoed by %s', event_name, str(hfunc))
                            nomore = True
                        except SystemExit as e:
                            self.exitcode = e.code
                        except Exception as msg:
                            self.error('Handler %s could not handle event %s: %s: %s %s', hfunc.__class__.__name__, event_name, msg.__class__.__name__, msg, extract_tb(sys.exc_info()[2]))

                    finally:
                        elapsed = time.clock() - timer_plugin_begin
                        self._eventsStats.add_event_handled(hfunc.__class__.__name__, event_name, elapsed * 1000)

        self.bot('Shutting down event handler')
        if self.exiting.locked():
            self.exiting.release()

    def write(self, msg, maxRetries=None, socketTimeout=None):
        """
        Write a message to Rcon/Console
        """
        if self.output:
            res = self.output.write(msg, maxRetries=maxRetries, socketTimeout=socketTimeout)
            self.output.flush()
            return res

    def writelines(self, msg):
        """
        Write a sequence of messages to Rcon/Console. Optimized for speed.
        :param msg: The message to be sent to Rcon/Console.
        """
        if self.output and msg:
            res = self.output.writelines(msg)
            self.output.flush()
            return res

    def __read_input(self, game_log):
        """
        Read lines from the log file
        :param game_log: The gamelog file pointer
        """
        return game_log.readlines()

    def ___read_input_darwin(self, game_log):
        """
        Read lines from the log file (darwin version)
        :param game_log: The gamelog file pointer
        """
        return [
         game_log.readline()]

    def read(self):
        """
        Read from game server log file
        """
        if not hasattr(self, 'input'):
            self.critical("Cannot read game log file: check that you have a correct value for the 'game_log' setting in your main config file")
        filestats = os.fstat(self.input.fileno())
        if self.input.tell() > filestats.st_size:
            self.debug('Parser: game log is suddenly smaller than it was before (%s bytes, now %s), the log was probably either rotated or emptied. B3 will now re-adjust to the new size of the log' % (
             str(self.input.tell()), str(filestats.st_size)))
            self.input.seek(0, os.SEEK_END)
        return self.__read(self.input)

    def shutdown(self):
        """
        Shutdown B3.
        """
        try:
            if self.working and self.exiting.acquire():
                self.bot('Shutting down...')
                self.working = False
                for k, plugin in self._plugins.items():
                    plugin.parseEvent(b3.events.Event(self.getEventID('EVT_STOP'), ''))

                if self._cron:
                    self.bot('Stopping cron')
                    self._cron.stop()
                if self.storage:
                    self.bot('Shutting down database connection')
                    self.storage.shutdown()
        except Exception as e:
            self.error(e)

    def finalize(self):
        """
        Commons operation to be done on B3 shutdown.
        Called internally by b3.parser.die()
        """
        if b3.getPlatform() in ('linux', 'darwin'):
            b3_name = os.path.basename(self.config.fileName)
            for x in ('.xml', '.ini'):
                b3_name = right_cut(b3_name, x)

            pidpath = os.path.join(b3.getAbsolutePath('@b3/', decode=True), '..', 'scripts', 'pid', '%s.pid' % b3_name)
            if os.path.isfile(pidpath):
                self.bot('Found PID file : %s : attempt to remove it' % pidpath)
                try:
                    os.unlink(pidpath)
                except Exception as e:
                    self.error('Could not remove PID file (%s) : %s' % (pidpath, e))
                else:
                    self.bot('PID file removed (%s)' % pidpath)

    def getWrap(self, text):
        """
        Returns a sequence of lines for text that fits within the limits.
        :param text: The text that needs to be splitted.
        """
        if not text:
            return []
        else:
            if not self._use_color_codes:
                text = self.stripColors(text)
            if not self.wrapper:
                self.wrapper = TextWrapper(width=self._line_length, drop_whitespace=True, break_long_words=True, break_on_hyphens=False)
            wrapped_text = self.wrapper.wrap(text)
            if self._use_color_codes:
                lines = []
                color = self._line_color_prefix
                for line in wrapped_text:
                    if not lines:
                        lines.append('%s%s' % (color, line))
                    else:
                        lines.append('^3>%s%s' % (color, line))
                    match = re.findall(self._reColor, line)
                    if match:
                        color = match[(-1)]

                return lines
            lines = [
             wrapped_text[0]]
            if len(wrapped_text) > 1:
                for line in wrapped_text[1:]:
                    lines.append('>%s' % line)

            return lines

    def error(self, msg, *args, **kwargs):
        """
        Log an ERROR message.
        """
        self.log.error(msg, *args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        """
        Log a DEBUG message.
        """
        self.log.debug(msg, *args, **kwargs)

    def bot(self, msg, *args, **kwargs):
        """
        Log a BOT message.
        """
        self.log.bot(msg, *args, **kwargs)

    def verbose(self, msg, *args, **kwargs):
        """
        Log a VERBOSE message.
        """
        self.log.verbose(msg, *args, **kwargs)

    def verbose2(self, msg, *args, **kwargs):
        """
        Log an EXTRA VERBOSE message.
        """
        self.log.verbose2(msg, *args, **kwargs)

    def console(self, msg, *args, **kwargs):
        """
        Log a CONSOLE message.
        """
        self.log.console(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        """
        Log a WARNING message.
        """
        self.log.warning(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        """
        Log an INFO message.
        """
        self.log.info(msg, *args, **kwargs)

    def exception(self, msg, *args, **kwargs):
        """
        Log an EXCEPTION message.
        """
        self.log.exception(msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        """
        Log a CRITICAL message and shutdown B3.
        """
        self.log.critical(msg, *args, **kwargs)
        self.shutdown()
        self.finalize()
        time.sleep(2)
        self.exitcode = 220
        raise SystemExit(self.exitcode)

    @staticmethod
    def time():
        """
        Return the current time in GMT/UTC.
        """
        return int(time.time())

    def _get_cron(self):
        """
        Instantiate the main Cron object.
        """
        if not self._cron:
            self._cron = b3.cron.Cron(self)
            self._cron.start()
        return self._cron

    cron = property(_get_cron)

    def stripColors(self, text):
        """
        Remove color codes from the given text.
        :param text: the text to clean from color codes.
        :return: str
        """
        return re.sub(self._reColor, '', text).strip()

    def isFrostbiteGame(self, gamename=None):
        """
        Tells whether we are running a Frostbite based game.
        :return: True if we are running a Frostbite game, False otherwise
        """
        if not gamename:
            gamename = self.gameName
        return gamename in self._frostBiteGameNames

    def updateDocumentation(self):
        """
        Create a documentation for all available commands.
        """
        if self.config.has_section('autodoc'):
            try:
                from b3.tools.documentationBuilder import DocBuilder
                docbuilder = DocBuilder(self)
                docbuilder.save()
            except Exception as err:
                self.error('Failed to generate user documentation')
                self.exception(err)

        else:
            self.info('No user documentation generated: to enable update your configuration file')

    def getPlayerList(self):
        """
        Query the game server for connected players.
        return a dict having players' id for keys and players' data as another dict for values
        """
        raise NotImplementedError

    def authorizeClients(self):
        """
        For all connected players, fill the client object with properties allowing to find 
        the user in the database (usualy guid, or punkbuster id, ip) and call the 
        Client.auth() method 
        """
        raise NotImplementedError

    def sync(self):
        """
        For all connected players returned by self.getPlayerList(), get the matching Client
        object from self.clients (with self.clients.getByCID(cid) or similar methods) and
        look for inconsistencies. If required call the client.disconnect() method to remove
        a client from self.clients.
        This is mainly useful for games where clients are identified by the slot number they
        occupy. On map change, a player A on slot 1 can leave making room for player B who
        connects on slot 1.
        """
        raise NotImplementedError

    def say(self, msg, *args):
        """
        Broadcast a message to all players
        """
        raise NotImplementedError

    def saybig(self, msg, *args):
        """
        Broadcast a message to all players in a way that will catch their attention.
        """
        raise NotImplementedError

    def message(self, client, text, *args):
        """
        Display a message to a given player
        """
        raise NotImplementedError

    def kick(self, client, reason='', admin=None, silent=False, *kwargs):
        """
        Kick a given player
        """
        raise NotImplementedError

    def ban(self, client, reason='', admin=None, silent=False, *kwargs):
        """
        Ban a given player on the game server and in case of success
        fire the event ('EVT_CLIENT_BAN', data={'reason': reason, 
        'admin': admin}, client=target)
        """
        raise NotImplementedError

    def unban(self, client, reason='', admin=None, silent=False, *kwargs):
        """
        Unban a given player on the game server
        """
        raise NotImplementedError

    def tempban(self, client, reason='', duration=2, admin=None, silent=False, *kwargs):
        """
        Tempban a given player on the game server and in case of success
        fire the event ('EVT_CLIENT_BAN_TEMP', data={'reason': reason, 
        'duration': duration, 'admin': admin}, client=target)
        """
        raise NotImplementedError

    def getMap(self):
        """
        Return the current map/level name
        """
        raise NotImplementedError

    def getNextMap(self):
        """
        Return the next map/level name to be played
        """
        raise NotImplementedError

    def getMaps(self):
        """
        Return the available maps/levels name
        """
        raise NotImplementedError

    def rotateMap(self):
        """
        Load the next map/level
        """
        raise NotImplementedError

    def changeMap(self, map_name):
        """
        Load a given map/level
        Return a list of suggested map names in cases it fails to recognize the map that was provided
        """
        raise NotImplementedError

    def getPlayerPings(self, filter_client_ids=None):
        """
        Returns a dict having players' id for keys and players' ping for values
        :param filter_client_ids: If filter_client_id is an iterable, only return values for the given client ids.
        """
        raise NotImplementedError

    def getPlayerScores(self):
        """
        Returns a dict having players' id for keys and players' scores for values
        """
        raise NotImplementedError

    def inflictCustomPenalty(self, penalty_type, client, reason=None, duration=None, admin=None, data=None):
        r"""
        Called if b3.admin.penalizeClient() does not know a given penalty type. 
        Overwrite this to add customized penalties for your game like 'slap', 'nuke', 
        'mute', 'kill' or anything you want.
        /!\ This method must return True if the penalty was inflicted.
        """
        pass


class StubParser(object):
    """
    Parser implementation used when dealing with the Storage module while updating B3 database.
    """
    screen = sys.stdout

    def __init__(self):

        class StubSTDOut(object):

            def write(self, *args, **kwargs):
                pass

        if not main_is_frozen():
            self.screen = StubSTDOut()

    def bot(self, msg, *args, **kwargs):
        pass

    def info(self, msg, *args, **kwargs):
        pass

    def debug(self, msg, *args, **kwargs):
        pass

    def error(self, msg, *args, **kwargs):
        pass

    def warning(self, msg, *args, **kwargs):
        pass

    def verbose(self, msg, *args, **kwargs):
        pass

    def verbose2(self, msg, *args, **kwargs):
        pass

    def critical(self, msg, *args, **kwargs):
        pass