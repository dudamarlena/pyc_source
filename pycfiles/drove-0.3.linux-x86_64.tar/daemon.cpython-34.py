# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ajdiaz/env/drove/lib/python3.4/site-packages/drove/command/daemon.py
# Compiled at: 2015-01-20 05:42:58
# Size of source mod 2**32: 3740 bytes
import sys
from . import Command
from .. import VERSION
from ..util import log
from ..channel import Channel
from ..reloader import Reloader
from ..plugin import PluginManager
from ..util.daemon import Daemon
from ..util.network import getfqdn

class DaemonCommand(Command):
    __doc__ = 'This class extends :class:`Command` to implement ``daemon`` command.\n    '

    def _exit_handler(self):
        if self.log:
            self.log.error('Received TERM signal. Try to exit gently...')
        if self.plugins:
            self.plugins.stop_all()
        sys.exit(15)

    def _daemon(self):
        try:
            self.plugins.start_all()
            self.log.debug('Starting reloader')
            reloader = Reloader([getfqdn, self.config] + [x for x in self.plugins], interval=self.config.get('reload', 60))
            reloader.start()
            self.log.info('Entering data gathering loop')
            self.plugins.loop()
        except KeyboardInterrupt:
            self.log.fatal('Received a Keyboard Interrupt. Exit silently.')
            sys.exit(15)
        except BaseException as e:
            if self.args.verbose:
                raise
            self.log.fatal('Unexpected error happened during drove ' + 'execution: {message}'.format(message=str(e)))
            sys.exit(1)

    def execute(self):
        """When invoked run drove as daemon (usually in background)
        """
        if self.config.get('nodename', None) is None:
            self.config['nodename'] = getfqdn
        self.log = log.getLogger(syslog=self.config.get('syslog', True), console=self.config.get('logconsole', False), logfile=self.config.get('logfile', None), logfile_size=self.config.get('logfile_size', 0), logfile_keep=self.config.get('logfile_keep', 0))
        if self.args.verbose:
            self.log.setLevel(log.DEBUG)
        try:
            from setproctitle import setproctitle
            setproctitle('drove %s' % ' '.join(sys.argv[1:]))
        except ImportError:
            pass

        self.log.info('Starting drove daemon (%s)' % (VERSION,))
        self.log.info('Using configuration file: %s' % (
         self.config.config_file,))
        self.log.debug('Creating channel')
        channel = Channel()
        self.log.debug('Starting plugins')
        self.plugins = PluginManager(self.config, channel)
        if len(self.plugins) == 0:
            self.log.warning('No plugins installed... ' + 'drove has no work to do.')
            if self.args.exit_if_no_plugins:
                sys.exit(0)
            daemon = Daemon.create(self._daemon, self._exit_handler)
            if self.args.foreground:
                daemon.foreground()
        else:
            return daemon.start()