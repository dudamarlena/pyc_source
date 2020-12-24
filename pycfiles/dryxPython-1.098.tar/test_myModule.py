# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dave/Dropbox/github_projects/dryxPython/dryxPython/htmlframework/tests/test_myModule.py
# Compiled at: 2013-08-11 08:13:40
import os
from nose import with_setup

def setUpModule():
    """set up test fixtures"""
    global pathToInputDataDir
    global pathToOutputDataDir
    global pathToOutputDir
    global testlog
    moduleDirectory = os.path.dirname(__file__)
    pathToInputDataDir = moduleDirectory + '/input/data/'
    pathToOutputDir = moduleDirectory + '/output/'
    pathToOutputDataDir = pathToOutputDir + 'data/'
    testlog = open(pathToOutputDir + 'tests.log', 'w')
    return


def tearDownModule():
    """tear down test fixtures"""
    testlog.close()
    return


def setUpFunc():
    """set up the test fixtures"""
    return


def tearDownFunc():
    """tear down the test fixtures"""
    return