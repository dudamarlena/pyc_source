# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./build/lib/supervisor/options.py
# Compiled at: 2019-06-16 14:41:06
# Size of source mod 2**32: 87231 bytes
import socket, getopt, os, sys, tempfile, errno, signal, re, pwd, grp, resource, stat, pkg_resources, glob, platform, warnings, fcntl
from supervisor.compat import PY2
from supervisor.compat import ConfigParser
from supervisor.compat import as_bytes, as_string
from supervisor.compat import xmlrpclib
from supervisor.compat import StringIO
from supervisor.compat import basestring
import supervisor.medusa as asyncore
from supervisor.datatypes import process_or_group_name
from supervisor.datatypes import boolean
from supervisor.datatypes import integer
from supervisor.datatypes import name_to_uid
from supervisor.datatypes import gid_for_uid
from supervisor.datatypes import existing_dirpath
from supervisor.datatypes import byte_size
from supervisor.datatypes import signal_number
from supervisor.datatypes import list_of_exitcodes
from supervisor.datatypes import dict_of_key_value_pairs
from supervisor.datatypes import logfile_name
from supervisor.datatypes import list_of_strings
from supervisor.datatypes import octal_type
from supervisor.datatypes import existing_directory
from supervisor.datatypes import logging_level
from supervisor.datatypes import colon_separated_user_group
from supervisor.datatypes import inet_address
from supervisor.datatypes import InetStreamSocketConfig
from supervisor.datatypes import UnixStreamSocketConfig
from supervisor.datatypes import url
from supervisor.datatypes import Automatic
from supervisor.datatypes import auto_restart
from supervisor.datatypes import profile_options
from supervisor import loggers
from supervisor import states
from supervisor import xmlrpc
from supervisor import poller

def _read_version_txt--- This code section failed: ---

 L.  58         0  LOAD_GLOBAL              os
                2  LOAD_ATTR                path
                4  LOAD_METHOD              abspath
                6  LOAD_GLOBAL              os
                8  LOAD_ATTR                path
               10  LOAD_METHOD              dirname
               12  LOAD_GLOBAL              __file__
               14  CALL_METHOD_1         1  ''
               16  CALL_METHOD_1         1  ''
               18  STORE_FAST               'mydir'

 L.  59        20  LOAD_GLOBAL              os
               22  LOAD_ATTR                path
               24  LOAD_METHOD              join
               26  LOAD_FAST                'mydir'
               28  LOAD_STR                 'version.txt'
               30  CALL_METHOD_2         2  ''
               32  STORE_FAST               'version_txt'

 L.  60        34  LOAD_GLOBAL              open
               36  LOAD_FAST                'version_txt'
               38  LOAD_STR                 'r'
               40  CALL_FUNCTION_2       2  ''
               42  SETUP_WITH           70  'to 70'
               44  STORE_FAST               'f'

 L.  61        46  LOAD_FAST                'f'
               48  LOAD_METHOD              read
               50  CALL_METHOD_0         0  ''
               52  LOAD_METHOD              strip
               54  CALL_METHOD_0         0  ''
               56  POP_BLOCK        
               58  ROT_TWO          
               60  BEGIN_FINALLY    
               62  WITH_CLEANUP_START
               64  WITH_CLEANUP_FINISH
               66  POP_FINALLY           0  ''
               68  RETURN_VALUE     
             70_0  COME_FROM_WITH       42  '42'
               70  WITH_CLEANUP_START
               72  WITH_CLEANUP_FINISH
               74  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 58


VERSION = _read_version_txt()

def normalize_path(v):
    return os.path.normpathos.path.abspathos.path.expanduserv


class Dummy:
    pass


class Options:
    stderr = sys.stderr
    stdout = sys.stdout
    exit = sys.exit
    warnings = warnings
    uid = gid = None
    progname = sys.argv[0]
    configfile = None
    schemadir = None
    configroot = None
    here = None
    positional_args_allowed = 0

    def __init__(self, require_configfile=True):
        """Constructor.

        Params:
        require_configfile -- whether we should fail on no config file.
        """
        self.names_list = []
        self.short_options = []
        self.long_options = []
        self.options_map = {}
        self.default_map = {}
        self.required_map = {}
        self.environ_map = {}
        self.attr_priorities = {}
        self.require_configfile = require_configfile
        self.add(None, None, 'h', 'help', self.help)
        self.add('configfile', None, 'c:', 'configuration=')
        here = os.path.dirnameos.path.dirnamesys.argv[0]
        searchpaths = [os.path.join(here, 'etc', 'supervisord.conf'),
         os.path.joinhere'supervisord.conf',
         'supervisord.conf',
         'etc/supervisord.conf',
         '/etc/supervisord.conf',
         '/etc/supervisor/supervisord.conf']
        self.searchpaths = searchpaths
        self.environ_expansions = {}
        for k, v in os.environ.items:
            self.environ_expansions['ENV_%s' % k] = v

    def default_configfile(self):
        """Return the name of the found config file or print usage/exit."""
        config = None
        for path in self.searchpaths:
            if os.path.existspath:
                config = path
                break
            if config is None:
                if self.require_configfile:
                    self.usage('No config file found at default paths (%s); use the -c option to specify a config file at a different path' % ', '.joinself.searchpaths)
            return config

    def help(self, dummy):
        """Print a long help message to stdout and exit(0).

        Occurrences of "%s" in are replaced by self.progname.
        """
        help = self.doc + '\n'
        if help.find'%s' > 0:
            help = help.replace'%s'self.progname
        self.stdout.writehelp
        self.exit0

    def usage(self, msg):
        """Print a brief error message to stderr and exit(2)."""
        self.stderr.write('Error: %s\n' % str(msg))
        self.stderr.write('For help, use %s -h\n' % self.progname)
        self.exit2

    def add(self, name=None, confname=None, short=None, long=None, handler=None, default=None, required=None, flag=None, env=None):
        """Add information about a configuration option.

        This can take several forms:

        add(name, confname)
            Configuration option 'confname' maps to attribute 'name'
        add(name, None, short, long)
            Command line option '-short' or '--long' maps to 'name'
        add(None, None, short, long, handler)
            Command line option calls handler
        add(name, None, short, long, handler)
            Assign handler return value to attribute 'name'

        In addition, one of the following keyword arguments may be given:

        default=...  -- if not None, the default value
        required=... -- if nonempty, an error message if no value provided
        flag=...     -- if not None, flag value for command line option
        env=...      -- if not None, name of environment variable that
                        overrides the configuration file or default
        """
        if flag is not None:
            if handler is not None:
                raise ValueError('use at most one of flag= and handler=')
            else:
                if not long:
                    if not short:
                        raise ValueError('flag= requires a command line flag')
                if short:
                    if short.endswith':':
                        raise ValueError('flag= requires a command line flag')
                if long and long.endswith'=':
                    raise ValueError('flag= requires a command line flag')
            handler = lambda arg, flag=flag: flag
        else:
            if short:
                if long:
                    if short.endswith':' != long.endswith'=':
                        raise ValueError('inconsistent short/long options: %r %r' % (
                         short, long))
            if short:
                if short[0] == '-':
                    raise ValueError("short option should not start with '-'")
                key, rest = short[:1], short[1:]
                if rest not in ('', ':'):
                    raise ValueError("short option should be 'x' or 'x:'")
                key = '-' + key
                if key in self.options_map:
                    raise ValueError("duplicate short option key '%s'" % key)
                self.options_map[key] = (
                 name, handler)
                self.short_options.appendshort
            if long:
                if long[0] == '-':
                    raise ValueError("long option should not start with '-'")
                key = long
                if key[(-1)] == '=':
                    key = key[:-1]
                key = '--' + key
                if key in self.options_map:
                    raise ValueError("duplicate long option key '%s'" % key)
                self.options_map[key] = (
                 name, handler)
                self.long_options.appendlong
            if env:
                self.environ_map[env] = (
                 name, handler)
            if name:
                if not hasattr(self, name):
                    setattr(self, name, None)
                self.names_list.append(name, confname)
                if default is not None:
                    self.default_map[name] = default
                if required:
                    self.required_map[name] = required

    def _set(self, attr, value, prio):
        current = self.attr_priorities.getattr(-1)
        if prio >= current:
            setattr(self, attr, value)
            self.attr_priorities[attr] = prio

    def realize(self, args=None, doc=None, progname=None):
        """Realize a configuration.

        Optional arguments:

        args     -- the command line arguments, less the program name
                    (default is sys.argv[1:])

        doc      -- usage message (default is __main__.__doc__)
        """
        if args is None:
            args = sys.argv[1:]
        else:
            if progname is None:
                progname = sys.argv[0]
            if doc is None:
                try:
                    import __main__
                    doc = __main__.__doc__
                except Exception:
                    pass

        self.progname = progname
        self.doc = doc
        self.options = []
        self.args = []
        try:
            self.options, self.args = getopt.getopt(args, ''.joinself.short_options, self.long_options)
        except getopt.error as exc:
            try:
                self.usagestr(exc)
            finally:
                exc = None
                del exc

        else:
            if self.args:
                if not self.positional_args_allowed:
                    self.usage('positional arguments are not supported: %s' % str(self.args))
            for opt, arg in self.options:
                name, handler = self.options_map[opt]
                if handler is not None:
                    try:
                        arg = handler(arg)
                    except ValueError as msg:
                        try:
                            self.usage('invalid value for %s %r: %s' % (opt, arg, msg))
                        finally:
                            msg = None
                            del msg

                    if name:
                        if arg is not None:
                            if getattr(self, name) is not None:
                                self.usage('conflicting command line option %r' % opt)
                        self._set(name, arg, 2)

        for envvar in self.environ_map.keys:
            name, handler = self.environ_map[envvar]
            if envvar in os.environ:
                value = os.environ[envvar]
                if handler is not None:
                    try:
                        value = handler(value)
                    except ValueError as msg:
                        try:
                            self.usage('invalid environment value for %s %r: %s' % (
                             envvar, value, msg))
                        finally:
                            msg = None
                            del msg

                if name and value is not None:
                    self._set(name, value, 1)
        else:
            if self.configfile is None:
                self.configfile = self.default_configfile
            self.process_config

    def process_config(self, do_usage=True):
        """Process configuration data structure.

        This includes reading config file if necessary, setting defaults etc.
        """
        if self.configfile:
            self.process_config_filedo_usage
        for name, confname in self.names_list:
            if confname:
                parts = confname.split'.'
                obj = self.configroot
                for part in parts:
                    if obj is None:
                        break
                    obj = getattr(obj, part)
                else:
                    self._set(name, obj, 0)

        else:
            for name, value in self.default_map.items:
                if getattr(self, name) is None:
                    setattr(self, name, value)
            else:
                for name, message in self.required_map.items:
                    if getattr(self, name) is None:
                        self.usagemessage

    def process_config_file(self, do_usage):
        if not hasattr(self.configfile, 'read'):
            self.here = os.path.abspathos.path.dirnameself.configfile
        try:
            self.read_configself.configfile
        except ValueError as msg:
            try:
                if do_usage:
                    self.usagestr(msg)
                else:
                    raise ValueError(msg)
            finally:
                msg = None
                del msg

    def exists(self, path):
        return os.path.existspath

    def open(self, fn, mode='r'):
        return open(fn, mode)

    def get_plugins(self, parser, factory_key, section_prefix):
        factories = []
        for section in parser.sections:
            if not section.startswithsection_prefix:
                pass
            else:
                name = section.split':'1[1]
                factory_spec = parser.saneget(section, factory_key, None)
                if factory_spec is None:
                    raise ValueError('section [%s] does not specify a %s' % (
                     section, factory_key))

        try:
            factory = self.import_specfactory_spec
        except ImportError:
            raise ValueError('%s cannot be resolved within [%s]' % (
             factory_spec, section))
        else:
            extras = {}
            for k in parser.optionssection:
                if k != factory_key:
                    extras[k] = parser.sanegetsectionk
                factories.append(name, factory, extras)
            else:
                return factories

    def import_spec(self, spec):
        ep = pkg_resources.EntryPoint.parse('x=' + spec)
        if hasattr(ep, 'resolve'):
            return ep.resolve
        return ep.loadFalse


class ServerOptions(Options):
    user = None
    sockchown = None
    sockchmod = None
    logfile = None
    loglevel = None
    pidfile = None
    passwdfile = None
    nodaemon = None
    environment = None
    httpservers = ()
    unlink_pidfile = False
    unlink_socketfiles = False
    mood = states.SupervisorStates.RUNNING

    def __init__(self):
        Options.__init__self
        self.configroot = Dummy()
        self.configroot.supervisord = Dummy()
        self.add(None, None, 'v', 'version', self.version)
        self.add('nodaemon', 'supervisord.nodaemon', 'n', 'nodaemon', flag=1, default=0)
        self.add('user', 'supervisord.user', 'u:', 'user=')
        self.add('umask', 'supervisord.umask', 'm:', 'umask=', octal_type,
          default='022')
        self.add('directory', 'supervisord.directory', 'd:', 'directory=', existing_directory)
        self.add('logfile', 'supervisord.logfile', 'l:', 'logfile=', existing_dirpath,
          default='supervisord.log')
        self.add('logfile_maxbytes', 'supervisord.logfile_maxbytes', 'y:',
          'logfile_maxbytes=', byte_size, default=52428800)
        self.add('logfile_backups', 'supervisord.logfile_backups', 'z:',
          'logfile_backups=', integer, default=10)
        self.add('loglevel', 'supervisord.loglevel', 'e:', 'loglevel=', logging_level,
          default='info')
        self.add('pidfile', 'supervisord.pidfile', 'j:', 'pidfile=', existing_dirpath,
          default='supervisord.pid')
        self.add('identifier', 'supervisord.identifier', 'i:', 'identifier=', str,
          default='supervisor')
        self.add('childlogdir', 'supervisord.childlogdir', 'q:', 'childlogdir=', existing_directory,
          default=(tempfile.gettempdir))
        self.add('minfds', 'supervisord.minfds', 'a:',
          'minfds=', int, default=1024)
        self.add('minprocs', 'supervisord.minprocs', '',
          'minprocs=', int, default=200)
        self.add('nocleanup', 'supervisord.nocleanup', 'k',
          'nocleanup', flag=1, default=0)
        self.add('strip_ansi', 'supervisord.strip_ansi', 't',
          'strip_ansi', flag=1, default=0)
        self.add('profile_options', 'supervisord.profile_options', '',
          'profile_options=', profile_options, default=None)
        self.pidhistory = {}
        self.process_group_configs = []
        self.parse_criticals = []
        self.parse_warnings = []
        self.parse_infos = []
        self.signal_receiver = SignalReceiver()
        self.poller = poller.Pollerself

    def version(self, dummy):
        """Print version to stdout and exit(0).
        """
        self.stdout.write('%s\n' % VERSION)
        self.exit0

    def getLogger(self, *args, **kwargs):
        return (loggers.getLogger)(*args, **kwargs)

    def default_configfile(self):
        if os.getuid == 0:
            self.warnings.warn'Supervisord is running as root and it is searching for its configuration file in default locations (including its current working directory); you probably want to specify a "-c" argument specifying an absolute path to a configuration file for improved security.'
        return Options.default_configfileself

    def realize(self, *arg, **kw):
        (Options.realize)(self, *arg, **kw)
        section = self.configroot.supervisord
        if self.user is not None:
            try:
                uid = name_to_uid(self.user)
            except ValueError as msg:
                try:
                    self.usagemsg
                finally:
                    msg = None
                    del msg

            else:
                self.uid = uid
                self.gid = gid_for_uid(uid)
        if not self.loglevel:
            self.loglevel = section.loglevel
        else:
            if self.logfile:
                logfile = self.logfile
            else:
                logfile = section.logfile
            self.logfile = normalize_path(logfile)
            if self.pidfile:
                pidfile = self.pidfile
            else:
                pidfile = section.pidfile
        self.pidfile = normalize_path(pidfile)
        self.rpcinterface_factories = section.rpcinterface_factories
        self.serverurl = None
        self.server_configs = sconfigs = section.server_configs
        for config in [config for config in sconfigs if config['family'] is socket.AF_UNIX]:
            path = config['file']
            self.serverurl = 'unix://%s' % path
            break
        else:
            if self.serverurl is None:
                for config in [config for config in sconfigs if config['family'] is socket.AF_INET]:
                    host = config['host']
                    port = config['port']
                    if not host:
                        host = 'localhost'
                    self.serverurl = 'http://%s:%s' % (host, port)

            self.identifier = section.identifier

    def process_config(self, do_usage=True):
        Options.process_config(self, do_usage=do_usage)
        new = self.configroot.supervisord.process_group_configs
        self.process_group_configs = new

    def read_config(self, fp):
        self.parse_criticals = []
        self.parse_warnings = []
        self.parse_infos = []
        section = self.configroot.supervisord
        need_close = False
        if not hasattr(fp, 'read'):
            if not self.existsfp:
                raise ValueError('could not find config file %s' % fp)
            try:
                fp = self.openfp'r'
                need_close = True
            except (IOError, OSError):
                raise ValueError('could not read config file %s' % fp)
            else:
                parser = UnhosedConfigParser()
                parser.expansions = self.environ_expansions
                try:
                    try:
                        try:
                            parser.read_filefp
                        except AttributeError:
                            parser.readfpfp

                    except ConfigParser.ParsingError as why:
                        try:
                            raise ValueError(str(why))
                        finally:
                            why = None
                            del why

                finally:
                    if need_close:
                        fp.close

                host_node_name = platform.node
                expansions = {'here':self.here,  'host_node_name':host_node_name}
                expansions.updateself.environ_expansions
                if parser.has_section'include':
                    parser.expand_hereself.here
                    if not parser.has_option'include''files':
                        raise ValueError('.ini file has [include] section, but no files setting')
                    files = parser.get'include''files'
                    files = expand(files, expansions, 'include.files')
                    files = files.split
                    if hasattr(fp, 'name'):
                        base = os.path.dirnameos.path.abspathfp.name
        else:
            base = '.'
        for pattern in files:
            pattern = os.path.joinbasepattern
            filenames = glob.globpattern
            if not filenames:
                self.parse_warnings.append('No file matches via include "%s"' % pattern)
            else:
                for filename in sorted(filenames):
                    self.parse_infos.append('Included extra file "%s" during parsing' % filename)
                    try:
                        parser.readfilename
                    except ConfigParser.ParsingError as why:
                        try:
                            raise ValueError(str(why))
                        finally:
                            why = None
                            del why

                    else:
                        parser.expand_hereos.path.abspathos.path.dirnamefilename
                else:
                    sections = parser.sections
                    if 'supervisord' not in sections:
                        raise ValueError('.ini file does not include supervisord section')
                    else:
                        common_expansions = {'here': self.here}

                        def get(opt, default, **kwargs):
                            expansions = kwargs.get'expansions'{}
                            expansions.updatecommon_expansions
                            kwargs['expansions'] = expansions
                            return (parser.getdefault)(opt, default, **kwargs)

                        section.minfds = integer(get('minfds', 1024))
                        section.minprocs = integer(get('minprocs', 200))
                        directory = get('directory', None)
                        if directory is None:
                            section.directory = None
                        else:
                            section.directory = existing_directory(directory)
                    section.user = get('user', None)
                    section.umask = octal_type(get('umask', '022'))
                    section.logfile = existing_dirpath(get('logfile', 'supervisord.log'))
                    section.logfile_maxbytes = byte_size(get('logfile_maxbytes', '50MB'))
                    section.logfile_backups = integer(get('logfile_backups', 10))
                    section.loglevel = logging_level(get('loglevel', 'info'))
                    section.pidfile = existing_dirpath(get('pidfile', 'supervisord.pid'))
                    section.identifier = get('identifier', 'supervisor')
                    section.nodaemon = boolean(get('nodaemon', 'false'))
                    tempdir = tempfile.gettempdir
                    section.childlogdir = existing_directory(get('childlogdir', tempdir))
                    section.nocleanup = boolean(get('nocleanup', 'false'))
                    section.strip_ansi = boolean(get('strip_ansi', 'false'))
                    environ_str = get('environment', '')
                    environ_str = expand(environ_str, expansions, 'environment')
                    section.environment = dict_of_key_value_pairs(environ_str)
                    section.rpcinterface_factories = self.get_plugins(parser, 'supervisor.rpcinterface_factory', 'rpcinterface:')
                    section.process_group_configs = self.process_groups_from_parserparser
                    for group in section.process_group_configs:
                        for proc in group.process_configs:
                            env = section.environment.copy
                            env.updateproc.environment
                            proc.environment = env
                        else:
                            section.server_configs = self.server_configs_from_parserparser
                            section.profile_options = None
                            return section

    def process_groups_from_parser(self, parser):
        groups = []
        all_sections = parser.sections
        homogeneous_exclude = []
        common_expansions = {'here': self.here}

        def get(section, opt, default, **kwargs):
            expansions = kwargs.get'expansions'{}
            expansions.updatecommon_expansions
            kwargs['expansions'] = expansions
            return (parser.saneget)(section, opt, default, **kwargs)

        for section in all_sections:
            if not section.startswith'group:':
                pass
            else:
                group_name = process_or_group_name(section.split':'1[1])
                programs = list_of_strings(get(section, 'programs', None))
                priority = integer(get(section, 'priority', 999))
                group_processes = []
                for program in programs:
                    program_section = 'program:%s' % program
                    fcgi_section = 'fcgi-program:%s' % program
                    if program_section not in all_sections:
                        if fcgi_section not in all_sections:
                            raise ValueError('[%s] names unknown program or fcgi-program %s' % (section, program))
                    if program_section in all_sections:
                        if fcgi_section in all_sections:
                            raise ValueError('[%s] name %s is ambiguous (exists as program and fcgi-program)' % (
                             section, program))
                    section = program_section if program_section in all_sections else fcgi_section
                    homogeneous_exclude.appendsection
                    processes = self.processes_from_section(parser, section, group_name, ProcessConfig)
                    group_processes.extendprocesses
                else:
                    groups.appendProcessGroupConfig(self, group_name, priority, group_processes)

        else:
            for section in all_sections:
                if section.startswith'program:':
                    if section in homogeneous_exclude:
                        pass
                    else:
                        program_name = process_or_group_name(section.split':'1[1])
                        priority = integer(get(section, 'priority', 999))
                        processes = self.processes_from_section(parser, section, program_name, ProcessConfig)
                        groups.appendProcessGroupConfig(self, program_name, priority, processes)
                for section in all_sections:
                    if not section.startswith'eventlistener:':
                        pass
                    else:
                        pool_name = section.split':'1[1]
                        priority = integer(get(section, 'priority', -1))
                        buffer_size = integer(get(section, 'buffer_size', 10))
                        if buffer_size < 1:
                            raise ValueError('[%s] section sets invalid buffer_size (%d)' % (
                             section, buffer_size))
                        result_handler = get(section, 'result_handler', 'supervisor.dispatchers:default_handler')
                        try:
                            result_handler = self.import_specresult_handler
                        except ImportError:
                            raise ValueError('%s cannot be resolved within [%s]' % (
                             result_handler, section))
                        else:
                            pool_event_names = [x.upper for x in list_of_strings(get(section, 'events', ''))]
                            pool_event_names = set(pool_event_names)
                            if not pool_event_names:
                                raise ValueError('[%s] section requires an "events" line' % section)
                            from supervisor.events import EventTypes
                            pool_events = []
                        for pool_event_name in pool_event_names:
                            pool_event = getattr(EventTypes, pool_event_name, None)
                            if pool_event is None:
                                raise ValueError('Unknown event type %s in [%s] events' % (
                                 pool_event_name, section))
                            pool_events.appendpool_event
                        else:
                            redirect_stderr = boolean(get(section, 'redirect_stderr', 'false'))
                            if redirect_stderr:
                                raise ValueError('[%s] section sets redirect_stderr=true but this is not allowed because it will interfere with the eventlistener protocol' % section)
                            processes = self.processes_from_section(parser, section, pool_name, EventListenerConfig)
                            groups.appendEventListenerPoolConfig(self, pool_name, priority, processes, buffer_size, pool_events, result_handler)

                for section in all_sections:
                    if section.startswith'fcgi-program:':
                        if section in homogeneous_exclude:
                            pass
                        else:
                            program_name = process_or_group_name(section.split':'1[1])
                            priority = integer(get(section, 'priority', 999))
                            fcgi_expansions = {'program_name': program_name}
                            proc_user = get(section, 'user', None)
                            if proc_user is None:
                                proc_uid = None
                            else:
                                proc_uid = name_to_uid(proc_user)
                            socket_backlog = get(section, 'socket_backlog', None)
                            if socket_backlog is not None:
                                socket_backlog = integer(socket_backlog)
                                if socket_backlog < 1 or socket_backlog > 65535:
                                    raise ValueError('Invalid socket_backlog value %s' % socket_backlog)
                            socket_owner = get(section, 'socket_owner', None)
                            if socket_owner is not None:
                                try:
                                    socket_owner = colon_separated_user_group(socket_owner)
                                except ValueError:
                                    raise ValueError('Invalid socket_owner value %s' % socket_owner)

                            socket_mode = get(section, 'socket_mode', None)
                            if socket_mode is not None:
                                try:
                                    socket_mode = octal_type(socket_mode)
                                except (TypeError, ValueError):
                                    raise ValueError('Invalid socket_mode value %s' % socket_mode)

                            socket = get(section, 'socket', None, expansions=fcgi_expansions)
                            if not socket:
                                raise ValueError('[%s] section requires a "socket" line' % section)
                            try:
                                socket_config = self.parse_fcgi_socket(socket, proc_uid, socket_owner, socket_mode, socket_backlog)
                            except ValueError as e:
                                try:
                                    raise ValueError('%s in [%s] socket' % (str(e), section))
                                finally:
                                    e = None
                                    del e

                            else:
                                processes = self.processes_from_section(parser, section, program_name, FastCGIProcessConfig)
                                groups.appendFastCGIGroupConfig(self, program_name, priority, processes, socket_config)
                    groups.sort
                    return groups

    def parse_fcgi_socket(self, sock, proc_uid, socket_owner, socket_mode, socket_backlog):
        if sock.startswith'unix://':
            path = sock[7:]
            if not os.path.isabspath:
                raise ValueError('Unix socket path %s is not an absolute path', path)
            path = normalize_path(path)
            if socket_owner is None:
                uid = os.getuid
                if proc_uid is not None:
                    if proc_uid != uid:
                        socket_owner = (
                         proc_uid, gid_for_uid(proc_uid))
            if socket_mode is None:
                socket_mode = 448
            return UnixStreamSocketConfig(path, owner=socket_owner, mode=socket_mode,
              backlog=socket_backlog)
        if socket_owner is not None or socket_mode is not None:
            raise ValueError('socket_owner and socket_mode params should only be used with a Unix domain socket')
        m = re.match'tcp://([^\\s:]+):(\\d+)$'sock
        if m:
            host = m.group1
            port = int(m.group2)
            return InetStreamSocketConfig(host, port, backlog=socket_backlog)
        raise ValueError('Bad socket format %s', sock)

    def processes_from_section(self, parser, section, group_name, klass=None):
        try:
            return self._processes_from_section(parser, section, group_name, klass)
            except ValueError as e:
            try:
                filename = parser.section_to_file.getsectionself.configfile
                raise ValueError('%s in section %r (file: %r)' % (
                 e, section, filename))
            finally:
                e = None
                del e

    def _processes_from_section(self, parser, section, group_name, klass=None):
        if klass is None:
            klass = ProcessConfig
        else:
            programs = []
            program_name = process_or_group_name(section.split':'1[1])
            host_node_name = platform.node
            common_expansions = {'here':self.here,  'program_name':program_name, 
             'host_node_name':host_node_name, 
             'group_name':group_name}

            def get(section, opt, *args, **kwargs):
                expansions = kwargs.get'expansions'{}
                expansions.updatecommon_expansions
                kwargs['expansions'] = expansions
                return (parser.saneget)(section, opt, *args, **kwargs)

            priority = integer(get(section, 'priority', 999))
            autostart = boolean(get(section, 'autostart', 'true'))
            autorestart = auto_restart(get(section, 'autorestart', 'unexpected'))
            startsecs = integer(get(section, 'startsecs', 1))
            startretries = integer(get(section, 'startretries', 3))
            stopsignal = signal_number(get(section, 'stopsignal', 'TERM'))
            stopwaitsecs = integer(get(section, 'stopwaitsecs', 10))
            stopasgroup = boolean(get(section, 'stopasgroup', 'false'))
            killasgroup = boolean(get(section, 'killasgroup', stopasgroup))
            exitcodes = list_of_exitcodes(get(section, 'exitcodes', '0'))
            redirect_stderr = boolean(get(section, 'redirect_stderr', 'false'))
            numprocs = integer(get(section, 'numprocs', 1))
            numprocs_start = integer(get(section, 'numprocs_start', 0))
            environment_str = get(section, 'environment', '', do_expand=False)
            stdout_cmaxbytes = byte_size(get(section, 'stdout_capture_maxbytes', '0'))
            stdout_events = boolean(get(section, 'stdout_events_enabled', 'false'))
            stderr_cmaxbytes = byte_size(get(section, 'stderr_capture_maxbytes', '0'))
            stderr_events = boolean(get(section, 'stderr_events_enabled', 'false'))
            serverurl = get(section, 'serverurl', None)
            if serverurl:
                if serverurl.strip.upper == 'AUTO':
                    serverurl = None
            else:
                user = get(section, 'user', None)
                if user is None:
                    uid = None
                else:
                    uid = name_to_uid(user)
            umask = get(section, 'umask', None)
            if umask is not None:
                umask = octal_type(umask)
            process_name = process_or_group_name(get(section, 'process_name', '%(program_name)s', do_expand=False))
            if numprocs > 1:
                if '%(process_num)' not in process_name:
                    raise ValueError('%(process_num) must be present within process_name when numprocs > 1')
            if stopasgroup and not killasgroup:
                raise ValueError('Cannot set stopasgroup=true and killasgroup=false')
        for process_num in range(numprocs_start, numprocs + numprocs_start):
            expansions = common_expansions
            expansions.update{'process_num': process_num}
            expansions.updateself.environ_expansions
            environment = dict_of_key_value_pairs(expand(environment_str, expansions, 'environment'))
            directory = get(section, 'directory', None)
            logfiles = {}
            for k in ('stdout', 'stderr'):
                n = '%s_logfile' % k
                lf_val = get(section, n, Automatic)
                if isinstance(lf_val, basestring):
                    lf_val = expand(lf_val, expansions, n)
                lf_val = logfile_name(lf_val)
                logfiles[n] = lf_val
                bu_key = '%s_logfile_backups' % k
                backups = integer(get(section, bu_key, 10))
                logfiles[bu_key] = backups
                mb_key = '%s_logfile_maxbytes' % k
                maxbytes = byte_size(get(section, mb_key, '50MB'))
                logfiles[mb_key] = maxbytes
                sy_key = '%s_syslog' % k
                syslog = boolean(get(section, sy_key, False))
                logfiles[sy_key] = syslog
                if lf_val is Automatic:
                    if not maxbytes:
                        self.parse_warnings.append('For [%s], AUTO logging used for %s without rollover, set maxbytes > 0 to avoid filling up filesystem unintentionally' % (
                         section, n))
                    if redirect_stderr:
                        if logfiles['stderr_logfile'] not in (Automatic, None):
                            self.parse_warnings.append('For [%s], redirect_stderr=true but stderr_logfile has also been set to a filename, the filename has been ignored' % section)
                        logfiles['stderr_logfile'] = None
                    command = get(section, 'command', None, expansions=expansions)
                    if command is None:
                        raise ValueError('program section %s does not specify a command' % section)
                    pconfig = klass(self,
                      name=(expand(process_name, expansions, 'process_name')),
                      command=command,
                      directory=directory,
                      umask=umask,
                      priority=priority,
                      autostart=autostart,
                      autorestart=autorestart,
                      startsecs=startsecs,
                      startretries=startretries,
                      uid=uid,
                      stdout_logfile=(logfiles['stdout_logfile']),
                      stdout_capture_maxbytes=stdout_cmaxbytes,
                      stdout_events_enabled=stdout_events,
                      stdout_logfile_backups=(logfiles['stdout_logfile_backups']),
                      stdout_logfile_maxbytes=(logfiles['stdout_logfile_maxbytes']),
                      stdout_syslog=(logfiles['stdout_syslog']),
                      stderr_logfile=(logfiles['stderr_logfile']),
                      stderr_capture_maxbytes=stderr_cmaxbytes,
                      stderr_events_enabled=stderr_events,
                      stderr_logfile_backups=(logfiles['stderr_logfile_backups']),
                      stderr_logfile_maxbytes=(logfiles['stderr_logfile_maxbytes']),
                      stderr_syslog=(logfiles['stderr_syslog']),
                      stopsignal=stopsignal,
                      stopwaitsecs=stopwaitsecs,
                      stopasgroup=stopasgroup,
                      killasgroup=killasgroup,
                      exitcodes=exitcodes,
                      redirect_stderr=redirect_stderr,
                      environment=environment,
                      serverurl=serverurl)
                    programs.appendpconfig
                programs.sort
                return programs

    def _parse_servernames(self, parser, stype):
        options = []
        for section in parser.sections:
            if section.startswithstype:
                parts = section.split':'1
                if len(parts) > 1:
                    name = parts[1]
                else:
                    name = None
                options.append(name, section)
            return options

    def _parse_username_and_password(self, parser, section):
        get = parser.saneget
        username = get(section, 'username', None)
        password = get(section, 'password', None)
        if username is not None or password is not None:
            if username is None or password is None:
                raise ValueError('Section [%s] contains incomplete authentication: If a username or a password is specified, both the username and password must be specified' % section)
        return {'username':username, 
         'password':password}

    def server_configs_from_parser(self, parser):
        configs = []
        inet_serverdefs = self._parse_servernamesparser'inet_http_server'
        for name, section in inet_serverdefs:
            config = {}
            get = parser.saneget
            config.updateself._parse_username_and_passwordparsersection
            config['name'] = name
            config['family'] = socket.AF_INET
            port = get(section, 'port', None)
            if port is None:
                raise ValueError('section [%s] has no port value' % section)
            host, port = inet_address(port)
            config['host'] = host
            config['port'] = port
            config['section'] = section
            configs.appendconfig
        else:
            unix_serverdefs = self._parse_servernamesparser'unix_http_server'
            for name, section in unix_serverdefs:
                config = {}
                get = parser.saneget
                sfile = get(section, 'file', None, expansions={'here': self.here})
                if sfile is None:
                    raise ValueError('section [%s] has no file value' % section)
                else:
                    sfile = sfile.strip
                    config['name'] = name
                    config['family'] = socket.AF_UNIX
                    config['file'] = normalize_path(sfile)
                    config.updateself._parse_username_and_passwordparsersection
                    chown = get(section, 'chown', None)
                    if chown is not None:
                        try:
                            chown = colon_separated_user_group(chown)
                        except ValueError:
                            raise ValueError('Invalid sockchown value %s' % chown)

                    else:
                        chown = (-1, -1)
                    config['chown'] = chown
                    chmod = get(section, 'chmod', None)
                    if chmod is not None:
                        try:
                            chmod = octal_type(chmod)
                        except (TypeError, ValueError):
                            raise ValueError('Invalid chmod value %s' % chmod)

                    else:
                        chmod = 448
                config['chmod'] = chmod
                config['section'] = section
                configs.appendconfig
            else:
                return configs

    def daemonize(self):
        self.poller.before_daemonize
        self._daemonize
        self.poller.after_daemonize

    def _daemonize(self):
        pid = os.fork
        if pid != 0:
            self.logger.blather'supervisord forked; parent exiting'
            os._exit0
        else:
            self.logger.info'daemonizing the supervisord process'
            if self.directory:
                try:
                    os.chdirself.directory
                except OSError as err:
                    try:
                        self.logger.critical("can't chdir into %r: %s" % (
                         self.directory, err))
                    finally:
                        err = None
                        del err

                else:
                    self.logger.info('set current directory: %r' % self.directory)
        os.close0
        self.stdin = sys.stdin = sys.__stdin__ = open('/dev/null')
        os.close1
        self.stdout = sys.stdout = sys.__stdout__ = open('/dev/null', 'w')
        os.close2
        self.stderr = sys.stderr = sys.__stderr__ = open('/dev/null', 'w')
        os.setsid
        os.umaskself.umask

    def write_pidfile(self):
        pid = os.getpid
        try:
            with open(self.pidfile, 'w') as (f):
                f.write('%s\n' % pid)
        except (IOError, OSError):
            self.logger.critical('could not write pidfile %s' % self.pidfile)
        else:
            self.unlink_pidfile = True
            self.logger.info('supervisord started with pid %s' % pid)

    def cleanup(self):
        for config, server in self.httpservers:
            if config['family'] == socket.AF_UNIX and self.unlink_socketfiles:
                socketname = config['file']
                self._try_unlinksocketname
        else:
            if self.unlink_pidfile:
                self._try_unlinkself.pidfile
            self.poller.close

    def _try_unlink(self, path):
        try:
            os.unlinkpath
        except OSError:
            pass

    def close_httpservers(self):
        dispatcher_servers = []
        for config, server in self.httpservers:
            server.close

        for dispatcher in self.get_socket_map.values:
            dispatcher_server = getattr(dispatcher, 'server', None)
            if dispatcher_server is server:
                dispatcher_servers.appenddispatcher
        else:
            for server in dispatcher_servers:
                server.close

    def close_logger(self):
        self.logger.close

    def setsignals(self):
        receive = self.signal_receiver.receive
        signal.signalsignal.SIGTERMreceive
        signal.signalsignal.SIGINTreceive
        signal.signalsignal.SIGQUITreceive
        signal.signalsignal.SIGHUPreceive
        signal.signalsignal.SIGCHLDreceive
        signal.signalsignal.SIGUSR2receive

    def get_signal(self):
        return self.signal_receiver.get_signal

    def openhttpservers(self, supervisord):
        try:
            self.httpservers = self.make_http_serverssupervisord
            self.unlink_socketfiles = True
        except socket.error as why:
            try:
                if why.args[0] == errno.EADDRINUSE:
                    self.usage'Another program is already listening on a port that one of our HTTP servers is configured to use.  Shut this program down first before starting supervisord.'
                else:
                    help = 'Cannot open an HTTP server: socket.error reported'
                    errorname = errno.errorcode.getwhy.args[0]
                    if errorname is None:
                        self.usage('%s %s' % (help, why.args[0]))
                    else:
                        self.usage('%s errno.%s (%d)' % (
                         help, errorname, why.args[0]))
            finally:
                why = None
                del why

        except ValueError as why:
            try:
                self.usagewhy.args[0]
            finally:
                why = None
                del why

    def get_autochildlog_name(self, name, identifier, channel):
        prefix = '%s-%s---%s-' % (name, channel, identifier)
        logfile = self.mktempfile(suffix='.log',
          prefix=prefix,
          dir=(self.childlogdir))
        return logfile

    def clear_autochildlogdir--- This code section failed: ---

 L.1269         0  LOAD_FAST                'self'
                2  LOAD_ATTR                childlogdir
                4  STORE_FAST               'childlogdir'

 L.1270         6  LOAD_GLOBAL              re
                8  LOAD_METHOD              compile
               10  LOAD_STR                 '.+?---%s-\\S+\\.log\\.{0,1}\\d{0,4}'
               12  LOAD_FAST                'self'
               14  LOAD_ATTR                identifier
               16  BINARY_MODULO    
               18  CALL_METHOD_1         1  ''
               20  STORE_FAST               'fnre'

 L.1271        22  SETUP_FINALLY        38  'to 38'

 L.1272        24  LOAD_GLOBAL              os
               26  LOAD_METHOD              listdir
               28  LOAD_FAST                'childlogdir'
               30  CALL_METHOD_1         1  ''
               32  STORE_FAST               'filenames'
               34  POP_BLOCK        
               36  JUMP_FORWARD         76  'to 76'
             38_0  COME_FROM_FINALLY    22  '22'

 L.1273        38  DUP_TOP          
               40  LOAD_GLOBAL              IOError
               42  LOAD_GLOBAL              OSError
               44  BUILD_TUPLE_2         2 
               46  COMPARE_OP               exception-match
               48  POP_JUMP_IF_FALSE    74  'to 74'
               50  POP_TOP          
               52  POP_TOP          
               54  POP_TOP          

 L.1274        56  LOAD_FAST                'self'
               58  LOAD_ATTR                logger
               60  LOAD_METHOD              warn
               62  LOAD_STR                 'Could not clear childlog dir'
               64  CALL_METHOD_1         1  ''
               66  POP_TOP          

 L.1275        68  POP_EXCEPT       
               70  LOAD_CONST               None
               72  RETURN_VALUE     
             74_0  COME_FROM            48  '48'
               74  END_FINALLY      
             76_0  COME_FROM            36  '36'

 L.1277        76  LOAD_FAST                'filenames'
               78  GET_ITER         
             80_0  COME_FROM            92  '92'
               80  FOR_ITER            166  'to 166'
               82  STORE_FAST               'filename'

 L.1278        84  LOAD_FAST                'fnre'
               86  LOAD_METHOD              match
               88  LOAD_FAST                'filename'
               90  CALL_METHOD_1         1  ''
               92  POP_JUMP_IF_FALSE    80  'to 80'

 L.1279        94  LOAD_GLOBAL              os
               96  LOAD_ATTR                path
               98  LOAD_METHOD              join
              100  LOAD_FAST                'childlogdir'
              102  LOAD_FAST                'filename'
              104  CALL_METHOD_2         2  ''
              106  STORE_FAST               'pathname'

 L.1280       108  SETUP_FINALLY       124  'to 124'

 L.1281       110  LOAD_FAST                'self'
              112  LOAD_METHOD              remove
              114  LOAD_FAST                'pathname'
              116  CALL_METHOD_1         1  ''
              118  POP_TOP          
              120  POP_BLOCK        
              122  JUMP_BACK            80  'to 80'
            124_0  COME_FROM_FINALLY   108  '108'

 L.1282       124  DUP_TOP          
              126  LOAD_GLOBAL              OSError
              128  LOAD_GLOBAL              IOError
              130  BUILD_TUPLE_2         2 
              132  COMPARE_OP               exception-match
              134  POP_JUMP_IF_FALSE   162  'to 162'
              136  POP_TOP          
              138  POP_TOP          
              140  POP_TOP          

 L.1283       142  LOAD_FAST                'self'
              144  LOAD_ATTR                logger
              146  LOAD_METHOD              warn
              148  LOAD_STR                 'Failed to clean up %r'
              150  LOAD_FAST                'pathname'
              152  BINARY_MODULO    
              154  CALL_METHOD_1         1  ''
              156  POP_TOP          
              158  POP_EXCEPT       
              160  JUMP_BACK            80  'to 80'
            162_0  COME_FROM           134  '134'
              162  END_FINALLY      
              164  JUMP_BACK            80  'to 80'

Parse error at or near `LOAD_CONST' instruction at offset 70

    def get_socket_map(self):
        return asyncore.socket_map

    def cleanup_fds(self):
        start = 5
        for x in range(start, self.minfds):
            try:
                os.closex
            except OSError:
                pass

    def kill(self, pid, signal):
        os.killpidsignal

    def waitpid(self):
        try:
            pid, sts = os.waitpid(-1)os.WNOHANG
        except OSError as exc:
            try:
                code = exc.args[0]
                if code not in (errno.ECHILD, errno.EINTR):
                    self.logger.critical('waitpid error %r; a process may not be cleaned up properly' % code)
                if code == errno.EINTR:
                    self.logger.blather'EINTR during reap'
                pid, sts = (None, None)
            finally:
                exc = None
                del exc

        else:
            return (
             pid, sts)

    def drop_privileges--- This code section failed: ---

 L.1329         0  LOAD_DEREF               'user'
                2  LOAD_CONST               None
                4  COMPARE_OP               is
                6  POP_JUMP_IF_FALSE    12  'to 12'

 L.1330         8  LOAD_STR                 'No user specified to setuid to!'
               10  RETURN_VALUE     
             12_0  COME_FROM             6  '6'

 L.1333        12  SETUP_FINALLY        26  'to 26'

 L.1334        14  LOAD_GLOBAL              int
               16  LOAD_DEREF               'user'
               18  CALL_FUNCTION_1       1  ''
               20  STORE_FAST               'uid'
               22  POP_BLOCK        
               24  JUMP_FORWARD        102  'to 102'
             26_0  COME_FROM_FINALLY    12  '12'

 L.1335        26  DUP_TOP          
               28  LOAD_GLOBAL              ValueError
               30  COMPARE_OP               exception-match
               32  POP_JUMP_IF_FALSE   100  'to 100'
               34  POP_TOP          
               36  POP_TOP          
               38  POP_TOP          

 L.1336        40  SETUP_FINALLY        56  'to 56'

 L.1337        42  LOAD_GLOBAL              pwd
               44  LOAD_METHOD              getpwnam
               46  LOAD_DEREF               'user'
               48  CALL_METHOD_1         1  ''
               50  STORE_FAST               'pwrec'
               52  POP_BLOCK        
               54  JUMP_FORWARD         88  'to 88'
             56_0  COME_FROM_FINALLY    40  '40'

 L.1338        56  DUP_TOP          
               58  LOAD_GLOBAL              KeyError
               60  COMPARE_OP               exception-match
               62  POP_JUMP_IF_FALSE    86  'to 86'
               64  POP_TOP          
               66  POP_TOP          
               68  POP_TOP          

 L.1339        70  LOAD_STR                 "Can't find username %r"
               72  LOAD_DEREF               'user'
               74  BINARY_MODULO    
               76  ROT_FOUR         
               78  POP_EXCEPT       
               80  ROT_FOUR         
               82  POP_EXCEPT       
               84  RETURN_VALUE     
             86_0  COME_FROM            62  '62'
               86  END_FINALLY      
             88_0  COME_FROM            54  '54'

 L.1340        88  LOAD_FAST                'pwrec'
               90  LOAD_CONST               2
               92  BINARY_SUBSCR    
               94  STORE_FAST               'uid'
               96  POP_EXCEPT       
               98  JUMP_FORWARD        146  'to 146'
            100_0  COME_FROM            32  '32'
              100  END_FINALLY      
            102_0  COME_FROM            24  '24'

 L.1342       102  SETUP_FINALLY       118  'to 118'

 L.1343       104  LOAD_GLOBAL              pwd
              106  LOAD_METHOD              getpwuid
              108  LOAD_FAST                'uid'
              110  CALL_METHOD_1         1  ''
              112  STORE_FAST               'pwrec'
              114  POP_BLOCK        
              116  JUMP_FORWARD        146  'to 146'
            118_0  COME_FROM_FINALLY   102  '102'

 L.1344       118  DUP_TOP          
              120  LOAD_GLOBAL              KeyError
              122  COMPARE_OP               exception-match
              124  POP_JUMP_IF_FALSE   144  'to 144'
              126  POP_TOP          
              128  POP_TOP          
              130  POP_TOP          

 L.1345       132  LOAD_STR                 "Can't find uid %r"
              134  LOAD_FAST                'uid'
              136  BINARY_MODULO    
              138  ROT_FOUR         
              140  POP_EXCEPT       
              142  RETURN_VALUE     
            144_0  COME_FROM           124  '124'
              144  END_FINALLY      
            146_0  COME_FROM           116  '116'
            146_1  COME_FROM            98  '98'

 L.1347       146  LOAD_GLOBAL              os
              148  LOAD_METHOD              getuid
              150  CALL_METHOD_0         0  ''
              152  STORE_FAST               'current_uid'

 L.1349       154  LOAD_FAST                'current_uid'
              156  LOAD_FAST                'uid'
              158  COMPARE_OP               ==
              160  POP_JUMP_IF_FALSE   166  'to 166'

 L.1354       162  LOAD_CONST               None
              164  RETURN_VALUE     
            166_0  COME_FROM           160  '160'

 L.1356       166  LOAD_FAST                'current_uid'
              168  LOAD_CONST               0
              170  COMPARE_OP               !=
              172  POP_JUMP_IF_FALSE   178  'to 178'

 L.1357       174  LOAD_STR                 "Can't drop privilege as nonroot user"
              176  RETURN_VALUE     
            178_0  COME_FROM           172  '172'

 L.1359       178  LOAD_FAST                'pwrec'
              180  LOAD_CONST               3
              182  BINARY_SUBSCR    
              184  STORE_FAST               'gid'

 L.1360       186  LOAD_GLOBAL              hasattr
              188  LOAD_GLOBAL              os
              190  LOAD_STR                 'setgroups'
              192  CALL_FUNCTION_2       2  ''
          194_196  POP_JUMP_IF_FALSE   280  'to 280'

 L.1361       198  LOAD_FAST                'pwrec'
              200  LOAD_CONST               0
              202  BINARY_SUBSCR    
              204  STORE_DEREF              'user'

 L.1362       206  LOAD_CLOSURE             'user'
              208  BUILD_TUPLE_1         1 
              210  LOAD_LISTCOMP            '<code_object <listcomp>>'
              212  LOAD_STR                 'ServerOptions.drop_privileges.<locals>.<listcomp>'
              214  MAKE_FUNCTION_8          'closure'
              216  LOAD_GLOBAL              grp
              218  LOAD_METHOD              getgrall
              220  CALL_METHOD_0         0  ''
              222  GET_ITER         
              224  CALL_FUNCTION_1       1  ''
              226  STORE_FAST               'groups'

 L.1370       228  LOAD_FAST                'groups'
              230  LOAD_METHOD              insert
              232  LOAD_CONST               0
              234  LOAD_FAST                'gid'
              236  CALL_METHOD_2         2  ''
              238  POP_TOP          

 L.1371       240  SETUP_FINALLY       256  'to 256'

 L.1372       242  LOAD_GLOBAL              os
              244  LOAD_METHOD              setgroups
              246  LOAD_FAST                'groups'
              248  CALL_METHOD_1         1  ''
              250  POP_TOP          
              252  POP_BLOCK        
              254  JUMP_FORWARD        280  'to 280'
            256_0  COME_FROM_FINALLY   240  '240'

 L.1373       256  DUP_TOP          
              258  LOAD_GLOBAL              OSError
              260  COMPARE_OP               exception-match
          262_264  POP_JUMP_IF_FALSE   278  'to 278'
              266  POP_TOP          
              268  POP_TOP          
              270  POP_TOP          

 L.1374       272  POP_EXCEPT       
              274  LOAD_STR                 'Could not set groups of effective user'
              276  RETURN_VALUE     
            278_0  COME_FROM           262  '262'
              278  END_FINALLY      
            280_0  COME_FROM           254  '254'
            280_1  COME_FROM           194  '194'

 L.1375       280  SETUP_FINALLY       296  'to 296'

 L.1376       282  LOAD_GLOBAL              os
              284  LOAD_METHOD              setgid
              286  LOAD_FAST                'gid'
              288  CALL_METHOD_1         1  ''
              290  POP_TOP          
              292  POP_BLOCK        
              294  JUMP_FORWARD        320  'to 320'
            296_0  COME_FROM_FINALLY   280  '280'

 L.1377       296  DUP_TOP          
              298  LOAD_GLOBAL              OSError
              300  COMPARE_OP               exception-match
          302_304  POP_JUMP_IF_FALSE   318  'to 318'
              306  POP_TOP          
              308  POP_TOP          
              310  POP_TOP          

 L.1378       312  POP_EXCEPT       
              314  LOAD_STR                 'Could not set group id of effective user'
              316  RETURN_VALUE     
            318_0  COME_FROM           302  '302'
              318  END_FINALLY      
            320_0  COME_FROM           294  '294'

 L.1379       320  LOAD_GLOBAL              os
              322  LOAD_METHOD              setuid
              324  LOAD_FAST                'uid'
              326  CALL_METHOD_1         1  ''
              328  POP_TOP          

Parse error at or near `ROT_FOUR' instruction at offset 80

    def set_uid_or_exit(self):
        """Set the uid of the supervisord process.  Called during supervisord
        startup only.  No return value.  Exits the process via usage() if
        privileges could not be dropped."""
        if self.uid is None:
            if os.getuid == 0:
                self.parse_criticals.append'Supervisor is running as root.  Privileges were not dropped because no user is specified in the config file.  If you intend to run as root, you can set user=root in the config file to avoid this message.'
        else:
            msg = self.drop_privilegesself.uid
            if msg is None:
                self.parse_infos.append('Set uid to user %s succeeded' % self.uid)
            else:
                self.usagemsg

    def set_rlimits_or_exit(self):
        """Set the rlimits of the supervisord process.  Called during
        supervisord startup only.  No return value.  Exits the process via
        usage() if any rlimits could not be set."""
        limits = []
        if hasattr(resource, 'RLIMIT_NOFILE'):
            limits.append{'msg':'The minimum number of file descriptors required to run this process is %(min_limit)s as per the "minfds" command-line argument or config file setting. The current environment will only allow you to open %(hard)s file descriptors.  Either raise the number of usable file descriptors in your environment (see README.rst) or lower the minfds setting in the config file to allow the process to start.', 
             'min':self.minfds, 
             'resource':resource.RLIMIT_NOFILE, 
             'name':'RLIMIT_NOFILE'}
        if hasattr(resource, 'RLIMIT_NPROC'):
            limits.append{'msg':'The minimum number of available processes required to run this program is %(min_limit)s as per the "minprocs" command-line argument or config file setting. The current environment will only allow you to open %(hard)s processes.  Either raise the number of usable processes in your environment (see README.rst) or lower the minprocs setting in the config file to allow the program to start.', 
             'min':self.minprocs, 
             'resource':resource.RLIMIT_NPROC, 
             'name':'RLIMIT_NPROC'}
        for limit in limits:
            min_limit = limit['min']
            res = limit['resource']
            msg = limit['msg']
            name = limit['name']
            name = name
            soft, hard = resource.getrlimitres
            if soft < min_limit:
                if soft != -1:
                    if hard < min_limit:
                        if hard != -1:
                            hard = min_limit
                try:
                    resource.setrlimitres(min_limit, hard)
                    self.parse_infos.append('Increased %(name)s limit to %(min_limit)s' % locals())
                except (resource.error, ValueError):
                    self.usage(msg % locals())

    def make_logger(self):
        format = '%(asctime)s %(levelname)s %(message)s\n'
        self.logger = loggers.getLoggerself.loglevel
        if self.nodaemon:
            loggers.handle_stdoutself.loggerformat
        loggers.handle_file((self.logger),
          (self.logfile),
          format,
          rotating=(not not self.logfile_maxbytes),
          maxbytes=(self.logfile_maxbytes),
          backups=(self.logfile_backups))
        for msg in self.parse_criticals:
            self.logger.criticalmsg
        else:
            for msg in self.parse_warnings:
                self.logger.warnmsg
            else:
                for msg in self.parse_infos:
                    self.logger.infomsg

    def make_http_servers(self, supervisord):
        from supervisor.http import make_http_servers
        return make_http_servers(self, supervisord)

    def close_fd(self, fd):
        try:
            os.closefd
        except OSError:
            pass

    def fork(self):
        return os.fork

    def dup2(self, frm, to):
        return os.dup2frmto

    def setpgrp(self):
        return os.setpgrp

    def stat(self, filename):
        return os.statfilename

    def write(self, fd, data):
        return os.writefdas_bytes(data)

    def execve(self, filename, argv, env):
        return os.execve(filename, argv, env)

    def mktempfile(self, suffix, prefix, dir):
        os._urandomfd = None
        fd, filename = tempfile.mkstemp(suffix, prefix, dir)
        os.closefd
        return filename

    def remove(self, path):
        os.removepath

    def _exit(self, code):
        os._exitcode

    def setumask(self, mask):
        os.umaskmask

    def get_path(self):
        """Return a list corresponding to $PATH, or a default."""
        path = [
         '/bin', '/usr/bin', '/usr/local/bin']
        if 'PATH' in os.environ:
            p = os.environ['PATH']
            if p:
                path = p.splitos.pathsep
        return path

    def get_pid(self):
        return os.getpid

    def check_execv_args(self, filename, argv, st):
        if st is None:
            raise NotFound("can't find command %r" % filename)
        else:
            if stat.S_ISDIRst[stat.ST_MODE]:
                raise NotExecutable('command at %r is a directory' % filename)
            else:
                if not stat.S_IMODEst[stat.ST_MODE] & 73:
                    raise NotExecutable('command at %r is not executable' % filename)
                else:
                    if not os.accessfilenameos.X_OK:
                        raise NoPermission('no permission to run command %r' % filename)

    def reopenlogs(self):
        self.logger.info'supervisord logreopen'
        for handler in self.logger.handlers:
            if hasattr(handler, 'reopen'):
                handler.reopen

    def readfd(self, fd):
        try:
            data = os.readfd131072
        except OSError as why:
            try:
                if why.args[0] not in (errno.EWOULDBLOCK, errno.EBADF, errno.EINTR):
                    raise
                data = ''
            finally:
                why = None
                del why

        else:
            return data

    def process_environment(self):
        os.environ.update(self.environment or {})

    def chdir(self, dir):
        os.chdirdir

    def make_pipes--- This code section failed: ---

 L.1579         0  LOAD_CONST               None

 L.1580         2  LOAD_CONST               None

 L.1581         4  LOAD_CONST               None

 L.1582         6  LOAD_CONST               None

 L.1583         8  LOAD_CONST               None

 L.1584        10  LOAD_CONST               None

 L.1579        12  LOAD_CONST               ('child_stdin', 'stdin', 'stdout', 'child_stdout', 'stderr', 'child_stderr')
               14  BUILD_CONST_KEY_MAP_6     6 
               16  STORE_FAST               'pipes'

 L.1585        18  SETUP_FINALLY       192  'to 192'

 L.1586        20  LOAD_GLOBAL              os
               22  LOAD_METHOD              pipe
               24  CALL_METHOD_0         0  ''
               26  UNPACK_SEQUENCE_2     2 
               28  STORE_FAST               'stdin'
               30  STORE_FAST               'child_stdin'

 L.1587        32  LOAD_FAST                'stdin'
               34  LOAD_FAST                'child_stdin'
               36  ROT_TWO          
               38  LOAD_FAST                'pipes'
               40  LOAD_STR                 'child_stdin'
               42  STORE_SUBSCR     
               44  LOAD_FAST                'pipes'
               46  LOAD_STR                 'stdin'
               48  STORE_SUBSCR     

 L.1588        50  LOAD_GLOBAL              os
               52  LOAD_METHOD              pipe
               54  CALL_METHOD_0         0  ''
               56  UNPACK_SEQUENCE_2     2 
               58  STORE_FAST               'stdout'
               60  STORE_FAST               'child_stdout'

 L.1589        62  LOAD_FAST                'stdout'
               64  LOAD_FAST                'child_stdout'
               66  ROT_TWO          
               68  LOAD_FAST                'pipes'
               70  LOAD_STR                 'stdout'
               72  STORE_SUBSCR     
               74  LOAD_FAST                'pipes'
               76  LOAD_STR                 'child_stdout'
               78  STORE_SUBSCR     

 L.1590        80  LOAD_FAST                'stderr'
               82  POP_JUMP_IF_FALSE   114  'to 114'

 L.1591        84  LOAD_GLOBAL              os
               86  LOAD_METHOD              pipe
               88  CALL_METHOD_0         0  ''
               90  UNPACK_SEQUENCE_2     2 
               92  STORE_FAST               'stderr'
               94  STORE_FAST               'child_stderr'

 L.1592        96  LOAD_FAST                'stderr'
               98  LOAD_FAST                'child_stderr'
              100  ROT_TWO          
              102  LOAD_FAST                'pipes'
              104  LOAD_STR                 'stderr'
              106  STORE_SUBSCR     
              108  LOAD_FAST                'pipes'
              110  LOAD_STR                 'child_stderr'
              112  STORE_SUBSCR     
            114_0  COME_FROM            82  '82'

 L.1593       114  LOAD_FAST                'pipes'
              116  LOAD_STR                 'stdout'
              118  BINARY_SUBSCR    
              120  LOAD_FAST                'pipes'
              122  LOAD_STR                 'stderr'
              124  BINARY_SUBSCR    
              126  LOAD_FAST                'pipes'
              128  LOAD_STR                 'stdin'
              130  BINARY_SUBSCR    
              132  BUILD_TUPLE_3         3 
              134  GET_ITER         
            136_0  COME_FROM           146  '146'
              136  FOR_ITER            186  'to 186'
              138  STORE_FAST               'fd'

 L.1594       140  LOAD_FAST                'fd'
              142  LOAD_CONST               None
              144  COMPARE_OP               is-not
              146  POP_JUMP_IF_FALSE   136  'to 136'

 L.1595       148  LOAD_GLOBAL              fcntl
              150  LOAD_METHOD              fcntl
              152  LOAD_FAST                'fd'
              154  LOAD_GLOBAL              fcntl
              156  LOAD_ATTR                F_GETFL
              158  CALL_METHOD_2         2  ''
              160  LOAD_GLOBAL              os
              162  LOAD_ATTR                O_NDELAY
              164  BINARY_OR        
              166  STORE_FAST               'flags'

 L.1596       168  LOAD_GLOBAL              fcntl
              170  LOAD_METHOD              fcntl
              172  LOAD_FAST                'fd'
              174  LOAD_GLOBAL              fcntl
              176  LOAD_ATTR                F_SETFL
              178  LOAD_FAST                'flags'
              180  CALL_METHOD_3         3  ''
              182  POP_TOP          
              184  JUMP_BACK           136  'to 136'

 L.1597       186  LOAD_FAST                'pipes'
              188  POP_BLOCK        
              190  RETURN_VALUE     
            192_0  COME_FROM_FINALLY    18  '18'

 L.1598       192  DUP_TOP          
              194  LOAD_GLOBAL              OSError
              196  COMPARE_OP               exception-match
              198  POP_JUMP_IF_FALSE   244  'to 244'
              200  POP_TOP          
              202  POP_TOP          
              204  POP_TOP          

 L.1599       206  LOAD_FAST                'pipes'
              208  LOAD_METHOD              values
              210  CALL_METHOD_0         0  ''
              212  GET_ITER         
            214_0  COME_FROM           224  '224'
              214  FOR_ITER            238  'to 238'
              216  STORE_FAST               'fd'

 L.1600       218  LOAD_FAST                'fd'
              220  LOAD_CONST               None
              222  COMPARE_OP               is-not
              224  POP_JUMP_IF_FALSE   214  'to 214'

 L.1601       226  LOAD_FAST                'self'
              228  LOAD_METHOD              close_fd
              230  LOAD_FAST                'fd'
              232  CALL_METHOD_1         1  ''
              234  POP_TOP          
              236  JUMP_BACK           214  'to 214'

 L.1602       238  RAISE_VARARGS_0       0  'reraise'
              240  POP_EXCEPT       
              242  JUMP_FORWARD        246  'to 246'
            244_0  COME_FROM           198  '198'
              244  END_FINALLY      
            246_0  COME_FROM           242  '242'

Parse error at or near `POP_TOP' instruction at offset 202

    def close_parent_pipes(self, pipes):
        for fdname in ('stdin', 'stdout', 'stderr'):
            fd = pipes.getfdname
            if fd is not None:
                self.close_fdfd

    def close_child_pipes(self, pipes):
        for fdname in ('child_stdin', 'child_stdout', 'child_stderr'):
            fd = pipes.getfdname
            if fd is not None:
                self.close_fdfd


class ClientOptions(Options):
    positional_args_allowed = 1
    interactive = None
    prompt = None
    serverurl = None
    username = None
    password = None
    history_file = None

    def __init__(self):
        Options.__init__(self, require_configfile=False)
        self.configroot = Dummy()
        self.configroot.supervisorctl = Dummy()
        self.configroot.supervisorctl.interactive = None
        self.configroot.supervisorctl.prompt = 'supervisor'
        self.configroot.supervisorctl.serverurl = None
        self.configroot.supervisorctl.username = None
        self.configroot.supervisorctl.password = None
        self.configroot.supervisorctl.history_file = None
        from supervisor.supervisorctl import DefaultControllerPlugin
        default_factory = (
         'default', DefaultControllerPlugin, {})
        self.plugin_factories = [
         default_factory]
        self.add('interactive', 'supervisorctl.interactive', 'i', 'interactive',
          flag=1, default=0)
        self.add('prompt', 'supervisorctl.prompt', default='supervisor')
        self.add('serverurl', 'supervisorctl.serverurl', 's:', 'serverurl=', url,
          default='http://localhost:9001')
        self.add('username', 'supervisorctl.username', 'u:', 'username=')
        self.add('password', 'supervisorctl.password', 'p:', 'password=')
        self.add('history', 'supervisorctl.history_file', 'r:', 'history_file=')

    def realize(self, *arg, **kw):
        (Options.realize)(self, *arg, **kw)
        if not self.args:
            self.interactive = 1

    def read_config(self, fp):
        section = self.configroot.supervisorctl
        need_close = False
        self.here = hasattr(fp, 'read') or os.path.dirnamenormalize_path(fp)
        if not self.existsfp:
            raise ValueError('could not find config file %s' % fp)
        try:
            fp = self.openfp'r'
            need_close = True
        except (IOError, OSError):
            raise ValueError('could not read config file %s' % fp)
        else:
            parser = UnhosedConfigParser()
            parser.expansions = self.environ_expansions
            parser.mysection = 'supervisorctl'
            try:
                parser.read_filefp
            except AttributeError:
                parser.readfpfp
            else:
                if need_close:
                    fp.close
                else:
                    sections = parser.sections
                    if 'supervisorctl' not in sections:
                        raise ValueError('.ini file does not include supervisorctl section')
                    serverurl = parser.getdefault('serverurl', 'http://localhost:9001', expansions={'here': self.here})
                    if serverurl.startswith'unix://':
                        path = normalize_path(serverurl[7:])
                        serverurl = 'unix://%s' % path
                    section.serverurl = serverurl
                    section.prompt = parser.getdefault'prompt'section.prompt
                    section.username = parser.getdefault'username'section.username
                    section.password = parser.getdefault'password'section.password
                    history_file = parser.getdefault('history_file', (section.history_file), expansions={'here': self.here})
                    if history_file:
                        history_file = normalize_path(history_file)
                        section.history_file = history_file
                        self.history_file = history_file
                    else:
                        section.history_file = None
                    self.history_file = None
                self.plugin_factories += self.get_plugins(parser, 'supervisor.ctl_factory', 'ctlplugin:')
                return section

    def getServerProxy(self):
        return xmlrpclib.ServerProxy('http://127.0.0.1',
          transport=(xmlrpc.SupervisorTransport(self.username, self.password, self.serverurl)))


_marker = []

class UnhosedConfigParser(ConfigParser.RawConfigParser):
    mysection = 'supervisord'

    def __init__(self, *args, **kwargs):
        if not PY2:
            if 'inline_comment_prefixes' not in kwargs:
                kwargs['inline_comment_prefixes'] = (';', '#')
            if 'strict' not in kwargs:
                kwargs['strict'] = False
        (ConfigParser.RawConfigParser.__init__)(self, *args, **kwargs)
        self.section_to_file = {}
        self.expansions = {}

    def read_string--- This code section failed: ---

 L.1749         0  SETUP_FINALLY        20  'to 20'

 L.1750         2  LOAD_GLOBAL              ConfigParser
                4  LOAD_ATTR                RawConfigParser
                6  LOAD_METHOD              read_string

 L.1751         8  LOAD_FAST                'self'

 L.1751        10  LOAD_FAST                'string'

 L.1751        12  LOAD_FAST                'source'

 L.1750        14  CALL_METHOD_3         3  ''
               16  POP_BLOCK        
               18  RETURN_VALUE     
             20_0  COME_FROM_FINALLY     0  '0'

 L.1752        20  DUP_TOP          
               22  LOAD_GLOBAL              AttributeError
               24  COMPARE_OP               exception-match
               26  POP_JUMP_IF_FALSE    52  'to 52'
               28  POP_TOP          
               30  POP_TOP          
               32  POP_TOP          

 L.1753        34  LOAD_FAST                'self'
               36  LOAD_METHOD              readfp
               38  LOAD_GLOBAL              StringIO
               40  LOAD_FAST                'string'
               42  CALL_FUNCTION_1       1  ''
               44  CALL_METHOD_1         1  ''
               46  ROT_FOUR         
               48  POP_EXCEPT       
               50  RETURN_VALUE     
             52_0  COME_FROM            26  '26'
               52  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 30

    def read(self, filenames, **kwargs):
        """Attempt to read and parse a list of filenames, returning a list
        of filenames which were successfully parsed.  This is a method of
        RawConfigParser that is overridden to build self.section_to_file,
        which is a mapping of section names to the files they came from.
        """
        if isinstance(filenames, basestring):
            filenames = [
             filenames]
        ok_filenames = []
        for filename in filenames:
            sections_orig = self._sections.copy
            ok_filenames.extend(ConfigParser.RawConfigParser.read)(self, [filename], **kwargs)
            diff = frozenset(self._sections) - frozenset(sections_orig)
            for section in diff:
                self.section_to_file[section] = filename
            else:
                return ok_filenames

    def saneget(self, section, option, default=_marker, do_expand=True, expansions={}):
        try:
            optval = self.getsectionoption
        except ConfigParser.NoOptionError:
            if default is _marker:
                raise
            else:
                optval = default
        else:
            if do_expand:
                if isinstance(optval, basestring):
                    combined_expansions = dict(list(self.expansions.items) + list(expansions.items))
                    optval = expand(optval, combined_expansions, '%s.%s' % (section, option))
            return optval

    def getdefault(self, option, default=_marker, expansions={}, **kwargs):
        return (self.saneget)(self.mysection, option, default=default, expansions=expansions, **kwargs)

    def expand_here(self, here):
        HERE_FORMAT = '%(here)s'
        for section in self.sections:
            for key, value in self.itemssection:
                if HERE_FORMAT in value:
                    assert here is not None, 'here has not been set to a path'
                    value = value.replaceHERE_FORMAThere
                    self.set(section, key, value)


class Config(object):

    def __ne__(self, other):
        return not self.__eq__other

    def __lt__(self, other):
        if self.priority == other.priority:
            return self.name < other.name
        return self.priority < other.priority

    def __le__(self, other):
        if self.priority == other.priority:
            return self.name <= other.name
        return self.priority <= other.priority

    def __gt__(self, other):
        if self.priority == other.priority:
            return self.name > other.name
        return self.priority > other.priority

    def __ge__(self, other):
        if self.priority == other.priority:
            return self.name >= other.name
        return self.priority >= other.priority

    def __repr__(self):
        return '<%s instance at %s named %s>' % (self.__class__, id(self),
         self.name)


class ProcessConfig(Config):
    req_param_names = [
     'name', 'uid', 'command', 'directory', 'umask', 'priority',
     'autostart', 'autorestart', 'startsecs', 'startretries',
     'stdout_logfile', 'stdout_capture_maxbytes',
     'stdout_events_enabled', 'stdout_syslog',
     'stdout_logfile_backups', 'stdout_logfile_maxbytes',
     'stderr_logfile', 'stderr_capture_maxbytes',
     'stderr_logfile_backups', 'stderr_logfile_maxbytes',
     'stderr_events_enabled', 'stderr_syslog',
     'stopsignal', 'stopwaitsecs', 'stopasgroup', 'killasgroup',
     'exitcodes', 'redirect_stderr']
    optional_param_names = ['environment', 'serverurl']

    def __init__(self, options, **params):
        self.options = options
        for name in self.req_param_names:
            setattr(self, name, params[name])
        else:
            for name in self.optional_param_names:
                setattr(self, name, params.getnameNone)

    def __eq__(self, other):
        if not isinstance(other, ProcessConfig):
            return False
        for name in self.req_param_names + self.optional_param_names:
            if Automatic in (getattr(self, name), getattr(other, name)):
                pass
            elif getattr(self, name) != getattr(other, name):
                return False
            return True

    def get_path(self):
        """Return a list corresponding to $PATH that is configured to be set
        in the process environment, or the system default."""
        if self.environment is not None:
            path = self.environment.get'PATH'
            if path is not None:
                return path.splitos.pathsep
        return self.options.get_path

    def create_autochildlogs(self):
        get_autoname = self.options.get_autochildlog_name
        sid = self.options.identifier
        name = self.name
        if self.stdout_logfile is Automatic:
            self.stdout_logfile = get_autoname(name, sid, 'stdout')
        if self.stderr_logfile is Automatic:
            self.stderr_logfile = get_autoname(name, sid, 'stderr')

    def make_process(self, group=None):
        from supervisor.process import Subprocess
        process = Subprocess(self)
        process.group = group
        return process

    def make_dispatchers(self, proc):
        use_stderr = not self.redirect_stderr
        p = self.options.make_pipesuse_stderr
        stdout_fd, stderr_fd, stdin_fd = p['stdout'], p['stderr'], p['stdin']
        dispatchers = {}
        from supervisor.dispatchers import POutputDispatcher
        from supervisor.dispatchers import PInputDispatcher
        from supervisor import events
        if stdout_fd is not None:
            etype = events.ProcessCommunicationStdoutEvent
            dispatchers[stdout_fd] = POutputDispatcher(proc, etype, stdout_fd)
        if stderr_fd is not None:
            etype = events.ProcessCommunicationStderrEvent
            dispatchers[stderr_fd] = POutputDispatcher(proc, etype, stderr_fd)
        if stdin_fd is not None:
            dispatchers[stdin_fd] = PInputDispatcher(proc, 'stdin', stdin_fd)
        return (
         dispatchers, p)


class EventListenerConfig(ProcessConfig):

    def make_dispatchers(self, proc):
        use_stderr = True
        p = self.options.make_pipesuse_stderr
        stdout_fd, stderr_fd, stdin_fd = p['stdout'], p['stderr'], p['stdin']
        dispatchers = {}
        from supervisor.dispatchers import PEventListenerDispatcher
        from supervisor.dispatchers import PInputDispatcher
        from supervisor.dispatchers import POutputDispatcher
        from supervisor import events
        if stdout_fd is not None:
            dispatchers[stdout_fd] = PEventListenerDispatcher(proc, 'stdout', stdout_fd)
        if stderr_fd is not None:
            etype = events.ProcessCommunicationStderrEvent
            dispatchers[stderr_fd] = POutputDispatcher(proc, etype, stderr_fd)
        if stdin_fd is not None:
            dispatchers[stdin_fd] = PInputDispatcher(proc, 'stdin', stdin_fd)
        return (
         dispatchers, p)


class FastCGIProcessConfig(ProcessConfig):

    def make_process(self, group=None):
        if group is None:
            raise NotImplementedError('FastCGI programs require a group')
        from supervisor.process import FastCGISubprocess
        process = FastCGISubprocess(self)
        process.group = group
        return process

    def make_dispatchers(self, proc):
        dispatchers, p = ProcessConfig.make_dispatchersselfproc
        stdin_fd = p['stdin']
        if stdin_fd is not None:
            dispatchers[stdin_fd].close
        return (
         dispatchers, p)


class ProcessGroupConfig(Config):

    def __init__(self, options, name, priority, process_configs):
        self.options = options
        self.name = name
        self.priority = priority
        self.process_configs = process_configs

    def __eq__(self, other):
        if not isinstance(other, ProcessGroupConfig):
            return False
        if self.name != other.name:
            return False
        if self.priority != other.priority:
            return False
        if self.process_configs != other.process_configs:
            return False
        return True

    def after_setuid(self):
        for config in self.process_configs:
            config.create_autochildlogs

    def make_group(self):
        from supervisor.process import ProcessGroup
        return ProcessGroup(self)


class EventListenerPoolConfig(Config):

    def __init__(self, options, name, priority, process_configs, buffer_size, pool_events, result_handler):
        self.options = options
        self.name = name
        self.priority = priority
        self.process_configs = process_configs
        self.buffer_size = buffer_size
        self.pool_events = pool_events
        self.result_handler = result_handler

    def __eq__(self, other):
        if not isinstance(other, EventListenerPoolConfig):
            return False
        if self.name == other.name:
            if self.priority == other.priority:
                if self.process_configs == other.process_configs:
                    if self.buffer_size == other.buffer_size:
                        if self.pool_events == other.pool_events:
                            if self.result_handler == other.result_handler:
                                return True
        return False

    def after_setuid(self):
        for config in self.process_configs:
            config.create_autochildlogs

    def make_group(self):
        from supervisor.process import EventListenerPool
        return EventListenerPool(self)


class FastCGIGroupConfig(ProcessGroupConfig):

    def __init__(self, options, name, priority, process_configs, socket_config):
        ProcessGroupConfig.__init__(self, options, name, priority, process_configs)
        self.socket_config = socket_config

    def __eq__(self, other):
        if not isinstance(other, FastCGIGroupConfig):
            return False
        if self.socket_config != other.socket_config:
            return False
        return ProcessGroupConfig.__eq__selfother

    def make_group(self):
        from supervisor.process import FastCGIProcessGroup
        return FastCGIProcessGroup(self)


def readFile(filename, offset, length):
    """ Read length bytes from the file named by filename starting at
    offset """
    absoffset = abs(offset)
    abslength = abs(length)
    try:
        with open(filename, 'rb') as (f):
            if absoffset != offset:
                if length:
                    raise ValueError('BAD_ARGUMENTS')
                f.seek02
                sz = f.tell
                pos = int(sz - absoffset)
                if pos < 0:
                    pos = 0
                f.seekpos
                data = f.readabsoffset
            else:
                if abslength != length:
                    raise ValueError('BAD_ARGUMENTS')
                elif length == 0:
                    f.seekoffset
                    data = f.read
                else:
                    f.seekoffset
                    data = f.readlength
    except (OSError, IOError):
        raise ValueError('FAILED')
    else:
        return data


def tailFile--- This code section failed: ---

 L.2086         0  SETUP_FINALLY       198  'to 198'

 L.2087         2  LOAD_GLOBAL              open
                4  LOAD_FAST                'filename'
                6  LOAD_STR                 'rb'
                8  CALL_FUNCTION_2       2  ''
               10  SETUP_WITH          188  'to 188'
               12  STORE_FAST               'f'

 L.2088        14  LOAD_CONST               False
               16  STORE_FAST               'overflow'

 L.2089        18  LOAD_FAST                'f'
               20  LOAD_METHOD              seek
               22  LOAD_CONST               0
               24  LOAD_CONST               2
               26  CALL_METHOD_2         2  ''
               28  POP_TOP          

 L.2090        30  LOAD_FAST                'f'
               32  LOAD_METHOD              tell
               34  CALL_METHOD_0         0  ''
               36  STORE_FAST               'sz'

 L.2092        38  LOAD_FAST                'sz'
               40  LOAD_FAST                'offset'
               42  LOAD_FAST                'length'
               44  BINARY_ADD       
               46  COMPARE_OP               >
               48  POP_JUMP_IF_FALSE    62  'to 62'

 L.2093        50  LOAD_CONST               True
               52  STORE_FAST               'overflow'

 L.2094        54  LOAD_FAST                'sz'
               56  LOAD_CONST               1
               58  BINARY_SUBTRACT  
               60  STORE_FAST               'offset'
             62_0  COME_FROM            48  '48'

 L.2096        62  LOAD_FAST                'offset'
               64  LOAD_FAST                'length'
               66  BINARY_ADD       
               68  LOAD_FAST                'sz'
               70  COMPARE_OP               >
               72  POP_JUMP_IF_FALSE    98  'to 98'

 L.2097        74  LOAD_FAST                'offset'
               76  LOAD_FAST                'sz'
               78  LOAD_CONST               1
               80  BINARY_SUBTRACT  
               82  COMPARE_OP               >
               84  POP_JUMP_IF_FALSE    90  'to 90'

 L.2098        86  LOAD_CONST               0
               88  STORE_FAST               'length'
             90_0  COME_FROM            84  '84'

 L.2099        90  LOAD_FAST                'sz'
               92  LOAD_FAST                'length'
               94  BINARY_SUBTRACT  
               96  STORE_FAST               'offset'
             98_0  COME_FROM            72  '72'

 L.2101        98  LOAD_FAST                'offset'
              100  LOAD_CONST               0
              102  COMPARE_OP               <
              104  POP_JUMP_IF_FALSE   110  'to 110'

 L.2102       106  LOAD_CONST               0
              108  STORE_FAST               'offset'
            110_0  COME_FROM           104  '104'

 L.2103       110  LOAD_FAST                'length'
              112  LOAD_CONST               0
              114  COMPARE_OP               <
              116  POP_JUMP_IF_FALSE   122  'to 122'

 L.2104       118  LOAD_CONST               0
              120  STORE_FAST               'length'
            122_0  COME_FROM           116  '116'

 L.2106       122  LOAD_FAST                'length'
              124  LOAD_CONST               0
              126  COMPARE_OP               ==
              128  POP_JUMP_IF_FALSE   136  'to 136'

 L.2107       130  LOAD_STR                 ''
              132  STORE_FAST               'data'
              134  JUMP_FORWARD        156  'to 156'
            136_0  COME_FROM           128  '128'

 L.2109       136  LOAD_FAST                'f'
              138  LOAD_METHOD              seek
              140  LOAD_FAST                'offset'
              142  CALL_METHOD_1         1  ''
              144  POP_TOP          

 L.2110       146  LOAD_FAST                'f'
              148  LOAD_METHOD              read
              150  LOAD_FAST                'length'
              152  CALL_METHOD_1         1  ''
              154  STORE_FAST               'data'
            156_0  COME_FROM           134  '134'

 L.2112       156  LOAD_FAST                'sz'
              158  STORE_FAST               'offset'

 L.2113       160  LOAD_GLOBAL              as_string
              162  LOAD_FAST                'data'
              164  CALL_FUNCTION_1       1  ''
              166  LOAD_FAST                'offset'
              168  LOAD_FAST                'overflow'
              170  BUILD_LIST_3          3 
              172  POP_BLOCK        
              174  ROT_TWO          
              176  BEGIN_FINALLY    
              178  WITH_CLEANUP_START
              180  WITH_CLEANUP_FINISH
              182  POP_FINALLY           0  ''
              184  POP_BLOCK        
              186  RETURN_VALUE     
            188_0  COME_FROM_WITH       10  '10'
              188  WITH_CLEANUP_START
              190  WITH_CLEANUP_FINISH
              192  END_FINALLY      
              194  POP_BLOCK        
              196  JUMP_FORWARD        232  'to 232'
            198_0  COME_FROM_FINALLY     0  '0'

 L.2114       198  DUP_TOP          
              200  LOAD_GLOBAL              OSError
              202  LOAD_GLOBAL              IOError
              204  BUILD_TUPLE_2         2 
              206  COMPARE_OP               exception-match
              208  POP_JUMP_IF_FALSE   230  'to 230'
              210  POP_TOP          
              212  POP_TOP          
              214  POP_TOP          

 L.2115       216  LOAD_STR                 ''
              218  LOAD_FAST                'offset'
              220  LOAD_CONST               False
              222  BUILD_LIST_3          3 
              224  ROT_FOUR         
              226  POP_EXCEPT       
              228  RETURN_VALUE     
            230_0  COME_FROM           208  '208'
              230  END_FINALLY      
            232_0  COME_FROM           196  '196'

Parse error at or near `ROT_TWO' instruction at offset 174


def decode_wait_status(sts):
    """Decode the status returned by wait() or waitpid().

    Return a tuple (exitstatus, message) where exitstatus is the exit
    status, or -1 if the process was killed by a signal; and message
    is a message telling what happened.  It is the caller's
    responsibility to display the message.
    """
    if os.WIFEXITEDsts:
        es = os.WEXITSTATUSsts & 65535
        msg = 'exit status %s' % es
        return (es, msg)
    if os.WIFSIGNALEDsts:
        sig = os.WTERMSIGsts
        msg = 'terminated by %s' % signame(sig)
        if hasattr(os, 'WCOREDUMP'):
            iscore = os.WCOREDUMPsts
        else:
            iscore = sts & 128
        if iscore:
            msg += ' (core dumped)'
        return (
         -1, msg)
    msg = 'unknown termination cause 0x%04x' % sts
    return (-1, msg)


_signames = None

def signame(sig):
    """Return a symbolic name for a signal.

    Return "signal NNN" if there is no corresponding SIG name in the
    signal module.
    """
    global _signames
    if _signames is None:
        _init_signames()
    return _signames.getsig or 'signal %d' % sig


def _init_signames():
    global _signames
    d = {}
    for k, v in signal.__dict__.items:
        k_startswith = getattr(k, 'startswith', None)
        if k_startswith is None:
            pass
        elif k_startswith('SIG'):
            d[v] = k_startswith('SIG_') or k
    else:
        _signames = d


class SignalReceiver:

    def __init__(self):
        self._signals_recvd = []

    def receive(self, sig, frame):
        if sig not in self._signals_recvd:
            self._signals_recvd.appendsig

    def get_signal(self):
        if self._signals_recvd:
            sig = self._signals_recvd.pop0
        else:
            sig = None
        return sig


def expand--- This code section failed: ---

 L.2187         0  SETUP_FINALLY        12  'to 12'

 L.2188         2  LOAD_FAST                's'
                4  LOAD_FAST                'expansions'
                6  BINARY_MODULO    
                8  POP_BLOCK        
               10  RETURN_VALUE     
             12_0  COME_FROM_FINALLY     0  '0'

 L.2189        12  DUP_TOP          
               14  LOAD_GLOBAL              KeyError
               16  COMPARE_OP               exception-match
               18  POP_JUMP_IF_FALSE    94  'to 94'
               20  POP_TOP          
               22  STORE_FAST               'ex'
               24  POP_TOP          
               26  SETUP_FINALLY        82  'to 82'

 L.2190        28  LOAD_GLOBAL              list
               30  LOAD_FAST                'expansions'
               32  LOAD_METHOD              keys
               34  CALL_METHOD_0         0  ''
               36  CALL_FUNCTION_1       1  ''
               38  STORE_FAST               'available'

 L.2191        40  LOAD_FAST                'available'
               42  LOAD_METHOD              sort
               44  CALL_METHOD_0         0  ''
               46  POP_TOP          

 L.2192        48  LOAD_GLOBAL              ValueError

 L.2193        50  LOAD_STR                 'Format string %r for %r contains names (%s) which cannot be expanded. Available names: %s'

 L.2195        52  LOAD_FAST                's'
               54  LOAD_FAST                'name'
               56  LOAD_GLOBAL              str
               58  LOAD_FAST                'ex'
               60  CALL_FUNCTION_1       1  ''
               62  LOAD_STR                 ', '
               64  LOAD_METHOD              join
               66  LOAD_FAST                'available'
               68  CALL_METHOD_1         1  ''
               70  BUILD_TUPLE_4         4 

 L.2193        72  BINARY_MODULO    

 L.2192        74  CALL_FUNCTION_1       1  ''
               76  RAISE_VARARGS_1       1  'exception instance'
               78  POP_BLOCK        
               80  BEGIN_FINALLY    
             82_0  COME_FROM_FINALLY    26  '26'
               82  LOAD_CONST               None
               84  STORE_FAST               'ex'
               86  DELETE_FAST              'ex'
               88  END_FINALLY      
               90  POP_EXCEPT       
               92  JUMP_FORWARD        150  'to 150'
             94_0  COME_FROM            18  '18'

 L.2196        94  DUP_TOP          
               96  LOAD_GLOBAL              Exception
               98  COMPARE_OP               exception-match
              100  POP_JUMP_IF_FALSE   148  'to 148'
              102  POP_TOP          
              104  STORE_FAST               'ex'
              106  POP_TOP          
              108  SETUP_FINALLY       136  'to 136'

 L.2197       110  LOAD_GLOBAL              ValueError

 L.2198       112  LOAD_STR                 'Format string %r for %r is badly formatted: %s'

 L.2199       114  LOAD_FAST                's'
              116  LOAD_FAST                'name'
              118  LOAD_GLOBAL              str
              120  LOAD_FAST                'ex'
              122  CALL_FUNCTION_1       1  ''
              124  BUILD_TUPLE_3         3 

 L.2198       126  BINARY_MODULO    

 L.2197       128  CALL_FUNCTION_1       1  ''
              130  RAISE_VARARGS_1       1  'exception instance'
              132  POP_BLOCK        
              134  BEGIN_FINALLY    
            136_0  COME_FROM_FINALLY   108  '108'
              136  LOAD_CONST               None
              138  STORE_FAST               'ex'
              140  DELETE_FAST              'ex'
              142  END_FINALLY      
              144  POP_EXCEPT       
              146  JUMP_FORWARD        150  'to 150'
            148_0  COME_FROM           100  '100'
              148  END_FINALLY      
            150_0  COME_FROM           146  '146'
            150_1  COME_FROM            92  '92'

Parse error at or near `DUP_TOP' instruction at offset 94


def make_namespec(group_name, process_name):
    if group_name == process_name:
        name = process_name
    else:
        name = '%s:%s' % (group_name, process_name)
    return name


def split_namespec(namespec):
    names = namespec.split':'1
    if len(names) == 2:
        group_name, process_name = names
        if not process_name or process_name == '*':
            process_name = None
    else:
        group_name, process_name = namespec, namespec
    return (
     group_name, process_name)


class ProcessException(Exception):
    __doc__ = ' Specialized exceptions used when attempting to start a process '


class BadCommand(ProcessException):
    __doc__ = ' Indicates the command could not be parsed properly. '


class NotExecutable(ProcessException):
    __doc__ = ' Indicates that the filespec cannot be executed because its path\n    resolves to a file which is not executable, or which is a directory. '


class NotFound(ProcessException):
    __doc__ = ' Indicates that the filespec cannot be executed because it could not\n    be found '


class NoPermission(ProcessException):
    __doc__ = ' Indicates that the file cannot be executed because the supervisor\n    process does not possess the appropriate UNIX filesystem permission\n    to execute the file. '