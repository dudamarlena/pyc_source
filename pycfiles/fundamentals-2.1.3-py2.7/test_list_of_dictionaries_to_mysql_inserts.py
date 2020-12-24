# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fundamentals/files/tests/test_list_of_dictionaries_to_mysql_inserts.py
# Compiled at: 2020-04-17 06:44:40
from __future__ import print_function
from builtins import str
import os, unittest, shutil, unittest, yaml, pickle
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
pathToPickleFile = pathToInputDir + '/list-of-dictionaries.p'
listOfDictionaries = pickle.load(open(pathToPickleFile, 'rb'))

class test_list_of_dictionaries_to_mysql(unittest.TestCase):

    def test_list_of_dictionaries_to_mysql_function(self):
        from fundamentals.files.list_of_dictionaries_to_mysql_inserts import list_of_dictionaries_to_mysql_inserts
        mysqlInserts = list_of_dictionaries_to_mysql_inserts(log=log, datalist=listOfDictionaries, tableName='my_new_table')

    def test_list_of_dictionaries_to_mysql_function_exception(self):
        from fundamentals.files.list_of_dictionaries_to_mysql_inserts import list_of_dictionaries_to_mysql_inserts
        try:
            this = list_of_dictionaries_to_mysql_inserts(log=log, settings=settings, fakeKey='break the code')
            this.get()
            assert False
        except Exception as e:
            assert True
            print(str(e))