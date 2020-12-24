# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/p4a/ploneaudio/ataudio/ataudiotests.py
# Compiled at: 2007-11-27 08:53:01
from unittest import TestSuite
from p4a.ploneaudio import testing
from Testing.ZopeTestCase.zopedoctest import ZopeDocFileSuite
from Products.PloneTestCase import layer

def test_suite():
    suite = TestSuite()
    suite.layer = layer.ZCMLLayer
    suite.addTest(ZopeDocFileSuite('migration.txt', package='p4a.ploneaudio.ataudio', test_class=testing.IntegrationTestCase))
    return suite