# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fundamentals/renderer/tests/test_list_of_dictionaries.py
# Compiled at: 2020-04-17 06:44:40
from __future__ import print_function
from builtins import str
import os, unittest, shutil, unittest, pickle, yaml
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

class test_list_of_dictionaries(unittest.TestCase):

    def test_list_of_dictionaries_function(self):
        from fundamentals.renderer import list_of_dictionaries
        dataSet = list_of_dictionaries(log=log, listOfDictionaries=listOfDictionaries)
        dataSet.table(filepath=pathToOutputDir + 'myData.dat')
        dataSet.csv(filepath=pathToOutputDir + 'myData.csv')
        dataSet.mysql(tableName='TNS', filepath=pathToOutputDir + 'myData.mysql')
        dataSet.json(filepath=pathToOutputDir + 'myData.json')
        dataSet.yaml(filepath=pathToOutputDir + 'myData.yaml')
        dataSet.markdown(filepath=pathToOutputDir + 'myData.md')

    def test_list_of_dictionaries_function_02(self):
        dataList = [
         {'owner': 'daisy', 
            'pet': 'dog', 
            'address': 'belfast, uk'},
         {'owner': 'john', 
            'pet': 'snake', 
            'address': 'the moon'},
         {'owner': 'susan', 
            'pet': 'crocodile', 
            'address': 'larne'}]
        from fundamentals.renderer import list_of_dictionaries
        dataSet = list_of_dictionaries(log=log, listOfDictionaries=dataList)
        dataSet.table(filepath=pathToOutputDir + 'myData.dat')
        dataSet.csv(filepath=pathToOutputDir + 'myData.csv')
        dataSet.mysql(tableName='TNS', filepath=pathToOutputDir + 'myData.mysql')
        dataSet.json(filepath=pathToOutputDir + 'myData.json')
        dataSet.yaml(filepath=pathToOutputDir + 'myData.yaml')
        dataSet.markdown(filepath=pathToOutputDir + 'myData.md')

    def test_list_of_dictionaries_function_exception(self):
        from fundamentals.renderer import list_of_dictionaries
        try:
            this = list_of_dictionaries(log=log, listOfDictionaries=listOfDictionaries, fakeKey='break the code')
            this.get()
            assert False
        except Exception as e:
            assert True