# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \Ft\Lib\TestSuite\TestObject.py
# Compiled at: 2002-08-16 12:38:09
"""
Provides the TestObject base class used in TestSuite modules.

Copyright 2002 Fourthought, Inc. (USA).
Detailed license and copyright information: http://4suite.org/COPYRIGHT
Project home, documentation, distributions: http://4suite.org/
"""
__revision__ = '$Id: TestObject.py,v 1.2 2002-08-16 17:38:09 molson Exp $'
import os, TestMode

class TestObject:
    """Base class for all test objects."""
    __module__ = __name__
    modes = None
    tests = None

    def __init__(self, name):
        self.name = name
        return

    def __str__(self):
        return '<%s, name %r>' % (self.__class__.__name__, self.name)

    def run(self, tester):
        raise NotImplementedError

    def getModes(self):
        return self.modes

    def getTests(self):
        return self.tests

    def showTests(self, indent):
        return