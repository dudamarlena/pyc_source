# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/config/config.py
# Compiled at: 2020-04-14 15:22:04
# Size of source mod 2**32: 3311 bytes
"""
Created on Mar 7, 2018

Wrapper for a dbConfig file whose format is
[mysql]
mySqlCnfPath = "a MySql conformant dbConfig file"

[dbName1]
server = <section in the file specified in [mysql]['mySqlCnfPath']

[dbName2]
server = ....
[...]

Abstracts the databases into aliases, e.g. [dev] [qa], [prod]

@author: jsk

Properties:
"""
import configparser, os
from pathlib import Path
from builtins import property

class DBConfig:
    __doc__ = '\n    :summary: Prepares mySql connector option semi securely\n    :param dbName: section in the DbApp file\n    :param configFile: Path to DbAppConfig file\n    \n    '

    def __init__(self, dbName=None, configFileName=None):
        """
        
        """
        if dbName is not None:
            self.db_alias = dbName
        if configFileName is not None:
            self.config_file_name = os.path.expanduser(configFileName)

    @property
    def db_host(self):
        """ De alias db_alias """
        self.test_init()
        return self._configParser[self.db_alias][self._DBConfig__serverKey]

    @property
    def db_cnf(self):
        """    MySQL ConfigFile - read only    """
        self.test_init
        return self._configParser[self._DBConfig__cnfFileSection][self._DBConfig__cnfKey]

    @property
    def config_file_name(self):
        """Config file we are parsing"""
        return self._configFQPath

    @config_file_name.setter
    def config_file_name(self, value):
        """Set the name of the DbAppConfig file"""
        cfgPath = Path(value)
        if cfgPath.is_file():
            self._configFQPath = str(cfgPath)
            self._parser(self._configFQPath)
        else:
            raise FileNotFoundError(str(cfgPath))

    @property
    def db_alias(self):
        """The _parser dbConfig file's server section"""
        return self._serverSection

    @db_alias.setter
    def db_alias(self, value):
        self._serverSection = value

    def _parser(self, fileName):
        """
        Creates a dbConfig _parser from fileName
        """
        self._configParser = configparser.ConfigParser()
        self._configParser.read(fileName)

    def test_init(self):
        """Tests for variable setup before action"""
        if not (self.db_alias and self._DBConfig__serverKey and self._DBConfig__cnfFileSection and self._configParser and self._DBConfig__cnfKey):
            raise ValueError

    _configFQPath = None
    _configParser = None
    _serverSection = None
    _DBConfig__serverKey = 'server'
    _DBConfig__cnfFileSection = 'mysql'
    _DBConfig__cnfKey = 'mySqlCnfPath'