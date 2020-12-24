# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sloancone/tests/test_check_coverage.py
# Compiled at: 2020-05-06 13:40:52
from __future__ import print_function
from builtins import str
import os, unittest, shutil, yaml
from sloancone.utKit import utKit
from fundamentals import tools
from os.path import expanduser
home = expanduser('~')
packageDirectory = utKit('').get_project_root()
settingsFile = packageDirectory + '/test_settings.yaml'
su = tools(arguments={'settingsFile': settingsFile}, docString=__doc__, logLevel='DEBUG', options_first=False, projectName=None, defaultSettingsFile=False)
arguments, settings, log, dbConn = su.setup()
moduleDirectory = os.path.dirname(__file__)
pathToInputDir = moduleDirectory + '/input/'
pathToOutputDir = moduleDirectory + '/output/'
try:
    shutil.rmtree(pathToOutputDir)
except:
    pass

shutil.copytree(pathToInputDir, pathToOutputDir)
if not os.path.exists(pathToOutputDir):
    os.makedirs(pathToOutputDir)

class test_check_coverage(unittest.TestCase):

    def test_check_coverage_function(self):
        from sloancone import check_coverage
        covered = check_coverage(log=log, ra='122.3343', dec='45.34343').get()
        print(covered)

    def test_check_coverage_function2(self):
        from sloancone import check_coverage
        covered = check_coverage(log=log, ra=122.3343, dec=-45.34343).get()
        print(covered)

    def test_check_coverage_function3(self):
        from sloancone import check_coverage
        covered = check_coverage(log=log, ra='12:45:4.45466', dec='-25:22:34.3434').get()
        print(covered)

    def test_check_coverage_function_exception(self):
        from sloancone import check_coverage
        try:
            this = check_coverage(log=log, settings=settings, fakeKey='break the code')
            this.get()
            assert False
        except Exception as e:
            assert True
            print(str(e))