# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/astrocalc/coords/tests/test_translate.py
# Compiled at: 2020-05-01 12:03:38
from __future__ import print_function
from builtins import str
import os, unittest, shutil, unittest, yaml
from fundamentals import tools
from astrocalc.utKit import utKit
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

class test_translate(unittest.TestCase):

    def test_translate_function01(self):
        from astrocalc.coords import translate
        ra, dec = translate(log=log, settings=settings, ra='14:45:32.3432', dec='-45:34:23.3434', northArcsec=45, eastArcsec=68).get()
        print(ra, dec)

    def test_translate_function02(self):
        from astrocalc.coords import translate
        ra, dec = translate(log=log, settings=settings, ra='14.546', dec='-45.34232334', northArcsec=4560, eastArcsec=-5678).get()
        print(ra, dec)

    def test_translate_ra_gt_360(self):
        from astrocalc.coords import translate
        ra, dec = translate(log=log, settings=settings, ra='14.546438', dec='-45.34232', northArcsec=4560, eastArcsec=+967800).get()
        print(ra, dec)

    def test_translate_ra_lt_360(self):
        from astrocalc.coords import translate
        ra, dec = translate(log=log, settings=settings, ra='14.546438', dec='-45.34232334', northArcsec=4560, eastArcsec=-967800).get()
        print(ra, dec)

    def test_translate_dec_lt_m90(self):
        from astrocalc.coords import translate
        ra, dec = translate(log=log, settings=settings, ra='14.546438', dec='-85.34', northArcsec=-43560, eastArcsec=-967800).get()
        print(ra, dec)

    def test_translate_dec_gt_90(self):
        from astrocalc.coords import translate
        ra, dec = translate(log=log, settings=settings, ra='14.546438', dec='85.34232334', northArcsec=45600, eastArcsec=-967800).get()
        print(ra, dec)