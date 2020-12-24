# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/toutpt/workspace/collective.googlelibraries/collective/googlelibraries/tests/test_googleapi.py
# Compiled at: 2010-12-01 19:04:27
import unittest
from collective.googlelibraries import googleapi
from collective.googlelibraries.tests import base

class TestGoogleMaps(unittest.TestCase):

    def setUp(self):
        self.maps = googleapi.MapsLibrary()

    def test_url(self):
        self.failUnless(self.maps.url == 'http://maps.google.com/maps/api/js?sensor=false')


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestGoogleMaps))
    return suite