# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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