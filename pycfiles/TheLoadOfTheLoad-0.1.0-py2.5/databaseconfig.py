# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/src/lol/databaseconfig.py
# Compiled at: 2008-07-27 08:13:20
import os
from os import path
import yaml, logging
logger = logging.getLogger()

class DatabaseConfig(object):

    def __init__(self):
        self.dbms = None
        self.dsn = None
        self.user = None
        self.password = None
        self.host = None
        self.port = None
        self.database = None
        return

    def load(self, filePath):
        configYAML = None
        if path.exists(filePath) == False:
            raise IOError, filePath + ' is not found at ' + os.getcwdu()
        else:
            logger.info(filePath + ' is found at ' + os.getcwdu())
        configYAML = yaml.load(open(filePath).read())
        configYAML = configYAML['config']
        databaseYAML = configYAML['database']
        self.dbms = databaseYAML['dbms']
        self.dsn = databaseYAML['dsn']
        self.user = databaseYAML['user']
        self.password = databaseYAML['password']
        self.host = databaseYAML['host']
        self.port = databaseYAML['port']
        self.database = databaseYAML['database']
        return

    def getDbms(self):
        return self.dbms

    def getDsn(self):
        return self.dsn

    def getUser(self):
        return self.user

    def getPassword(self):
        return self.password

    def getHost(self):
        return self.host

    def getPort(self):
        return self.port

    def getDatabase(self):
        return self.database

    def __repr__(self):
        return self.dsn

    def __del__(self):
        if self.database is not None:
            del self.database
        if self.dbms is not None:
            del self.dbms
        if self.dsn is not None:
            del self.dsn
        if self.host is not None:
            del self.host
        if self.password is not None:
            del self.password
        if self.port is not None:
            del self.port
        if self.user is not None:
            del self.user
        return