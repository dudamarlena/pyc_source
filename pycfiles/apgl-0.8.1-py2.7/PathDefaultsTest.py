# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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