# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fundamentals/mysql/tests/test_yaml_to_database.py
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

class test_yaml_to_database(unittest.TestCase):

    def test_single_yaml_to_database_function(self):
        import shutil
        try:
            shutil.rmtree(pathToOutputDir)
        except:
            pass

        shutil.copytree(pathToInputDir, pathToOutputDir)
        from fundamentals.mysql import yaml_to_database
        yaml2db = yaml_to_database(log=log, settings=settings, dbConn=dbConn, pathToInputDir=pathToOutputDir + 'yaml')
        yaml2db.add_yaml_file_content_to_database(filepath=pathToOutputDir + 'yaml/20161219105124.yaml')

    def test_yaml_to_database_function(self):
        from fundamentals.mysql import yaml_to_database
        yaml2db = yaml_to_database(log=log, settings=settings, dbConn=dbConn, pathToInputDir=pathToOutputDir + '/yaml')
        yaml2db.ingest()

    def test_yaml_to_database_function_exception(self):
        from fundamentals.mysql import yaml_to_database
        try:
            this = yaml_to_database(log=log, settings=settings, dbConn=dbConn, fakeKey='break the code')
            this.get()
            assert False
        except Exception as e:
            assert True