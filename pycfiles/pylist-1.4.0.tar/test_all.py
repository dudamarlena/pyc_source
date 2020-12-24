# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/test/test_all.py
# Compiled at: 2008-11-11 11:44:56
import os
from unittest import TestSuite
from unittest import TextTestRunner
from doctest import DocFileSuite
from utils import findTests, importModule, buildUnittestSuites
from test_doctests import suite as doctestSuite
searchDirs = [
 'pylispng', 'test']
skipFiles = ['test_doctests.py', 'test_all.py']
suites = buildUnittestSuites(paths=searchDirs, skip=skipFiles)
suites.append(doctestSuite)
suites.append(DocFileSuite('../README'))
if __name__ == '__main__':
    runner = TextTestRunner(verbosity=2)
    runner.run(TestSuite(suites))