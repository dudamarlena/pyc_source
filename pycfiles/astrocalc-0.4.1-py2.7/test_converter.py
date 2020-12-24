# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/astrocalc/distances/tests/test_converter.py
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

class test_converter(unittest.TestCase):

    def test_converter_function01(self):
        from astrocalc.distances import converter
        c = converter(log=log)
        dists = c.redshift_to_distance(z=0.108, WM=0.3, WV=0.7, H0=70.0)
        print(dists)

    def test_converter_function02(self):
        from astrocalc.distances import converter
        c = converter(log=log)
        dists = c.distance_to_redshift(mpc=500)
        print(dists)