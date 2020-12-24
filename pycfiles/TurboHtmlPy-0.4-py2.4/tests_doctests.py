# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/turbohtmlpy/tests_doctests.py
# Compiled at: 2006-01-20 09:19:32
import unittest, doctest, glob, os.path

def test_doctests():
    dir = os.path.dirname(__file__)
    suite = unittest.TestSuite()
    for f in glob.glob(dir + '/*.txt'):
        suite.addTest(doctest.DocFileSuite(os.path.basename(f)))

    for f in glob.glob(dir + '/*.rst'):
        suite.addTest(doctest.DocFileSuite(os.path.basename(f)))

    runner = unittest.TextTestRunner()
    return runner.run(suite)


if __name__ == '__main__':
    test_doctests()