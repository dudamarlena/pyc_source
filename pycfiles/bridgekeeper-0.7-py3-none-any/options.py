# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/bridgedb/parse/options.py
# Compiled at: 2015-11-05 10:40:17
__doc__ = b'Parsers for BridgeDB commandline options.\n\n.. py:module:: bridgedb.parse.options\n   :synopsis: Parsers for BridgeDB commandline options.\n\n\nbridgedb.parse.options\n======================\n::\n\n  bridgedb.parse.options\n   |__ setConfig()\n   |__ getConfig() - Set/Get the config file path.\n   |__ setRundir()\n   |__ getRundir() - Set/Get the runtime directory.\n   |__ parseOptions() - Create the main options parser for BridgeDB.\n   |\n   \\_ BaseOptions - Base options, included in all other options menus.\n       ||\n       |\\__ findRundirAndConfigFile() - Find the absolute path of the config\n       |                                file and runtime directory, or find\n       |                                suitable defaults.\n       |\n       |__ SIGHUPOptions - Menu to explain SIGHUP signal handling and usage.\n       |__ SIGUSR1Options - Menu to explain SIGUSR1 handling and usage.\n       |\n       |__ MockOptions - Suboptions for creating fake bridge descriptors for\n       |                 testing purposes.\n       \\__ MainOptions - Main commandline options parser for BridgeDB.\n..\n'
from __future__ import print_function
from __future__ import unicode_literals
import sys, textwrap, traceback, os
from twisted.python import usage
from bridgedb import __version__
_rundir = None
_config = None

def setConfig(path):
    """Set the absolute path to the config file.

    See :meth:`BaseOptions.postOptions`.

    :param string path: The path to set.
    """
    global _config
    _config = path


def getConfig():
    """Get the absolute path to the config file.

    :rtype: string
    :returns: The path to the config file.
    """
    return _config


def setRundir(path):
    """Set the absolute path to the runtime directory.

    See :meth:`BaseOptions.postOptions`.

    :param string path: The path to set.
    """
    global _rundir
    _rundir = path


def getRundir():
    """Get the absolute path to the runtime directory.

    :rtype: string
    :returns: The path to the config file.
    """
    return _rundir


def parseOptions():
    """Create the main options parser and its subcommand parsers.

    Any :exc:`~twisted.python.usage.UsageErrors` which are raised due to
    invalid options are ignored; their error message is printed and then we
    exit the program.

    :rtype: :class:`MainOptions`
    :returns: The main options parsing class, with any commandline arguments
        already parsed.
    """
    options = MainOptions()
    try:
        options.parseOptions()
    except usage.UsageError as uerr:
        print(uerr.message)
        print(options.getUsage())
        sys.exit(1)
    except Exception as error:
        exc, value, tb = sys.exc_info()
        print(b'Unhandled Error: %s' % error.message)
        print(traceback.format_exc(tb))

    return options


class BaseOptions(usage.Options):
    """Base options included in all main and sub options menus."""
    longdesc = textwrap.dedent(b'BridgeDB is a proxy distribution system for\n    private relays acting as bridges into the Tor network. See `bridgedb\n    <command> --help` for addition help.')
    optParameters = [
     [
      b'config', b'c', None,
      b'Configuration file [default: <rundir>/bridgedb.conf]'],
     [
      b'rundir', b'r', None,
      b"Change to this directory before running. [default: `os.getcwd()']\n\n         All other paths, if not absolute, should be relative to this path.\n         This includes the config file and any further files specified within\n         the config file.\n         "]]

    def __init__(self):
        """Create an options parser. All flags, parameters, and attributes of
        this base options parser are inherited by all child classes.
        """
        super(BaseOptions, self).__init__()
        self[b'version'] = self.opt_version
        self[b'verbosity'] = 30

    def opt_quiet(self):
        """Decrease verbosity"""
        self[b'verbosity'] -= 10

    def opt_verbose(self):
        """Increase verbosity"""
        self[b'verbosity'] += 10

    opt_q = opt_quiet
    opt_v = opt_verbose

    def opt_version(self):
        """Display BridgeDB's version and exit."""
        print(b'%s-%s' % (__package__, __version__))
        sys.exit(0)

    @staticmethod
    def findRundirAndConfigFile(rundir=None, config=None):
        """Find the absolute path of the config file and runtime directory, or
        find suitable defaults.

        Attempts to set the absolute path of the runtime directory. If the
        config path is relative, its absolute path is set relative to the
        runtime directory path (unless it starts with '.' or '..', then it is
        interpreted relative to the current working directory). If the path to
        the config file is absolute, it is left alone.

        :type rundir: string or None
        :param rundir: The user-supplied path to the runtime directory, from
            the commandline options (i.e.
            ``options = BaseOptions().parseOptions(); options['rundir'];``).
        :type config: string or None
        :param config: The user-supplied path to the config file, from the
            commandline options (i.e.
            ``options = BaseOptions().parseOptions(); options['config'];``).
        :raises: :api:`twisted.python.usage.UsageError` if either the runtime
            directory or the config file cannot be found.
        """
        gRundir = getRundir()
        gConfig = getConfig()
        if gRundir is None:
            if rundir is not None:
                gRundir = os.path.abspath(os.path.expanduser(rundir))
            else:
                gRundir = os.getcwdu()
        setRundir(gRundir)
        if not os.path.isdir(gRundir):
            raise usage.UsageError(b"Could not change to runtime directory: `%s'" % gRundir)
        if gConfig is None:
            if config is None:
                config = b'bridgedb.conf'
            gConfig = config
            if not os.path.isabs(gConfig):
                if gConfig.startswith(b'.'):
                    gConfig = os.path.abspath(os.path.expanduser(gConfig))
                else:
                    gConfig = os.path.join(gRundir, gConfig)
        setConfig(gConfig)
        gConfig = getConfig()
        if not os.path.isfile(gConfig):
            raise usage.UsageError(b"Specified config file `%s' doesn't exist!" % gConfig)
        return

    def postOptions(self):
        """Automatically called by :meth:`parseOptions`.

        Determines appropriate values for the 'config' and 'rundir' settings.
        """
        super(BaseOptions, self).postOptions()
        self.findRundirAndConfigFile(self[b'rundir'], self[b'config'])
        gConfig = getConfig()
        gRundir = getRundir()
        if self[b'rundir'] is None and gRundir is not None:
            self[b'rundir'] = gRundir
        if self[b'config'] is None and gConfig is not None:
            self[b'config'] = gConfig
        if self[b'verbosity'] <= 10:
            print(b'%s.postOptions():' % self.__class__)
            print(b'  gCONFIG=%s' % gConfig)
            print(b"  self['config']=%s" % self[b'config'])
            print(b'  gRUNDIR=%s' % gRundir)
            print(b"  self['rundir']=%s" % self[b'rundir'])
        return


class MockOptions(BaseOptions):
    """Suboptions for creating necessary conditions for testing purposes."""
    optParameters = [
     [
      b'descriptors', b'n', 1000,
      b'Generate <n> mock bridge descriptor sets\n          (types: netstatus, extrainfo, server)']]


class SIGHUPOptions(BaseOptions):
    """Options menu to explain usage and handling of SIGHUP signals."""
    longdesc = b'If you send a SIGHUP to a running BridgeDB process, the\n    servers will parse and reload all bridge descriptor files into the\n    databases.\n\n    Note that this command WILL NOT handle sending the signal for you; see\n    signal(7) and kill(1) for additional help.'


class SIGUSR1Options(BaseOptions):
    """Options menu to explain usage and handling of SIGUSR1 signals."""
    longdesc = b'If you send a SIGUSR1 to a running BridgeDB process, the\n    servers will dump all bridge assignments by distributor from the\n    databases to files.\n\n    Note that this command WILL NOT handle sending the signal for you; see\n    signal(7) and kill(1) for additional help.'


class MainOptions(BaseOptions):
    """Main commandline options parser for BridgeDB."""
    optFlags = [
     [
      b'dump-bridges', b'd', b'Dump bridges by hashring assignment into files'],
     [
      b'reload', b'R', b'Reload bridge descriptors into running servers']]
    subCommands = [
     [
      b'mock', None, MockOptions, b'Generate a testing environment'],
     [
      b'SIGHUP', None, SIGHUPOptions,
      b'Reload bridge descriptors into running servers'],
     [
      b'SIGUSR1', None, SIGUSR1Options,
      b'Dump bridges by hashring assignment into files']]