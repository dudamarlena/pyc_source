# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/testoob/test_loaders.py
# Compiled at: 2009-10-07 18:08:46
"""Special test loaders"""
import unittest

class CustomMethodNameLoader(unittest.TestLoader):
    """Load test methods based on a predicate"""
    __module__ = __name__

    def __init__(self, *args, **kwargs):
        if hasattr(unittest.TestLoader, '__init__'):
            unittest.TestLoader.__init__(self, *args, **kwargs)

    def getTestCaseNames(self, testCaseClass):
        """Return the method names matching the predicate"""

        def isTestMethod(name):
            if not self._testNamePredicate(name):
                return False
            if not callable(getattr(testCaseClass, name)):
                return False
            return True

        testFnNames = filter(isTestMethod, dir(testCaseClass))
        for baseclass in testCaseClass.__bases__:
            for testFnName in self.getTestCaseNames(baseclass):
                if testFnName not in testFnNames:
                    testFnNames.append(testFnName)

        if self.sortTestMethodsUsing:
            testFnNames.sort(self.sortTestMethodsUsing)
        return testFnNames


class RegexLoader(CustomMethodNameLoader):
    """Load test methods matching the regular expression"""
    __module__ = __name__

    def __init__(self, regex):
        CustomMethodNameLoader.__init__(self)
        import re
        self.pattern = re.compile(regex)

    def _testNamePredicate(self, name):
        return self.pattern.search(name) is not None
        return


class GlobLoader(CustomMethodNameLoader):
    """Load test methods matching the glob pattern"""
    __module__ = __name__

    def __init__(self, pattern):
        CustomMethodNameLoader.__init__(self)
        self.pattern = pattern

    def _testNamePredicate(self, name):
        import fnmatch
        return fnmatch.fnmatch(name, self.pattern)