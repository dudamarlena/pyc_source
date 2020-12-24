# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/apgl/util/test/PathDefaultsTest.py
# Compiled at: 2014-01-10 12:07:50
import unittest
from apgl.util.PathDefaults import PathDefaults

class PathDefaultsTestCase(unittest.TestCase):

    def testGetProjectDir(self):
        print PathDefaults.getSourceDir()

    def testGetDataDir(self):
        print PathDefaults.getDataDir()

    def testGetOutputDir(self):
        print PathDefaults.getOutputDir()


if __name__ == '__main__':
    unittest.main()