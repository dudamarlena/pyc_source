# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/panstamps/tests/test_downloader.py
# Compiled at: 2020-05-07 14:43:36
from __future__ import print_function
from builtins import str
import os, unittest, shutil, yaml
from panstamps.utKit import utKit
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

class test_downloader(unittest.TestCase):

    def test_downloader_function(self):
        from panstamps import downloader
        kwargs = {}
        kwargs['log'] = log
        kwargs['settings'] = settings
        kwargs['fits'] = True
        kwargs['jpeg'] = False
        kwargs['arcsecSize'] = 60
        kwargs['filterSet'] = 'grizy'
        kwargs['color'] = True
        kwargs['singleFilters'] = True
        kwargs['ra'] = '70.60271'
        kwargs['dec'] = '-21.72433'
        kwargs['imageType'] = 'stack'
        testObject = downloader(**kwargs)
        testObject.get()

    def test_downloader_function02(self):
        from panstamps import downloader
        kwargs = {}
        kwargs['log'] = log
        kwargs['settings'] = settings
        kwargs['fits'] = True
        kwargs['jpeg'] = True
        kwargs['arcsecSize'] = 60
        kwargs['filterSet'] = 'grizy'
        kwargs['color'] = True
        kwargs['singleFilters'] = False
        kwargs['ra'] = '70.60271'
        kwargs['dec'] = '-21.72433'
        kwargs['imageType'] = 'stack'
        testObject = downloader(**kwargs)
        testObject.get()

    def test_downloader_function03(self):
        from panstamps import downloader
        kwargs = {}
        kwargs['log'] = log
        kwargs['settings'] = settings
        kwargs['fits'] = True
        kwargs['jpeg'] = False
        kwargs['arcsecSize'] = 60
        kwargs['filterSet'] = 'grizy'
        kwargs['color'] = False
        kwargs['singleFilters'] = True
        kwargs['ra'] = '70.60271'
        kwargs['dec'] = '-21.72433'
        kwargs['imageType'] = 'stack'
        testObject = downloader(**kwargs)
        testObject.get()

    def test_downloader_function04(self):
        from panstamps import downloader
        kwargs = {}
        kwargs['log'] = log
        kwargs['settings'] = settings
        kwargs['fits'] = False
        kwargs['jpeg'] = True
        kwargs['arcsecSize'] = 60
        kwargs['filterSet'] = 'grizy'
        kwargs['color'] = False
        kwargs['singleFilters'] = True
        kwargs['ra'] = '70.60271'
        kwargs['dec'] = '-21.72433'
        kwargs['imageType'] = 'stack'
        testObject = downloader(**kwargs)
        testObject.get()

    def test_downloader_function05(self):
        from panstamps import downloader
        kwargs = {}
        kwargs['log'] = log
        kwargs['settings'] = settings
        kwargs['fits'] = False
        kwargs['jpeg'] = True
        kwargs['arcsecSize'] = 600
        kwargs['filterSet'] = 'gri'
        kwargs['color'] = True
        kwargs['singleFilters'] = True
        kwargs['ra'] = '70.60271'
        kwargs['dec'] = '-21.72433'
        kwargs['imageType'] = 'stack'
        testObject = downloader(**kwargs)
        testObject.get()

    def test_downloader_function06(self):
        from panstamps import downloader
        kwargs = {}
        kwargs['log'] = log
        kwargs['settings'] = settings
        kwargs['fits'] = True
        kwargs['jpeg'] = True
        kwargs['arcsecSize'] = 60
        kwargs['filterSet'] = 'g'
        kwargs['color'] = True
        kwargs['singleFilters'] = True
        kwargs['ra'] = '189.1960991'
        kwargs['dec'] = '28.2374845'
        kwargs['imageType'] = 'stack'
        kwargs['mjdStart'] = 55246.62
        kwargs['mjdEnd'] = 55246.64
        testObject = downloader(**kwargs)
        testObject.get()

    def test_downloader_function07(self):
        from panstamps import downloader
        kwargs = {}
        kwargs['log'] = log
        kwargs['settings'] = settings
        kwargs['fits'] = True
        kwargs['jpeg'] = True
        kwargs['arcsecSize'] = 60
        kwargs['filterSet'] = 'g'
        kwargs['color'] = True
        kwargs['singleFilters'] = True
        kwargs['ra'] = '189.1960991'
        kwargs['dec'] = '28.2374845'
        kwargs['imageType'] = 'stack'
        kwargs['mjdStart'] = False
        kwargs['mjdEnd'] = 55246.63228
        testObject = downloader(**kwargs)
        testObject.get()

    def test_downloader_function08(self):
        from panstamps import downloader
        kwargs = {}
        kwargs['log'] = log
        kwargs['settings'] = settings
        kwargs['fits'] = True
        kwargs['jpeg'] = True
        kwargs['arcsecSize'] = 60
        kwargs['filterSet'] = 'g'
        kwargs['color'] = True
        kwargs['singleFilters'] = True
        kwargs['ra'] = '189.1960991'
        kwargs['dec'] = '28.2374845'
        kwargs['imageType'] = 'stack'
        kwargs['mjdStart'] = 55246.63228
        kwargs['mjdEnd'] = False
        testObject = downloader(**kwargs)
        testObject.get()

    def test_downloader_function09(self):
        from panstamps import downloader
        kwargs = {}
        kwargs['log'] = log
        kwargs['settings'] = settings
        kwargs['fits'] = True
        kwargs['jpeg'] = False
        kwargs['arcsecSize'] = 600
        kwargs['filterSet'] = 'grizy'
        kwargs['color'] = True
        kwargs['singleFilters'] = True
        kwargs['ra'] = '192.5991036'
        kwargs['dec'] = '26.4407364'
        kwargs['imageType'] = 'stack'
        kwargs['mjdEnd'] = 56710.5614
        testObject = downloader(**kwargs)
        testObject.get()