# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/test/utils.py
# Compiled at: 2008-11-09 13:08:20
"""
Utility functions for testing.
"""
import os, unittest, doctest
from StringIO import StringIO

def importModule(name):
    mod = __import__(name)
    components = name.split('.')
    for comp in components[1:]:
        mod = getattr(mod, comp)

    return mod


def fileIsTest(path, skipFiles=[]):
    if not os.path.isfile(path):
        return False
    filename = os.path.basename(path)
    if filename in skipFiles:
        return False
    if filename.startswith('test') and filename.endswith('.py'):
        return True


def find(start, func, skip=[]):
    for item in [ os.path.join(start, x) for x in os.listdir(start) ]:
        if func(item, skip):
            yield item
        if os.path.isdir(item):
            for subItem in find(item, func, skip):
                yield subItem


def findTests(startDir, skipFiles=[]):
    return find(startDir, fileIsTest, skipFiles)


def buildDoctestSuite(modules):
    suite = unittest.TestSuite()
    for modname in modules:
        mod = importModule(modname)
        suite.addTest(doctest.DocTestSuite(mod))

    return suite


def buildUnittestSuites(paths=[], skip=[]):
    """
    paths: a list of directories to search
    skip: a list of file names to skip
    """
    suites = []
    loader = unittest.TestLoader()
    for startDir in paths:
        for testFile in findTests(startDir, skip):
            modBase = os.path.splitext(testFile)[0]
            name = modBase.replace(os.path.sep, '.')
            mod = importModule(name)
            for objName in dir(mod):
                if not objName.endswith('TestCase'):
                    continue
                obj = getattr(mod, objName)
                if not issubclass(obj, unittest.TestCase):
                    continue
                suite = loader.loadTestsFromTestCase(obj)
                suites.append(suite)

    return suites


class BaseTestCase(unittest.TestCase):
    __module__ = __name__

    def getTestName(self):
        if hasattr(self, '_testMethodName'):
            return self._testMethodName.split('test_')[1]
        return self._TestCase__testMethodName.split('test_')[1]

    def getTestData(self, doc):
        result = StringIO()
        doc.write(result)
        testData = result.getvalue()
        result.close()
        return testData

    def callMake(self):
        return getattr(self, 'make_%s' % self.getTestName())()