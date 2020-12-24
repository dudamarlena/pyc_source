# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fundamentals/mysql/tests/test_insert_list_of_dictionaries_into_database_tables.py
# Compiled at: 2020-04-17 06:44:40
from __future__ import print_function
from builtins import str
import os, unittest, shutil, unittest, yaml, time
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
dictList = []
for i in range(100000):
    dictList.append({'col1': i, 
       'col2': i + 10.0, 
       'col3': i / 2.0, 
       'col4': i * 34.0})

dbSettings = dbSettings = {'host': '127.0.0.1', 
   'user': 'utuser', 
   'tunnel': False, 
   'password': 'utpass', 
   'db': 'unit_tests'}

class test_insert_list_of_dictionaries_into_database_tables(unittest.TestCase):

    def test_insert_list_of_dictionaries_into_database_tables_function(self):
        t1 = time.time()
        from fundamentals.mysql import insert_list_of_dictionaries_into_database_tables
        insert_list_of_dictionaries_into_database_tables(dbConn=dbConn, log=log, dictList=dictList, dbTableName='test_insert_many', uniqueKeyList=[
         'col1', 'col3'], dateModified=True, batchSize=10000, replace=True, dbSettings=dbSettings)