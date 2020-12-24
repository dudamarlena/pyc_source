# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/astrocalc/coords/tests/test_separations.py
# Compiled at: 2020-05-01 12:03:38
from __future__ import print_function
from builtins import str
import os, unittest, shutil, unittest, yaml
from astrocalc.utKit import utKit
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

class test_separations(unittest.TestCase):

    def test_separations_function(self):
        from astrocalc.coords import separations
        calculator = separations(log=log, ra1='23:32:23.2324', dec1='-13:32:45.43553', ra2='23:32:34.642', dec2='-12:12:34.9334')
        print(calculator.get())
        calculator = separations(log=log, ra1=2.3342343, dec1=89.23244233, ra2=45.343545345, dec2=87.3435435)
        print(calculator.get())
        calculator = separations(log=log, ra1=352.5342343, dec1=89.23, ra2='23:32:34.642', dec2='89:12:34.9334')
        print(calculator.get())