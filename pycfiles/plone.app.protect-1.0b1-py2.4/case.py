# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/plone/app/protect/tests/case.py
# Compiled at: 2008-03-07 17:28:21
from unittest import TestCase
from zope.component import getGlobalSiteManager
from zope.interface import implements
from plone.keyring.interfaces import IKeyManager
from AccessControl.SecurityManagement import newSecurityManager
from AccessControl.SecurityManagement import noSecurityManager
from AccessControl.User import User

class MockKeyManager:
    __module__ = __name__
    implements(IKeyManager)
    keys = [
     'one', 'two', 'three', 'four', 'five']

    def secret(self):
        return self.keys[0]

    def __getitem__(self, key):
        return self.keys


class KeyringTestCase(TestCase):
    __module__ = __name__

    def setUp(self):
        self.sm = getGlobalSiteManager()
        self.manager = MockKeyManager()
        self.sm.registerUtility(self.manager, provided=IKeyManager, event=False)
        newSecurityManager(None, User('dummy', 'secret', (), ()))
        return

    def tearDown(self):
        self.sm.unregisterUtility(self.manager, provided=IKeyManager)
        noSecurityManager()