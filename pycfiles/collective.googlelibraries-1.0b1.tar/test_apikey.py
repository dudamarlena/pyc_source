# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/toutpt/workspace/collective.googlelibraries/collective/googlelibraries/tests/test_apikey.py
# Compiled at: 2010-12-01 16:10:29
import unittest
from collective.googlelibraries import apikey
from collective.googlelibraries.tests import base
LOCAL_KEY = 'ABQIAAAAaKes6QWqobpCx2AOamo-shTwM0brOpm-All5BF6PoaKBxRWWERSUWbHs4SIAMkeC1KV98E2EdJKuJw'
LOCAL_REQ = {'SERVER_URL': 'http://localhost:8080'}

class Test(base.TestCase):

    def afterSetUp(self):
        self.manager = apikey.APIKeyManager(self.portal)

    def test_setup(self):
        self.failUnless(len(self.manager.google_keys) == 2)
        self.failUnless(self.manager.api_key(LOCAL_REQ) == LOCAL_KEY)

    def test_api_key(self):
        self.manager.google_keys = ('http://nohost | ZZOOPPEE', )
        self.failUnless(self.manager.api_key(self.portal.REQUEST) == 'ZZOOPPEE')

    def test_nokey(self):
        self.failUnless(self.manager.api_key(self.portal.REQUEST) is None)
        return

    def test_set_google_keys(self):
        self.manager.google_keys = ('http://nohost | ZZOOPPEE', )
        self.failUnless(len(self.manager.google_keys) == 1)
        self.manager.google_keys = ('wrong syntax but good type', )
        self.failUnless(len(self.manager.google_keys) == 0)
        self.manager.google_keys = 'wrong type'
        self.failUnless(len(self.manager.google_keys) == 0)


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Test))
    return suite