# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fundamentals/mysql/tests/test_directory_script_runner.py
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

class test_directory_script_runner(unittest.TestCase):

    def test_directory_script_runner_function(self):
        from fundamentals.mysql import directory_script_runner
        directory_script_runner(log=log, pathToScriptDirectory=pathToOutputDir + '/mysql_scripts', databaseName='unit_tests', loginPath='unittesting')

    def test_directory_script_runner_function_02(self):
        from fundamentals.mysql import directory_script_runner
        directory_script_runner(log=log, pathToScriptDirectory=pathToOutputDir + '/mysql_scripts', databaseName='unit_tests', loginPath='unittesting', successRule='passed', failureRule='failed')

    def test_directory_script_runner_function_03(self):
        from fundamentals.mysql import directory_script_runner
        directory_script_runner(log=log, pathToScriptDirectory=pathToOutputDir + '/mysql_scripts', databaseName='unit_tests', loginPath='unittesting', successRule='delete', failureRule='failed')

    def test_directory_script_runner_function_04(self):
        from fundamentals.mysql import directory_script_runner
        directory_script_runner(log=log, pathToScriptDirectory=pathToOutputDir + '/mysql_scripts', databaseName='unit_tests', loginPath='unittesting', successRule='delete', failureRule='delete')

    def test_directory_script_runner_function_05(self):
        from fundamentals.mysql import directory_script_runner
        directory_script_runner(log=log, pathToScriptDirectory=pathToOutputDir + '/mysql_scripts', force=True, databaseName='unit_tests', loginPath='unittesting', successRule='delete', failureRule='failed')

    def test_directory_script_runner_function_exception(self):
        from fundamentals.mysql import directory_script_runner
        try:
            directory_script_runner(log=log, settings=settings, fakeKey='break the code')
            assert False
        except Exception as e:
            assert True