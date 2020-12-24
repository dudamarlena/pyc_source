# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/collective/customizablePersonalizeForm/tests/test_overrides.py
# Compiled at: 2011-09-08 04:35:46
from Products.CMFPlone.tests import PloneTestCase
from base import CollectiveCPFTestCase
from zope.component import getAdapters, getMultiAdapter, getUtility
from collective.customizablePersonalizeForm.browser.personalpreferences import ExtendedUserDataPanel
from collective.customizablePersonalizeForm.adapters.interfaces import IExtendedUserDataSchema
from plone.app.users.userdataschema import IUserDataSchemaProvider
default_user = PloneTestCase.default_user

class CollectiveCPFOverridesTestCase(CollectiveCPFTestCase):

    def afterSetUp(self):
        self.catalog = self.portal.portal_catalog
        self.portal.acl_users._doAddUser('member', 'secret', ['Member'], [])
        self.portal.acl_users._doAddUser('manager', 'secret', ['Manager'], [])
        self.login('manager')

    def testPersonalPrefsOverride(self):
        personalPrefs = getMultiAdapter((self.portal, self.portal.REQUEST), name='personal-information')
        self.failUnless(isinstance(personalPrefs, ExtendedUserDataPanel))

    def testIUserDataSchemaOverride(self):
        util = getUtility(IUserDataSchemaProvider)
        schema = util.getSchema()
        self.failUnless(schema is IExtendedUserDataSchema)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(CollectiveCPFOverridesTestCase))
    return suite