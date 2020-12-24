# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/futuregrid_passwdstack/passwdstack/PasswdStackClientConf.py
# Compiled at: 2012-08-20 15:17:26
"""
Class to read PasswdStack Client configuration
"""
__author__ = 'Javier Diaz'
import os, ConfigParser, string, sys, logging, re
configFileName = 'fg-client.conf'

class PasswdStackClientConf(object):

    def __init__(self):
        super(PasswdStackClientConf, self).__init__()
        self._fgpath = ''
        try:
            self._fgpath = os.environ['FG_PATH']
        except KeyError:
            self._fgpath = os.path.dirname(__file__) + '/../../'

        self._localpath = '~/.fg/'
        self._configfile = os.path.expanduser(self._localpath) + '/' + configFileName
        if not os.path.isfile(self._configfile):
            self._configfile = '/etc/futuregrid/' + configFileName
            if not os.path.isfile(self._configfile):
                print 'ERROR: configuration file ' + configFileName + ' not found'
                sys.exit(1)
        self._logLevel_default = 'DEBUG'
        self._logType = ['DEBUG', 'INFO', 'WARNING', 'ERROR']
        self._serveraddr = ''
        self._port = 0
        self._ca_certs = ''
        self._certfile = ''
        self._keyfile = ''
        self._logFile = ''
        self._logLevel = ''
        self._config = ConfigParser.ConfigParser()
        self._config.read(self._configfile)

    def getConfigFile(self):
        return self._configfile

    def getServeraddr(self):
        return self._serveraddr

    def getPort(self):
        return self._port

    def getCaCerts(self):
        return self._ca_certs

    def getCertFile(self):
        return self._certfile

    def getKeyFile(self):
        return self._keyfile

    def getLogFile(self):
        return self._logFile

    def getLogLevel(self):
        return self._logLevel

    def load_passwdstackConfig(self):
        section = 'PasswdStack'
        try:
            self._serveraddr = self._config.get(section, 'serveraddr', 0)
        except ConfigParser.NoOptionError:
            print 'Error: No serveraddr option found in section ' + section + ' file ' + self._configfile
            sys.exit(1)
        except ConfigParser.NoSectionError:
            print 'Error: no section ' + section + ' found in the ' + self._configfile + ' config file'
            sys.exit(1)

        try:
            self._port = int(self._config.get(section, 'port', 0))
        except ConfigParser.NoOptionError:
            print 'Error: No port option found in section ' + section + ' file ' + self._configfile
            sys.exit(1)

        try:
            self._ca_certs = os.path.expanduser(self._config.get(section, 'ca_cert', 0))
        except ConfigParser.NoOptionError:
            print 'Error: No ca_cert option found in section ' + section + ' file ' + self._configfile
            sys.exit(1)

        if not os.path.isfile(self._ca_certs):
            print 'Error: ca_cert file not found in ' + self._ca_certs
            sys.exit(1)
        try:
            self._certfile = os.path.expanduser(self._config.get(section, 'certfile', 0))
        except ConfigParser.NoOptionError:
            print 'Error: No certfile option found in section ' + section + ' file ' + self._configfile
            sys.exit(1)

        if not os.path.isfile(self._certfile):
            print 'Error: certfile file not found in ' + self._certfile
            sys.exit(1)
        try:
            self._keyfile = os.path.expanduser(self._config.get(section, 'keyfile', 0))
        except ConfigParser.NoOptionError:
            print 'Error: No keyfile option found in section ' + section + ' file ' + self._configfile
            sys.exit(1)

        if not os.path.isfile(self._keyfile):
            print 'Error: keyfile file not found in ' + self._keyfile
            sys.exit(1)
        try:
            self._logFile = os.path.expanduser(self._config.get(section, 'log', 0))
        except ConfigParser.NoOptionError:
            print 'Error: No log option found in section ' + section + ' file ' + self._configfile
            sys.exit(1)

        try:
            tempLevel = string.upper(self._config.get(section, 'log_level', 0))
        except ConfigParser.NoOptionError:
            tempLevel = self._logLevel_default

        if tempLevel not in self._logType:
            print 'Log level ' + tempLevel + ' not supported. Using the default one ' + self._logLevel_default
            tempLevel = self._logLevel_default
        self._logLevel = eval('logging.' + tempLevel)