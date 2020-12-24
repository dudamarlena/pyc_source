# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ice/adverlet/tests/ftests.py
# Compiled at: 2008-12-22 07:00:12
__license__ = 'GPL v.3'
import unittest
from zope.app.testing import functional
try:
    from z3c import sampledata
    sampledata = True
except ImportError:
    sampledata = False

functional.defineLayer('TestLayer', 'ftesting.zcml')

def setUp(test):
    pass


def tearDown(test):
    pass


def test_suite():
    suite = unittest.TestSuite()
    if not sampledata:
        return suite
    suites = (
     functional.FunctionalDocFileSuite('ftests.txt', setUp=setUp, tearDown=tearDown),)
    for s in suites:
        s.layer = TestLayer
        suite.addTest(s)

    return suite