# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/futuregrid/rain/RainClientConf.py
# Compiled at: 2012-09-06 11:03:15
"""
Class to read Rain Client configuration
"""
__author__ = 'Javier Diaz'
import os, ConfigParser, string, sys, logging
configFileName = 'fg-client.conf'

class RainClientConf(object):

    def __init__(self):
        super(RainClientConf, self).__init__()
        self._fgpath = ''
        try:
            self._fgpath = os.environ['FG_PATH']
        except KeyError:
            self._fgpath = os.path.dirname(__file__) + '/../'

        self._localpath = '~/.fg/'
        self._configfile = os.path.expanduser(self._localpath) + '/' + configFileName
        if not os.path.isfile(self._configfile):
            self._configfile = '/etc/futuregrid/' + configFileName
            if not os.path.isfile(self._configfile):
                print 'ERROR: configuration file ' + configFileName + ' not found'
                sys.exit(1)
        self._refresh = 0
        self._moab_max_wait = 0
        self._moab_images_file = ''
        self._http_server = ''
        self._loginnode = ''
        self._logfile = ''
        self._logLevel = 'DEBUG'
        self._logType = ['DEBUG', 'INFO', 'WARNING', 'ERROR']
        self.loadConfig()

    def getConfigFile(self):
        return self._configfile

    def getMoabMaxWait(self):
        return self._moab_max_wait

    def getMoabImagesFile(self):
        return self._moab_images_file

    def getLoginNode(self):
        return self._loginnode

    def getRefresh(self):
        return self._refresh

    def getLogFile(self):
        return self._logfile

    def getLogLevel(self):
        return self._logLevel

    def getHttpServer(self):
        return self._http_server

    def loadConfig(self):
        section = 'Rain'
        config = ConfigParser.ConfigParser()
        if os.path.isfile(self._configfile):
            config.read(self._configfile)
        else:
            print 'Error: Config file not found' + self._configfile
            sys.exit(1)
        try:
            self._moab_max_wait = int(config.get(section, 'moab_max_wait', 0))
        except ConfigParser.NoOptionError:
            print 'Error: No moab_max_wait option found in section ' + section + ' file ' + self._configfile
            sys.exit(1)
        except ConfigParser.NoSectionError:
            print 'Error: no section ' + section + ' found in the ' + self._configfile + ' config file'
            sys.exit(1)

        try:
            self._moab_images_file = os.path.expanduser(config.get(section, 'moab_images_file', 0))
        except ConfigParser.NoOptionError:
            print 'Error: No moab_images_file option found in section ' + section + ' file ' + self._configfile
            sys.exit(1)

        try:
            self._refresh = int(config.get(section, 'refresh', 0))
        except ConfigParser.NoOptionError:
            print 'Error: No refresh option found in section ' + section + ' file ' + self._configfile
            sys.exit(1)

        try:
            self._loginnode = config.get(section, 'loginnode', 0)
        except ConfigParser.NoOptionError:
            print 'Error: No loginnode option found in section ' + section + ' file ' + self._configfile
            sys.exit(1)

        try:
            self._http_server = config.get(section, 'http_server', 0)
        except ConfigParser.NoOptionError:
            print 'Error: No http_server option found in section ' + section + ' file ' + self._configfile
            sys.exit(1)

        try:
            self._logfile = os.path.expanduser(config.get(section, 'log', 0))
        except ConfigParser.NoOptionError:
            print 'Error: No log option found in section ' + section + ' file ' + self._configfile
            sys.exit(1)

        try:
            tempLevel = string.upper(config.get(section, 'log_level', 0))
        except ConfigParser.NoOptionError:
            tempLevel = self._LogLevel

        if tempLevel not in self._logType:
            print 'Log level ' + tempLevel + ' not supported. Using the default one ' + self._logLevel
            tempLevel = self._logLevel
        self._logLevel = eval('logging.' + tempLevel)