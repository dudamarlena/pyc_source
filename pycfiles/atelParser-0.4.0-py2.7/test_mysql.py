# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/atelParser/tests/test_mysql.py
# Compiled at: 2020-05-04 14:34:29
from __future__ import print_function
from builtins import str
import os, unittest, shutil, yaml
from atelParser.utKit import utKit
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
settings['atel-directory'] = pathToOutputDir + 'atel-directory'

def drop_database_tables(dbConn, log):
    log.debug('starting the ``drop_database_tables`` function')
    from fundamentals.mysql import writequery
    sqlQuery = '\n        drop table if exists atel_coordinates;\n        drop table if exists atel_names;\n        drop table if exists atel_fullcontent;\n        ' % locals()
    writequery(log=log, sqlQuery=sqlQuery, dbConn=dbConn)
    log.debug('completed the ``drop_database_tables`` function')
    return


drop_database_tables(dbConn, log)

class test_mysql(unittest.TestCase):

    def test_01_atels_to_database_function(self):
        from atelParser import mysql
        parser = mysql(log=log, settings=settings)
        parser.atels_to_database()

    def test_02_parse_atels_function(self):
        from atelParser import mysql
        parser = mysql(log=log, settings=settings)
        parser.parse_atels()

    def test_03_update_htm_function(self):
        from atelParser import mysql
        parser = mysql(log=log, settings=settings)
        parser.populate_htm_columns()

    def test_04_mysql_function_exception(self):
        from atelParser import mysql
        try:
            this = mysql(log=log, settings=settings, fakeKey='break the code')
            this.get()
            assert False
        except Exception as e:
            assert True
            print(str(e))