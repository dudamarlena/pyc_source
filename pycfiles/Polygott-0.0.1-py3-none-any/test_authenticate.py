# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/polygot/tests/test_authenticate.py
# Compiled at: 2016-10-08 10:29:42
import os, nose, shutil, yaml
from polygot.utKit import utKit
from fundamentals import tools
su = tools(arguments={'settingsFile': None}, docString=__doc__, logLevel='DEBUG', options_first=False, projectName='polygot', tunnel=False)
arguments, settings, log, dbConn = su.setup()
moduleDirectory = os.path.dirname(__file__)
utKit = utKit(moduleDirectory)
log, dbConn, pathToInputDir, pathToOutputDir = utKit.setupModule()
utKit.tearDownModule()
stream = file(pathToInputDir + '/example_settings.yaml', 'r')
settings = yaml.load(stream)
stream.close()
import shutil
try:
    shutil.rmtree(pathToOutputDir)
except:
    pass

if not os.path.exists(pathToOutputDir):
    os.makedirs(pathToOutputDir)

class test_authenticate:

    def test_authenticate_function(self):
        from polygot import authenticate
        parserClient = authenticate(log=log, settings=settings).get()