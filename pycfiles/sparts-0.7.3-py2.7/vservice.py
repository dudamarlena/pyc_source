# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sparts/vservice.py
# Compiled at: 2015-02-07 04:24:19
"""vservice defines the base service class, `VService`

VService can be used directly, for example with `VService.initFromCLI()`,
or it can be subclassed and used similarly.
"""
from __future__ import absolute_import
from __future__ import print_function
import copy, functools, logging, re, signal, sys, threading, time
from argparse import ArgumentParser
from .compat import OrderedDict, captureWarnings
from sparts import vtask
from .deps import HAS_PSUTIL, HAS_DAEMONIZE
from .sparts import _SpartsObject, option
from sparts import daemon

class VService(_SpartsObject):
    """Core class for implementing services."""
    DEFAULT_LOGLEVEL = 'DEBUG'
    DEFAULT_LOGFILE = None
    DEFAULT_PID = lambda cls: '/var/run/%s.pid' % cls.__name__
    REGISTER_SIGNAL_HANDLERS = True
    TASKS = []
    VERSION = ''
    _name = None
    dryrun = option(action='store_true', help='Run in "dryrun" mode')
    level = option(default=DEFAULT_LOGLEVEL, help='Log Level [%(default)s]')
    logfile = option(default=lambda cls: cls.DEFAULT_LOGFILE, help='Log to this file instead of stderr.  None or "" logs to stderr [%(default)s]')
    register_tasks = option(name='tasks', default=None, metavar='TASK', nargs='*', help='Tasks to run.  Pass without args to see the list. If not passed, all tasks will be started')
    if HAS_DAEMONIZE:
        daemon = option(action='store_true', help='Start as a daemon using PIDFILE')
        pidfile = option(default=DEFAULT_PID, help='Daemon pid file path [%(default)s]', metavar='PIDFILE')
        kill = option(action='store_true', help='Kill the currently running daemon for PIDFILE')
        status = option(action='store_true', help='Output whether the daemon for PIDFILE is running')
    if HAS_PSUTIL:
        runit_install = option(action='store_true', help='Install this service under runit.')

    def __init__(self, ns):
        super(VService, self).__init__()
        self.logger = logging.getLogger(self.name)
        self.options = ns
        self.initLogging()
        self._stop = False
        self._restart = False
        self.tasks = vtask.Tasks()
        for t in vtask.REGISTERED:
            self.tasks.register(t)

        for t in self.TASKS:
            self.tasks.register(t)

        self.warnings = OrderedDict()
        self.warning_id = 0
        self.exported_values = {}
        self.start_time = time.time()

    def initService(self):
        """Override this to do any service-specific initialization"""
        pass

    @classmethod
    def _loptName(cls, name):
        return '--' + name.replace('_', '-')

    def preprocessOptions(self):
        """Processes "action" oriented options."""
        if self.getOption('runit_install'):
            self._install()
        if HAS_DAEMONIZE:
            if self.status:
                if daemon.status(pidfile=self.pidfile, logger=self.logger):
                    sys.exit(0)
                else:
                    sys.exit(1)
            if self.kill:
                if daemon.kill(pidfile=self.pidfile, logger=self.logger):
                    sys.exit(0)
                else:
                    sys.exit(1)
        if self.options.tasks == []:
            print('Available Tasks:')
            for t in self.tasks:
                print(' - %s' % t.__name__)

            sys.exit(1)

    def _createTasks(self):
        all_tasks = set(self.tasks)
        selected_tasks = self.options.tasks
        if selected_tasks is None:
            selected_tasks = [ t.__name__ for t in all_tasks ]
        unregister_tasks = [ t for t in all_tasks if t.__name__ not in selected_tasks
                           ]
        for t in unregister_tasks:
            self.tasks.unregister(t)

        self.tasks.create(self)
        self.initService()
        self.tasks.init()
        return

    def _handleShutdownSignals(self, signum, frame):
        assert signum in (signal.SIGINT, signal.SIGTERM)
        self.logger.info('signal -%d received', signum)
        self.shutdown()

    def _startTasks(self):
        if self.REGISTER_SIGNAL_HANDLERS:
            signal.signal(signal.SIGINT, self._handleShutdownSignals)
            signal.signal(signal.SIGTERM, self._handleShutdownSignals)
        self.tasks.start()
        self.logger.debug('All tasks started')

    def getTask(self, name):
        """Returns a task for the given class `name` or type, or None."""
        return self.tasks.get(name)

    def requireTask(self, name):
        """Returns a task for the given class `name` or type, or throws."""
        return self.tasks.require(name)

    def shutdown(self):
        """Request a graceful shutdown.  Does not block."""
        self.logger.info('Received graceful shutdown request')
        self.stop()

    def restart(self):
        """Request a graceful restart.  Does not block."""
        self.logger.info('Received graceful restart request')
        self._restart = True
        self.stop()

    def stop(self):
        self._stop = True

    def _wait(self):
        try:
            self.logger.debug('VService Active.  Awaiting graceful shutdown.')
            while not self._stop:
                time.sleep(0.1)

        except KeyboardInterrupt:
            self.logger.info('KeyboardInterrupt Received!  Stopping Tasks...')

        for t in reversed(self.tasks):
            t.stop()

        try:
            self.logger.info('Waiting for tasks to shutdown gracefully...')
            for t in reversed(self.tasks):
                self.logger.debug('Waiting for %s to stop...', t)
                t.join()

        except KeyboardInterrupt:
            self.logger.warning('Abandon all hope ye who enter here')

    def join(self):
        """Blocks until a stop is requested, waits for all tasks to shutdown"""
        while not self._stop:
            time.sleep(0.1)

        for t in reversed(self.tasks):
            t.join()

    @classmethod
    def initFromCLI(cls, name=None):
        """Starts this service, processing command line arguments."""
        ap = cls._buildArgumentParser()
        ns = ap.parse_args()
        instance = cls.initFromOptions(ns, name=name)
        return instance

    @classmethod
    def initFromOptions(cls, ns, name=None):
        """Starts this service, arguments from `ns`"""
        instance = cls(ns)
        if name is not None:
            instance.name = name
        instance.preprocessOptions()
        if HAS_DAEMONIZE and ns.daemon:
            daemon.daemonize(command=functools.partial(cls._runloop, instance), name=instance.name, pidfile=ns.pidfile, logger=instance.logger)
        else:
            return cls._runloop(instance)
        return

    @classmethod
    def _runloop(cls, instance):
        while not instance._stop:
            try:
                instance._createTasks()
                instance._startTasks()
            except Exception:
                instance.logger.exception('Unexpected Exception during init')
                instance.shutdown()

            instance._wait()
            if instance._restart:
                instance = cls(instance.options)

        instance.logger.info('Instance shut down gracefully')

    def startBG(self):
        """Starts this service in the background

        Returns a thread that will join() on graceful shutdown."""
        self._createTasks()
        self._startTasks()
        t = threading.Thread(target=self._wait)
        t.start()
        return t

    @property
    def name(self):
        if self._name is None:
            self._name = self.__class__.__name__
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    def initLogging(self):
        """Basic stderr logging.  Override this to do something else."""
        if self.logfile:
            logging.basicConfig(level=self.loglevel, filename=self.logfile)
        else:
            logging.basicConfig(level=self.loglevel, stream=sys.stderr)
        captureWarnings(True)

    @classmethod
    def _makeArgumentParser(cls):
        """Create an argparse.ArgumentParser instance.

        Override this method if you already have an ArgumentParser instance to use
        or you simply want to specify some of the optional arguments to
        argparse.ArgumentParser.__init__
        (e.g. "fromfile_prefix_chars" or "conflict_handler"...)
        """
        return ArgumentParser()

    @classmethod
    def _buildArgumentParser(cls):
        ap = cls._makeArgumentParser()
        cls._addArguments(ap)
        all_tasks = vtask.Tasks()
        all_tasks.register_all(cls.TASKS)
        all_tasks.register_all(vtask.REGISTERED)
        for t in all_tasks:
            t._addArguments(ap)

        return ap

    @property
    def loglevel(self):
        return getattr(logging, self.options.level)

    def getOption(self, name, default=None):
        return getattr(self.options, name, default)

    def setOption(self, name, value):
        setattr(self.options, name, value)

    def getOptions(self):
        return self.options.__dict__

    def _install(self):
        if not HAS_PSUTIL:
            raise NotImplementedError('You need psutil installed to install under runit')
        import sparts.runit
        sparts.runit.install(self.name)
        sys.exit(0)

    def getChildren(self):
        return dict((t.name, t) for t in self.tasks)

    def getWarnings(self):
        return self.warnings

    def registerWarning(self, message):
        wid = self.warning_id
        self.warning_id += 1
        self.warnings[wid] = message
        return wid

    def clearWarnings(self):
        self.warnings = OrderedDict()

    def clearWarning(self, id):
        if id not in self.warnings:
            return False
        del self.warnings[id]
        return True

    def getExportedValue(self, name):
        return self.exported_values.get(name, '')

    def setExportedValue(self, name, value):
        if value is None:
            del self.exported_values[name]
        else:
            self.exported_values[name] = value
        return

    def getExportedValues(self):
        return copy.copy(self.exported_values)

    def getRegexExportedValues(self, regex):
        matcher = re.compile(regex)
        keys = [ key for key in self.exported_values.keys() if matcher.match(key) is not None
               ]
        return self.getSelectedExportedValues(keys)

    def getSelectedExportedValues(self, keys):
        return dict([ (key, self.getExportedValue(key)) for key in keys
                    ])