# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fundamentals/tests/test_fmultiprocess.py
# Compiled at: 2020-04-17 06:44:40
from __future__ import print_function
from builtins import str
import os, unittest, shutil, unittest, yaml
from fundamentals.utKit import utKit
from fundamentals import tools
from os.path import expanduser
import time
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

def f(n, anotherKeyword='nothing'):
    result = 0
    for x in range(10000):
        result += n * n * x

    return result


class test_multiprocess(unittest.TestCase):

    def test_multiprocess_function(self):
        from fundamentals import fmultiprocess
        inputArray = list(range(1000))
        t1 = time.time()
        result = fmultiprocess(log=log, function=f, inputArray=inputArray, anotherKeyword='cheese')
        took = time.time() - t1
        print('Multiprocessing took: %(took)s' % locals())
        t2 = time.time()
        result = []
        for i in inputArray:
            result.append(f(i))

        took = time.time() - t2
        print('Serial processing took: %(took)s' % locals())

    def test_multiprocess_function_exception(self):
        from fundamentals import fmultiprocess
        try:
            this = fmultiprocess(log=log, settings=settings, fakeKey='break the code')
            this.get()
            assert False
        except Exception as e:
            assert True
            print(str(e))