# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fundamentals/mysql/tests/test_table_exists.py
# Compiled at: 2020-04-17 06:44:40
from __future__ import print_function
from builtins import str
import os, unittest, shutil, unittest, yaml
from fundamentals.utKit import utKit
from fundamentals import tools
from os.path import expanduser
home = expanduser('~')
packageDirectory = utKit('').get_project_root()
settingsFile = packageDirectory + '/test_settings.yaml'
su = tools(arguments={'settingsFile': settingsFile}, docString=__doc__, logLevel='DEBUG', options_first=False, projectName=None, defaultSettingsFile=False)
arguments, settings, log, dbConn = su.setup()
moduleDirectory = os.path.dirname(__file__)
utKit = utKit(moduleDirectory)
log, dbConn, pathToInputDir, pathToOutputDir = utKit.setupModule()
utKit.tearDownModule()
try:
    shutil.rmtree(pathToOutputDir)
except:
    pass

shutil.copytree(pathToInputDir, pathToOutputDir)
if not os.path.exists(pathToOutputDir):
    os.makedirs(pathToOutputDir)

class test_table_exists(unittest.TestCase):

    def test_table_exists_function(self):
        from fundamentals.mysql import writequery
        sqlQuery = 'CREATE TABLE IF NOT EXISTS `testing_table` (`id` INT NOT NULL, PRIMARY KEY (`id`))'
        writequery(log=log, sqlQuery=sqlQuery, dbConn=dbConn, Force=False, manyValueList=False)
        from fundamentals.mysql import table_exists
        tableName = 'testing_table'
        this = table_exists(dbConn=dbConn, log=log, dbTableName=tableName)
        from fundamentals.mysql import writequery
        sqlQuery = 'DROP TABLE `testing_table`;'
        writequery(log=log, sqlQuery=sqlQuery, dbConn=dbConn, Force=False, manyValueList=False)

    def test_table_exists_function02(self):
        from fundamentals.mysql import table_exists
        tableName = 'stupid_named_table'
        this = table_exists(dbConn=dbConn, log=log, dbTableName=tableName)