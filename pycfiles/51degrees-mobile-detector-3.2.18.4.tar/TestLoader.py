# uncompyle6 version 3.6.7
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: \Ft\Lib\TestSuite\TestLoader.py
# Compiled at: 2006-08-11 10:50:12
__doc__ = '\nProvides the TestLoader class for loading test modules or packages.\n\nCopyright 2006 Fourthought, Inc. (USA).\nDetailed license and copyright information: http://4suite.org/COPYRIGHT\nProject home, documentation, distributions: http://4suite.org/\n'
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