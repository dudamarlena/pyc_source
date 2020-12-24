# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ice/template/tests/ftests.py
# Compiled at: 2009-05-04 14:30:04
import unittest
from zope.app.testing import functional
functional.defineLayer('TestLayer', 'ftesting.zcml')

def test_suite():
    suite = unittest.TestSuite()
    suites = (
     functional.FunctionalDocFileSuite('ftests.txt'),)
    for s in suites:
        s.layer = TestLayer
        suite.addTest(s)

    return suite