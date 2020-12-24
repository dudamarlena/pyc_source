# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/z3c/securitytool/tests.py
# Compiled at: 2010-10-22 19:01:08
from zope.app.testing import functional
from zope.app.testing.functional import ZCMLLayer
import doctest, os, unittest
SecurityToolTestingLayer = ZCMLLayer(os.path.join(os.path.split(__file__)[0], 'ftesting.zcml'), __name__, 'SecurityToolTestingLayer', allow_teardown=True)

def test_suite():
    suite = functional.FunctionalDocFileSuite('README.txt')
    suite.layer = SecurityToolTestingLayer
    return suite