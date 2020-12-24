# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/futuregrid_move/rain/move/RainMoveClientConf.py
# Compiled at: 2012-05-30 11:12:55
"""
Class to read Rain Move Client configuration
"""
__author__ = 'Javier Diaz'
import os, ConfigParser, string, sys, logging
configFileName = 'fg-client.conf'

class RainMoveClientConf(object):

    def __init__(self):
        super(RainMoveClientConf, self).__init__()
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
        self._rainmoveport = 0
        self._rainmoveserveraddr = 0
        self._rainmoveca_certs = ''
        self._rainmovecertfile = ''
        self._rainmovekeyfile = ''
        self._rainmovelogfile = ''
        self._rainmovelogLevel = 'DEBUG'
        self._logType = ['DEBUG', 'INFO', 'WARNING', 'ERROR']
        self.loadConfig()

    def getPort(self):
        return self._rainmoveport

    def getServeraddr(self):
        return self._rainmoveserveraddr

    def getLogFile(self):
        return self._rainmovelogfile

    def getLogLevel(self):
        return self._rainmovelogLevel

    def getCaCerts(self):
        return self._rainmoveca_certs

    def getCertFile(self):
        return self._rainmovecertfile

    def getKeyFile(self):
        return self._rainmovekeyfile

    def loadConfig(self):
        section = 'RainMove'
        config = ConfigParser.ConfigParser()
        if os.path.isfile(self._configfile):
            config.read(self._configfile)
        else:
            print 'Error: Config file not found' + self._configfile
            sys.exit(1)
        try:
            self._rainmoveport = int(config.get(section, 'port', 0))
        except ConfigParser.NoOptionError:
            print 'Error: No port option found in section ' + section + ' file ' + self._configfile
            sys.exit(1)
        except ConfigParser.NoSectionError:
            print 'Error: no section ' + section + ' found in the ' + self._configfile + ' config file'
            sys.exit(1)

        try:
            self._rainmoveserveraddr = os.path.expanduser(config.get(section, 'serveraddr', 0))
        except ConfigParser.NoOptionError:
            print 'Error: No serveraddr option found in section ' + section + ' file ' + self._configfile
            sys.exit(1)

        try:
            self._rainmovelogfile = os.path.expanduser(config.get(section, 'log', 0))
        except ConfigParser.NoOptionError:
            print 'Error: No log option found in section ' + section + ' file ' + self._configfile
            sys.exit(1)

        try:
            tempLevel = string.upper(config.get(section, 'log_level', 0))
        except ConfigParser.NoOptionError:
            tempLevel = self._rainmoveLogLevel

        if tempLevel not in self._logType:
            print 'Log level ' + tempLevel + ' not supported. Using the default one ' + self._rainmovelogLevel
            tempLevel = self._rainmovelogLevel
        self._rainmovelogLevel = eval('logging.' + tempLevel)
        try:
            self._rainmoveca_certs = os.path.expanduser(config.get(section, 'ca_cert', 0))
        except ConfigParser.NoOptionError:
            print 'Error: No ca_cert option found in section ' + section + ' file ' + self._configfile
            sys.exit(1)

        if not os.path.isfile(self._rainmoveca_certs):
            print 'Error: ca_cert file not found in ' + self._rainmoveca_certs
            sys.exit(1)
        try:
            self._rainmovecertfile = os.path.expanduser(config.get(section, 'certfile', 0))
        except ConfigParser.NoOptionError:
            print 'Error: No certfile option found in section ' + section + ' file ' + self._configfile
            sys.exit(1)

        if not os.path.isfile(self._rainmovecertfile):
            print 'Error: certfile file not found in ' + self._rainmovecertfile
            sys.exit(1)
        try:
            self._rainmovekeyfile = os.path.expanduser(config.get(section, 'keyfile', 0))
        except ConfigParser.NoOptionError:
            print 'Error: No keyfile option found in section ' + section + ' file ' + self._configfile
            sys.exit(1)

        if not os.path.isfile(self._rainmovekeyfile):
            print 'Error: keyfile file not found in ' + self._rainmovekeyfile
            sys.exit(1)