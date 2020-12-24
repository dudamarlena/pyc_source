# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/panstamps/tests/test_image.py
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

class test_image(unittest.TestCase):

    def test_image_function(self):
        from panstamps import downloader
        from panstamps.image import image
        kwargs = {}
        kwargs['log'] = log
        kwargs['settings'] = settings
        kwargs['arcsecSize'] = 4
        kwargs['fits'] = False
        kwargs['jpeg'] = True
        kwargs['arcsecSize'] = 60
        kwargs['filterSet'] = 'grizy'
        kwargs['color'] = True
        kwargs['singleFilters'] = True
        kwargs['ra'] = '70.60271'
        kwargs['dec'] = '-21.72433'
        kwargs['imageType'] = 'stack'
        testObject = downloader(**kwargs)
        testObject.get()
        kwargs['imageType'] = 'stack'
        testObject = downloader(**kwargs)
        testObject.get()
        kwargs['arcsecSize'] = 600
        testObject = downloader(**kwargs)
        testObject.get()
        kwargs = {}
        kwargs['log'] = log
        kwargs['settings'] = settings
        kwargs['arcsecSize'] = 4
        kwargs['imagePath'] = pathToOutputDir + '/something.png'
        kwargs['settings'] = False
        kwargs['crosshairs'] = True
        kwargs['transient'] = False
        kwargs['scale'] = True
        kwargs['invert'] = False
        kwargs['greyscale'] = False
        testObject = image(**kwargs)
        testObject.get()

    def test_image_function02(self):
        from panstamps import downloader
        from panstamps.image import image
        kwargs = {}
        kwargs['log'] = log
        kwargs['settings'] = settings
        kwargs['fits'] = False
        kwargs['jpeg'] = True
        kwargs['arcsecSize'] = 60
        kwargs['filterSet'] = 'grizy'
        kwargs['color'] = True
        kwargs['singleFilters'] = True
        kwargs['ra'] = '208.49364'
        kwargs['dec'] = '-27.22365'
        kwargs['imageType'] = 'stack'
        testObject = downloader(**kwargs)
        testObject.get()
        kwargs['imageType'] = 'stack'
        testObject = downloader(**kwargs)
        testObject.get()
        kwargs['arcsecSize'] = 600
        testObject = downloader(**kwargs)
        testObject.get()
        kwargs = {}
        kwargs['log'] = log
        kwargs['settings'] = settings
        kwargs['arcsecSize'] = 4
        kwargs['imagePath'] = pathToOutputDir + '/something.png'
        kwargs['settings'] = False
        kwargs['crosshairs'] = True
        kwargs['transient'] = False
        kwargs['scale'] = True
        kwargs['invert'] = False
        kwargs['greyscale'] = False
        testObject = image(**kwargs)
        testObject.get()