# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fundamentals/mysql/tests/test_convert_dictionary_to_mysql_table.py
# Compiled at: 2020-04-17 06:44:40
from __future__ import print_function
from builtins import str
import os, unittest, shutil, unittest, yaml, re
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
reDatetime = re.compile('^[0-9]{4}-[0-9]{2}-[0-9]{2}T')

class test_convert_dictionary_to_mysql_table(unittest.TestCase):

    def test_convert_dictionary_to_mysql_table_function(self):
        from fundamentals.mysql import writequery
        sqlQuery = "DROP TABLE IF EXISTS `testing_table`; CREATE TABLE IF NOT EXISTS `testing_table` (`id` INT NOT NULL  AUTO_INCREMENT,`uniquekey1` varchar(45) NOT NULL default 'ha',`uniqueKey2` varchar(45) NOT NULL default 'ha', `dateCreated` TIMESTAMP NOT NULL default CURRENT_TIMESTAMP, `dateModified` TIMESTAMP NOT NULL default CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, PRIMARY KEY (`id`) )"
        writequery(log=log, sqlQuery=sqlQuery, dbConn=dbConn, Force=False, manyValueList=False)
        dictionary = {'a newKey': 'cool', 'and another': 'super cool', 'uniquekey1': 'cheese', 
           'uniqueKey2': 'burgers'}
        from fundamentals.mysql import convert_dictionary_to_mysql_table
        message = convert_dictionary_to_mysql_table(dbConn=dbConn, log=log, dictionary=dictionary, dbTableName='testing_table', uniqueKeyList=[
         'uniquekey1', 'uniqueKey2'], createHelperTables=False, dateModified=True, returnInsertOnly=False)

    def test_return_inserts(self):
        from fundamentals.mysql import writequery
        sqlQuery = 'CREATE TABLE IF NOT EXISTS `testing_table` (`id` INT NOT NULL, PRIMARY KEY (`id`))'
        writequery(log=log, sqlQuery=sqlQuery, dbConn=dbConn, Force=False, manyValueList=False)
        dictionary = {'a newKey': 'cool', 'and another': 'super cool', 'uniquekey1': 'cheese', 
           'uniqueKey2': 'burgers'}
        from fundamentals.mysql import convert_dictionary_to_mysql_table
        message = convert_dictionary_to_mysql_table(dbConn=dbConn, log=log, dictionary=dictionary, dbTableName='testing_table', uniqueKeyList=[
         'uniquekey1', 'uniqueKey2'], createHelperTables=False, dateModified=False, returnInsertOnly=True)

    def test_return_inserts_with_datetime_pre_compiled(self):
        from fundamentals.mysql import writequery
        sqlQuery = 'CREATE TABLE IF NOT EXISTS `testing_table` (`id` INT NOT NULL, PRIMARY KEY (`id`))'
        writequery(log=log, sqlQuery=sqlQuery, dbConn=dbConn, Force=False, manyValueList=False)
        dictionary = {'a newKey': 'cool', 'and another': 'super cool', 'uniquekey1': 'cheese', 
           'uniqueKey2': 'burgers'}
        from fundamentals.mysql import convert_dictionary_to_mysql_table
        message = convert_dictionary_to_mysql_table(dbConn=dbConn, log=log, dictionary=dictionary, dbTableName='testing_table', uniqueKeyList=[
         'uniquekey1', 'uniqueKey2'], createHelperTables=False, dateModified=False, returnInsertOnly=True, reDatetime=reDatetime)

    def test_return_inserts_non_batch(self):
        dictionary = {'a newKey': 'cool', 'and another': 'super cool', 'uniquekey1': 'cheese', 
           'uniqueKey2': 'burgers'}
        from fundamentals.mysql import convert_dictionary_to_mysql_table
        inserts = convert_dictionary_to_mysql_table(dbConn=dbConn, log=log, dictionary=dictionary, dbTableName='testing_table', uniqueKeyList=[
         'uniquekey1', 'uniqueKey2'], dateModified=False, returnInsertOnly=True, replace=True, batchInserts=False)