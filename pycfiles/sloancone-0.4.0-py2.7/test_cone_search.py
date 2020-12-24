# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sloancone/tests/test_cone_search.py
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

class test_cone_search(unittest.TestCase):

    def test_cone_search_function(self):
        from sloancone.cone_search import cone_search
        this = cone_search(log=log, ra='12:45:23.2323', dec='30.343122', searchRadius=60.0, nearest=True, outputFormat='table', galaxyType='all')
        print(this.get())
        from sloancone.cone_search import cone_search
        this = cone_search(log=log, ra='12:45:23.2323', dec='30.343122', searchRadius=60.0, nearest=False, outputFormat='table', galaxyType='all')
        print(this.get())

    def test_cone_search_function2(self):
        from sloancone.cone_search import cone_search
        this = cone_search(log=log, ra='112.233432', dec='15:34:31.22', searchRadius=60.0, nearest=True, outputFormat='table', galaxyType='all')
        print(this.get())
        from sloancone.cone_search import cone_search
        this = cone_search(log=log, ra='112.233432', dec='15:34:31.22', searchRadius=60.0, nearest=False, outputFormat='table', galaxyType='all')
        print(this.get())

    def test_cone_search_function3(self):
        from sloancone.cone_search import cone_search
        this = cone_search(log=log, ra='112.233432', dec='15:34:31.22', searchRadius=60.0, nearest=True, outputFormat='csv', galaxyType='all')
        print(this.get())
        from sloancone.cone_search import cone_search
        this = cone_search(log=log, ra='112.233432', dec='15:34:31.22', searchRadius=60.0, nearest=False, outputFormat='csv', galaxyType='all')
        print(this.get())

    def test_cone_search_function4(self):
        from sloancone.cone_search import cone_search
        csResults = cone_search(log=log, ra='12:45:23.2323', dec='30.343122', searchRadius=600.0, nearest=False, outputFormat='table', galaxyType='specz').get()
        print(csResults)

    def test_cone_search_function5(self):
        from sloancone.cone_search import cone_search
        csResults = cone_search(log=log, ra='12:45:23.2323', dec='30.343122', searchRadius=60.0, nearest=False, outputFormat='table', galaxyType=False).get()
        print(csResults)

    def test_cone_search_function_exception(self):
        from sloancone.cone_search import cone_search
        try:
            this = cone_search(log=log, fakeKey='break the code')
            this.get()
            assert False
        except Exception as e:
            assert True
            print(str(e))