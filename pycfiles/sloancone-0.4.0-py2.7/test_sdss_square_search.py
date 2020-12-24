# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sloancone/tests/test_sdss_square_search.py
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

class test_sdss_square_search(unittest.TestCase):

    def test_sdss_square_search_function_01(self):
        from sloancone import sdss_square_search
        kwargs = {}
        kwargs['log'] = log
        kwargs['ra'] = 179.5
        kwargs['dec'] = -1.0
        kwargs['searchRadius'] = 10.0
        search = sdss_square_search(**kwargs)
        search.get()

    def test_sdss_square_search_function_02(self):
        from sloancone import sdss_square_search
        kwargs = {}
        kwargs['log'] = log
        kwargs['ra'] = '23:23:13.23234'
        kwargs['dec'] = '-01:00:00.22323'
        kwargs['searchRadius'] = 170.0
        search = sdss_square_search(**kwargs)
        search.get()