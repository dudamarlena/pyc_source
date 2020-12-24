# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/polygot/tests/test_htmlCleaner.py
# Compiled at: 2016-10-08 10:29:42
import os, nose, shutil, yaml
from polygot import htmlCleaner, cl_utils
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

class test_htmlCleaner:

    def test_htmlCleaner_function(self):
        from polygot import htmlCleaner
        this = htmlCleaner(log=log, settings=settings, url='http://www.thespacedoctor.co.uk/blog/2016/09/26/mysqlSucker-index.html', outputDirectory=pathToOutputDir, title=False)
        this.clean()
        from polygot import htmlCleaner
        cleaner = htmlCleaner(log=log, settings=settings, url='http://www.thespacedoctor.co.uk/blog/2016/09/26/mysqlSucker-index.html', outputDirectory=pathToOutputDir, title='my_clean_doc.html')
        cleaner.clean()

    def test_htmlCleaner_function_exception(self):
        from polygot import htmlCleaner
        try:
            this = htmlCleaner(log=log, settings=settings, fakeKey='break the code')
            this.get()
            assert False
        except Exception as e:
            assert True
            print str(e)