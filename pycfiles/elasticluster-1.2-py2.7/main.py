# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/elasticluster/main.py
# Compiled at: 2014-10-22 18:35:47
__author__ = 'Nicolas Baer <nicolas.baer@uzh.ch>, Antonio Messina <antonio.s.messina@gmail.com>'
import logging, os, shutil, sys, cli.app
try:
    from voluptuous import MultipleInvalid, Invalid
except ImportError:
    from voluptuous.voluptuous import MultipleInvalid, Invalid

from elasticluster import log
from elasticluster.subcommands import Start, SetupCluster
from elasticluster.subcommands import Stop
from elasticluster.subcommands import AbstractCommand
from elasticluster.subcommands import ListClusters
from elasticluster.subcommands import ListNodes
from elasticluster.subcommands import ListTemplates
from elasticluster.subcommands import ResizeCluster
from elasticluster.subcommands import SshFrontend
from elasticluster.subcommands import SftpFrontend
from elasticluster.conf import Configurator
from elasticluster.exceptions import ConfigurationError

class ElastiCluster(cli.app.CommandLineApp):
    name = 'elasticluster'
    default_configuration_file = os.path.expanduser('~/.elasticluster/config')

    def setup(self):
        cli.app.CommandLineApp.setup(self)
        commands = [
         Start(self.params),
         Stop(self.params),
         ListClusters(self.params),
         ListNodes(self.params),
         ListTemplates(self.params),
         SetupCluster(self.params),
         ResizeCluster(self.params),
         SshFrontend(self.params),
         SftpFrontend(self.params)]
        self.add_param('-v', '--verbose', action='count', default=0, help='Increase verbosity. If at least four `-v` option are given, elasticluster will create new VMs sequentially instead of doing it in parallel.')
        self.add_param('-s', '--storage', metavar='PATH', help='Path to the storage folder. Default: `%s`' % Configurator.default_storage_dir, default=Configurator.default_storage_dir)
        self.add_param('-c', '--config', metavar='PATH', help='Path to the configuration file. Default: `%s`' % self.default_configuration_file, default=self.default_configuration_file)
        self.add_param('--version', action='store_true', help='Print version information and exit.')
        self.subparsers = self.argparser.add_subparsers(title='COMMANDS', help='Available commands. Run `elasticluster cmd --help` to have information on command `cmd`.')
        for command in commands:
            if isinstance(command, AbstractCommand):
                command.setup(self.subparsers)

    def pre_run(self):
        if '--version' in sys.argv:
            import pkg_resources
            version = pkg_resources.get_distribution('elasticluster').version
            print 'elasticluster version %s' % version
            sys.exit(0)
        cli.app.CommandLineApp.pre_run(self)
        loglevel = max(1, logging.WARNING - 10 * max(0, self.params.verbose))
        log.setLevel(loglevel)
        if self.params.verbose > 3:
            log.DO_NOT_FORK = True
        if not os.path.isdir(self.params.storage):
            try:
                os.makedirs(self.params.storage)
            except OSError as ex:
                sys.stderr.write('Unable to create storage directory: %s\n' % str(ex))
                sys.exit(1)

        if not os.path.isfile(self.params.config):
            if self.params.config == self.default_configuration_file:
                if not os.path.exists(os.path.dirname(self.params.config)):
                    os.mkdir(os.path.dirname(self.params.config))
                template = os.path.join(sys.prefix, 'share/elasticluster/etc/config.template')
                log.warning('Deploying default configuration file to %s.', self.params.config)
                shutil.copyfile(template, self.params.config)
            elif not os.path.isfile(self.params.config):
                sys.stderr.write('Unable to read configuration file `%s`.\n' % self.params.config)
                sys.exit(1)
        if self.params.func:
            try:
                self.params.func.pre_run()
            except (RuntimeError, ConfigurationError) as ex:
                sys.stderr.write(str(ex).strip() + '\n')
                sys.exit(1)

    def main(self):
        """
        Elasticluster will start, stop, grow, shrink clusters on an EC2 cloud.
        """
        try:
            return self.params.func()
        except MultipleInvalid as ex:
            for error in ex.errors:
                print "Error validating configuration file '%s': `%s`" % (
                 self.params.config, error)

            sys.exit(1)
        except Invalid as ex:
            print "Error validating configuration file '%s': `%s`" % (
             self.params.config, ex)
            sys.exit(1)


def main():
    try:
        app = ElastiCluster()
        app.run()
    except KeyboardInterrupt:
        sys.stderr.write('\nWARNING: execution interrupted by the user!\nYour clusters may be in inconsistent state!\n')
        return 1


if __name__ == '__main__':
    main()