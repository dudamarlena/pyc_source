# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \Ft\Lib\TestSuite\TestLoader.py
# Compiled at: 2006-08-11 10:50:12
"""
Provides the TestLoader class for loading test modules or packages.

Copyright 2006 Fourthought, Inc. (USA).
Detailed license and copyright information: http://4suite.org/COPYRIGHT
Project home, documentation, distributions: http://4suite.org/
"""
from Ft.Lib.TestSuite import TestObject

class TestLoader(TestObject.TestObject):
    __module__ = __name__

    def __init__(self, name, path, addModes, skipModes, allModes):
        TestObject.TestObject.__init__(self, name)
        self.path = path
        self.addModes = addModes
        self.skipModes = skipModes
        self.allModes = allModes
        self.tests = []
        return

    def loadTest(self, name):
        from Ft.Lib.TestSuite import TestModule
        if self.path:
            module_name = self.path + '.' + name
        else:
            module_name = name
        module = __import__(module_name, {}, {}, ['*'])
        return TestModule.TestModule(name, module, self.addModes, self.skipModes, self.allModes)

    def addTest(self, name):
        test = self.loadTest(name)
        self.tests.append(test)
        return test

    def getTests(self):
        return self.tests