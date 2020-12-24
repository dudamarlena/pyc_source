# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fundamentals/mysql/tests/test_writequery.py
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

class test_writequery(unittest.TestCase):

    def test_writequery_function(self):
        from fundamentals.mysql import writequery
        sqlQuery = 'CREATE TABLE  IF NOT EXISTS `testing_table` (`id` INT NOT NULL, PRIMARY KEY (`id`))'
        writequery(log=log, sqlQuery=sqlQuery, dbConn=dbConn, Force=False, manyValueList=False)

    def test_manyvalue_insert(self):
        from fundamentals.mysql import writequery
        sqlQuery = 'CREATE TABLE  IF NOT EXISTS  `testing_table` (`id` INT NOT NULL, PRIMARY KEY (`id`))'
        writequery(log=log, sqlQuery=sqlQuery, dbConn=dbConn, Force=False, manyValueList=False)
        from fundamentals.mysql import writequery
        sqlQuery = 'INSERT INTO testing_table (id) values (%s)'
        writequery(log=log, sqlQuery=sqlQuery, dbConn=dbConn, Force=False, manyValueList=[
         (1, ), (2, ), (3, ), (4, ), (5, ), (6, ), (7, ),
         (8, ), (9, ), (10, ), (11, ), (12, )])

    def test_writequery_function_delete(self):
        from fundamentals.mysql import writequery
        sqlQuery = 'DROP TABLE `testing_table`;'
        writequery(log=log, sqlQuery=sqlQuery, dbConn=dbConn, Force=False, manyValueList=False)

    def test_writequery_error_force(self):
        from fundamentals.mysql import writequery
        sqlQuery = 'rubbish query;'
        writequery(log=log, sqlQuery=sqlQuery, dbConn=dbConn, Force=True, manyValueList=False)