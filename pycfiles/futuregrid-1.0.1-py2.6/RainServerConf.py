# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/futuregrid/rain/RainServerConf.py
# Compiled at: 2012-05-09 14:35:33
"""
Class to read Rain Server configuration
"""
import os, ConfigParser, string, sys, logging, re
configFileName = 'fg-server.conf'

class RainServerConf(object):

    def __init__(self):
        super(RainServerConf, self).__init__()
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
        self._port_rainmovesites = 0
        self._proc_max_rainmovesites = 0
        self._nopasswdusers_rainmovesites = {}
        self._log_rainmovesites = ''
        self._logLevel_rainmovesites = ''
        self._ca_certs_rainmovesites = ''
        self._certfile_rainmovesites = ''
        self._keyfile_rainmovesites = ''
        self._port_rainmove = 0
        self._proc_max_rainmove = 0
        self._nopasswdusers_rainmove = {}
        self._log_rainmove = ''
        self._logLevel_rainmove = ''
        self._ca_certs_rainmove = ''
        self._certfile_rainmove = ''
        self._keyfile_rainmove = ''
        self._logLevel_default = 'DEBUG'
        self._logType = ['DEBUG', 'INFO', 'WARNING', 'ERROR']
        self._config = ConfigParser.ConfigParser()
        self._config.read(self._configfile)

    def getConfigFile(self):
        return self._configfile

    def getPortRainMoveSites(self):
        return self._port_rainmovesites

    def getProcMaxRainMoveSites(self):
        return self._proc_max_rainmovesites

    def getNopasswdUsersRainMoveSites(self):
        return self._nopasswdusers_rainmovesites

    def getLogRainMoveSites(self):
        return self._log_rainmovesites

    def getLogLevelRainMoveSites(self):
        return self._logLevel_rainmovesites

    def getCaCertsRainMoveSites(self):
        return self._ca_certs_rainmovesites

    def getCertFileRainMoveSites(self):
        return self._certfile_rainmovesites

    def getKeyFileRainMoveSites(self):
        return self._keyfile_rainmovesites

    def getPortRainMove(self):
        return self._port_rainmove

    def getProcMaxRainMove(self):
        return self._proc_max_rainmove

    def getNopasswdUsersRainMove(self):
        return self._nopasswdusers_rainmove

    def getLogRainMove(self):
        return self._log_rainmove

    def getLogLevelRainMove(self):
        return self._logLevel_rainmove

    def getCaCertsRainMove(self):
        return self._ca_certs_rainmove

    def getCertFileRainMove(self):
        return self._certfile_rainmove

    def getKeyFileRainMove(self):
        return self._keyfile_rainmove

    def load_rainMoveServerSitesConfig(self):
        section = 'RainMoveServerSites'
        try:
            self._port_rainmovesites = int(self._config.get(section, 'port', 0))
        except ConfigParser.NoOptionError:
            print 'Error: No port option found in section ' + section + ' file ' + self._configfile
            sys.exit(1)
        except ConfigParser.NoSectionError:
            print 'Error: no section ' + section + ' found in the ' + self._configfile + ' config file'
            sys.exit(1)
        except ValueError:
            print 'Error: Invalid value in section ' + section + ' file ' + self._configfile
            sys.exit(1)

        try:
            self._proc_max_rainmovesites = int(self._config.get(section, 'proc_max', 0))
        except ConfigParser.NoOptionError:
            print 'Error: No proc_max option found in section ' + section + ' file ' + self._configfile
            sys.exit(1)
        except ValueError:
            print 'Error: Invalid value in section ' + section + ' file ' + self._configfile
            sys.exit(1)

        try:
            self._log_rainmovesites = os.path.expanduser(self._config.get(section, 'log', 0))
        except ConfigParser.NoOptionError:
            print 'Error: No log option found in section ' + section + ' file ' + self._configfile
            sys.exit(1)

        try:
            aux = self._config.get(section, 'nopasswdusers', 0).strip()
            aux = ('').join(aux.split())
            parts = aux.split(';')
            for i in parts:
                temp = i.split(':')
                if len(temp) == 2:
                    self._nopasswdusers_rainmovesites[temp[0]] = temp[1].split(',')

        except ConfigParser.NoOptionError:
            pass

        try:
            tempLevel = string.upper(self._config.get(section, 'log_level', 0))
        except ConfigParser.NoOptionError:
            tempLevel = self._logLevel_default

        if tempLevel not in self._logType:
            print 'Log level ' + tempLevel + ' not supported. Using the default one ' + self._logLevel_default
            tempLevel = self._logLevel_default
        self._logLevel_rainmovesites = eval('logging.' + tempLevel)
        try:
            self._ca_certs_rainmovesites = os.path.expanduser(self._config.get(section, 'ca_cert', 0))
        except ConfigParser.NoOptionError:
            print 'Error: No ca_cert option found in section ' + section + ' file ' + self._configfile
            sys.exit(1)

        if not os.path.isfile(self._ca_certs_rainmovesites):
            print 'Error: ca_cert file not found in ' + self._ca_certs_rainmovesites
            sys.exit(1)
        try:
            self._certfile_rainmovesites = os.path.expanduser(self._config.get(section, 'certfile', 0))
        except ConfigParser.NoOptionError:
            print 'Error: No certfile option found in section ' + section + ' file ' + self._configfile
            sys.exit(1)

        if not os.path.isfile(self._certfile_rainmovesites):
            print 'Error: certfile file not found in ' + self._certfile_rainmovesites
            sys.exit(1)
        try:
            self._keyfile_rainmovesites = os.path.expanduser(self._config.get(section, 'keyfile', 0))
        except ConfigParser.NoOptionError:
            print 'Error: No keyfile option found in section ' + section + ' file ' + self._configfile
            sys.exit(1)

        if not os.path.isfile(self._keyfile_rainmovesites):
            print 'Error: keyfile file not found in ' + self._keyfile_rainmovesites
            sys.exit(1)

    def load_rainMoveServerConfig(self):
        section = 'RainMoveServer'
        try:
            self._port_rainmove = int(self._config.get(section, 'port', 0))
        except ConfigParser.NoOptionError:
            print 'Error: No port option found in section ' + section + ' file ' + self._configfile
            sys.exit(1)
        except ConfigParser.NoSectionError:
            print 'Error: no section ' + section + ' found in the ' + self._configfile + ' config file'
            sys.exit(1)
        except ValueError:
            print 'Error: Invalid value in section ' + section + ' file ' + self._configfile
            sys.exit(1)

        try:
            self._proc_max_rainmove = int(self._config.get(section, 'proc_max', 0))
        except ConfigParser.NoOptionError:
            print 'Error: No proc_max option found in section ' + section + ' file ' + self._configfile
            sys.exit(1)
        except ValueError:
            print 'Error: Invalid value in section ' + section + ' file ' + self._configfile
            sys.exit(1)

        try:
            aux = self._config.get(section, 'nopasswdusers', 0).strip()
            aux = ('').join(aux.split())
            parts = aux.split(';')
            for i in parts:
                temp = i.split(':')
                if len(temp) == 2:
                    self._nopasswdusers_rainmove[temp[0]] = temp[1].split(',')

        except ConfigParser.NoOptionError:
            pass

        try:
            self._log_rainmove = os.path.expanduser(self._config.get(section, 'log', 0))
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
        self._logLevel_rainmove = eval('logging.' + tempLevel)
        try:
            self._ca_certs_rainmove = os.path.expanduser(self._config.get(section, 'ca_cert', 0))
        except ConfigParser.NoOptionError:
            print 'Error: No ca_cert option found in section ' + section + ' file ' + self._configfile
            sys.exit(1)

        if not os.path.isfile(self._ca_certs_rainmove):
            print 'Error: ca_cert file not found in ' + self._ca_certs_rainmove
            sys.exit(1)
        try:
            self._certfile_rainmove = os.path.expanduser(self._config.get(section, 'certfile', 0))
        except ConfigParser.NoOptionError:
            print 'Error: No certfile option found in section ' + section + ' file ' + self._configfile
            sys.exit(1)

        if not os.path.isfile(self._certfile_rainmove):
            print 'Error: certfile file not found in ' + self._certfile_rainmove
            sys.exit(1)
        try:
            self._keyfile_rainmove = os.path.expanduser(self._config.get(section, 'keyfile', 0))
        except ConfigParser.NoOptionError:
            print 'Error: No keyfile option found in section ' + section + ' file ' + self._configfile
            sys.exit(1)

        if not os.path.isfile(self._keyfile_rainmove):
            print 'Error: keyfile file not found in ' + self._keyfile_rainmove
            sys.exit(1)