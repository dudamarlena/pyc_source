# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/fruit/simpletests.py
# Compiled at: 2005-12-14 15:26:33
import apple, unittest, doctest

def getTestSuite():
    suite = unittest.TestSuite()
    for mod in (apple,):
        suite.addTest(doctest.DocTestSuite(mod))

    return suite


runner = unittest.TextTestRunner()
runner.run(getTestSuite())