# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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