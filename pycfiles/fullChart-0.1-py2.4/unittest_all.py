# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/charts/unittest_all.py
# Compiled at: 2006-04-13 13:59:58
import genTriggers, mosixDataStore, mosixChart, doctest, unittest

def getTestSuite():
    suite = unittest.TestSuite()
    for mod in (genTriggers, mosixChart, mosixDataStore):
        suite.addTest(doctest.DocTestSuite(mod))

    return suite


runner = unittest.TextTestRunner()
runner.run(getTestSuite())