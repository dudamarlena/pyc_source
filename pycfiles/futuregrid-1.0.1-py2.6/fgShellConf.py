# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/futuregrid/shell/fgShellConf.py
# Compiled at: 2012-09-06 11:03:15
"""
FutureGrid Command Line Interface

Read configuration from file
"""
__author__ = 'Javier Diaz'
__version__ = '0.9'
import os, ConfigParser, string, logging
from futuregrid.utils import fgLog
import sys
configFileName = 'fg-client.conf'

class fgShellConf(object):

    def __init__(self):
        """initialize the shell configuration"""
        self._fgpath = ''
        try:
            self._fgpath = os.environ['FG_PATH']
        except KeyError:
            self._fgpath = os.path.dirname(__file__) + '/../'

        self._loghistdir = '~/.fg/'
        self._configfile = os.path.expanduser(self._loghistdir) + '/' + configFileName
        if not os.path.isfile(self._configfile):
            self._configfile = '/etc/futuregrid/' + configFileName
            if not os.path.isfile(self._configfile):
                print 'ERROR: configuration file ' + configFileName + ' not found'
                sys.exit(1)
        self._logfile = ''
        self._histfile = ''
        self._scriptfile = os.environ['PWD'] + '/script'
        self._logLevel = 'DEBUG'
        self._logType = ['DEBUG', 'INFO', 'WARNING', 'ERROR']
        self.loadConfig()

    def getLogHistDir(self):
        """returns the directory of the history file"""
        return self._loghistdir

    def getConfigFile(self):
        """returns the configuration file"""
        return self._configfile

    def getLogFile(self):
        """returns the logfile"""
        return self._logfile

    def getHistFile(self):
        """returns the history file"""
        return self._histfile

    def getScriptFile(self):
        """returns the script file"""
        return self._scriptfile

    def getLogLevel(self):
        """returns the loglevel"""
        return self._logLevel

    def loadConfig(self):
        """loads the configuration from the config file"""
        config = ConfigParser.ConfigParser()
        config.read(self._configfile)
        section = 'fg-shell'
        try:
            self._logfile = os.path.expanduser(config.get(section, 'log', 0))
        except ConfigParser.NoOptionError:
            print 'Error: No option log in section LogHist'
            sys.exit(0)

        try:
            self._histfile = os.path.expanduser(config.get(section, 'history', 0))
        except ConfigParser.NoOptionError:
            print 'Error: No option history in section LogHist'
            sys.exit(0)

        try:
            self._scriptfile = os.path.expanduser(config.get(section, 'script', 0))
        except ConfigParser.NoOptionError:
            pass

        try:
            tempLevel = string.upper(config.get(section, 'log_level', 0))
        except ConfigParser.NoOptionError:
            tempLevel = self._LogLevel

        if tempLevel not in self._logType:
            print 'Log level ' + self._log_level + ' not supported. Using the default one ' + self._defaultLogLevel
        self._logLevel = eval('logging.' + tempLevel)