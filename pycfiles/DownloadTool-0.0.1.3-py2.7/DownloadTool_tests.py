# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tests\DownloadTool_tests.py
# Compiled at: 2014-12-10 21:27:26
from nose.tools import *
import DownloadTool

def setup():
    print 'SETUP'


def teardown():
    print 'TEAR DOWN!'


def test_basic():
    print "I'm running..."